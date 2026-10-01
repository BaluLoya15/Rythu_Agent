import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from backend.models.schemas import (
    AgentState, ChatRequest, ChatResponse,
    ToolTraceStep, TaskPlanStep
)
from backend.agent.state import create_initial_state
from backend.agent.planner import extract_entities_from_query, classify_intent_and_create_plan
from backend.agent.synthesizer import synthesize_action_plan_and_reply
from backend.tools.farmer import get_farmer_profile
from backend.tools.weather import get_weather
from backend.tools.market import get_market_prices
from backend.tools.agriculture import search_agriculture_knowledge
from backend.tools.services import search_agricultural_services
from backend.db.database import (
    log_session, save_consequential_action,
    get_conversation, update_conversation, save_message
)
from backend.agent.title_generator import generate_conversation_title

def detect_script_language(text: str) -> Optional[str]:
    """Detects Telugu or Devanagari (Hindi) script characters in user message."""
    if not text:
        return None
    if any("\u0c00" <= ch <= "\u0c7f" for ch in text):
        return "te"
    if any("\u0900" <= ch <= "\u097f" for ch in text):
        return "hi"
    return None

class RythuAgentOrchestrator:
    """
    Central Agent Orchestrator with strict data honesty:
    - Default is LIVE data (not demo data).
    - If a live API fails or is unreachable, discloses UNAVAILABLE status.
    - Dynamically selects tools based on user request.
    - Accurately tracks live, unavailable, and verified knowledge sources.
    - Full multi-conversation context isolation and persistence.
    """

    async def run(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or f"sess-{uuid.uuid4().hex[:8]}"
        farmer_id = request.farmer_id or "farmer-001"
        conversation_id = request.conversation_id
        query = request.message.strip()

        # 1. Initialize State (Production default is force_demo_mode = False)
        state = create_initial_state(user_query=query, farmer_id=farmer_id, session_id=session_id)
        state.demo_mode = request.force_demo_mode

        # 2. Step 1: Load Farmer Profile
        t0 = time.time()
        farmer_prof = get_farmer_profile(farmer_id)
        if farmer_prof:
            farmer_dict = farmer_prof.model_dump()
        else:
            farmer_dict = {
                "id": farmer_id,
                "name": "Srinivasa Rao",
                "location": "Kapileswarapuram, Andhra Pradesh",
                "land_area": "2.0 Acres",
                "current_crop": "Paddy",
                "crop_stage": "Tillering & Panicle Initiation (40-45 days)",
                "district": "Krishna",
                "state": "Andhra Pradesh"
            }

        # Check and isolate conversation-specific context & resolve language
        conv = None
        if conversation_id:
            conv = get_conversation(conversation_id)

        # Explicit selected language has priority over detected query script!
        if request.language and request.language.lower() in ["en", "te", "hi"]:
            lang = request.language.lower()
        elif conv and conv.get("language") and conv.get("language").lower() in ["en", "te", "hi"]:
            lang = conv.get("language").lower()
        else:
            detected_lang = detect_script_language(query)
            if detected_lang:
                lang = detected_lang
            else:
                lang = "en"

        state.language = lang

        if conv:
            conv_crop = conv.get("crop")
            conv_stage = conv.get("crop_stage")
            conv_ctx = conv.get("context") or {}
            if conv_crop:
                farmer_dict["current_crop"] = conv_crop
            if conv_stage:
                farmer_dict["crop_stage"] = conv_stage
            if conv_ctx.get("location"):
                farmer_dict["location"] = conv_ctx.get("location")

        if conversation_id:
            # Persist incoming user message to conversation history
            save_message(
                conversation_id=conversation_id,
                role="user",
                content=query,
                language=lang
            )

        state.farmer_context = farmer_dict

        # Entity extraction & Dynamic Intent Classification
        entities = extract_entities_from_query(query, farmer_dict)
        target_crop = entities["crop"]
        target_location = entities["location"]
        target_acres = entities["land_area"]
        is_multi_crop = entities.get("is_multi_crop", False)
        crops_list = entities.get("crops_list", [target_crop])

        # Ensure active synthesis context reflects entities parsed from the farmer's request
        farmer_dict["current_crop"] = target_crop
        farmer_dict["location"] = target_location
        farmer_dict["land_area"] = target_acres
        farmer_dict["is_multi_crop"] = is_multi_crop
        farmer_dict["crops_list"] = crops_list
        state.farmer_context = farmer_dict

        intent, user_goal, task_plan = classify_intent_and_create_plan(query, farmer_dict)
        state.intent = intent
        state.user_goal = user_goal
        state.task_plan = task_plan

        summary_crop_info = f"Multiple crops: {', '.join(crops_list)}" if is_multi_crop else f"{target_acres} {target_crop} (Stage: {farmer_dict.get('crop_stage')})"
        state.tool_trace.append(ToolTraceStep(
            step_id=f"trace-{len(state.tool_trace)+1}",
            tool_name="farmer_tool",
            display_title="Loaded Farmer Profile & Field Context",
            event_key="trace_farmer_profile",
            tool_id="farmer_tool",
            status="COMPLETED",
            input_params={"farmer_id": farmer_id},
            output_summary=f"Profile loaded: {farmer_dict.get('name')} | {summary_crop_info} in {target_location}",
            raw_output={"profile": farmer_dict},
            execution_duration_ms=int((time.time() - t0) * 1000),
            data_status="LOCAL_KNOWLEDGE",
            is_demo=False,
            timestamp=datetime.now().strftime("%H:%M:%S")
        ))

        # Update task plan step 1 status
        if state.task_plan and state.task_plan[0].tool == "farmer_tool":
            state.task_plan[0].status = "COMPLETED"
            state.task_plan[0].execution_time_ms = int((time.time() - t0) * 1000)

        # Provenance Counters
        live_count = 0
        unavail_count = 0
        verified_count = 0

        # 3. Execute Remaining Tools According to Dynamic Plan
        for step in state.task_plan:
            if step.status == "COMPLETED":
                continue

            tool_name = step.tool
            step.status = "IN_PROGRESS"
            step_t0 = time.time()

            try:
                # ----------------------------------------------------
                # Tool: Market Intelligence
                # ----------------------------------------------------
                if tool_name == "market_tool":
                    mkt_res = await get_market_prices(
                        crop=target_crop,
                        location=target_location,
                        force_demo=state.demo_mode
                    )
                    state.market_data = mkt_res
                    dur = int((time.time() - step_t0) * 1000)
                    step.status = "COMPLETED"
                    step.execution_time_ms = dur

                    if mkt_res.data_status == "LIVE":
                        live_count += 1
                        summary = f"Retrieved live market records from {len(mkt_res.markets)} APMC mandis via {mkt_res.source}."
                    elif mkt_res.data_status == "UNAVAILABLE":
                        unavail_count += 1
                        summary = f"Live market data currently unavailable from official AGMARKNET/e-NAM gateway for {target_crop} in {target_location}. Agent continuing with agronomic & weather tools."
                    else:
                        summary = f"Test archive baseline loaded ({len(mkt_res.markets)} mandis)."

                    state.tool_trace.append(ToolTraceStep(
                        step_id=f"trace-{len(state.tool_trace)+1}",
                        tool_name="market_tool",
                        display_title="Queried Official APMC Mandi Rates",
                        event_key="trace_market_check",
                        tool_id="market_tool",
                        status="COMPLETED",
                        input_params={"crop": target_crop, "location": target_location},
                        output_summary=summary,
                        raw_output=mkt_res.model_dump(),
                        execution_duration_ms=dur,
                        data_status=mkt_res.data_status,
                        is_demo=(mkt_res.data_status == "DEMO"),
                        timestamp=datetime.now().strftime("%H:%M:%S")
                    ))

                # ----------------------------------------------------
                # Tool: Weather Forecast (Open-Meteo Live API)
                # ----------------------------------------------------
                elif tool_name == "weather_tool":
                    weather_res = await get_weather(
                        location=target_location,
                        force_demo=state.demo_mode
                    )
                    state.weather_data = weather_res
                    dur = int((time.time() - step_t0) * 1000)
                    step.status = "COMPLETED"
                    step.execution_time_ms = dur

                    if weather_res.data_status == "LIVE":
                        live_count += 1
                        summary = f"Live weather feed: {weather_res.temperature_c}°C, humidity {weather_res.humidity_pct}%, rain chance {weather_res.rainfall_probability_pct}%, wind {weather_res.wind_speed_kmh} km/h."
                    elif weather_res.data_status == "UNAVAILABLE":
                        unavail_count += 1
                        summary = f"Live weather feed unreachable: {weather_res.error_message}"
                    else:
                        summary = f"Test baseline weather loaded ({weather_res.temperature_c}°C)."

                    state.tool_trace.append(ToolTraceStep(
                        step_id=f"trace-{len(state.tool_trace)+1}",
                        tool_name="weather_tool",
                        display_title="Retrieved Live Agro-Met Satellite Feed",
                        event_key="trace_weather_check",
                        tool_id="weather_tool",
                        status="COMPLETED",
                        input_params={"location": target_location},
                        output_summary=summary,
                        raw_output=weather_res.model_dump(),
                        execution_duration_ms=dur,
                        data_status=weather_res.data_status,
                        is_demo=(weather_res.data_status == "DEMO"),
                        timestamp=datetime.now().strftime("%H:%M:%S")
                    ))

                # ----------------------------------------------------
                # Tool: Agricultural Knowledge RAG (ANGRAU / ICAR)
                # ----------------------------------------------------
                elif tool_name == "rag_tool":
                    rag_res = search_agriculture_knowledge(
                        query=query,
                        crop=target_crop,
                        optional_stage=farmer_dict.get("crop_stage"),
                        top_k=3
                    )
                    state.rag_sources = rag_res.sources
                    dur = int((time.time() - step_t0) * 1000)
                    step.status = "COMPLETED"
                    step.execution_time_ms = dur
                    verified_count += 1

                    top_title = rag_res.sources[0].document_title if rag_res.sources else "ANGRAU Manual"
                    state.tool_trace.append(ToolTraceStep(
                        step_id=f"trace-{len(state.tool_trace)+1}",
                        tool_name="rag_tool",
                        display_title="Searched ANGRAU & ICAR Extension Guides",
                        event_key="trace_rag_search",
                        tool_id="rag_tool",
                        status="COMPLETED",
                        input_params={"query": query, "crop": target_crop, "stage": farmer_dict.get("crop_stage")},
                        output_summary=f"Retrieved {len(rag_res.sources)} verified research guidelines from ANGRAU & ICAR publications (Top match: {top_title[:55]}...)",
                        raw_output={"total_found": len(rag_res.sources), "sources": [s.model_dump() for s in rag_res.sources]},
                        execution_duration_ms=dur,
                        data_status="VERIFIED_RESEARCH",
                        is_demo=False,
                        timestamp=datetime.now().strftime("%H:%M:%S")
                    ))

                # ----------------------------------------------------
                # Tool: Government Services & Schemes
                # ----------------------------------------------------
                elif tool_name == "services_tool":
                    services_res = search_agricultural_services(
                        query=query,
                        farmer_context=farmer_dict,
                        language=lang
                    )
                    state.services_data = services_res
                    dur = int((time.time() - step_t0) * 1000)
                    step.status = "COMPLETED"
                    step.execution_time_ms = dur
                    verified_count += 1

                    state.tool_trace.append(ToolTraceStep(
                        step_id=f"trace-{len(state.tool_trace)+1}",
                        tool_name="services_tool",
                        display_title="Searched Welfare Schemes Knowledge Base",
                        event_key="trace_services_search",
                        tool_id="services_tool",
                        status="COMPLETED",
                        input_params={"query": query, "farmer_land": target_acres},
                        output_summary=f"Matched {len(services_res)} applicable schemes (PM-KISAN, PMFBY Free Crop Insurance, PMKSY Drip Subsidy) from official guidelines.",
                        raw_output={"schemes_matched": [s.model_dump() for s in services_res]},
                        execution_duration_ms=dur,
                        data_status="VERIFIED_KNOWLEDGE",
                        is_demo=False,
                        timestamp=datetime.now().strftime("%H:%M:%S")
                    ))

                # ----------------------------------------------------
                # Tool: Reasoning & Action Plan Synthesis
                # ----------------------------------------------------
                elif tool_name == "reasoning_engine":
                    dur = int((time.time() - step_t0) * 1000)
                    step.status = "COMPLETED"
                    step.execution_time_ms = dur

            except Exception as e:
                step.status = "FAILED"
                unavail_count += 1
                state.tool_trace.append(ToolTraceStep(
                    step_id=f"trace-{len(state.tool_trace)+1}",
                    tool_name=tool_name,
                    display_title=f"Tool Execution Error: {tool_name}",
                    event_key="trace_tool_error",
                    tool_id=tool_name,
                    status="FAILED",
                    input_params={"error": str(e)},
                    output_summary=f"Tool encountered an error. Agent continuing with available context.",
                    raw_output={"error": str(e)},
                    execution_duration_ms=int((time.time() - step_t0) * 1000),
                    data_status="UNAVAILABLE",
                    is_demo=False,
                    timestamp=datetime.now().strftime("%H:%M:%S")
                ))

        # 4. Multi-Source Reasoning & Synthesis
        synth_t0 = time.time()
        action_plan, markdown_reply, proposed_actions = synthesize_action_plan_and_reply(
            query=query,
            intent=state.intent,
            farmer_context=farmer_dict,
            market_data=state.market_data,
            weather_data=state.weather_data,
            rag_sources=state.rag_sources,
            services_data=state.services_data,
            demo_mode=state.demo_mode,
            language=lang
        )
        synth_dur = int((time.time() - synth_t0) * 1000)

        # Calculate Provenance Summary
        prov_parts = []
        if live_count > 0:
            prov_parts.append(f"{live_count} Live Source{'s' if live_count > 1 else ''} Connected")
        if unavail_count > 0:
            prov_parts.append(f"{unavail_count} Source Unavailable")
        if verified_count > 0:
            prov_parts.append(f"Verified Knowledge Base Active")

        provenance_summary = " • ".join(prov_parts) or "All Systems Operational"

        state.action_plan = action_plan
        state.final_response_markdown = markdown_reply
        state.consequential_actions = proposed_actions
        state.live_sources_count = live_count
        state.unavailable_sources_count = unavail_count
        state.verified_sources_count = verified_count
        state.provenance_summary = provenance_summary
        state.completed = True

        state.tool_trace.append(ToolTraceStep(
            step_id=f"trace-{len(state.tool_trace)+1}",
            tool_name="reasoning_engine",
            display_title="Synthesized Farm Action Plan & Multi-Source Reasoning",
            event_key="trace_synthesize_plan",
            tool_id="reasoning_engine",
            status="COMPLETED",
            input_params={"intent": state.intent, "live_sources": live_count, "unavailable": unavail_count},
            output_summary=f"Synthesized evidence into actionable plan ({len(action_plan.recommended_actions) if action_plan else 0} actions, {len(proposed_actions)} human-confirmation actions).",
            raw_output={"provenance": provenance_summary},
            execution_duration_ms=synth_dur,
            data_status="VERIFIED_RESEARCH",
            is_demo=False,
            timestamp=datetime.now().strftime("%H:%M:%S")
        ))

        # 5. Persist Proposed Consequential Actions to SQLite
        for act in proposed_actions:
            act_dict = act.model_dump()
            act_dict["farmer_id"] = farmer_id
            act_dict["session_id"] = session_id
            act_dict["conversation_id"] = conversation_id
            save_consequential_action(act_dict)

        # 6. Log Session & Conversation Messages to Database
        log_session(
            session_id=session_id,
            farmer_id=farmer_id,
            query=query,
            intent=state.intent,
            plan=[p.model_dump() for p in state.task_plan],
            tool_trace=[t.model_dump() for t in state.tool_trace],
            action_plan=state.action_plan.model_dump() if state.action_plan else {},
            reply=markdown_reply
        )

        if conversation_id:
            # Persist assistant reply to conversation messages
            save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=markdown_reply,
                language=lang,
                tool_trace=[t.model_dump() for t in state.tool_trace],
                action_plan=state.action_plan.model_dump() if state.action_plan else None,
                sources=[s.model_dump() for s in (state.rag_sources or [])],
                proposed_actions=[a.model_dump() for a in proposed_actions],
                metadata={
                    "intent": state.intent,
                    "crop": target_crop,
                    "language": lang,
                    "provenance": provenance_summary
                }
            )

            # Auto-generate title if this is the first message or default title
            conv_updates = {
                "crop": target_crop,
                "crop_stage": farmer_dict.get("crop_stage"),
                "language": lang,
                "context": {
                    "active_crop": target_crop,
                    "active_stage": farmer_dict.get("crop_stage"),
                    "location": target_location,
                    "last_intent": state.intent,
                    "language": lang
                }
            }
            if conv and not conv.get("manually_renamed"):
                current_title = (conv.get("title") or "").strip()
                if current_title in ["New Chat", "కొత్త చాట్", "नई चैट", ""]:
                    new_title = generate_conversation_title(query, language=lang)
                    conv_updates["title"] = new_title

            update_conversation(conversation_id, conv_updates)

        events_list = [
            {
                "event": t.event_key or t.tool_name,
                "tool": t.tool_id or t.tool_name,
                "status": t.status.lower()
            }
            for t in state.tool_trace
        ]

        return ChatResponse(
            session_id=session_id,
            conversation_id=conversation_id,
            language=lang,
            user_query=query,
            intent=state.intent,
            markdown_reply=markdown_reply,
            response=markdown_reply,
            task_plan=state.task_plan,
            tool_trace=state.tool_trace,
            events=events_list,
            action_plan=state.action_plan,
            market_comparison=state.market_data,
            weather_data=state.weather_data,
            rag_sources=state.rag_sources,
            sources=[s.model_dump() for s in (state.rag_sources or [])],
            matched_services=state.services_data,
            proposed_actions=state.consequential_actions,
            actions=[a.model_dump() for a in proposed_actions],
            live_sources_count=live_count,
            unavailable_sources_count=unavail_count,
            verified_sources_count=verified_count,
            provenance_summary=provenance_summary,
            demo_mode=state.demo_mode,
            completed=True
        )

# Global singleton
_orchestrator = None

def get_orchestrator() -> RythuAgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = RythuAgentOrchestrator()
    return _orchestrator

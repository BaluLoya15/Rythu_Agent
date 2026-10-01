import pytest
import uuid
from backend.models.schemas import ChatRequest
from backend.agent.orchestrator import get_orchestrator
from backend.agent.planner import extract_entities_from_query, classify_intent_and_create_plan
from backend.db.database import create_conversation, get_conversation

@pytest.mark.asyncio
async def test_multilingual_entity_and_intent_extraction_parity():
    """
    Test 27: Verify that English, Telugu, and Hindi queries map to
    the exact same canonical internal representations.
    """
    context = {
        "current_crop": "Paddy",
        "location": "Vijayawada, Andhra Pradesh",
        "land_area": "2.0 Acres",
        "crop_stage": "Panicle Initiation (40 days)"
    }

    en_query = "My paddy crop is 40 days old. What should I do this week? Is there a chance of rain? What is the market price?"
    te_query = "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి? వర్షం వచ్చే అవకాశం ఉందా? మార్కెట్ ధర ఎలా ఉంది?"
    hi_query = "मेरी धान की फसल 40 दिन की है। इस सप्ताह मुझे क्या करना चाहिए? क्या बारिश की संभावना है? मंडी भाव कैसा है?"

    # Entity extraction
    en_ent = extract_entities_from_query(en_query, context)
    te_ent = extract_entities_from_query(te_query, context)
    hi_ent = extract_entities_from_query(hi_query, context)

    assert en_ent["crop"] == "Paddy"
    assert te_ent["crop"] == "Paddy"
    assert hi_ent["crop"] == "Paddy"

    assert en_ent["crop_age_days"] == 40
    assert te_ent["crop_age_days"] == 40
    assert hi_ent["crop_age_days"] == 40

    # Intent classification
    en_intent, _, en_plan = classify_intent_and_create_plan(en_query, context)
    te_intent, _, te_plan = classify_intent_and_create_plan(te_query, context)
    hi_intent, _, hi_plan = classify_intent_and_create_plan(hi_query, context)

    assert en_intent == "HYBRID_PLANNING_AND_MARKET"
    assert te_intent == "HYBRID_PLANNING_AND_MARKET"
    assert hi_intent == "HYBRID_PLANNING_AND_MARKET"

    en_tools = [p.tool for p in en_plan]
    te_tools = [p.tool for p in te_plan]
    hi_tools = [p.tool for p in hi_plan]
    assert en_tools == te_tools == hi_tools
    assert "weather_tool" in en_tools
    assert "market_tool" in en_tools
    assert "rag_tool" in en_tools


@pytest.mark.asyncio
async def test_telugu_end_to_end_workflow():
    """
    Test 29: End-to-End Telugu Workflow
    Query: "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి? వర్షం వచ్చే అవకాశం ఉందా? మార్కెట్ ధర ఎలా ఉంది?"
    """
    orchestrator = get_orchestrator()
    conv_id = f"test-conv-{uuid.uuid4().hex[:8]}"
    create_conversation(conv_id=conv_id, farmer_id="farmer-001", title="వరి పంట సలహా", language="te")

    req = ChatRequest(
        message="నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి? వర్షం వచ్చే అవకాశం ఉందా? మార్కెట్ ధర ఎలా ఉంది?",
        farmer_id="farmer-001",
        conversation_id=conv_id,
        language="te",
        force_demo_mode=False
    )

    res = await orchestrator.run(req)

    # 1. Authoritative language output
    assert res.language == "te"

    # 2. Canonical intent & crop
    assert res.intent == "HYBRID_PLANNING_AND_MARKET"

    # 3. Structured tool trace with event_key and tool_id
    tool_ids = [t.tool_id for t in res.tool_trace]
    assert "farmer_tool" in tool_ids
    assert "weather_tool" in tool_ids
    assert "market_tool" in tool_ids
    assert "rag_tool" in tool_ids
    assert "reasoning_engine" in tool_ids

    # 4. Structured events list for UI translation
    assert res.events is not None and len(res.events) > 0
    event_names = [e["event"] for e in res.events]
    assert "trace_farmer_profile" in event_names
    assert "trace_weather_check" in event_names
    assert "trace_market_check" in event_names
    assert "trace_rag_search" in event_names

    # 5. Localized Action Plan
    assert res.action_plan is not None
    assert res.action_plan.language == "te"
    assert "వరి" in res.action_plan.crop or "Paddy" in res.action_plan.crop
    assert len(res.action_plan.recommended_actions) >= 3
    # Check for Telugu characters in action plan titles & considerations
    has_telugu_action = any(
        any('\u0C00' <= char <= '\u0C7F' for char in act.get("title", ""))
        for act in res.action_plan.recommended_actions
    )
    assert has_telugu_action, "Action plan recommended_actions should contain Telugu text"

    # 6. Localized Consequential Action
    assert len(res.proposed_actions) > 0
    proposed = res.proposed_actions[0]
    assert proposed.requires_confirmation is True
    assert any('\u0C00' <= char <= '\u0C7F' for char in proposed.title)

    # 7. Localized Final Markdown Reply
    assert "వరి" in res.markdown_reply or "ప్రణాళిక" in res.markdown_reply


@pytest.mark.asyncio
async def test_hindi_end_to_end_workflow():
    """
    Test: End-to-End Hindi Workflow
    Query: "मेरी धान की फसल 40 दिन की है। इस सप्ताह मुझे क्या करना चाहिए? क्या बारिश की संभावना है? मंडी भाव कैसा है?"
    """
    orchestrator = get_orchestrator()
    conv_id = f"test-conv-{uuid.uuid4().hex[:8]}"
    create_conversation(conv_id=conv_id, farmer_id="farmer-001", title="धान फसल सलाह", language="hi")

    req = ChatRequest(
        message="मेरी धान की फसल 40 दिन की है। इस सप्ताह मुझे क्या करना चाहिए? क्या बारिश की संभावना है? मंडी भाव कैसा है?",
        farmer_id="farmer-001",
        conversation_id=conv_id,
        language="hi",
        force_demo_mode=False
    )

    res = await orchestrator.run(req)

    assert res.language == "hi"
    assert res.intent == "HYBRID_PLANNING_AND_MARKET"
    assert res.action_plan is not None
    assert res.action_plan.language == "hi"

    # Check for Devanagari characters in action plan
    has_hindi_action = any(
        any('\u0900' <= char <= '\u097F' for char in act.get("title", ""))
        for act in res.action_plan.recommended_actions
    )
    assert has_hindi_action, "Action plan recommended_actions should contain Hindi text"
    assert any('\u0900' <= char <= '\u097F' for char in res.markdown_reply)


@pytest.mark.asyncio
async def test_english_end_to_end_workflow():
    """
    Test: End-to-End English Workflow
    """
    orchestrator = get_orchestrator()
    conv_id = f"test-conv-{uuid.uuid4().hex[:8]}"
    create_conversation(conv_id=conv_id, farmer_id="farmer-001", title="Paddy Advisory", language="en")

    req = ChatRequest(
        message="My paddy crop is 40 days old. What should I do this week? Is there a chance of rain? What is the market price?",
        farmer_id="farmer-001",
        conversation_id=conv_id,
        language="en",
        force_demo_mode=False
    )

    res = await orchestrator.run(req)

    assert res.language == "en"
    assert res.intent == "HYBRID_PLANNING_AND_MARKET"
    assert res.action_plan is not None
    assert res.action_plan.language == "en"
    assert "Nutrient" in res.action_plan.recommended_actions[0]["title"] or "Mandi" in res.action_plan.recommended_actions[0]["title"]
    assert "Paddy" in res.markdown_reply


@pytest.mark.asyncio
async def test_multilingual_chat_context_isolation():
    """
    Test 17: Context Isolation across distinct conversations and languages.
    """
    orchestrator = get_orchestrator()

    # Conv 1: Sugarcane in Telugu
    conv1_id = f"test-conv-{uuid.uuid4().hex[:8]}"
    create_conversation(conv_id=conv1_id, farmer_id="farmer-001", title="చెరకు చాట్", language="te")
    res1 = await orchestrator.run(ChatRequest(
        message="నా చెరకు పంటకు ఎరువులు ఎప్పుడు వేయాలి?",
        conversation_id=conv1_id,
        language="te"
    ))
    assert res1.language == "te"

    # Conv 2: Chilli in Hindi
    conv2_id = f"test-conv-{uuid.uuid4().hex[:8]}"
    create_conversation(conv_id=conv2_id, farmer_id="farmer-001", title="मिर्च चैट", language="hi")
    res2 = await orchestrator.run(ChatRequest(
        message="मेरी मिर्च की फसल में पत्तियां पीली हो रही हैं। क्या करूं?",
        conversation_id=conv2_id,
        language="hi"
    ))
    assert res2.language == "hi"

    # Verify conversation contexts in DB remain isolated
    c1 = get_conversation(conv1_id)
    c2 = get_conversation(conv2_id)
    assert c1["language"] == "te"
    assert c2["language"] == "hi"
    assert c1["crop"] == "Sugarcane"
    assert c2["crop"] == "Chilli"

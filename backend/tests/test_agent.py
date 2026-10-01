import pytest
import asyncio
from backend.models.schemas import ChatRequest, ActionConfirmRequest
from backend.tools.weather import get_weather
from backend.tools.market import get_market_prices
from backend.tools.agriculture import search_agriculture_knowledge
from backend.tools.services import search_agricultural_services
from backend.tools.farmer import get_farmer_profile, update_farmer_profile
from backend.agent.planner import classify_intent_and_create_plan
from backend.agent.orchestrator import get_orchestrator

# =====================================================================
# Live Data & Tool Tests
# =====================================================================

@pytest.mark.asyncio
async def test_live_weather_open_meteo():
    """Tests live weather retrieval via Open-Meteo with live geocoding."""
    weather = await get_weather("Vijayawada", force_demo=False)
    assert weather is not None
    assert weather.data_status == "LIVE"
    assert weather.is_live is True
    assert weather.latitude is not None
    assert weather.longitude is not None
    assert "Open-Meteo" in weather.source
    assert weather.temperature_c != 0.0
    assert weather.humidity_pct > 0
    assert len(weather.forecast) >= 3
    assert weather.timestamp != ""

@pytest.mark.asyncio
async def test_market_tool_no_silent_fallback():
    """
    Verifies that when live market data is requested (force_demo=False) and no live API key is set,
    the market tool strictly returns UNAVAILABLE without silently injecting fake demo prices.
    """
    market = await get_market_prices("tomato", "Vijayawada", force_demo=False)
    assert market is not None
    # If no live API key is provided on this machine, must return UNAVAILABLE
    if market.data_status == "UNAVAILABLE":
        assert len(market.markets) == 0
        assert "unavailable" in market.recommended_strategy.lower()
        assert "unavailable" in market.disclaimer.lower()
    else:
        assert market.data_status == "LIVE"
        assert len(market.markets) > 0

@pytest.mark.asyncio
async def test_market_tool_test_mode_only():
    """Verifies that demo baseline is only returned in explicit force_demo=True test mode."""
    market = await get_market_prices("tomato", "Vijayawada", force_demo=True)
    assert market is not None
    assert market.data_status == "DEMO"
    assert len(market.markets) >= 3
    assert market.best_market == "Guntur Agricultural Market Yard"
    for m in market.markets:
        assert m.net_effective_price_per_quintal == m.modal_price_per_quintal - m.estimated_transport_cost_per_quintal

def test_rag_retrieval_and_citations():
    """Verifies ANGRAU & ICAR extension citations and relevance scoring."""
    res = search_agriculture_knowledge("tomato flowering fruit drop blossom end rot", crop="Tomato")
    assert res.total_found > 0
    top = res.sources[0]
    assert "Tomato" in top.document_title or "Tomato" in top.content_snippet
    assert top.relevance_score > 0.4
    assert top.official_reference != ""
    assert top.data_status == "VERIFIED_RESEARCH"

    # Groundnut 40 days pegging
    res_gnd = search_agriculture_knowledge("groundnut 40 days gypsum pegging", crop="Groundnut")
    assert res_gnd.total_found > 0
    assert any("gypsum" in s.content_snippet.lower() for s in res_gnd.sources)

    # Chilli yellow leaves
    res_chl = search_agriculture_knowledge("chilli yellow leaves mites thrips", crop="Chilli")
    assert res_chl.total_found > 0
    assert any("mite" in s.content_snippet.lower() or "thrip" in s.content_snippet.lower() for s in res_chl.sources)

def test_services_retrieval_verified_knowledge():
    """Verifies government services data is labeled as verified knowledge with official portals."""
    schemes = search_agricultural_services("government schemes relevant to me")
    assert len(schemes) >= 3
    for s in schemes:
        assert s.data_status == "VERIFIED_KNOWLEDGE"
        assert len(s.required_documents) > 0
        assert len(s.eligibility_criteria) > 0
        assert s.official_portal_url.startswith("http")
        assert s.last_verified_date != ""

def test_farmer_profile():
    prof = get_farmer_profile("farmer-001")
    assert prof is not None
    assert prof.name == "Venkat Rao"
    assert "Vijayawada" in prof.location
    assert prof.current_crop == "Paddy"
    assert "Paddy" in prof.crops

def test_planner_intent_detection():
    farmer_ctx = {"current_crop": "Tomato", "location": "Vijayawada", "land_area": "2.0 Acres"}
    
    # Farmer natural query
    q1 = "I have 2 acres of tomato near Vijayawada. What should I do this week and where should I check for better market prices?"
    intent1, goal1, plan1 = classify_intent_and_create_plan(q1, farmer_ctx)
    assert intent1 == "HYBRID_PLANNING_AND_MARKET"
    assert len(plan1) >= 4
    tools = [p.tool for p in plan1]
    assert "farmer_tool" in tools
    assert "market_tool" in tools
    assert "weather_tool" in tools
    assert "rag_tool" in tools

    # Services query
    q2 = "What agricultural government services may be relevant to me?"
    intent2, goal2, plan2 = classify_intent_and_create_plan(q2, farmer_ctx)
    assert intent2 == "SERVICES_AND_GOVERNMENT_SCHEMES"
    tools2 = [p.tool for p in plan2]
    assert "services_tool" in tools2

@pytest.mark.asyncio
async def test_end_to_end_live_execution():
    """
    Tests live execution path (force_demo_mode=False):
    - Real Open-Meteo live weather is pulled
    - Market tool handles live endpoint honestly
    - RAG searches ANGRAU/ICAR research
    - Action plan generated without crashing
    - Human-in-the-loop action proposed with natural reason
    """
    orchestrator = get_orchestrator()
    req = ChatRequest(
        message="I have 2 acres of tomato near Vijayawada. What should I do this week and where should I check for better market prices?",
        farmer_id="farmer-001",
        force_demo_mode=False  # LIVE DEFAULT
    )
    resp = await orchestrator.run(req)

    assert resp.completed is True
    assert resp.intent == "HYBRID_PLANNING_AND_MARKET"
    assert resp.action_plan is not None
    assert resp.action_plan.crop == "Tomato"
    assert len(resp.action_plan.recommended_actions) >= 3
    assert resp.weather_data is not None
    assert resp.weather_data.data_status in ["LIVE", "UNAVAILABLE"]
    if resp.weather_data.data_status == "LIVE":
        assert resp.weather_data.temperature_c != 0.0
        assert resp.live_sources_count >= 1
    assert len(resp.rag_sources) > 0
    assert len(resp.proposed_actions) >= 1
    # Check natural why reason
    assert resp.proposed_actions[0].why_reason != ""

@pytest.mark.asyncio
async def test_end_to_end_services_workflow():
    """Tests government services workflow independently."""
    orchestrator = get_orchestrator()
    req = ChatRequest(
        message="What agricultural government services may be relevant to me?",
        farmer_id="farmer-001",
        force_demo_mode=False
    )
    resp = await orchestrator.run(req)

    assert resp.completed is True
    assert resp.intent == "SERVICES_AND_GOVERNMENT_SCHEMES"
    assert len(resp.matched_services) >= 3
    assert "PM-KISAN" in resp.markdown_reply
    assert "Based on the available criteria" in resp.markdown_reply
    assert len(resp.proposed_actions) >= 1

@pytest.mark.asyncio
async def test_dynamic_farm_plan_chip_execution_paddy():
    """Tests that clicking the dynamic farm plan chip executes the genuine agent flow for Paddy."""
    orchestrator = get_orchestrator()
    req = ChatRequest(
        message="Create a weekly farm plan for my current crop using my farm profile, current weather, agricultural knowledge, and relevant market information.",
        farmer_id="farmer-001",
        force_demo_mode=False
    )
    resp = await orchestrator.run(req)
    assert resp.completed is True
    assert resp.intent == "HYBRID_PLANNING_AND_MARKET"
    assert resp.action_plan is not None
    assert resp.action_plan.crop == "Paddy"
    assert "Paddy" in resp.markdown_reply
    assert len(resp.tool_trace) >= 4

@pytest.mark.asyncio
async def test_dynamic_farm_plan_chip_telugu_and_hindi():
    """Tests multilingual natural language prompt execution for farm planning."""
    orchestrator = get_orchestrator()
    
    # Telugu prompt
    q_telugu = "నా ప్రస్తుత పంటకు నా వ్యవసాయ ప్రొఫైల్, ప్రస్తుత వాతావరణం, వ్యవసాయ సమాచారం మరియు అవసరమైన మార్కెట్ సమాచారాన్ని ఉపయోగించి ఈ వారానికి వ్యవసాయ ప్రణాళికను రూపొందించండి."
    resp_te = await orchestrator.run(ChatRequest(message=q_telugu, farmer_id="farmer-001", force_demo_mode=False))
    assert resp_te.completed is True
    assert resp_te.intent == "HYBRID_PLANNING_AND_MARKET"
    assert "రైతు కార్యాచరణ ప్రణాళిక" in resp_te.markdown_reply

    # Hindi prompt
    q_hindi = "मेरी वर्तमान फसल के लिए मेरे किसान प्रोफ़ाइल, वर्तमान मौसम, कृषि जानकारी और आवश्यक बाजार जानकारी का उपयोग करके इस सप्ताह की कृषि योजना बनाएं।"
    resp_hi = await orchestrator.run(ChatRequest(message=q_hindi, farmer_id="farmer-001", force_demo_mode=False))
    assert resp_hi.completed is True
    assert resp_hi.intent == "HYBRID_PLANNING_AND_MARKET"
    assert "रायतु कार्य योजना" in resp_hi.markdown_reply

@pytest.mark.asyncio
async def test_relevant_services_chip_execution_multilingual():
    """Tests that clicking the relevant agricultural services chip executes the genuine agentic search."""
    orchestrator = get_orchestrator()
    
    # English prompt
    q_en = "Find agricultural government services that may be relevant to my farmer profile. Check the available eligibility criteria, required documents and application process."
    resp_en = await orchestrator.run(ChatRequest(message=q_en, farmer_id="farmer-001", force_demo_mode=False))
    assert resp_en.completed is True
    assert resp_en.intent == "SERVICES_AND_GOVERNMENT_SCHEMES"
    assert len(resp_en.matched_services) >= 3
    assert "Required Documents for Application" in resp_en.markdown_reply
    assert "Step-by-Step Application Process" in resp_en.markdown_reply
    assert "Toll-Free Helpline" in resp_en.markdown_reply

    # Telugu prompt
    q_te = "నా రైతు ప్రొఫైల్‌కు సంబంధించి వర్తించే ప్రభుత్వ వ్యవసాయ సేవలను కనుగొనండి. అందుబాటులో ఉన్న అర్హత ప్రమాణాలు, అవసరమైన పత్రాలు మరియు దరఖాస్తు ప్రక్రియను పరిశీలించండి."
    resp_te = await orchestrator.run(ChatRequest(message=q_te, farmer_id="farmer-001", force_demo_mode=False))
    assert resp_te.completed is True
    assert resp_te.intent == "SERVICES_AND_GOVERNMENT_SCHEMES"
    assert "ప్రభుత్వ వ్యవసాయ సేవలు" in resp_te.markdown_reply

@pytest.mark.asyncio
async def test_multi_crop_farmer_planning():
    """Tests Requirement 8: Multiple-crop farmer (e.g. Paddy + Sugarcane) handling."""
    from backend.tools.farmer import update_farmer_profile
    from backend.models.schemas import FarmerProfileUpdate

    # Set multi-crop
    update_farmer_profile("farmer-001", FarmerProfileUpdate(current_crop="Paddy", crops=["Paddy", "Sugarcane"]))
    try:
        orchestrator = get_orchestrator()
        q = "Create a weekly farm plan for my current crop using my farm profile, current weather, agricultural knowledge, and relevant market information."
        resp = await orchestrator.run(ChatRequest(message=q, farmer_id="farmer-001", force_demo_mode=False))
        
        assert resp.completed is True
        assert resp.intent == "HYBRID_PLANNING_AND_MARKET"
        # Agent acknowledges multiple crops and clarifies
        assert "Multiple Crops Registered" in resp.markdown_reply or "Sugarcane" in resp.markdown_reply
    finally:
        # Reset back to single crop Paddy
        update_farmer_profile("farmer-001", FarmerProfileUpdate(current_crop="Paddy", crops=["Paddy"]))

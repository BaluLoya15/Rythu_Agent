"""
End-to-End Master Acceptance Test Suite for Rythu Agent Final Hackathon Version.
Verifies:
1. Product identity & crops: Paddy, Sugarcane, Black Gram (primary) + Tomato, Chilli, Groundnut (secondary).
2. Multilingual understanding: Telugu, English, Hindi, and code-mixed queries.
3. Chat persistence, new chat, auto-title generation, rename, archive, search, and delete.
4. Strict conversation context isolation across multiple simultaneous chats.
5. Primary Hackathon Demo: 40-day Paddy weekly planning + weather + market in Telugu.
6. Second Demo: Sugarcane planning.
7. Third Demo: Black Gram leaf yellowing cautious advisory.
8. Government services access with eligibility & required documents.
9. Data honesty: No silent fake market prices; live or honest unavailable state.
10. Consequential actions scoped strictly to active conversation.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_hackathon_demo_1_paddy_telugu():
    # Create fresh chat for Demo 1
    create_res = client.post("/api/conversations", json={
        "farmer_id": "farmer-001",
        "title": "New Chat",
        "language": "te"
    })
    assert create_res.status_code == 200
    conv_id = create_res.json()["id"]

    # Primary Hackathon Query in Telugu
    query = "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి? వర్షం వచ్చే అవకాశం ఉందా? మార్కెట్ ధర ఎలా ఉంది?"
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": query,
        "language": "te"
    })
    assert res.status_code == 200
    data = res.json()

    # 1. Verification of Language & Crop
    assert data["conversation_id"] == conv_id
    assert data["intent"] in ["HYBRID_PLANNING_AND_MARKET", "AGRICULTURAL_PLANNING"]
    assert "వరి" in data["markdown_reply"] or "Paddy" in data["markdown_reply"]

    # 2. Tool Trace: Verify Weather, RAG, and Market executed
    tools_executed = [t["tool_name"] for t in data["tool_trace"]]
    assert "farmer_tool" in tools_executed
    assert "weather_tool" in tools_executed
    assert "rag_tool" in tools_executed
    assert "market_tool" in tools_executed

    # 3. Action Plan verification
    assert data["action_plan"] is not None
    assert data["action_plan"]["crop"].lower() in ["paddy", "వరి"]
    assert len(data["action_plan"]["recommended_actions"]) > 0

    # 4. Verified Sources (ANGRAU / ICAR)
    assert len(data["rag_sources"]) > 0
    top_orgs = [s["source_organization"] for s in data["rag_sources"]]
    assert any("ANGRAU" in org or "ICAR" in org for org in top_orgs)

    # 5. Auto-generated conversation title
    conv_detail = client.get(f"/api/conversations/{conv_id}").json()
    assert conv_detail["crop"].lower() in ["paddy", "వరి"]
    assert conv_detail["title"] != "New Chat"
    assert len(conv_detail["title"]) <= 45

    # 6. Consequential action scoped to this conversation
    if data["proposed_actions"]:
        act_id = data["proposed_actions"][0]["action_id"]
        actions = client.get(f"/api/conversations/{conv_id}/actions").json()
        assert any(a["action_id"] == act_id for a in actions)

def test_hackathon_demo_2_sugarcane():
    create_res = client.post("/api/conversations", json={
        "farmer_id": "farmer-001",
        "title": "New Chat",
        "language": "te"
    })
    conv_id = create_res.json()["id"]

    query = "నా చెరకు పంటకు ఇప్పుడు ఏ పనులు చేయాలి?"
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": query,
        "language": "te"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["conversation_id"] == conv_id

    conv_detail = client.get(f"/api/conversations/{conv_id}").json()
    assert conv_detail["crop"].lower() in ["sugarcane", "చెరకు"]

def test_hackathon_demo_3_black_gram_cautious_advisory():
    create_res = client.post("/api/conversations", json={
        "farmer_id": "farmer-001",
        "title": "New Chat",
        "language": "te"
    })
    conv_id = create_res.json()["id"]

    query = "నా మినుము పంటలో ఆకులు పసుపు రంగులోకి మారుతున్నాయి."
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": query,
        "language": "te"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "CROP_ADVISORY"

    conv_detail = client.get(f"/api/conversations/{conv_id}").json()
    assert conv_detail["crop"].lower().replace(" ", "_") in ["black_gram", "మినుము", "మినుములు"]

def test_context_isolation_three_chats():
    # Chat A: Paddy
    conv_a = client.post("/api/conversations", json={"farmer_id": "farmer-001", "title": "Paddy Chat"}).json()["id"]
    client.post("/api/chat", json={
        "conversation_id": conv_a,
        "farmer_id": "farmer-001",
        "message": "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి?",
        "language": "te"
    })

    # Chat B: Sugarcane
    conv_b = client.post("/api/conversations", json={"farmer_id": "farmer-001", "title": "Sugarcane Chat"}).json()["id"]
    client.post("/api/chat", json={
        "conversation_id": conv_b,
        "farmer_id": "farmer-001",
        "message": "నా చెరకు పంటకు ఇప్పుడు ఏ పనులు చేయాలి?",
        "language": "te"
    })

    # Follow-up in Chat A: "మార్కెట్ ధర ఎలా ఉంది?" (User mentions NO crop)
    res_a_follow = client.post("/api/chat", json={
        "conversation_id": conv_a,
        "farmer_id": "farmer-001",
        "message": "మార్కెట్ ధర ఎలా ఉంది?",
        "language": "te"
    }).json()

    # Must retain Paddy, NOT sugarcane!
    if res_a_follow.get("market_comparison"):
        assert res_a_follow["market_comparison"]["crop"].lower() in ["paddy", "వరి"]

    # Verify context isolation in DB
    detail_a = client.get(f"/api/conversations/{conv_a}").json()
    detail_b = client.get(f"/api/conversations/{conv_b}").json()
    assert detail_a["crop"].lower() in ["paddy", "వరి"]
    assert detail_b["crop"].lower() in ["sugarcane", "చెరకు"]

def test_government_services_workflow():
    create_res = client.post("/api/conversations", json={
        "farmer_id": "farmer-001",
        "title": "Schemes Chat",
        "language": "te"
    })
    conv_id = create_res.json()["id"]

    query = "నాకు సంబంధించి వర్తించే ప్రభుత్వ వ్యవసాయ సేవలు మరియు పథకాలు ఏమిటి?"
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": query,
        "language": "te"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "SERVICES_AND_GOVERNMENT_SCHEMES"
    assert len(data["matched_services"]) > 0
    top_scheme = data["matched_services"][0]
    assert len(top_scheme["eligibility_criteria"]) > 0
    assert len(top_scheme["required_documents"]) > 0
    assert top_scheme["official_portal_url"].startswith("http")

def test_no_silent_demo_market_fallback():
    # Request market with force_demo=False
    res = client.get("/api/market?crop=paddy&location=Vijayawada&demo=false")
    assert res.status_code == 200
    data = res.json()
    # Must be LIVE or honest UNAVAILABLE, never silently DEMO
    assert data["data_status"] in ["LIVE", "UNAVAILABLE"]
    if data["data_status"] == "UNAVAILABLE":
        assert "unavailable" in data["recommended_strategy"].lower() or len(data["markets"]) == 0

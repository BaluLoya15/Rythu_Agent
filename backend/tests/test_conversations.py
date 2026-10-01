import pytest
import uuid
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_conversation_lifecycle():
    # 1. Create a new conversation
    res = client.post("/api/conversations", json={
        "farmer_id": "farmer-001",
        "title": "New Chat",
        "language": "te"
    })
    assert res.status_code == 200, res.text
    conv = res.json()
    conv_id = conv["id"]
    assert conv["title"] == "New Chat"
    assert conv["language"] == "te"

    # 2. List conversations
    res = client.get("/api/conversations?farmer_id=farmer-001")
    assert res.status_code == 200
    items = res.json()
    assert any(c["id"] == conv_id for c in items)

    # 3. Post first user message: Telugu Paddy question
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి?",
        "language": "te"
    })
    assert res.status_code == 200, res.text
    chat_resp = res.json()
    assert chat_resp["conversation_id"] == conv_id
    assert chat_resp["intent"] in ["HYBRID_PLANNING_AND_MARKET", "AGRICULTURAL_PLANNING"]

    # 4. Verify auto-generated title and context
    res = client.get(f"/api/conversations/{conv_id}")
    assert res.status_code == 200
    conv_detail = res.json()
    assert conv_detail["crop"].lower() == "paddy"
    assert "వరి" in conv_detail["title"] or "పంట" in conv_detail["title"] or len(conv_detail["title"]) > 0
    assert len(conv_detail["messages"]) >= 2  # user + assistant

    # 5. Follow-up query in the same conversation without mentioning Paddy
    res = client.post("/api/chat", json={
        "conversation_id": conv_id,
        "farmer_id": "farmer-001",
        "message": "మార్కెట్ ధర ఎలా ఉంది?",
        "language": "te"
    })
    assert res.status_code == 200
    follow_up = res.json()
    # Should maintain Paddy context!
    if follow_up["market_comparison"]:
        assert follow_up["market_comparison"]["crop"].lower() == "paddy"

    # 6. Test Manual Rename
    res = client.patch(f"/api/conversations/{conv_id}", json={
        "title": "నా వరి పంట రికార్డు",
        "manually_renamed": True
    })
    assert res.status_code == 200
    renamed = res.json()
    assert renamed["title"] == "నా వరి పంట రికార్డు"
    assert renamed["manually_renamed"] is True

    # 7. Search conversations
    res = client.get("/api/conversations/search?q=వరి")
    assert res.status_code == 200
    matches = res.json()
    assert any(m["id"] == conv_id for m in matches)

    # 8. Archive conversation
    res = client.post(f"/api/conversations/{conv_id}/archive?archived=true")
    assert res.status_code == 200

    # Verify not in regular list unless include_archived=True
    res = client.get("/api/conversations?farmer_id=farmer-001&include_archived=false")
    assert not any(c["id"] == conv_id for c in res.json())

    res = client.get("/api/conversations?farmer_id=farmer-001&include_archived=true")
    assert any(c["id"] == conv_id for c in res.json())

    # 9. Delete conversation
    res = client.delete(f"/api/conversations/{conv_id}")
    assert res.status_code == 200

    # Verify 404 after deletion
    res = client.get(f"/api/conversations/{conv_id}")
    assert res.status_code == 404

def test_context_isolation_between_chats():
    # Chat A: Paddy
    res_a = client.post("/api/conversations", json={"farmer_id": "farmer-001", "title": "Chat A"})
    conv_a_id = res_a.json()["id"]

    client.post("/api/chat", json={
        "conversation_id": conv_a_id,
        "farmer_id": "farmer-001",
        "message": "నా వరి పంట 40 రోజులు అయింది. ఈ వారం ఏమి చేయాలి?",
        "language": "te"
    })

    # Chat B: Sugarcane
    res_b = client.post("/api/conversations", json={"farmer_id": "farmer-001", "title": "Chat B"})
    conv_b_id = res_b.json()["id"]

    res_b_chat = client.post("/api/chat", json={
        "conversation_id": conv_b_id,
        "farmer_id": "farmer-001",
        "message": "నా చెరకు పంటకు ఇప్పుడు ఏ పనులు చేయాలి?",
        "language": "te"
    })
    b_data = res_b_chat.json()
    # Chat B should have sugarcane
    detail_b = client.get(f"/api/conversations/{conv_b_id}").json()
    assert detail_b["crop"].lower() in ["sugarcane", "చెరకు"]

    # Chat C: Black Gram
    res_c = client.post("/api/conversations", json={"farmer_id": "farmer-001", "title": "Chat C"})
    conv_c_id = res_c.json()["id"]

    res_c_chat = client.post("/api/chat", json={
        "conversation_id": conv_c_id,
        "farmer_id": "farmer-001",
        "message": "నా మినుము పంటలో ఆకులు పసుపు రంగులోకి మారుతున్నాయి.",
        "language": "te"
    })
    detail_c = client.get(f"/api/conversations/{conv_c_id}").json()
    assert detail_c["crop"].lower().replace(" ", "_") in ["black_gram", "మినుము", "మినుములు"]

    # SWITCH BACK TO CHAT A: Follow-up question about market price
    res_a_follow = client.post("/api/chat", json={
        "conversation_id": conv_a_id,
        "farmer_id": "farmer-001",
        "message": "మార్కెట్ ధర ఎలా ఉంది?",
        "language": "te"
    })
    a_data = res_a_follow.json()
    if a_data.get("market_comparison"):
        assert a_data["market_comparison"]["crop"].lower() in ["paddy", "వరి"], "Chat A must retain Paddy and not leak Chat B/C context!"

    detail_a = client.get(f"/api/conversations/{conv_a_id}").json()
    assert detail_a["crop"].lower() in ["paddy", "వరి"]

    # Cleanup
    client.delete(f"/api/conversations/{conv_a_id}")
    client.delete(f"/api/conversations/{conv_b_id}")
    client.delete(f"/api/conversations/{conv_c_id}")

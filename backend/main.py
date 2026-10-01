import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.models.schemas import (
    ChatRequest, ChatResponse,
    FarmerProfile, FarmerProfileUpdate,
    MarketComparison, WeatherData,
    RAGSearchResult, GovernmentService,
    ActionConfirmRequest, ActionConfirmResponse,
    ConversationItem, ConversationDetail,
    ConversationCreateRequest, ConversationUpdateRequest
)
from backend.agent.orchestrator import get_orchestrator
from backend.tools.farmer import get_farmer_profile, update_farmer_profile, list_all_farmers
from backend.tools.weather import get_weather
from backend.tools.market import get_market_prices
from backend.tools.agriculture import search_agriculture_knowledge
from backend.tools.services import search_agricultural_services
from backend.db.database import (
    update_action_status, save_farm_plan, get_farmer_plans,
    get_connection,
    create_conversation, get_conversation, list_conversations,
    update_conversation, archive_conversation, delete_conversation,
    search_conversations, get_conversation_messages, save_message,
    get_conversation_actions
)

app = FastAPI(
    title="Rythu Agent API",
    description="An AI-powered action agent for India's farmers and rural communities (BharatAgentic Hackathon)",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 1. Health & Status
# =====================================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": "Rythu Agent v1.0.0",
        "category": "Agri Tech & Rural Bharat",
        "capabilities": [
            "Crop Advisory",
            "Market Intelligence",
            "Agricultural Planning",
            "Access to Government Services"
        ],
        "tools_ready": ["farmer_tool", "market_tool", "weather_tool", "rag_tool", "services_tool"],
        "demo_mode_available": True,
        "database": "SQLite (Initialized)"
    }

# =====================================================================
# 2. Main Agent Execution
# =====================================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(req: ChatRequest):
    # Ensure conversation exists if conversation_id was provided
    if req.conversation_id:
        existing = get_conversation(req.conversation_id)
        if not existing:
            create_conversation(
                conv_id=req.conversation_id,
                farmer_id=req.farmer_id or "farmer-001",
                title="New Chat",
                language=req.language or "en"
            )
    orchestrator = get_orchestrator()
    response = await orchestrator.run(req)
    return response

@app.post("/api/agent/run", response_model=ChatResponse)
async def run_agent(req: ChatRequest):
    return await chat_with_agent(req)

# =====================================================================
# 2B. Multi-Conversation Management Endpoints
# =====================================================================

@app.get("/api/conversations", response_model=List[ConversationItem])
async def api_list_conversations(
    farmer_id: str = "farmer-001",
    include_archived: bool = False
):
    """List conversations for farmer, sorted by updated_at descending."""
    return list_conversations(farmer_id=farmer_id, include_archived=include_archived)

@app.post("/api/conversations")
async def api_create_conversation(req: ConversationCreateRequest):
    """Create a new conversation."""
    return create_conversation(
        farmer_id=req.farmer_id,
        title=req.title or "New Chat",
        language=req.language or "en"
    )

@app.get("/api/conversations/search")
async def api_search_conversations(
    q: str = Query(..., description="Search query across titles, messages, and crops"),
    farmer_id: str = "farmer-001"
):
    """Search conversation history across titles, messages, crops, and context."""
    return search_conversations(query=q, farmer_id=farmer_id)

@app.get("/api/conversations/{conversation_id}", response_model=ConversationDetail)
async def api_get_conversation(conversation_id: str):
    """Retrieve full conversation details including message history."""
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = get_conversation_messages(conversation_id)
    conv["messages"] = messages
    return conv

@app.patch("/api/conversations/{conversation_id}")
async def api_update_conversation(conversation_id: str, req: ConversationUpdateRequest):
    """Update conversation metadata (title, archive status, etc)."""
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    updates = {}
    if req.title is not None:
        updates["title"] = req.title
    if req.archived is not None:
        updates["archived"] = req.archived
    if req.manually_renamed is not None:
        updates["manually_renamed"] = req.manually_renamed
    if req.language is not None:
        updates["language"] = req.language
    if req.crop is not None:
        updates["crop"] = req.crop
    if req.crop_stage is not None:
        updates["crop_stage"] = req.crop_stage

    if updates:
        update_conversation(conversation_id, updates)
    return get_conversation(conversation_id)

@app.delete("/api/conversations/{conversation_id}")
async def api_delete_conversation(conversation_id: str):
    """Delete conversation and all its messages."""
    success = delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted", "conversation_id": conversation_id}

@app.post("/api/conversations/{conversation_id}/archive")
async def api_archive_conversation(conversation_id: str, archived: bool = True):
    """Toggle archive state for a conversation."""
    success = archive_conversation(conversation_id, archived=archived)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "success", "conversation_id": conversation_id, "archived": archived}

@app.get("/api/conversations/{conversation_id}/messages")
async def api_get_conversation_messages(conversation_id: str):
    """Retrieve message history for a conversation."""
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return get_conversation_messages(conversation_id)

@app.post("/api/conversations/{conversation_id}/messages")
async def api_post_conversation_message(conversation_id: str, req: ChatRequest):
    """Send a message within an existing conversation."""
    req.conversation_id = conversation_id
    return await chat_with_agent(req)

@app.get("/api/conversations/{conversation_id}/actions")
async def api_get_conversation_actions(conversation_id: str):
    """Retrieve consequential actions linked to this conversation."""
    return get_conversation_actions(conversation_id)

# 3. Farmer Profile Endpoints
# =====================================================================

@app.get("/api/farmer/{farmer_id}", response_model=FarmerProfile)
async def get_farmer(farmer_id: str):
    prof = get_farmer_profile(farmer_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Farmer profile not found")
    return prof

@app.put("/api/farmer/{farmer_id}", response_model=FarmerProfile)
async def update_farmer(farmer_id: str, updates: FarmerProfileUpdate):
    prof = update_farmer_profile(farmer_id, updates)
    if not prof:
        raise HTTPException(status_code=400, detail="Failed to update farmer profile")
    return prof

@app.get("/api/farmers", response_model=List[FarmerProfile])
async def list_farmers():
    return list_all_farmers()

@app.get("/api/farmer/{farmer_id}/plans")
async def get_saved_plans(farmer_id: str):
    return get_farmer_plans(farmer_id)

# =====================================================================
# 4. Direct Tool Endpoints (Observability & Direct Inspection)
# =====================================================================

@app.get("/api/market", response_model=MarketComparison)
async def api_get_market(crop: str = "tomato", location: str = "Vijayawada", demo: bool = False):
    return await get_market_prices(crop=crop, location=location, force_demo=demo)

@app.get("/api/weather", response_model=WeatherData)
async def api_get_weather(location: str = "Vijayawada", demo: bool = False):
    return await get_weather(location=location, force_demo=demo)

@app.post("/api/rag/search", response_model=RAGSearchResult)
async def api_rag_search(query: str = Query(...), crop: Optional[str] = None, stage: Optional[str] = None):
    return search_agriculture_knowledge(query=query, crop=crop, optional_stage=stage)

@app.get("/api/services", response_model=List[GovernmentService])
async def api_get_services(query: str = "all schemes", language: str = "en"):
    return search_agricultural_services(query=query, language=language)

# =====================================================================
# 5. Human-in-the-Loop Consequential Action Execution
# =====================================================================

@app.post("/api/action/confirm", response_model=ActionConfirmResponse)
async def confirm_action(req: ActionConfirmRequest):
    """
    Executes a consequential action strictly after explicit farmer approval.
    Ensures safe operations (e.g., saving farm plans, price alerts, activity reminders).
    """
    if not req.approved:
        update_action_status(req.action_id, "REJECTED")
        return ActionConfirmResponse(
            action_id=req.action_id,
            status="REJECTED",
            message="Action was declined by farmer. No changes were made."
        )

    # Fetch action details from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consequential_actions WHERE action_id = ?", (req.action_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Action not found or expired")

    action_row = dict(row)
    import json
    payload = json.loads(action_row["payload_json"])
    action_type = action_row["action_type"]

    result_details = {}

    if action_type == "SAVE_FARM_PLAN":
        crop = payload.get("crop", "Tomato")
        location = payload.get("location", "Vijayawada")
        stage = payload.get("stage", "Flowering")
        plan_id = save_farm_plan(
            farmer_id=req.farmer_id,
            crop=crop,
            location=location,
            stage=stage,
            plan_data=payload
        )
        result_details = {"saved_plan_id": plan_id, "crop": crop, "location": location}
        msg = f"Successfully saved {crop} action plan (ID #{plan_id}) to {req.farmer_id}'s farm notebook."

    elif action_type == "CREATE_PRICE_ALERT":
        msg = f"Price watch alert activated for {payload.get('crop')} at {payload.get('market', 'local mandi')}."
        result_details = payload

    elif action_type == "ADD_SPRAY_REMINDER":
        msg = f"Notification scheduled for {payload.get('activity')} at {payload.get('scheduled_time')}."
        result_details = payload

    elif action_type == "SAVE_PREFERENCE":
        msg = "Application document checklist and eligibility notes saved to your offline farm profile."
        result_details = payload

    else:
        msg = f"Permitted action '{action_row['title']}' executed successfully."

    # Mark action as EXECUTED
    update_action_status(req.action_id, "EXECUTED")

    return ActionConfirmResponse(
        action_id=req.action_id,
        status="EXECUTED",
        message=msg,
        result_data=result_details
    )

@app.get("/api/action/history/{farmer_id}")
async def get_action_history(farmer_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consequential_actions WHERE farmer_id = ? ORDER BY created_at DESC LIMIT 20", (farmer_id,))
    rows = cursor.fetchall()
    conn.close()
    
    import json
    history = []
    for r in rows:
        d = dict(r)
        d["payload"] = json.loads(d["payload_json"])
        del d["payload_json"]
        history.append(d)
    return history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

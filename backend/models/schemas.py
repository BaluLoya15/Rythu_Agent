from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# =====================================================================
# Farmer Profile Schemas
# =====================================================================

class FarmerProfile(BaseModel):
    id: str = "farmer-001"
    name: str = "Venkat Rao"
    location: str = "Vijayawada, Andhra Pradesh"
    district: str = "Krishna"
    state: str = "Andhra Pradesh"
    land_area: str = "2.0 Acres"
    soil_type: str = "Clay loam with assured irrigation"
    current_crop: str = "Paddy"
    crop_variety: str = "BPT-5204 (Samba Mahsuri)"
    crop_stage: str = "Panicle Initiation & Active Tillering (55-60 days)"
    sowing_date: str = "2026-08-10"
    irrigation_type: str = "Canal & Borewell System"
    farming_type: str = "Small & Marginal Farmer"
    contact_phone: Optional[str] = "+91 98480 12345"
    crops: List[str] = Field(default_factory=lambda: ["Paddy"])
    active_schemes: List[str] = Field(default_factory=lambda: ["PM-KISAN", "YSR Rythu Bharosa"])
    constraints: List[str] = Field(default_factory=lambda: ["Sensitive to waterlogging", "Requires balanced fertilizer schedule"])
    passport_photo_url: Optional[str] = "/assets/farmer_photo.jpg"
    aadhaar_number: Optional[str] = "XXXX-XXXX-4829"
    pan_number: Optional[str] = "ABCDE1234F"
    bank_name: Optional[str] = "State Bank of India (SBI)"
    bank_account_number: Optional[str] = "XXXXXX5621"
    bank_ifsc: Optional[str] = "SBIN0001234"
    dbt_linked: Optional[bool] = True
    pattadar_passbook_number: Optional[str] = "AP-KRI-2024-88412 (Khata: 412, Survey: 84/2A)"
    documents: Optional[List[Dict[str, Any]]] = Field(default_factory=lambda: [
        {
            "id": "doc-001",
            "type": "passport_photo",
            "name": "Farmer_Passport_Photo.jpg",
            "title": "Passport Size Photo",
            "status": "Verified",
            "format": "JPG",
            "size": "240 KB",
            "upload_date": "2026-08-15",
            "file_url": "/assets/farmer_photo.jpg"
        },
        {
            "id": "doc-002",
            "type": "aadhaar_card",
            "name": "Aadhaar_Card_VenkatRao.pdf",
            "title": "Aadhaar Card (UIDAI)",
            "number": "XXXX-XXXX-4829",
            "status": "e-KYC Verified",
            "format": "PDF",
            "size": "1.2 MB",
            "upload_date": "2026-08-15"
        },
        {
            "id": "doc-003",
            "type": "pan_card",
            "name": "PAN_Card_ABCDE1234F.pdf",
            "title": "PAN Card (Income Tax Dept)",
            "number": "ABCDE1234F",
            "status": "Verified",
            "format": "PDF",
            "size": "850 KB",
            "upload_date": "2026-08-16"
        },
        {
            "id": "doc-004",
            "type": "bank_passbook",
            "name": "SBI_Passbook_AadhaarLinked.pdf",
            "title": "Bank Passbook (DBT Linked)",
            "bank_name": "State Bank of India",
            "account_number": "XXXXXX5621",
            "ifsc": "SBIN0001234",
            "status": "DBT Active",
            "format": "PDF",
            "size": "1.8 MB",
            "upload_date": "2026-08-15"
        },
        {
            "id": "doc-005",
            "type": "pattadar_passbook",
            "name": "RoR_1B_Pattadar_Passbook.pdf",
            "title": "Pattadar Passbook / 1B Record",
            "passbook_number": "AP-KRI-2024-88412",
            "survey_numbers": "84/2A, 84/2B (2.0 Acres)",
            "status": "Revenue Dept Certified",
            "format": "PDF",
            "size": "2.4 MB",
            "upload_date": "2026-08-15"
        }
    ])

class FarmerProfileUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    land_area: Optional[str] = None
    soil_type: Optional[str] = None
    current_crop: Optional[str] = None
    crop_variety: Optional[str] = None
    crop_stage: Optional[str] = None
    sowing_date: Optional[str] = None
    irrigation_type: Optional[str] = None
    farming_type: Optional[str] = None
    crops: Optional[List[str]] = None
    passport_photo_url: Optional[str] = None
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    dbt_linked: Optional[bool] = None
    pattadar_passbook_number: Optional[str] = None
    documents: Optional[List[Dict[str, Any]]] = None

# =====================================================================
# Tool Output Schemas with Strict Data Provenance
# =====================================================================

class WeatherForecastDay(BaseModel):
    day: str
    temp_min: float
    temp_max: float
    condition: str
    rain_probability_pct: int
    spray_recommendation: str

class WeatherData(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    temperature_c: float
    humidity_pct: int
    rainfall_probability_pct: int
    precipitation_mm: float = 0.0
    wind_speed_kmh: float
    weather_condition: str
    forecast: List[WeatherForecastDay]
    spray_window_advisory: str
    timestamp: str
    source: str = "Open-Meteo"
    data_status: str = "LIVE"  # "LIVE", "UNAVAILABLE", "DEMO"
    is_live: bool = True
    error_message: Optional[str] = None

class MarketDataPoint(BaseModel):
    market_name: str
    district: str
    crop: str
    variety: str
    modal_price_per_quintal: float
    min_price_per_quintal: float
    max_price_per_quintal: float
    price_per_kg: float
    daily_arrival_tonnes: float
    price_trend: str  # "RISING", "FALLING", "STABLE"
    distance_km: float
    estimated_transport_cost_per_quintal: float
    net_effective_price_per_quintal: float
    date: str
    data_source: str
    data_status: str = "LIVE"  # "LIVE", "UNAVAILABLE", "DEMO"
    is_live: bool = True

class MarketComparison(BaseModel):
    crop: str
    primary_location: str
    markets: List[MarketDataPoint] = Field(default_factory=list)
    best_market: Optional[str] = None
    price_spread_per_quintal: float = 0.0
    recommended_strategy: str = ""
    analysis: str = ""
    disclaimer: str = ""
    data_status: str = "LIVE"  # "LIVE", "UNAVAILABLE", "DEMO"
    source: str = "AGMARKNET / e-NAM"
    error_message: Optional[str] = None

class RAGSource(BaseModel):
    document_title: str
    source_organization: str  # e.g., "ANGRAU / ICAR"
    section_or_chapter: str
    page_number: Optional[int] = None
    relevance_score: float
    content_snippet: str
    official_reference: str
    data_status: str = "VERIFIED_RESEARCH"  # Verified extension manual

class RAGSearchResult(BaseModel):
    query: str
    crop: Optional[str] = None
    sources: List[RAGSource] = Field(default_factory=list)
    total_found: int = 0
    data_status: str = "VERIFIED_RESEARCH"

class GovernmentService(BaseModel):
    id: str
    name: str
    scheme_code: str
    level: str  # "Central" or "State (Andhra Pradesh)"
    purpose: str
    target_beneficiaries: str
    eligibility_criteria: List[str]
    benefits: str
    subsidy_percentage: Optional[str] = None
    required_documents: List[str]
    application_process: List[str]
    official_portal_url: str
    helpline_number: str
    verified_status: Optional[str] = "Officially Verified (Ministry of Agriculture & Farmers Welfare)"
    last_verified_date: str = "2026-08"
    data_status: str = "VERIFIED_KNOWLEDGE"
    is_demo_data: bool = False

# =====================================================================
# Agent Planning & Execution Trace Schemas
# =====================================================================

class TaskPlanStep(BaseModel):
    step_number: int
    title: str
    tool: str  # "farmer_tool", "market_tool", "weather_tool", "rag_tool", "services_tool", "reasoning_engine"
    goal: str
    status: str = "PENDING"  # "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "SKIPPED"
    execution_time_ms: Optional[int] = None

class ToolTraceStep(BaseModel):
    step_id: str
    tool_name: str
    display_title: str
    status: str  # "RUNNING", "COMPLETED", "FAILED"
    input_params: Dict[str, Any]
    output_summary: str
    raw_output: Optional[Dict[str, Any]] = None
    execution_duration_ms: int
    data_status: str = "LIVE"  # "LIVE", "VERIFIED_KNOWLEDGE", "LOCAL_KNOWLEDGE", "UNAVAILABLE", "DEMO"
    is_demo: bool = False
    timestamp: str
    event_key: Optional[str] = None
    tool_id: Optional[str] = None

class ConsequentialAction(BaseModel):
    action_id: str
    title: str
    description: str
    why_reason: str = "This will help you keep track of needed actions on your farm profile."
    action_type: str  # "SAVE_FARM_PLAN", "CREATE_PRICE_ALERT", "ADD_SPRAY_REMINDER", "SAVE_PREFERENCE"
    payload: Dict[str, Any]
    status: str = "PROPOSED"  # "PROPOSED", "APPROVED", "REJECTED", "EXECUTED"
    requires_confirmation: bool = True
    consequences_summary: str
    created_at: str
    executed_at: Optional[str] = None

# =====================================================================
# Action Plan Schemas
# =====================================================================

class ActionPlan(BaseModel):
    crop: str
    location: str
    stage: str
    market_summary: str
    weather_summary: str
    critical_considerations: List[str]
    recommended_actions: List[Dict[str, Any]]  # step, title, detail, priority, timeline
    monitoring_tasks: List[str]
    risk_mitigation: List[str]
    sources_cited: List[str]
    data_provenance_notes: List[str] = Field(default_factory=list)
    generated_at: str
    language: str = "en"

# =====================================================================
# Agent State & API Schemas
# =====================================================================

class AgentState(BaseModel):
    session_id: str
    user_id: str
    query: str
    intent: str
    user_goal: str
    farmer_context: Optional[Dict[str, Any]] = None
    task_plan: List[TaskPlanStep] = Field(default_factory=list)
    tool_trace: List[ToolTraceStep] = Field(default_factory=list)
    market_data: Optional[MarketComparison] = None
    weather_data: Optional[WeatherData] = None
    rag_sources: List[RAGSource] = Field(default_factory=list)
    services_data: List[GovernmentService] = Field(default_factory=list)
    action_plan: Optional[ActionPlan] = None
    consequential_actions: List[ConsequentialAction] = Field(default_factory=list)
    final_response_markdown: str = ""
    live_sources_count: int = 0
    unavailable_sources_count: int = 0
    verified_sources_count: int = 0
    provenance_summary: str = ""
    language: str = "en"
    demo_mode: bool = False  # Production default is FALSE (LIVE FIRST)
    completed: bool = False

class ChatRequest(BaseModel):
    message: str
    farmer_id: Optional[str] = "farmer-001"
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
    language: Optional[str] = None
    force_demo_mode: bool = False  # Production default is FALSE (LIVE FIRST)

class ChatResponse(BaseModel):
    session_id: str
    conversation_id: Optional[str] = None
    language: str = "en"
    user_query: str
    intent: str
    markdown_reply: str
    response: Optional[str] = None
    task_plan: List[TaskPlanStep]
    tool_trace: List[ToolTraceStep]
    events: Optional[List[Dict[str, Any]]] = None
    action_plan: Optional[ActionPlan] = None
    market_comparison: Optional[MarketComparison] = None
    weather_data: Optional[WeatherData] = None
    rag_sources: List[RAGSource] = Field(default_factory=list)
    sources: Optional[List[Dict[str, Any]]] = None
    matched_services: List[GovernmentService] = Field(default_factory=list)
    proposed_actions: List[ConsequentialAction] = Field(default_factory=list)
    actions: Optional[List[Dict[str, Any]]] = None
    live_sources_count: int = 0
    unavailable_sources_count: int = 0
    verified_sources_count: int = 0
    provenance_summary: str = ""
    demo_mode: bool = False
    completed: bool = True

class ActionConfirmRequest(BaseModel):
    action_id: str
    farmer_id: str = "farmer-001"
    session_id: str
    conversation_id: Optional[str] = None
    approved: bool = True

class ActionConfirmResponse(BaseModel):
    action_id: str
    status: str
    message: str
    executed_at: Optional[str] = None
    result_data: Optional[Dict[str, Any]] = None

# =====================================================================
# Multi-Conversation Chat Schemas
# =====================================================================

class ConversationItem(BaseModel):
    id: str
    farmer_id: str
    title: str
    language: str = "en"
    crop: Optional[str] = None
    crop_stage: Optional[str] = None
    archived: bool = False
    manually_renamed: bool = False
    created_at: str
    updated_at: str

class ConversationDetail(BaseModel):
    id: str
    farmer_id: str
    title: str
    language: str = "en"
    crop: Optional[str] = None
    crop_stage: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    archived: bool = False
    manually_renamed: bool = False
    created_at: str
    updated_at: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)

class ConversationCreateRequest(BaseModel):
    farmer_id: str = "farmer-001"
    title: Optional[str] = "New Chat"
    language: Optional[str] = "en"

class ConversationUpdateRequest(BaseModel):
    title: Optional[str] = None
    archived: Optional[bool] = None
    manually_renamed: Optional[bool] = None
    language: Optional[str] = None
    crop: Optional[str] = None
    crop_stage: Optional[str] = None

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.models.schemas import (
    AgentState, TaskPlanStep, ToolTraceStep,
    MarketComparison, WeatherData, RAGSource,
    GovernmentService, ActionPlan, ConsequentialAction
)

def create_initial_state(user_query: str, farmer_id: str = "farmer-001", session_id: Optional[str] = None) -> AgentState:
    """Initializes a new explicit Agent State."""
    return AgentState(
        session_id=session_id or f"sess-{uuid.uuid4().hex[:8]}",
        user_id=farmer_id,
        query=user_query,
        intent="UNKNOWN",
        user_goal="Address farmer inquiry with actionable guidance",
        farmer_context=None,
        task_plan=[],
        tool_trace=[],
        market_data=None,
        weather_data=None,
        rag_sources=[],
        services_data=[],
        action_plan=None,
        consequential_actions=[],
        final_response_markdown="",
        demo_mode=True,
        completed=False
    )

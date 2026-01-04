from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class Explanation(BaseModel):
    """Human-readable explanation of agent decisions"""
    explanation_id: str = Field(..., description="Unique explanation identifier")
    decision_summary: str = Field(..., description="Brief summary of decision")
    narrative: Dict[str, Any] = Field(..., description="Detailed narrative explanation")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization data (graph, etc.)")


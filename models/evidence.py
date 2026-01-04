from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class RegulationFramework(str, Enum):
    PCI_DSS = "PCI-DSS"
    GDPR = "GDPR"
    CCPA = "CCPA"


class EventType(str, Enum):
    VIOLATION = "violation"
    REMEDIATION = "remediation"
    POLICY_CHECK = "policy_check"
    AGENT_DECISION = "agent_decision"


class EvidenceRecord(BaseModel):
    """Core evidence model for compliance events"""
    evidence_id: str = Field(..., description="Unique evidence identifier")
    event_type: EventType = Field(..., description="Type of event")
    regulation: Dict[str, Any] = Field(..., description="Regulation framework and clause details")
    detection: Dict[str, Any] = Field(..., description="Detection information")
    violation_state: Optional[Dict[str, Any]] = Field(None, description="Before/after violation states")
    remediation: Optional[Dict[str, Any]] = Field(None, description="Remediation action details")
    reasoning_chain: Optional[Dict[str, Any]] = Field(None, description="Agent reasoning and decision path")
    linkages: Optional[Dict[str, Any]] = Field(None, description="Links to related evidence, policies, controls")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")


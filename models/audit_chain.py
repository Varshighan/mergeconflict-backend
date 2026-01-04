from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class AuditChainNode(BaseModel):
    """Immutable audit chain node with hash chaining"""
    evidence_id: str = Field(..., description="Evidence identifier")
    previous_hash: Optional[str] = Field(None, description="Hash of previous node in chain")
    timestamp: datetime = Field(..., description="Node timestamp")
    evidence_data: Dict[str, Any] = Field(..., description="Evidence record data")
    data_hash: str = Field(..., description="Hash of evidence data")
    record_hash: str = Field(..., description="Hash of this record (includes previous_hash)")
    sequence_number: int = Field(..., description="Sequence number in chain")


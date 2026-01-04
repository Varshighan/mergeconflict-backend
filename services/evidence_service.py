import hashlib
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.evidence import EvidenceRecord, EventType
from services.audit_chain_service import AuditChainService


class EvidenceService:
    """Service for capturing and managing evidence records"""
    
    def __init__(self, audit_chain_service: AuditChainService):
        self.audit_chain_service = audit_chain_service
        self.evidence_store: Dict[str, EvidenceRecord] = {}  # In-memory store (replace with DB)
    
    def generate_evidence_id(self) -> str:
        """Generate unique evidence ID"""
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"EVID-{timestamp}-{unique_id}"
    
    def capture_evidence(
        self,
        event_type: EventType,
        regulation: Dict[str, Any],
        detection: Dict[str, Any],
        violation_state: Optional[Dict[str, Any]] = None,
        remediation: Optional[Dict[str, Any]] = None,
        reasoning_chain: Optional[Dict[str, Any]] = None,
        linkages: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EvidenceRecord:
        """Capture a new evidence record"""
        evidence_id = self.generate_evidence_id()
        
        evidence = EvidenceRecord(
            evidence_id=evidence_id,
            event_type=event_type,
            regulation=regulation,
            detection=detection,
            violation_state=violation_state,
            remediation=remediation,
            reasoning_chain=reasoning_chain,
            linkages=linkages,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        
        # Store evidence
        self.evidence_store[evidence_id] = evidence
        
        # Append to audit chain
        self.audit_chain_service.append(evidence)
        
        return evidence
    
    def get_evidence(self, evidence_id: str) -> Optional[EvidenceRecord]:
        """Retrieve evidence by ID"""
        return self.evidence_store.get(evidence_id)
    
    def update_evidence(self, evidence_id: str, updates: Dict[str, Any]) -> Optional[EvidenceRecord]:
        """Update evidence record (e.g., add after_state after remediation)"""
        evidence = self.evidence_store.get(evidence_id)
        if not evidence:
            return None
        
        # Update fields
        evidence_dict = evidence.model_dump()
        evidence_dict.update(updates)
        
        # Create new record with updates
        updated_evidence = EvidenceRecord(**evidence_dict)
        self.evidence_store[evidence_id] = updated_evidence
        
        return updated_evidence
    
    def get_evidence_in_range(
        self,
        start_date: datetime,
        end_date: datetime,
        tenant_id: Optional[str] = None
    ) -> List[EvidenceRecord]:
        """Get all evidence records in date range"""
        results = []
        for evidence in self.evidence_store.values():
            if start_date <= evidence.timestamp <= end_date:
                if tenant_id is None or (evidence.metadata and evidence.metadata.get("tenant_id") == tenant_id):
                    results.append(evidence)
        
        return sorted(results, key=lambda e: e.timestamp)
    
    def list_all_evidence(self) -> List[EvidenceRecord]:
        """List all evidence records"""
        return list(self.evidence_store.values())


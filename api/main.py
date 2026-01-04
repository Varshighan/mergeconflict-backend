from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from models.evidence import EvidenceRecord, EventType
from services.evidence_service import EvidenceService
from services.audit_chain_service import AuditChainService
from services.explanation_service import ExplanationService
from services.audit_bundle_service import AuditBundleService

# Initialize services
audit_chain_service = AuditChainService()
explanation_service = ExplanationService()
evidence_service = EvidenceService(audit_chain_service)
audit_bundle_service = AuditBundleService(audit_chain_service, explanation_service)

app = FastAPI(
    title="Evidence & Audit Trust Layer API",
    description="Evidence, Auditability & Trust Layer for PCI/PII Compliance System",
    version="1.0.0"
)


# Request/Response models
class CaptureEvidenceRequest(BaseModel):
    event_type: EventType
    regulation: Dict[str, Any]
    detection: Dict[str, Any]
    violation_state: Optional[Dict[str, Any]] = None
    remediation: Optional[Dict[str, Any]] = None
    reasoning_chain: Optional[Dict[str, Any]] = None
    linkages: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class CaptureEvidenceResponse(BaseModel):
    evidence_id: str
    message: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Evidence & Audit Trust Layer",
        "version": "1.0.0",
        "status": "operational"
    }


@app.post("/evidence/capture", response_model=CaptureEvidenceResponse)
async def capture_evidence(request: CaptureEvidenceRequest):
    """Capture a new evidence record"""
    try:
        evidence = evidence_service.capture_evidence(
            event_type=request.event_type,
            regulation=request.regulation,
            detection=request.detection,
            violation_state=request.violation_state,
            remediation=request.remediation,
            reasoning_chain=request.reasoning_chain,
            linkages=request.linkages,
            metadata=request.metadata
        )
        
        return CaptureEvidenceResponse(
            evidence_id=evidence.evidence_id,
            message="Evidence captured successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/evidence/{evidence_id}")
async def get_evidence(evidence_id: str):
    """Get evidence by ID"""
    evidence = evidence_service.get_evidence(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    
    return evidence.model_dump()


@app.get("/evidence")
async def list_evidence(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[str] = Query(None)
):
    """List evidence records, optionally filtered by date range"""
    if start_date and end_date:
        evidence_records = evidence_service.get_evidence_in_range(start_date, end_date, tenant_id)
    else:
        evidence_records = evidence_service.list_all_evidence()
    
    return {
        "count": len(evidence_records),
        "evidence": [e.model_dump() for e in evidence_records]
    }


@app.get("/audit/trail")
async def get_audit_trail(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """Get audit trail (hash chain)"""
    if start_date and end_date:
        chain_nodes = audit_chain_service.get_chain_in_range(start_date, end_date)
    else:
        chain_nodes = audit_chain_service.get_all_nodes()
    
    return {
        "count": len(chain_nodes),
        "chain": [node.model_dump() for node in chain_nodes]
    }


@app.get("/audit/verify")
async def verify_audit_trail():
    """Verify audit trail integrity"""
    verification = audit_chain_service.verify_chain()
    return verification


@app.get("/explanation/{evidence_id}")
async def get_explanation(evidence_id: str):
    """Get explanation for evidence record"""
    evidence = evidence_service.get_evidence(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    
    explanation = explanation_service.generate_explanation(evidence)
    return explanation.model_dump()


@app.post("/audit/generate-bundle")
async def generate_audit_bundle(
    tenant_id: str = Query(..., description="Tenant identifier"),
    start_date: datetime = Query(..., description="Start date"),
    end_date: datetime = Query(..., description="End date")
):
    """Generate audit bundle ZIP file"""
    # Get evidence in range
    evidence_records = evidence_service.get_evidence_in_range(start_date, end_date, tenant_id)
    
    if not evidence_records:
        raise HTTPException(status_code=404, detail="No evidence found in date range")
    
    # Generate bundle
    bundle_bytes = audit_bundle_service.generate_bundle(
        tenant_id=tenant_id,
        start_date=start_date,
        end_date=end_date,
        evidence_records=evidence_records
    )
    
    filename = f"audit_bundle_{tenant_id}_{start_date.date()}_{end_date.date()}.zip"
    
    return Response(
        content=bundle_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


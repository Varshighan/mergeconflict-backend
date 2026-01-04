# Evidence, Auditability & Trust Layer

**PCI/PII Compliance System - Evidence & Audit Layer**

## Overview

This is the Evidence, Auditability & Trust Layer for a RegTech PCI/PII compliance system. It provides:

- ✅ Autonomous evidence generation
- ✅ Immutable hash-chained audit trail
- ✅ Human-readable explanations
- ✅ One-click audit bundle generation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Demo Script (Optional - Test the Code)

```bash
python demo.py
```

This will:

- Capture sample evidence records
- Generate explanations
- Verify the audit trail
- Create an audit bundle ZIP file

### 3. Run the API Server

```bash
python -m api.main
```

Or using uvicorn directly:

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Access API Documentation

Open your browser to:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Evidence Management

- `POST /evidence/capture` - Capture new evidence
- `GET /evidence/{evidence_id}` - Get evidence by ID
- `GET /evidence` - List all evidence (optional date filter)

### Audit Trail

- `GET /audit/trail` - Get audit trail (hash chain)
- `GET /audit/verify` - Verify audit trail integrity

### Explanations

- `GET /explanation/{evidence_id}` - Get human-readable explanation

### Audit Bundles

- `POST /audit/generate-bundle` - Generate audit bundle ZIP

## Example Usage

### 1. Capture Evidence

```bash
curl -X POST "http://localhost:8000/evidence/capture" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "violation",
    "regulation": {
      "framework": "PCI-DSS",
      "clause": "3.2.1",
      "requirement": "PAN must be rendered unreadable"
    },
    "detection": {
      "detected_by": "Reflex Agent ID-7",
      "detection_method": "log_pattern",
      "confidence": 0.94
    },
    "violation_state": {
      "before": {"risk_score": 0.87},
      "after": {"risk_score": 0.12}
    },
    "remediation": {
      "agent_id": "RemediationAgent-1",
      "action_type": "mask_pan",
      "success": true
    },
    "reasoning_chain": {
      "steps": ["Step 1: Pattern matched", "Step 2: Validated", "Step 3: Remediated"]
    }
  }'
```

### 2. Get Evidence

```bash
curl "http://localhost:8000/evidence/EVID-1234567890-ABC123"
```

### 3. Get Explanation

```bash
curl "http://localhost:8000/explanation/EVID-1234567890-ABC123"
```

### 4. Verify Audit Trail

```bash
curl "http://localhost:8000/audit/verify"
```

### 5. Generate Audit Bundle

```bash
curl -X POST "http://localhost:8000/audit/generate-bundle?tenant_id=org_123&start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z" \
  --output audit_bundle.zip
```

## Project Structure

```
.
├── api/
│   └── main.py                 # FastAPI application
├── models/
│   ├── evidence.py             # EvidenceRecord model
│   ├── audit_chain.py          # AuditChainNode model
│   └── explanation.py          # Explanation model
├── services/
│   ├── evidence_service.py     # Evidence management
│   ├── audit_chain_service.py  # Hash-chained audit trail
│   ├── explanation_service.py  # Explanation generation
│   └── audit_bundle_service.py # Bundle generation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

### 1. Evidence Generation

- Automatic evidence ID generation
- Structured evidence records
- Links to regulations, policies, controls
- Before/after state tracking

### 2. Immutable Audit Trail

- Hash-chained records
- Tamper-evident design
- Integrity verification
- Append-only structure

### 3. Explainability

- Natural language narratives
- Regulation context
- Agent reasoning traces
- Decision summaries

### 4. Audit Bundles

- ZIP archive with all evidence
- Hash chain export
- Verification reports
- Executive summary
- Human-readable formats

## Testing

### Using Python

```python
from services.evidence_service import EvidenceService
from services.audit_chain_service import AuditChainService
from models.evidence import EventType

# Initialize services
audit_chain_service = AuditChainService()
evidence_service = EvidenceService(audit_chain_service)

# Capture evidence
evidence = evidence_service.capture_evidence(
    event_type=EventType.VIOLATION,
    regulation={"framework": "PCI-DSS", "clause": "3.2.1"},
    detection={"detected_by": "Agent-1", "confidence": 0.94}
)

print(f"Evidence ID: {evidence.evidence_id}")

# Verify chain
verification = audit_chain_service.verify_chain()
print(f"Chain valid: {verification['valid']}")
```

## Development Notes

### Current Implementation

- **Storage**: In-memory (Python dictionaries)
- **For Production**: Replace with PostgreSQL/SQLAlchemy
- **Architecture**: Ready for database migration

### Database Migration (Future)

To migrate to PostgreSQL:

1. Update `EvidenceService` to use SQLAlchemy
2. Update `AuditChainService` to use SQLAlchemy
3. Create database schema (see `db/schema.sql` if needed)
4. Add database connection pooling

### Production Considerations

- Add authentication/authorization
- Add rate limiting
- Add logging
- Add monitoring/metrics
- Use Redis for caching
- Use S3 for audit trail archival
- Add background jobs for integrity checks

## License

MIT

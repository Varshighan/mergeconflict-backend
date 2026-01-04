# Quick Start Guide - What to Do with the Code

## What You Have

A complete **Evidence, Auditability & Trust Layer** codebase with:

- ✅ **Models** (`models/`) - Data structures for Evidence, Audit Chain, Explanations
- ✅ **Services** (`services/`) - Business logic for evidence management, audit trails, explanations, bundle generation
- ✅ **API** (`api/main.py`) - FastAPI REST API with all endpoints
- ✅ **Demo Script** (`demo.py`) - Working example showing how everything works

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Test the Code (Run Demo)

```bash
python demo.py
```

This will:
- Create sample evidence records
- Generate explanations
- Verify the audit trail integrity
- Create an audit bundle ZIP file

**Expected Output:**
```
============================================================
Evidence & Audit Trust Layer - Demo
============================================================

1. Initializing services...
   ✓ Services initialized

2. Capturing evidence...
   ✓ Evidence captured: EVID-1234567890-ABC123

[... more output ...]

Demo completed successfully!
```

## Step 3: Start the API Server

```bash
python -m api.main
```

Or using uvicorn:

```bash
uvicorn api.main:app --reload --port 8000
```

## Step 4: Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## Step 5: Test the API Endpoints

### Capture Evidence

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
      "confidence": 0.94
    }
  }'
```

### Get Evidence

```bash
curl "http://localhost:8000/evidence/EVID-1234567890-ABC123"
```

### Verify Audit Trail

```bash
curl "http://localhost:8000/audit/verify"
```

### Generate Audit Bundle

```bash
curl -X POST "http://localhost:8000/audit/generate-bundle?tenant_id=org_123&start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z" \
  --output audit_bundle.zip
```

## Project Structure

```
.
├── api/
│   └── main.py                    # FastAPI application (START HERE for API)
├── models/
│   ├── evidence.py                # EvidenceRecord model
│   ├── audit_chain.py             # AuditChainNode model
│   └── explanation.py             # Explanation model
├── services/
│   ├── evidence_service.py        # Evidence management
│   ├── audit_chain_service.py     # Hash-chained audit trail
│   ├── explanation_service.py     # Explanation generation
│   └── audit_bundle_service.py    # Bundle generation
├── demo.py                         # Demo script (RUN THIS FIRST)
├── requirements.txt                # Dependencies
├── README.md                       # Full documentation
└── QUICK_START.md                  # This file
```

## Integration with Your System

To integrate this into your existing PCI compliance system:

1. **Replace in-memory storage** with your database (PostgreSQL, MongoDB, etc.)
   - Update `EvidenceService.evidence_store` to use SQLAlchemy/ORM
   - Update `AuditChainService.chain_store` to use database

2. **Add authentication/authorization** to API endpoints
   - Add JWT tokens or API keys
   - Add role-based access control

3. **Connect to your agents**
   - Have your Reflex/Cognitive agents call `/evidence/capture` endpoint
   - Pass evidence from your monitoring/logging systems

4. **Add background jobs**
   - Periodic integrity checks (`/audit/verify`)
   - Archive old audit chains to S3
   - Generate scheduled audit bundles

## Current Implementation Notes

- **Storage**: In-memory (Python dictionaries) - works for demo, needs database for production
- **No Authentication**: Add auth for production use
- **No Database**: Currently stores data in memory (lost on restart)

## For Hackathon Demo

1. **Run `python demo.py`** to show it works
2. **Start API**: `python -m api.main`
3. **Show Swagger UI**: http://localhost:8000/docs
4. **Generate audit bundle** via API
5. **Show verification** of audit trail

## Next Steps

1. ✅ Code is ready to run
2. ⏭️ Run `python demo.py` to test
3. ⏭️ Start API server for demo
4. ⏭️ Integrate with your existing agents/monitoring


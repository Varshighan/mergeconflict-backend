#!/usr/bin/env python3
"""
Demo script to show how to use the Evidence & Audit Trust Layer
"""

from datetime import datetime, timedelta
from models.evidence import EvidenceRecord, EventType
from services.evidence_service import EvidenceService
from services.audit_chain_service import AuditChainService
from services.explanation_service import ExplanationService
from services.audit_bundle_service import AuditBundleService


def main():
    print("=" * 60)
    print("Evidence & Audit Trust Layer - Demo")
    print("=" * 60)
    print()
    
    # Initialize services
    print("1. Initializing services...")
    audit_chain_service = AuditChainService()
    explanation_service = ExplanationService()
    evidence_service = EvidenceService(audit_chain_service)
    audit_bundle_service = AuditBundleService(audit_chain_service, explanation_service)
    print("   ✓ Services initialized\n")
    
    # Capture evidence
    print("2. Capturing evidence...")
    evidence = evidence_service.capture_evidence(
        event_type=EventType.VIOLATION,
        regulation={
            "framework": "PCI-DSS",
            "clause": "3.2.1",
            "requirement": "PAN must be rendered unreadable wherever stored",
            "severity": "critical"
        },
        detection={
            "detected_by": "Reflex Agent ID-7",
            "detection_method": "log_pattern",
            "confidence": 0.94,
            "pattern_matched": r"\b\d{13,19}\b",
            "location": "log_file:/var/log/app/transaction.log:line_1423"
        },
        violation_state={
            "before": {"risk_score": 0.87, "snapshot": "PAN visible in logs"},
            "after": {"risk_score": 0.12, "snapshot": "PAN masked"}
        },
        remediation={
            "agent_id": "RemediationAgent-1",
            "action_type": "mask_pan",
            "success": True,
            "executed_at": datetime.utcnow().isoformat()
        },
        reasoning_chain={
            "steps": [
                "Step 1: Pattern matched PAN candidate",
                "Step 2: Validated using Luhn algorithm (confidence: 0.94)",
                "Step 3: Checked policy POL-PCI-3.2.1-MASKING",
                "Step 4: Selected masking action (preserves audit trail)",
                "Step 5: Executed remediation in 2.1 minutes"
            ],
            "confidence_scores": {
                "detection": 0.94,
                "remediation": 0.98,
                "compliance_impact": 0.95
            }
        },
        metadata={
            "tenant_id": "org_123",
            "environment": "production"
        }
    )
    print(f"   ✓ Evidence captured: {evidence.evidence_id}\n")
    
    # Capture another evidence
    print("3. Capturing additional evidence...")
    evidence2 = evidence_service.capture_evidence(
        event_type=EventType.REMEDIATION,
        regulation={
            "framework": "GDPR",
            "clause": "Article 32",
            "requirement": "Ensure appropriate security measures"
        },
        detection={
            "detected_by": "Cognitive Agent ID-3",
            "detection_method": "policy_check",
            "confidence": 0.89
        },
        remediation={
            "agent_id": "RemediationAgent-2",
            "action_type": "encrypt_field",
            "success": True
        },
        metadata={
            "tenant_id": "org_123",
            "environment": "production"
        }
    )
    print(f"   ✓ Evidence captured: {evidence2.evidence_id}\n")
    
    # Get explanation
    print("4. Generating explanation...")
    explanation = explanation_service.generate_explanation(evidence)
    print(f"   ✓ Explanation generated: {explanation.explanation_id}")
    print(f"   Decision Summary: {explanation.decision_summary}\n")
    
    # Verify audit trail
    print("5. Verifying audit trail integrity...")
    verification = audit_chain_service.verify_chain()
    if verification["valid"]:
        print(f"   ✓ Audit trail is VALID ({verification['total_nodes']} nodes)")
    else:
        print(f"   ✗ Audit trail is INVALID")
        print(f"   Errors: {verification['errors']}")
    print()
    
    # Get audit trail
    print("6. Retrieving audit trail...")
    chain_nodes = audit_chain_service.get_all_nodes()
    print(f"   ✓ Retrieved {len(chain_nodes)} chain nodes")
    if chain_nodes:
        latest = chain_nodes[-1]
        print(f"   Latest node: {latest.evidence_id}")
        print(f"   Record hash: {latest.record_hash[:16]}...")
    print()
    
    # Generate audit bundle
    print("7. Generating audit bundle...")
    start_date = datetime.utcnow() - timedelta(days=1)
    end_date = datetime.utcnow()
    
    bundle_bytes = audit_bundle_service.generate_bundle(
        tenant_id="org_123",
        start_date=start_date,
        end_date=end_date,
        evidence_records=evidence_service.get_evidence_in_range(start_date, end_date, "org_123")
    )
    
    bundle_filename = f"audit_bundle_org_123_{datetime.utcnow().date()}.zip"
    with open(bundle_filename, "wb") as f:
        f.write(bundle_bytes)
    
    print(f"   ✓ Audit bundle generated: {bundle_filename}")
    print(f"   Bundle size: {len(bundle_bytes)} bytes\n")
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"  1. Check the generated audit bundle: {bundle_filename}")
    print(f"  2. Start the API server: python -m api.main")
    print(f"  3. Visit http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()


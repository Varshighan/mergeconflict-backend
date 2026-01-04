import io
import json
import zipfile
from datetime import datetime
from typing import List, Dict, Any, Optional
from models.evidence import EvidenceRecord
from services.audit_chain_service import AuditChainService
from services.explanation_service import ExplanationService


class AuditBundleService:
    """Service for generating audit-ready bundles"""
    
    def __init__(
        self,
        audit_chain_service: AuditChainService,
        explanation_service: ExplanationService
    ):
        self.audit_chain_service = audit_chain_service
        self.explanation_service = explanation_service
    
    def generate_bundle(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime,
        evidence_records: List[EvidenceRecord]
    ) -> bytes:
        """Generate audit bundle ZIP file"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Create manifest
            manifest = self._create_manifest(tenant_id, start_date, end_date, evidence_records)
            zip_file.writestr("MANIFEST.json", json.dumps(manifest, indent=2, default=str))
            
            # Add evidence directory
            evidence_index = []
            for evidence in evidence_records:
                evidence_index.append(evidence.evidence_id)
                evidence_data = evidence.model_dump()
                zip_file.writestr(
                    f"EVIDENCE/evidence_{evidence.evidence_id}.json",
                    json.dumps(evidence_data, indent=2, default=str)
                )
            zip_file.writestr("EVIDENCE/evidence_index.json", json.dumps(evidence_index, indent=2))
            
            # Add audit trail
            chain_nodes = self.audit_chain_service.get_chain_in_range(start_date, end_date)
            chain_data = [node.model_dump() for node in chain_nodes]
            zip_file.writestr(
                "AUDIT_TRAIL/hash_chain.json",
                json.dumps(chain_data, indent=2, default=str)
            )
            
            # Add verification report
            verification = self.audit_chain_service.verify_chain()
            zip_file.writestr(
                "AUDIT_TRAIL/chain_verification_report.txt",
                self._format_verification_report(verification)
            )
            
            # Add decision logs
            decision_logs = []
            for evidence in evidence_records:
                decision_logs.append({
                    "evidence_id": evidence.evidence_id,
                    "timestamp": evidence.timestamp.isoformat(),
                    "event_type": evidence.event_type,
                    "regulation": evidence.regulation.get("clause"),
                    "detected_by": evidence.detection.get("detected_by"),
                    "remediation": evidence.remediation.get("action_type") if evidence.remediation else None
                })
            
            # Save as JSONL (one JSON object per line)
            jsonl_content = "\n".join(json.dumps(log, default=str) for log in decision_logs)
            zip_file.writestr("DECISION_LOGS/agent_decisions.jsonl", jsonl_content)
            
            # Add explanations
            for evidence in evidence_records:
                explanation = self.explanation_service.generate_explanation(evidence)
                explanation_data = explanation.model_dump()
                zip_file.writestr(
                    f"DECISION_LOGS/explanations/{explanation.explanation_id}.json",
                    json.dumps(explanation_data, indent=2, default=str)
                )
            
            # Add executive summary
            summary = self._create_executive_summary(evidence_records)
            zip_file.writestr("EXECUTIVE_SUMMARY.md", summary)
        
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    def _create_manifest(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime,
        evidence_records: List[EvidenceRecord]
    ) -> Dict[str, Any]:
        """Create bundle manifest"""
        return {
            "tenant_id": tenant_id,
            "generated_at": datetime.utcnow().isoformat(),
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "evidence_count": len(evidence_records),
            "bundle_version": "1.0"
        }
    
    def _create_executive_summary(self, evidence_records: List[EvidenceRecord]) -> str:
        """Create executive summary markdown"""
        total = len(evidence_records)
        violations = sum(1 for e in evidence_records if e.event_type == "violation")
        remediations = sum(1 for e in evidence_records if e.remediation is not None)
        
        summary = f"""# Audit Executive Summary

## Overview
- **Total Events**: {total}
- **Violations Detected**: {violations}
- **Remediations Executed**: {remediations}

## Evidence Records
This bundle contains {total} evidence records covering compliance events, violations, and remediations.

## Audit Trail
The audit trail includes a hash-chained log of all evidence records, ensuring tamper-evident history.

## Verification
Run the verification script to confirm the integrity of the audit trail.
"""
        return summary
    
    def _format_verification_report(self, verification: Dict[str, Any]) -> str:
        """Format verification report as text"""
        lines = [
            "AUDIT TRAIL VERIFICATION REPORT",
            "=" * 50,
            "",
            f"Status: {'✓ VALID' if verification['valid'] else '✗ INVALID'}",
            f"Total Nodes: {verification.get('total_nodes', 0)}",
            ""
        ]
        
        if verification.get("errors"):
            lines.append("Errors Found:")
            for error in verification["errors"]:
                lines.append(f"  - {error.get('node')}: {error.get('issue')}")
        else:
            lines.append("No errors found. Chain integrity verified.")
        
        return "\n".join(lines)


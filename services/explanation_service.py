from typing import Dict, Any
from models.evidence import EvidenceRecord
from models.explanation import Explanation


class ExplanationService:
    """Service for generating human-readable explanations"""
    
    def generate_explanation(self, evidence: EvidenceRecord) -> Explanation:
        """Generate explanation for evidence record"""
        explanation_id = f"EXP-{evidence.evidence_id}"
        
        # Build narrative
        narrative = {
            "what": self._build_what(evidence),
            "why_flagged": self._build_why_flagged(evidence),
            "regulation_context": evidence.regulation,
            "detection_details": evidence.detection,
            "remediation_choice": evidence.remediation or {},
            "agent_reasoning": evidence.reasoning_chain or {}
        }
        
        # Build decision summary
        decision_summary = self._build_decision_summary(evidence)
        
        return Explanation(
            explanation_id=explanation_id,
            decision_summary=decision_summary,
            narrative=narrative
        )
    
    def _build_what(self, evidence: EvidenceRecord) -> str:
        """Build 'what happened' description"""
        detected_by = evidence.detection.get("detected_by", "System")
        violation_type = evidence.violation_state.get("violation_type") if evidence.violation_state else "compliance issue"
        
        return f"{detected_by} detected {violation_type}"
    
    def _build_why_flagged(self, evidence: EvidenceRecord) -> str:
        """Build 'why was this flagged' explanation"""
        regulation = evidence.regulation
        framework = regulation.get("framework", "")
        clause = regulation.get("clause", "")
        requirement = regulation.get("requirement", "")
        
        context = evidence.detection.get("context", "")
        
        explanation = f"{framework} {clause} requires that {requirement}."
        if context:
            explanation += f" This violation occurred because {context}."
        
        return explanation
    
    def _build_decision_summary(self, evidence: EvidenceRecord) -> str:
        """Build brief decision summary"""
        if evidence.remediation:
            action = evidence.remediation.get("action_type", "remediation")
            agent = evidence.remediation.get("agent_id", "agent")
            return f"{agent} executed {action} to resolve violation"
        
        detected_by = evidence.detection.get("detected_by", "System")
        return f"{detected_by} flagged violation for {evidence.regulation.get('clause', 'regulation')}"


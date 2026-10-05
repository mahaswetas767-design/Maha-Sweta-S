"""Reusable evaluation metrics for the Phase 2 analyst study framework."""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SessionMetrics:
    procedure_adherence_pct: float
    missed_steps: int
    evidence_completeness_pct: float
    decision_accuracy_pct: float
    investigation_time_sec: float
    critical_errors: int

    def as_dict(self) -> Dict[str, Any]:
        return {
            "procedure_adherence_pct": round(float(self.procedure_adherence_pct), 2),
            "missed_steps": int(self.missed_steps),
            "evidence_completeness_pct": round(float(self.evidence_completeness_pct), 2),
            "decision_accuracy_pct": round(float(self.decision_accuracy_pct), 2),
            "investigation_time_sec": round(float(self.investigation_time_sec), 2),
            "critical_errors": int(self.critical_errors),
        }

def compare_sessions(before: SessionMetrics, after: SessionMetrics) -> Dict[str, float]:
    """Compare a baseline session with an assistant-supported session.

    This is a calculation helper only. It does not claim a human study result.
    """
    time_reduction = 0.0
    if before.investigation_time_sec > 0:
        time_reduction = (before.investigation_time_sec - after.investigation_time_sec) / before.investigation_time_sec * 100
    return {
        "adherence_change_pct_points": round(after.procedure_adherence_pct - before.procedure_adherence_pct, 2),
        "evidence_completeness_change_pct_points": round(after.evidence_completeness_pct - before.evidence_completeness_pct, 2),
        "decision_accuracy_change_pct_points": round(after.decision_accuracy_pct - before.decision_accuracy_pct, 2),
        "investigation_time_reduction_pct": round(time_reduction, 2),
        "critical_error_change": int(after.critical_errors - before.critical_errors),
        "missed_step_change": int(after.missed_steps - before.missed_steps),
    }

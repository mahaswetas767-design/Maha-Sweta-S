from __future__ import annotations
from typing import Dict, Any, List
from .metrics import summarize_sessions, time_reduction_percent

TARGETS = {
    "procedure_adherence_pct": 90.0,
    "evidence_completeness_pct": 85.0,
    "critical_error_rate_pct_max": 5.0,
    "time_reduction_pct": 20.0,
}

def compare_baseline_and_assisted(
    baseline_sessions: List[Dict[str, Any]],
    assisted_sessions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    baseline = summarize_sessions(baseline_sessions)
    assisted = summarize_sessions(assisted_sessions)
    reduction = time_reduction_percent(
        baseline["avg_investigation_time_min"],
        assisted["avg_investigation_time_min"],
    )
    return {
        "baseline": baseline,
        "assisted": assisted,
        "time_reduction_pct": reduction,
        "target_status": {
            "procedure_adherence": assisted["procedure_adherence_pct"] >= TARGETS["procedure_adherence_pct"],
            "evidence_completeness": assisted["evidence_completeness_pct"] >= TARGETS["evidence_completeness_pct"],
            "critical_error_rate": assisted["critical_error_rate_pct"] <= TARGETS["critical_error_rate_pct_max"],
            "time_reduction": reduction >= TARGETS["time_reduction_pct"],
        },
        "note": "Simulated/template evaluation only. Replace with measured analyst study data before claiming effectiveness.",
    }

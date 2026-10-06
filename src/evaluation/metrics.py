from __future__ import annotations
from typing import Iterable, Dict, Any

def _safe_mean(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else 0.0

def procedure_adherence(completed_steps: int, expected_steps: int) -> float:
    return round((completed_steps / expected_steps) * 100, 2) if expected_steps else 0.0

def evidence_completeness(required: int, captured: int) -> float:
    return round((captured / required) * 100, 2) if required else 0.0

def critical_error_rate(critical_errors: int, total_cases: int) -> float:
    return round((critical_errors / total_cases) * 100, 2) if total_cases else 0.0

def time_reduction_percent(baseline_minutes: float, assisted_minutes: float) -> float:
    if baseline_minutes <= 0:
        return 0.0
    return round(((baseline_minutes - assisted_minutes) / baseline_minutes) * 100, 2)

def summarize_sessions(rows: Iterable[Dict[str, Any]]) -> Dict[str, float]:
    rows = list(rows)
    if not rows:
        return {
            "procedure_adherence_pct": 0.0,
            "evidence_completeness_pct": 0.0,
            "decision_accuracy_pct": 0.0,
            "critical_error_rate_pct": 0.0,
            "avg_investigation_time_min": 0.0,
        }
    return {
        "procedure_adherence_pct": round(_safe_mean(r.get("procedure_adherence_pct", 0) for r in rows), 2),
        "evidence_completeness_pct": round(_safe_mean(r.get("evidence_completeness_pct", 0) for r in rows), 2),
        "decision_accuracy_pct": round(_safe_mean(r.get("decision_accuracy_pct", 0) for r in rows), 2),
        "critical_error_rate_pct": round(_safe_mean(r.get("critical_error_rate_pct", 0) for r in rows), 2),
        "avg_investigation_time_min": round(_safe_mean(r.get("investigation_time_min", 0) for r in rows), 2),
    }

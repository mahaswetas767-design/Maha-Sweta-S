from __future__ import annotations
import random
from typing import List, Dict

def simulate_sessions(n: int = 20, seed: int = 42) -> List[Dict]:
    """Generate clearly labeled synthetic evaluation sessions; not real analyst results."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        rows.append({
            "session_id": f"S{i+1:03d}",
            "analyst_group": "synthetic_assisted",
            "procedure_adherence_pct": round(rng.uniform(78, 98), 2),
            "evidence_completeness_pct": round(rng.uniform(72, 97), 2),
            "decision_accuracy_pct": round(rng.uniform(78, 99), 2),
            "critical_error_rate_pct": round(rng.uniform(0, 8), 2),
            "investigation_time_min": round(rng.uniform(18, 50), 2),
        })
    return rows

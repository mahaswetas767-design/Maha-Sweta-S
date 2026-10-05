from src.evaluation.metrics import SessionMetrics, compare_sessions

def test_session_comparison():
    before = SessionMetrics(70, 3, 60, 75, 300, 2)
    after = SessionMetrics(90, 1, 90, 88, 240, 0)
    out = compare_sessions(before, after)
    assert out["adherence_change_pct_points"] == 20
    assert out["investigation_time_reduction_pct"] == 20
    assert out["critical_error_change"] == -2

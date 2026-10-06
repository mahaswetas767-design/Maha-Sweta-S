from src.evaluation.metrics import (
    procedure_adherence,
    evidence_completeness,
    critical_error_rate,
    time_reduction_percent,
)

def test_procedure_adherence():
    assert procedure_adherence(9, 10) == 90.0

def test_evidence_completeness():
    assert evidence_completeness(8, 10) == 80.0

def test_critical_error_rate():
    assert critical_error_rate(1, 20) == 5.0

def test_time_reduction():
    assert time_reduction_percent(50, 40) == 20.0

import pytest
from src.engine.decision_logger import DecisionLogger
def test_override_requires_reason():
    with pytest.raises(ValueError):
        DecisionLogger().log("I1","Override","Escalate","Overridden",override=True)

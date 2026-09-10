from src.engine.recommendation_engine import recommend
def test_failed_login_rule():
    r=recommend({"event_id":"E1","failed_login_count":8,"authentication_status":"Failed"})
    assert any(x["rule_id"]=="RULE-LOGIN-001" for x in r)

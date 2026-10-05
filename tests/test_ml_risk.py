import pandas as pd
from src.ml.train_risk_model import make_risk_label
def test_risk_label_has_expected_classes():
    df=pd.DataFrame({"severity":["Low","Critical"],"failed_login_count":[0,8],"data_access_count":[10,90],"malware_indicator":["None","Detected"],"event_type":["Endpoint Alert","Privilege Escalation"]})
    labels=make_risk_label(df)
    assert set(labels).issubset({"Low","Medium","High"})
    assert labels.iloc[1]=="High"

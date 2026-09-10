"""Explainable, deterministic SOC recommendations."""
RULES=[
("RULE-LOGIN-001",lambda e:e.get("failed_login_count",0)>=5,"Investigate suspicious authentication activity","Multiple failed authentication attempts detected.","High",True),
("RULE-LOGIN-002",lambda e:e.get("failed_login_count",0)>=5 and e.get("authentication_status")=="Success","Review possible account compromise","Successful authentication followed repeated failures.","High",True),
("RULE-MALWARE-001",lambda e:e.get("malware_indicator") in {"Detected","Suspected"},"Investigate malware alert","Malware indicator reported by security telemetry.","Critical",True),
("RULE-NETWORK-001",lambda e:e.get("event_type")=="Suspicious Network Connection","Review suspicious network activity","Security telemetry reported a suspicious connection.","High",True),
("RULE-ACCESS-001",lambda e:e.get("data_access_count",0)>=80,"Investigate abnormal data access","Data access volume exceeds the investigation threshold.","High",True),
("RULE-PRIV-001",lambda e:e.get("event_type")=="Privilege Escalation","Investigate privilege escalation","A privilege escalation event was detected.","Critical",True),
("RULE-DEVICE-001",lambda e:e.get("event_type")=="Device Communication Failure","Review medical device communication","A monitored medical device reported communication failure.","Medium",False),
("RULE-CORRELATION-001",lambda e:e.get("severity")=="Critical","Escalate critical investigation","Critical severity requires prompt human review.","Critical",True),
]
def recommend(event):
    results=[]
    for rid,cond,rec,reason,sev,confirm in RULES:
        if cond(event):
            results.append({"rule_id":rid,"recommendation":rec,"reason":reason,
                            "evidence":{k:event.get(k) for k in ["event_id","device_id","user_id","source_ip","timestamp","failed_login_count","data_access_count"]},
                            "severity":sev,"confidence":0.90,"requires_human_confirmation":confirm})
    return results

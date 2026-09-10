from ipaddress import ip_address
def validate_event(e):
    errors=[]
    if not e.get("event_id"): errors.append("Missing event_id")
    if e.get("severity") not in {"Low","Medium","High","Critical"}: errors.append("Invalid severity")
    for key in ("source_ip","destination_ip"):
        try: ip_address(str(e[key]))
        except Exception: errors.append(f"Invalid {key}")
    for key in ("failed_login_count","data_access_count"):
        try:
            if float(e[key]) < 0: errors.append(f"Negative {key}")
        except Exception: errors.append(f"Invalid {key}")
    return errors

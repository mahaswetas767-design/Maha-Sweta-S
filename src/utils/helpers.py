def high_impact(action):
    return action.lower() in {"isolate device","block network","disable account","escalate incident"}

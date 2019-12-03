def is_mobile_user_agent(user_agent):
    if "Android" in user_agent or "iPhone" in user_agent or "iPad" in user_agent:
        return True
    else:
        return False
    

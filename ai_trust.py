import time

user_attempts = {}


def evaluate_trust(user_id: str):
    """Returns {user, score, decision}."""
    score = 0
    current_time = time.time()

    if user_id not in user_attempts:
        user_attempts[user_id] = []

    recent_attempts = [t for t in user_attempts[user_id] if current_time - t < 10]

    if len(recent_attempts) > 3:
        score -= 40
    else:
        score += 70
        score += 20

    user_attempts[user_id].append(current_time)

    decision = "VERIFIED" if score >= 60 else "REJECTED"
    return {"user": user_id, "score": score, "decision": decision}

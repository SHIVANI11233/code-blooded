import time

# Track user attempts
user_attempts = {}

def ai_trust_validation(user_id: str, token: str, is_duplicate: bool):
    score = 0
    current_time = time.time()

    # Initialize user tracking
    if user_id not in user_attempts:
        user_attempts[user_id] = []

    # Check frequency (before appending this attempt)
    recent_attempts = [
        t for t in user_attempts[user_id]
        if current_time - t < 10  # last 10 seconds
    ]

    if len(recent_attempts) > 3:
        score -= 40  # suspicious: too many attempts in short time
    else:
        score += 70  # normal behavior: first valid attempt per window
        score += 20  # normal timing

    user_attempts[user_id].append(current_time)

    # Duplicate token check (handled by hash_engine before this)
    if is_duplicate:
        score -= 100

    # Final decision
    if score >= 60:
        decision = "VERIFIED"
    else:
        decision = "REJECTED"

    return {
        "user": user_id,
        "score": score,
        "decision": decision
    }

def evaluate_trust(user_id: str):
    """API wrapper: duplicate handled by hash_engine, so is_duplicate=False."""
    return ai_trust_validation(user_id, "", False)


# -------- TEST --------
if __name__ == "__main__":
    print(ai_trust_validation("student_1", "TOKEN_1", False))
    time.sleep(2)
    print(ai_trust_validation("student_1", "TOKEN_2", False))
    time.sleep(2)
    print(ai_trust_validation("student_1", "TOKEN_3", False))
    time.sleep(1)
    print(ai_trust_validation("student_1", "TOKEN_4", False))  # suspicious

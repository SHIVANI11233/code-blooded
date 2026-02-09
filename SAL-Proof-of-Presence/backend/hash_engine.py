import hashlib
import sys
import time

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Store hashes temporarily (later this goes to DB / blockchain)
seen_hashes = set()

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def verify_participation(token: str):
    """Returns (is_valid, hash_value). Used by server."""
    hashed = generate_hash(token)
    if hashed in seen_hashes:
        return False, hashed
    seen_hashes.add(hashed)
    return True, hashed

def process_presence_token(token: str):
    hashed = generate_hash(token)
    if hashed in seen_hashes:
        print("❌ Duplicate or replay attempt detected!")
        return False
    seen_hashes.add(hashed)
    print("✅ Valid participation")
    print("Hash:", hashed)
    return True

# ---- TEST ----
if __name__ == "__main__":
    token1 = "ROOM_101_AI_WORKSHOP_12345"
    token2 = "ROOM_101_AI_WORKSHOP_12345"  # duplicate
    token3 = "ROOM_101_AI_WORKSHOP_12350"  # new token

    process_presence_token(token1)
    time.sleep(1)
    process_presence_token(token2)
    time.sleep(1)
    process_presence_token(token3)

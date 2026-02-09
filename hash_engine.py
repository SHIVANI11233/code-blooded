import hashlib

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

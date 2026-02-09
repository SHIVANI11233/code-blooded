"""
SAL Backend - Privacy-Preserving Hash Module (Phase 1)
Generates and verifies cryptographic hashes for participation proofs.
"""

import hashlib
from typing import Optional

# Delimiter for payload construction (must match frontend)
PAYLOAD_DELIM = "|"


def build_payload(session_id: str, timestamp: str, student_id: str) -> str:
    """
    Build deterministic payload string for hashing.
    Order matters - must match frontend exactly.
    """
    return f"{session_id}{PAYLOAD_DELIM}{timestamp}{PAYLOAD_DELIM}{student_id}"


def compute_hash(payload: str) -> str:
    """
    Compute SHA-256 hash of payload.
    Returns hex-encoded hash string.
    """
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_participation_hash(
    participation_hash: str,
    session_id: str,
    timestamp: str,
    student_id: str,
) -> bool:
    """
    Verify that the provided hash matches the computed hash of the payload.
    Returns True if hash is valid.
    """
    payload = build_payload(session_id, timestamp, student_id)
    expected_hash = compute_hash(payload)
    return participation_hash == expected_hash

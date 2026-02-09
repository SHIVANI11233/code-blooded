"""
SAL Backend - AI Trust Score Engine (Step 3)
Validates attendance requests and generates trust scores.
"""

from datetime import datetime, timedelta
from models import AttendanceRequest, AttendanceResponse
from typing import List, Dict, Tuple

# Configuration
TRUST_THRESHOLD = 70.0  # Minimum score for approval
EVENT_START_TIME = "10:00:00"  # Workshop start (24h format)
EVENT_END_TIME = "12:00:00"   # Workshop end
EVENT_DATE = "2026-02-07"    # Event date (YYYY-MM-DD) - update per event

def validate_attendance(
    request: AttendanceRequest,
    history: List[Dict]
) -> AttendanceResponse:
    """
    Main AI validation function.
    Checks timing, duplicates, replay attacks, behavior patterns.
    
    Returns: AttendanceResponse with trust_score and approval status.
    """
    score = 100.0
    reasons = []
    
    # 1. Check timing validity
    timing_score, timing_reason = check_timing(request.timestamp)
    score -= (100 - timing_score)
    if timing_reason:
        reasons.append(timing_reason)
    
    # 2. Check for duplicates
    duplicate_score, duplicate_reason = check_duplicates(request, history)
    score -= (100 - duplicate_score)
    if duplicate_reason:
        reasons.append(duplicate_reason)
    
    # 3. Check for rapid retries (suspicious behavior)
    retry_score, retry_reason = check_rapid_retries(request, history)
    score -= (100 - retry_score)
    if retry_reason:
        reasons.append(retry_reason)
    
    # 4. Check signal reuse (if we had ESP signal data)
    # For now, we rely on timing + duplicate checks
    
    # Ensure score doesn't go negative
    score = max(0.0, min(100.0, score))
    
    approved = score >= TRUST_THRESHOLD
    reason = "; ".join(reasons) if reasons else "Valid attendance request"
    
    return AttendanceResponse(
        approved=approved,
        trust_score=round(score, 2),
        reason=reason
    )

def check_timing(timestamp_str: str) -> Tuple[float, str]:
    """
    Validates if request timestamp is within event window.
    Returns: (score, reason)
    """
    try:
        req_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        req_time_local = req_time.replace(tzinfo=None)
        
        event_start = datetime.fromisoformat(f"{EVENT_DATE}T{EVENT_START_TIME}")
        event_end = datetime.fromisoformat(f"{EVENT_DATE}T{EVENT_END_TIME}")
        
        # Allow 15 minutes before start (setup time)
        window_start = event_start - timedelta(minutes=15)
        # Allow 30 minutes after end (cleanup)
        window_end = event_end + timedelta(minutes=30)
        
        if window_start <= req_time_local <= window_end:
            return (100.0, None)
        elif req_time_local < window_start:
            return (0.0, f"Too early: request at {req_time_local.time()}, event starts at {EVENT_START_TIME}")
        else:
            return (0.0, f"Too late: request at {req_time_local.time()}, event ended at {EVENT_END_TIME}")
            
    except Exception as e:
        return (0.0, f"Invalid timestamp format: {str(e)}")

def check_duplicates(request: AttendanceRequest, history: List[Dict]) -> Tuple[float, str]:
    """
    Checks if this student already marked attendance for this event.
    Returns: (score, reason)
    """
    for entry in history:
        stored_req = entry.get('request', {})
        if (stored_req.get('student_id') == request.student_id and
            stored_req.get('event_id') == request.event_id):
            result = entry.get('result', {})
            if result.get('approved', False):
                return (0.0, f"Duplicate: Student {request.student_id} already marked attendance")
    
    return (100.0, None)

def check_rapid_retries(request: AttendanceRequest, history: List[Dict]) -> Tuple[float, str]:
    """
    Detects suspicious rapid retry patterns (potential automated attacks).
    Returns: (score, reason)
    """
    try:
        req_time = datetime.fromisoformat(request.timestamp.replace('Z', '+00:00'))
        req_time_local = req_time.replace(tzinfo=None)
        
        # Count requests from same student in last 2 minutes
        recent_count = 0
        for entry in history:
            stored_req = entry.get('request', {})
            if stored_req.get('student_id') == request.student_id:
                stored_time = datetime.fromisoformat(
                    stored_req.get('timestamp', '').replace('Z', '+00:00')
                ).replace(tzinfo=None)
                
                time_diff = abs((req_time_local - stored_time).total_seconds())
                if time_diff < 120:  # 2 minutes
                    recent_count += 1
        
        if recent_count >= 3:
            return (0.0, f"Suspicious: {recent_count + 1} rapid requests in 2 minutes")
        elif recent_count >= 1:
            return (50.0, f"Warning: Multiple requests detected")
        
        return (100.0, None)
        
    except Exception as e:
        return (50.0, f"Could not check retry pattern: {str(e)}")

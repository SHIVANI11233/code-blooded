"""
SAL Backend - Data Models
Defines request/response structures for attendance system.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class AttendanceRequest:
    """Attendance request from student (Step 2)"""
    student_id: str
    event_id: str
    timestamp: str
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'event_id': self.event_id,
            'timestamp': self.timestamp
        }


@dataclass
class ParticipationHashRequest:
    """Phase 1: Hash-based participation request"""
    participation_hash: str  # SHA-256 of (session_id|timestamp|student_id)
    session_id: str
    timestamp: str
    student_id: str
    
    def to_dict(self):
        return {
            'participation_hash': self.participation_hash,
            'session_id': self.session_id,
            'timestamp': self.timestamp,
            'student_id': self.student_id
        }

@dataclass
class AttendanceResponse:
    """AI validation result (Step 3)"""
    approved: bool
    trust_score: float
    reason: str
    
    def to_dict(self):
        return {
            'approved': self.approved,
            'trust_score': self.trust_score,
            'reason': self.reason
        }

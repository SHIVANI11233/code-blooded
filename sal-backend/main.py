"""
SAL Backend - Main API Server
Handles attendance requests and routes them to AI validation engine.
Phase 1: Hash-based participation verification.
"""

from flask import Flask, request, jsonify
from datetime import datetime
from models import AttendanceRequest, AttendanceResponse
from ai_engine import validate_attendance
from hashing import verify_participation_hash

app = Flask(__name__)


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

# In-memory storage (replace with database in production)
attendance_requests = []
stored_hashes = []  # Phase 1: For duplicate/replay detection

@app.route('/attendance/participate', methods=['OPTIONS'])
@app.route('/attendance/request', methods=['OPTIONS'])
def cors_preflight():
    return "", 204


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/attendance/request', methods=['POST'])
def request_attendance():
    """
    Step 2 → Step 3 bridge
    Receives attendance request from frontend, validates via AI engine.
    """
    try:
        data = request.json
        
        # Parse request
        req = AttendanceRequest(
            student_id=data.get('studentId'),
            event_id=data.get('eventId'),
            timestamp=data.get('timestamp', datetime.now().isoformat())
        )
        
        # Validate via AI engine (Step 3)
        result = validate_attendance(req, attendance_requests)
        
        # Store request (for duplicate detection, history)
        attendance_requests.append({
            'request': req.to_dict(),
            'result': result.to_dict(),
            'processed_at': datetime.now().isoformat()
        })
        
        return jsonify(result.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            "approved": False,
            "trust_score": 0,
            "reason": f"Error: {str(e)}"
        }), 400

@app.route('/attendance/participate', methods=['POST'])
def participate():
    """
    Phase 1: Hash-based participation request.
    Flow: session_id + timestamp + student_id → hash → verify → AI → record
    """
    try:
        data = request.json
        participation_hash = data.get('participation_hash', '').strip()
        session_id = data.get('session_id', '').strip()
        timestamp = data.get('timestamp', '')
        student_id = data.get('student_id', '').strip()

        if not all([participation_hash, session_id, timestamp, student_id]):
            return jsonify({
                "approved": False,
                "trust_score": 0,
                "reason": "Missing: participation_hash, session_id, timestamp, or student_id"
            }), 400

        # Step 1: Verify hash matches payload
        if not verify_participation_hash(participation_hash, session_id, timestamp, student_id):
            return jsonify({
                "approved": False,
                "trust_score": 0,
                "reason": "Hash verification failed: payload tampering or invalid hash"
            }), 400

        # Step 2: Hash matching - reject duplicates/replays
        if participation_hash in stored_hashes:
            return jsonify({
                "approved": False,
                "trust_score": 0,
                "reason": "Duplicate or replay: this participation hash was already recorded"
            }), 400

        # Step 3: AI Trust Validation
        req = AttendanceRequest(
            student_id=student_id,
            event_id=session_id,
            timestamp=timestamp
        )
        result = validate_attendance(req, attendance_requests)

        # Step 4: Store only if approved
        if result.approved:
            stored_hashes.append(participation_hash)

        attendance_requests.append({
            'request': req.to_dict(),
            'participation_hash': participation_hash,
            'result': result.to_dict(),
            'processed_at': datetime.now().isoformat()
        })

        return jsonify(result.to_dict()), 200

    except Exception as e:
        return jsonify({
            "approved": False,
            "trust_score": 0,
            "reason": f"Error: {str(e)}"
        }), 400


@app.route('/attendance/history', methods=['GET'])
def get_history():
    """Get all attendance requests (for debugging/admin)"""
    return jsonify({
        "total": len(attendance_requests),
        "requests": attendance_requests
    })

if __name__ == '__main__':
    print("🚀 SAL Backend starting on http://localhost:5000")
    print("📡 POST /attendance/request - Submit attendance (legacy)")
    print("📡 POST /attendance/participate - Phase 1: Hash-based participation")
    print("📊 GET /attendance/history - View all requests")
    app.run(host='0.0.0.0', port=5000, debug=True)

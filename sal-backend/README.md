# SAL Backend — AI Trust Score Engine (Step 3)

Backend API that validates attendance requests using AI trust scoring. This is where proxy attempts, duplicates, and replay attacks are detected.

## 🎯 What This Does

- **Receives** attendance requests from frontend (Step 2)
- **Validates** via AI engine:
  - ✅ Timing validity (within event window)
  - ✅ Duplicate detection (one attendance per student/event)
  - ✅ Rapid retry detection (suspicious behavior)
- **Returns** trust score + approval status

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask
```

### 2. Run the Server

```bash
python main.py
```

Server starts on **http://localhost:5000**

### 3. Test It

**Health check:**
```bash
curl http://localhost:5000/health
```

**Submit attendance request:**
```bash
curl -X POST http://localhost:5000/attendance/request \
  -H "Content-Type: application/json" \
  -d '{
    "studentId": "STUDENT_001",
    "eventId": "AI_WORKSHOP",
    "timestamp": "2026-02-06T10:30:00Z"
  }'
```

**View history:**
```bash
curl http://localhost:5000/attendance/history
```

## 📁 File Structure

- **`main.py`** — Flask API server, routes, request handling
- **`ai_engine.py`** — Trust score calculation, validation logic
- **`models.py`** — Data structures (AttendanceRequest, AttendanceResponse)

## 🔧 Configuration

Edit `ai_engine.py` to adjust:

- `TRUST_THRESHOLD` — Minimum score for approval (default: 70.0)
- `EVENT_START_TIME` — Event start time (default: "10:00:00")
- `EVENT_END_TIME` — Event end time (default: "12:00:00")
- `EVENT_DATE` — Event date (default: "2026-02-06")

## 🔗 Connect Frontend

Update `index.html` to POST to backend:

```javascript
// In markAttendance() function, after presence check:
const response = await fetch('http://localhost:5000/attendance/request', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(attendanceData)
});

const result = await response.json();
if (result.approved) {
  statusEl.innerText = '✅ Attendance approved! Trust score: ' + result.trust_score;
} else {
  statusEl.innerText = '❌ ' + result.reason;
}
```

## 🧠 How Trust Scoring Works

1. **Timing Check** (0–100 points)
   - Request within event window → +100
   - Too early/late → 0

2. **Duplicate Check** (0–100 points)
   - First request → +100
   - Already marked → 0

3. **Rapid Retry Check** (0–100 points)
   - Normal pattern → +100
   - 3+ requests in 2 min → 0
   - 1–2 requests → 50

**Final score** = weighted combination. If score ≥ threshold → **Approved**.

## 🔜 Next Steps

- Step 4: Blockchain integration (Algorand smart contract)
- Step 5: Soulbound Token (SBT) minting
- Database: Replace in-memory storage with SQLite/PostgreSQL

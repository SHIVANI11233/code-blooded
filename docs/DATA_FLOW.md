# Phase 1: Data Flow — ESP8266 + Hashing + Verification

This document describes the **session ID + timestamp → hash → verification** flow for SAL Proof-of-Presence.

---

## Flow Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ESP8266 Beacon │     │  Student App    │     │  Backend API    │
│  (in room)      │     │  (browser)      │     │  (Python)       │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │ 1. GET /session       │                       │
         │──────────────────────>│                       │
         │ { session_id,         │                       │
         │   timestamp, nonce }  │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │                       │ 2. Build payload:     │
         │                       │    session_id|ts|id   │
         │                       │ 3. Hash = SHA256()    │
         │                       │                       │
         │                       │ 4. POST /participate  │
         │                       │ { hash, session_id,   │
         │                       │   timestamp,          │
         │                       │   student_id }        │
         │                       │──────────────────────>│
         │                       │                       │
         │                       │                5. Verify hash
         │                       │                6. Hash matching
         │                       │                   (duplicate?)
         │                       │                7. AI trust score
         │                       │                       │
         │                       │<──────────────────────│
         │                       │ { approved,           │
         │                       │   trust_score }       │
```

---

## Step-by-Step

### 1. Physical Presence (ESP8266)

- ESP8266 runs as WiFi Access Point: `SAL_AI_WORKSHOP`
- Only devices in range can connect and reach `http://192.168.4.1/session`
- Response: `{ session_id, room_id, timestamp, nonce }`

### 2. Participation Request (Frontend)

Student enters **Student ID** and **Event ID** (or gets session from ESP). App:

1. Fetches `/session` from ESP (or uses mock in Demo mode)
2. Gets `session_id` and current `timestamp`
3. Builds payload: `session_id|timestamp|student_id`
4. Computes `participation_hash = SHA256(payload)`
5. POSTs to backend: `{ participation_hash, session_id, timestamp, student_id }`

### 3. Hash Creation (Privacy)

- Payload format: `SESSION_ID|2026-02-07T10:30:00.000Z|STUDENT_001`
- Hash: 64-char hex string (SHA-256)
- Raw payload is never stored; only the hash is persisted for duplicate checks

### 4. Hash Matching (Backend)

- Backend recomputes: `SHA256(session_id|timestamp|student_id)`
- Compares with received `participation_hash` → rejects if mismatch
- Checks `stored_hashes` → rejects if hash already seen (replay/duplicate)

### 5. AI Trust Validation

- Same logic as before: timing, duplicates, rapid retries
- Returns `{ approved, trust_score, reason }`

### 6. Recording

- If approved: add `participation_hash` to `stored_hashes`
- Store full request + result in `attendance_requests`

---

## Payload Format

| Field       | Source   | Example                    |
|------------|----------|----------------------------|
| session_id | ESP or form | `AI_WORKSHOP_R101`      |
| timestamp  | Client   | `2026-02-07T10:30:00.000Z` |
| student_id | Form     | `STUDENT_001`             |

**Delimiter:** `|`  
**Order:** Must match exactly between frontend and backend.

---

## API Endpoints

| Method | Endpoint                 | Purpose                          |
|--------|--------------------------|----------------------------------|
| GET    | `http://192.168.4.1/session` | ESP beacon (session data)    |
| POST   | `/attendance/participate` | Phase 1 hash-based participation  |
| POST   | `/attendance/request`    | Legacy (non-hash)                 |
| GET    | `/attendance/history`    | Debug: all requests               |

---

## Demo Mode

- Check **Demo mode** to skip ESP
- Uses `eventId` from form as `session_id`
- Still hashes and POSTs to backend
- Backend must be running at `http://localhost:5000`

---

## Running Phase 1

1. **Backend:** `cd sal-backend && python main.py`
2. **Frontend:** Open `index.html` or serve the folder (e.g. `python -m http.server 8080`)
3. **Demo:** Enable Demo mode and click **Mark Attendance**
4. **With ESP:** Flash `esp8266/sal_esp8266.ino`, connect phone to ESP WiFi, disable Demo, mark attendance

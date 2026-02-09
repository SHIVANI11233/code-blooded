# SAL — Proof-of-Presence (Phase 1)

Student check-in with **physical presence** (ESP8266), **privacy-preserving hashing**, and **AI trust validation**.

## Run the app

**1. Start the backend** (required for hash verification):

```bash
cd sal-backend
python main.py
```

**2. Serve the frontend**

```bash
# From project root
python -m http.server 8080
# Or: npx --yes serve -p 8080
```

Open **http://localhost:8080**. Use **Demo mode** to test without ESP8266.

## Phase 1 data flow

```
ESP8266 session → payload (session_id|timestamp|student_id) → SHA-256 hash
→ POST /attendance/participate → hash verify + duplicate check + AI trust → record
```

See [docs/DATA_FLOW.md](docs/DATA_FLOW.md) for details.

## With ESP8266

1. Flash `esp8266/sal_esp8266.ino` (see [esp8266/README.md](esp8266/README.md)).
2. Connect phone to ESP WiFi (`SAL_AI_WORKSHOP`).
3. Disable Demo mode, click **Mark Attendance**.

## What's next

- Phase 2: Algorand smart contract + immutable records
- Phase 3: Soulbound Achievement Tokens (SAL)

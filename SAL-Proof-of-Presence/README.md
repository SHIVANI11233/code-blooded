# SAL Proof-of-Presence

Decentralized campus participation and achievement system.

## Structure

```
SAL-Proof-of-Presence/
├── backend/
│   └── server.py      # Flask API, hashing, CORS
├── ai/
│   └── trust_engine.py # AI trust score validation
├── blockchain/
│   └── contract.py    # Placeholder (Phase 2: Algorand)
├── dashboard/
│   └── index.html     # Student attendance UI
└── hardware/
    └── esp8266_presence.ino  # ESP8266 presence beacon
```

## Run

**Backend:**
```bash
cd SAL-Proof-of-Presence
pip install flask
python backend/server.py
```

**Dashboard:** Serve `dashboard/` (e.g. `python -m http.server 8080`), open http://localhost:8080.

**Hardware:** Flash `hardware/esp8266_presence.ino` to ESP8266, connect to WiFi `SAL_AI_WORKSHOP`.

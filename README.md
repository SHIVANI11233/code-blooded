# 🏆 SAL + Proof-of-Presence  
### Decentralized AI-Verified Attendance & Achievement System

> **A next-generation, privacy-preserving system to verify real-world presence and participation using IoT, AI, and Blockchain.**

---

## 🚀 Problem Statement

Traditional attendance and participation systems are:
- ❌ Easily forgeable (proxy attendance)
- ❌ Centralized and tamper-prone
- ❌ Lacking privacy protection
- ❌ Not verifiable or portable across institutions

There is **no trusted, decentralized way** to prove *real-world presence* while preserving user privacy.

---

## 💡 Our Solution

**SAL + Proof-of-Presence** introduces a **trustless, decentralized, and privacy-first system** that verifies physical presence using IoT devices, validates it using AI logic, and permanently records achievements on the **Algorand blockchain**.

✔ No fake attendance  
✔ No central authority  
✔ No personal data leakage  
✔ Fully verifiable on-chain  

---

## 🧠 Key Features

### 🔐 Privacy-Preserving Presence
- Device data is **hashed (SHA-256)** before storage
- No raw biometric or identity data stored on-chain

### 🤖 AI-Assisted Verification
- AI logic flags abnormal patterns
- Prevents spoofing, replay, or mass fraud attempts

### 📡 IoT-Based Proof
- ESP8266 devices generate presence signals
- Works in classrooms, events, labs, campuses

### ⛓ Blockchain-Backed Trust
- Algorand smart contracts store proof immutably
- Transparent, tamper-proof verification

### 🪪 Soulbound Achievements (SBT-Ready)
- Attendance → Participation → Certification
- Non-transferable digital achievements

---

## 🏗 System Architecture

ESP8266 (IoT Device)
↓
Secure Backend (Python + Flask)
↓
SHA-256 Hash + AI Validation
↓
Algorand Smart Contract (TestNet)
↓
Immutable Proof + Dashboard View

---

## 🛠 Tech Stack

### Hardware
- ESP8266 WiFi Module

### Backend
- Python
- Flask
- Algorand Python SDK
- PyTeAL (Smart Contracts)

### Blockchain
- Algorand TestNet
- Stateless / Stateful Smart Contracts

### Security
- SHA-256 Cryptographic Hashing
- Timestamp & nonce validation

### Frontend (Optional)
- HTML / CSS / JavaScript
- Dashboard for proof visualization

---

## 📂 Project Structure

SAL-Proof-of-Presence/
│
├── esp8266/
│ └── esp8266_presence.ino
│
├── backend/
│ ├── server.py
│ ├── hash_utils.py
│ └── requirements.txt
│
├── blockchain/
│ ├── deploy_contract.py
│ └── contract.py
│
├── dashboard/
│ └── index.html
│
├── README.md
└── .gitignore

---

## ⚙ How It Works (Step-by-Step)

1️⃣ ESP8266 detects physical presence  
2️⃣ Data is hashed locally (privacy safe)  
3️⃣ Backend validates via AI logic  
4️⃣ Smart contract records proof on Algorand  
5️⃣ Proof becomes immutable & verifiable  

---

## 📈 Use Cases

- 🎓 Universities & Colleges (Attendance)
- 🏫 Hackathons & Tech Events
- 🏢 Corporate Training Programs
- 🪖 Defense & Secure Facilities
- 🌍 Government Skill Certification

---

## 🏆 Why This Can Win Hackathons

✔ Strong **real-world problem**  
✔ Combines **AI + IoT + Blockchain**  
✔ Focus on **privacy & decentralization**  
✔ Scalable beyond attendance  
✔ Clear future roadmap  

---

## 🔮 Future Enhancements

- Facial recognition (on-device, edge-AI)
- Offline proof syncing
- NFT-based certificates
- DAO-based validation
- Cross-institution identity layer

---

## 👩‍💻 Team

Built with  by **Code-Blooded**  

---

## 📜 License

MIT License – Free to use, modify, and build upon.

---

## ⭐ Final Note

This project demonstrates how **technology can replace trust with cryptography**,  
and how **presence itself can become a verifiable digital asset**.

If you like this project — ⭐ star the repo!


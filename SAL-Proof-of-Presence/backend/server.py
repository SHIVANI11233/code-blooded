import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify
from backend.hash_engine import verify_participation
from ai.trust_engine import evaluate_trust

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.route("/")
def index():
    return jsonify({
        "status": "SAL Backend OK",
        "message": "Use POST /presence with {\"user\": \"...\", \"token\": \"...\"}"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/presence", methods=["GET", "POST", "OPTIONS"])
def presence():
    if request.method == "OPTIONS":
        return "", 204
    if request.method == "GET":
        return jsonify({"message": "Use POST with {\"user\": \"...\", \"token\": \"...\"}"})
    data = request.json or {}
    user = data.get("user")
    token = data.get("token")

    if not user or not token:
        return jsonify({"status": "REJECTED", "reason": "Missing user or token"}), 400

    # 1. Hash verification
    hash_result, hash_value = verify_participation(token)
    if not hash_result:
        return jsonify({"status": "REJECTED", "reason": "Duplicate"}), 403

    # 2. AI Trust verification
    ai_result = evaluate_trust(user)
    if ai_result["decision"] != "VERIFIED":
        return jsonify({"status": "REJECTED", "reason": "AI Trust Failed"}), 403

    return jsonify({
        "status": "VERIFIED",
        "hash": hash_value,
        "score": ai_result["score"]
    })

if __name__ == "__main__":
    print("Running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

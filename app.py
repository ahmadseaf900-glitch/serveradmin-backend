
from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "ServerAdmin Backend",
        "version": "1.1.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/status")
def api_status():
    username = os.getenv("ATERNOS_USERNAME")
    password = os.getenv("ATERNOS_PASSWORD")

    return jsonify({
        "backend": "online",
        "username_found": bool(username),
        "password_found": bool(password),
        "aternos_credentials": "configured"
        if username and password
        else "missing"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

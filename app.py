from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "ServerAdmin Backend",
        "version": "1.2.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/status")
def api_status():
    username = os.getenv("ATER​NOS_USERNAME")
    password = os.getenv("ATER​NOS_PASSWORD")

    return jsonify({
        "backend": "online",
        "aternos": "configured" if username and password else "missing"
    })


@app.route("/api/servers")
def servers():
    username = os.getenv("ATER​NOS_USERNAME")
    password = os.getenv("ATER​NOS_PASSWORD")

    if not username or not password:
        return jsonify({
            "success": False,
            "error": "Aternos credentials are missing"
        }), 500

    try:
        from python_aternos import Client

        client = Client.from_credentials(username, password)
        server_list = client.list_servers()

        result = []

        for server in server_list:
            result.append({
                "name": server.name,
                "address": server.address,
                "status": server.status
            })

        return jsonify({
            "success": True,
            "servers": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

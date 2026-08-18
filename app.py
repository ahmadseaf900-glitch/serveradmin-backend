from flask import Flask, jsonify
import os

app = Flask(__name__)


# =========================
# Basic
# =========================

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "ServerAdmin Backend",
        "version": "2.0.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


# =========================
# Environment Status
# =========================

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


# =========================
# Aternos Login
# =========================

def get_aternos():
    try:
        from python_aternos import Client

        username = os.getenv("ATERNOS_USERNAME")
        password = os.getenv("ATERNOS_PASSWORD")

        if not username or not password:
            return None, "Aternos credentials are missing"

        client = Client(
            username,
            password
        )

        return client, None

    except Exception as e:
        return None, str(e)


# =========================
# Get Aternos Servers
# =========================

@app.route("/api/aternos/servers")
def aternos_servers():

    client, error = get_aternos()

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 500

    try:
        servers = client.list_servers()

        result = []

        for server in servers:
            result.append({
                "name": getattr(server, "name", None),
                "address": getattr(server, "address", None),
                "status": getattr(server, "status", None)
            })

        return jsonify({
            "success": True,
            "count": len(result),
            "servers": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# Server Status
# =========================

@app.route("/api/aternos/server/<server_name>/status")
def server_status(server_name):

    client, error = get_aternos()

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 500

    try:
        servers = client.list_servers()

        for server in servers:

            name = getattr(server, "name", "")

            if name.lower() == server_name.lower():

                return jsonify({
                    "success": True,
                    "server": {
                        "name": name,
                        "address": getattr(
                            server,
                            "address",
                            None
                        ),
                        "status": getattr(
                            server,
                            "status",
                            None
                        )
                    }
                })

        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# Run
# =========================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
        )

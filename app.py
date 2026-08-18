from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "ServerAdmin Backend",
        "version": "2.1.0"
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


def get_aternos():
    from python_aternos import Client

    username = os.getenv("ATERNOS_USERNAME")
    password = os.getenv("ATERNOS_PASSWORD")

    if not username or not password:
        raise Exception("Aternos credentials are missing")

    return Client.from_credentials(username, password)


@app.route("/api/aternos/servers")
def aternos_servers():
    try:
        client = get_aternos()

        servers = client.list_servers(cache=False)

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


@app.route("/api/aternos/server/<server_name>/status")
def server_status(server_name):
    try:
        client = get_aternos()

        servers = client.list_servers(cache=False)

        for server in servers:
            name = getattr(server, "name", "")

            if name.lower() == server_name.lower():

                try:
                    server.fetch()
                except Exception:
                    pass

                return jsonify({
                    "success": True,
                    "server": {
                        "name": getattr(server, "name", None),
                        "address": getattr(server, "address", None),
                        "status": getattr(server, "status", None)
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


@app.route("/api/aternos/server/<server_name>/start", methods=["POST", "GET"])
def start_server(server_name):
    try:
        client = get_aternos()
        servers = client.list_servers(cache=False)

        for server in servers:
            name = getattr(server, "name", "")

            if name.lower() == server_name.lower():
                server.start()

                return jsonify({
                    "success": True,
                    "message": "Server start requested",
                    "server": name
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


@app.route("/api/aternos/server/<server_name>/stop", methods=["POST", "GET"])
def stop_server(server_name):
    try:
        client = get_aternos()
        servers = client.list_servers(cache=False)

        for server in servers:
            name = getattr(server, "name", "")

            if name.lower() == server_name.lower():
                server.stop()

                return jsonify({
                    "success": True,
                    "message": "Server stop requested",
                    "server": name
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


@app.route("/api/aternos/server/<server_name>/restart", methods=["POST", "GET"])
def restart_server(server_name):
    try:
        client = get_aternos()
        servers = client.list_servers(cache=False)

        for server in servers:
            name = getattr(server, "name", "")

            if name.lower() == server_name.lower():
                server.restart()

                return jsonify({
                    "success": True,
                    "message": "Server restart requested",
                    "server": name
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


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

from flask import Flask, jsonify
import os
import time
import random
from datetime import datetime

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "dev")
APP_ENV = os.getenv("APP_ENV", "local")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI-Assisted SRE Workflow App",
        "status": "ok",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "ai-assisted-sre-workflow",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/slow", methods=["GET"])
def slow():
    time.sleep(5)
    return jsonify({
        "status": "ok",
        "message": "This endpoint intentionally responds slowly",
        "response_time_seconds": 5,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/error", methods=["GET"])
def error():
    return jsonify({
        "status": "error",
        "message": "Simulated application failure",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 500


@app.route("/random", methods=["GET"])
def random_issue():
    result = random.choice(["success", "failure"])
    if result == "success":
        return jsonify({
            "status": "ok",
            "message": "Random endpoint succeeded",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200

    return jsonify({
        "status": "error",
        "message": "Random intermittent failure occurred",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
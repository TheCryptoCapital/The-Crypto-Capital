from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Global bot status (in real use, sync with your bot process)
bot_status = {
    "scalp_mode": True,
    "capital": 1000.0,
    "pnl_today": 0.0,
    "last_trade": {},
    "active_position": None
}

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "capital": bot_status["capital"],
        "pnlToday": bot_status["pnl_today"],
        "lastTrade": bot_status["last_trade"],
        "activePosition": bot_status["active_position"]
    })

@app.route("/api/mode", methods=["POST"])
def toggle_scalp_mode():
    data = request.get_json()
    bot_status["scalp_mode"] = data.get("scalpMode", True)
    return jsonify({"scalpMode": bot_status["scalp_mode"]})

@app.route("/api/trade", methods=["POST"])
def update_trade_log():
    trade_data = request.get_json()
    bot_status["last_trade"] = trade_data
    bot_status["pnl_today"] += trade_data.get("pnl", 0.0)
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)


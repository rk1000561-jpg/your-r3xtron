from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NONCE = "320dbd2bd1"

@app.route("/")
def home():
    return jsonify({
        "owner": "r3xtron",
        "message": "Free Fire API Running"
    })

@app.route("/api")
def ff_lookup():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "status": False,
            "error": "uid required"
        })

    payload = {
        "action": "ff_get_player_info_paid",
        "uid": uid,
        "region": "ind",
        "nonce": NONCE
    }

    headers = {
        "x-requested-with": "XMLHttpRequest"
    }

    try:
        response = requests.post(
            "https://freefirenation.com/wp-admin/admin-ajax.php",
            data=payload,
            headers=headers
        )

        data = response.json()
        basic = data["data"]["profile"]["basicinfo"]

        return jsonify({
            "owner": "r3xtron",
            "status": True,
            "nickname": basic["nickname"],
            "uid": basic["accountid"],
            "level": basic["level"],
            "likes": basic["liked"],
            "region": basic["region"]
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })

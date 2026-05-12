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

        # 🔥 FIX 1: safe JSON parsing
        try:
            data = response.json()
        except:
            return jsonify({
                "status": False,
                "error": "Invalid API response (not JSON)"
            })

        # 🔥 FIX 2: type check
        if not isinstance(data, dict):
            return jsonify({
                "status": False,
                "error": "API returned invalid format"
            })

        # 🔥 FIX 3: structure safety check
        if "data" not in data or "profile" not in data["data"] or "basicinfo" not in data["data"]["profile"]:
            return jsonify({
                "status": False,
                "error": "Incomplete API response"
            })

        basic = data["data"]["profile"]["basicinfo"]

        return jsonify({
            "status": True,
            "owner": "r3xtron",
            "data": {
                "nickname": basic.get("nickname"),
                "accountid": basic.get("accountid"),
                "level": basic.get("level"),
                "exp": basic.get("exp"),
                "rank": basic.get("rank"),
                "rankingpoints": basic.get("rankingpoints"),
                "region": basic.get("region"),
                "liked": basic.get("liked"),
                "createat": basic.get("createat"),
                "lastloginat": basic.get("lastloginat"),
                "releaseversion": basic.get("releaseversion"),
                "accounttype": basic.get("accounttype"),
                "csrank": basic.get("csrank"),
                "csrankingpoints": basic.get("csrankingpoints"),
                "maxrank": basic.get("maxrank"),
                "csmaxrank": basic.get("csmaxrank"),
                "badgecnt": basic.get("badgecnt"),
                "badgeid": basic.get("badgeid"),
                "bannerid": basic.get("bannerid"),
                "headpic": basic.get("headpic"),
                "pinid": basic.get("pinid")
            }
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })

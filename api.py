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
            "status": True,
            "owner": "r3xtron",
            "data": {
                "nickname": basic["nickname"],
                "accountid": basic["accountid"],
                "level": basic["level"],
                "exp": basic["exp"],
                "rank": basic["rank"],
                "rankingpoints": basic["rankingpoints"],
                "region": basic["region"],
                "liked": basic["liked"],
                "createat": basic["createat"],
                "lastloginat": basic["lastloginat"],
                "releaseversion": basic["releaseversion"],
                "accounttype": basic["accounttype"],
                "csrank": basic["csrank"],
                "csrankingpoints": basic["csrankingpoints"],
                "maxrank": basic["maxrank"],
                "csmaxrank": basic["csmaxrank"],
                "badgecnt": basic["badgecnt"],
                "badgeid": basic["badgeid"],
                "bannerid": basic["bannerid"],
                "headpic": basic["headpic"],
                "pinid": basic["pinid"]
            }
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })

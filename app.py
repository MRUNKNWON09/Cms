import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Credentials - Later you can move to environment variables
USERNAME = os.environ.get("USERNAME", "C2008497")
PASSWORD = os.environ.get("PASSWORD", "5REo3OcRpk")
SENDER_ID = os.environ.get("SENDER_ID", "38541")

@app.route("/send_sms", methods=["GET"])
def send_sms():
    number = request.args.get("num", "")
    message = request.args.get("msg", "")

    if not number or not message:
        return jsonify({
            "status": "error",
            "number": number,
            "msg": message,
            "dev": "Mr Rafi",
            "error": "Number or message missing!"
        })

    import re
    if not re.match(r'^[\u0980-\u09FF\s.,!?।-]+$', message):
        return jsonify({
            "status": "error",
            "number": number,
            "msg": message,
            "dev": "Mr Rafi",
            "error": "Only Bengali message with allowed punctuations!"
        })

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; ORBIT Y70c Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.122 Mobile Safari/537.36"
    })

    # STEP 1: Get login token
    login_page = session.get("https://msg.elitbuzz-bd.com/login", verify=False)
    soup = BeautifulSoup(login_page.text, "html.parser")
    token_tag = soup.find("input", {"name": "_token"})
    if not token_tag:
        return jsonify({
            "status": "error",
            "number": number,
            "msg": message,
            "dev": "Mr Rafi",
            "error": "Login token not found!"
        })
    token = token_tag['value']

    # STEP 2: Login
    login_data = {
        "_token": token,
        "login_id": USERNAME,
        "password": PASSWORD
    }
    login_response = session.post("https://msg.elitbuzz-bd.com/login", data=login_data, verify=False)
    if "Logout" not in login_response.text and "dashboard" not in login_response.text:
        return jsonify({
            "status": "error",
            "number": number,
            "msg": message,
            "dev": "Mr Rafi",
            "error": "Login failed!"
        })

    # STEP 3: Get SMS token
    send_page = session.get("https://msg.elitbuzz-bd.com/Messaging/SendMessage", verify=False)
    soup2 = BeautifulSoup(send_page.text, "html.parser")
    sms_token_tag = soup2.find("input", {"name": "_token"})
    if not sms_token_tag:
        return jsonify({
            "status": "error",
            "number": number,
            "msg": message,
            "dev": "Mr Rafi",
            "error": "SMS token not found!"
        })
    sms_token = sms_token_tag['value']

    # STEP 4: Send SMS
    sms_data = {
        "sender_id": SENDER_ID,
        "msisdn": number,
        "recipientsmsRadios": "unicode",
        "message": message,
        "scheduleRecipientsRadios": "now",
        "isDeliveryReportRequest": "1",
        "_token": sms_token
    }
    sms_response = session.post("https://msg.elitbuzz-bd.com/Messaging/sendSmsToRecipients", data=sms_data, verify=False)

    return jsonify({
        "status": "success",
        "number": number,
        "msg": message,
        "dev": "Mr Rafi",
        "response": sms_response.text
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

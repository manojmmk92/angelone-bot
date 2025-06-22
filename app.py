from flask import Flask, request
from SmartApi.smartConnect import SmartConnect
import pyotp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "AngelOne Webhook Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)
    return {"status": "received"}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

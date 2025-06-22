from flask import Flask, request, jsonify
from smartapi import SmartConnect
import pyotp
import os

app = Flask(__name__)

# Load credentials from environment
API_KEY = os.getenv("API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

def angel_login():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = obj.generateSession(CLIENT_ID, PASSWORD, totp)
    return obj

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    obj = angel_login()
    
    try:
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": data['symbol'],
            "symboltoken": "99926009",  # NIFTY token — can be made dynamic
            "transactiontype": data['order_type'],
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": 0,
            "quantity": int(data['qty'])
        }

        order = obj.placeOrder(order_params)
        print("Order placed:", order)
        return jsonify({"status": "success", "order": order}), 200
    except Exception as e:
        print("Order failed:", e)
        return jsonify({"status": "error", "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

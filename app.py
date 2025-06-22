from flask import Flask, request, jsonify
from SmartApi.smartConnect import SmartConnect
import pyotp
import os

app = Flask(__name__)

# Read credentials from environment variables
API_KEY = os.getenv("API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")  # Google Authenticator secret

# Create SmartAPI session
def create_session():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = obj.generateSession(client_id=CLIENT_ID, password=PASSWORD, totp=totp)
    return obj

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received Webhook:", data)

    try:
        symbol = data["symbol"]
        exchange = data.get("exchange", "NSE")  # Default to NSE
        transaction_type = data["action"]  # BUY or SELL
        order_type = data.get("order_type", "MARKET")
        product_type = data.get("product_type", "INTRADAY")
        quantity = int(data["qty"])
        price = float(data.get("price", 0))

        # Start trading session
        obj = create_session()

        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": "",  # Can be left empty if using trading symbol
            "transactiontype": transaction_type.upper(),
            "exchange": exchange.upper(),
            "ordertype": order_type.upper(),
            "producttype": product_type.upper(),
            "duration": "DAY",
            "price": price,
            "quantity": quantity,
        }

        order = obj.placeOrder(order_params)
        return jsonify({"status": "success", "order_id": order})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/")
def home():
    return "✅ AngelOne Trading Webhook is LIVE"


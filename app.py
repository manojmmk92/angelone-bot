@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Received webhook:", data)

    action = data.get("action", "").upper()
    if action == "BUY":
        place_order("BUY")
    elif action == "SELL":
        place_order("SELL")
    else:
        return "Invalid action", 400

    return "Simulated Order Placed", 200

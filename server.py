from flask import Flask, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data and "message" in data:
        print(f"Received notification: {data['message']}")
        return "Notification received", 200
    return "Invalid data", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

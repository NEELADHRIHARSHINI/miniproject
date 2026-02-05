from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_url

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ---------- Default route ----------
@app.route("/", methods=["GET"])
def home():
    return "Backend is running!"

# ---------- URL check route ----------
@app.route("/check", methods=["POST"])
def check_url():
    # Get URL from JSON request
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]
    # Get prediction from ML model
    result = predict_url(url)
    return jsonify(result)

# ---------- Run server ----------
if __name__ == "__main__":
    app.run(debug=True)

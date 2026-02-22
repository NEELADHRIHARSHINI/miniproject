from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_url

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ---------- Default route ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

# ---------- Health check route ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# ---------- URL check route ----------
@app.route("/check", methods=["GET", "POST"])
def check_url():
    try:
        # Support both GET (browser testing) and POST (frontend)
        if request.method == "GET":
            url = request.args.get("url")
        else:
            data = request.get_json()
            url = data.get("url") if data else None

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Get prediction from ML model
        result = predict_url(url)
        return jsonify(result)

    except Exception as e:
        # Graceful error handling (helps in demos)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# ---------- Run server ----------
if __name__ == "__main__":
    app.run(debug=True)

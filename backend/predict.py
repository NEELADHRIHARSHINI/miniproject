import pickle
from utils.features import extract_url_features
from urllib.parse import urlparse

# Load trained ML model
with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

# Trusted domains whitelist (for demo reliability)
TRUSTED_DOMAINS = [
    "google.com",
    "www.google.com",
    "facebook.com",
    "www.facebook.com",
    "amazon.com",
    "www.amazon.com",
    "paypal.com",
    "www.paypal.com"
]

def predict_url(url):
    domain = urlparse(url).netloc.lower()

    # Whitelist check
    if domain in TRUSTED_DOMAINS:
        return {
            "url": url,
            "risk_percentage": 1.0,
            "status": "SAFE",
            "advice": "This domain is widely trusted. Still be cautious with personal information."
        }

    # Extract features and predict
    features = extract_url_features(url)
    probability = model.predict_proba([features])[0][1]
    risk = round(probability * 100, 2)

    # Multi-level classification
    if risk >= 75:
        status = "PHISHING"
        advice = "High risk detected. Do not enter any personal or financial information."
    elif risk >= 40:
        status = "SUSPICIOUS"
        advice = "This URL looks suspicious. Verify the website carefully before proceeding."
    else:
        status = "SAFE"
        advice = "This URL appears safe, but always remain cautious."

    return {
        "url": url,
        "risk_percentage": risk,
        "status": status,
        "advice": advice
    }

# Local test
if __name__ == "__main__":
    print(predict_url("https://secure-paypal-login.com"))
    print(predict_url("https://google.com"))

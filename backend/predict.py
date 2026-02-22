import pickle
from utils.features import extract_url_features
from urllib.parse import urlparse

# Load model once
with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

# Whitelist of trusted domains (for demo credibility)
SAFE_DOMAINS = {"google.com", "www.google.com", "github.com", "openai.com", "microsoft.com", "wikipedia.org"}

def is_whitelisted(url):
    domain = urlparse(url).netloc.lower()
    return domain in SAFE_DOMAINS

def predict_url(url):
    # If domain is trusted, override
    if is_whitelisted(url):
        return {
            "url": url,
            "risk_percentage": 1.0,
            "status": "SAFE"
        }

    features = extract_url_features(url)
    probability = model.predict_proba([features])[0][1]
    risk = round(probability * 100, 2)

    if risk >= 75:
        status = "PHISHING"
    elif risk >= 40:
        status = "SUSPICIOUS"
    else:
        status = "SAFE"

    return {
        "url": url,
        "risk_percentage": risk,
        "status": status
    }

# Test
if __name__ == "__main__":
    print(predict_url("https://secure-paypal-login.com"))
    print(predict_url("https://google.com"))

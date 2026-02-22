import pickle
from utils.features import extract_url_features
from urllib.parse import urlparse

with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

SAFE_DOMAINS = {"google.com", "www.google.com", "github.com", "openai.com", "microsoft.com", "wikipedia.org"}

def is_whitelisted(url):
    domain = urlparse(url).netloc.lower()
    return domain in SAFE_DOMAINS

def predict_url(url):
    if is_whitelisted(url):
        return {
            "url": url,
            "risk_percentage": 1.0,
            "status": "SAFE",
            "advice": "This domain is widely trusted. Still be cautious with personal information."
        }

    features = extract_url_features(url)
    probability = model.predict_proba([features])[0][1]
    risk = round(probability * 100, 2)

    if risk >= 75:
        status = "PHISHING"
        advice = "High risk detected. Avoid visiting this link or entering credentials."
    elif risk >= 40:
        status = "SUSPICIOUS"
        advice = "Proceed with caution. Verify the source before interacting."
    else:
        status = "SAFE"
        advice = "Low risk detected. Still verify the website authenticity."

    return {
        "url": url,
        "risk_percentage": risk,
        "status": status,
        "advice": advice
    }

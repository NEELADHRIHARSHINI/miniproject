import pickle
from utils.features import extract_url_features

with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_url(url):
    features = extract_url_features(url)
    probability = model.predict_proba([features])[0][1]
    risk = round(probability * 100, 2)

    return {
        "url": url,
        "risk_percentage": risk,
        "status": "PHISHING" if risk > 50 else "SAFE"
    }

# Test
if __name__ == "__main__":
    print(predict_url("https://secure-paypal-login.com"))

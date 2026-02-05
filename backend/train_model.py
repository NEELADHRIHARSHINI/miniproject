import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from utils.features import extract_url_features

# Sample dataset (replace later with Kaggle dataset)
data = {
    "url": [
        "https://google.com",
        "http://secure-login-paypal.com",
        "https://bankofamerica.com",
        "http://free-gift-cards.net/login"
    ],
    "label": [0, 1, 0, 1]   # 0 = Safe, 1 = Phishing
}

df = pd.DataFrame(data)

# Feature extraction
X = df["url"].apply(extract_url_features).tolist()
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y
)


# Train model
model = LogisticRegression(
    max_iter=1000,
    C=0.1,           # regularization
    solver="liblinear"
)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# Save model
with open("phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as phishing_model.pkl")


import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

FEATURES = [
    "amount",
    "hour",
    "distance_from_home_km",
    "transactions_last_24h",
    "international",
    "merchant_risk"
]


def train_model():
    # Load sample transaction dataset
    df = pd.read_csv("sample_transactions.csv")

    X = df[FEATURES]
    y = df["is_fraud"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create and train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("AI Fraud Detection Model Trained!")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    return model, accuracy


def predict_transaction(model, transaction):
    # Convert transaction into a DataFrame
    transaction_df = pd.DataFrame(
        [transaction],
        columns=FEATURES
    )

    # Predict fraud probability
    probability = model.predict_proba(transaction_df)[0][1]

    # Determine risk category
    if probability >= 0.5:
        result = "Suspicious"
    else:
        result = "Normal"

    return {
        "result": result,
        "fraud_probability": round(probability * 100, 2)
    }


if __name__ == "__main__":
    model, accuracy = train_model()

    sample_transaction = {
        "amount": 25000,
        "hour": 2,
        "distance_from_home_km": 450,
        "transactions_last_24h": 12,
        "international": 1,
        "merchant_risk": 0.9
    }

    result = predict_transaction(model, sample_transaction)

    print("\nSample Transaction Prediction:")
    print(result)

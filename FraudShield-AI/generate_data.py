
import pandas as pd
import numpy as np

def generate_dataset(n=2500):
    np.random.seed(42)

    data = []

    for i in range(n):
        is_fraud = np.random.choice([0, 1], p=[0.88, 0.12])

        if is_fraud == 0:
            amount = np.random.uniform(100, 5000)
            hour = np.random.randint(7, 23)
            distance = np.random.uniform(0, 30)
            transactions = np.random.randint(1, 5)
            international = np.random.choice([0, 1], p=[0.98, 0.02])
            merchant_risk = np.random.uniform(0, 0.5)

        else:
            amount = np.random.uniform(5000, 50000)
            hour = np.random.choice(
                list(range(0, 6)) + list(range(23, 24))
            )
            distance = np.random.uniform(50, 1000)
            transactions = np.random.randint(5, 20)
            international = np.random.choice([0, 1], p=[0.4, 0.6])
            merchant_risk = np.random.uniform(0.5, 1.0)

        data.append({
            "transaction_id": f"TXN{i+1:04d}",
            "amount": round(amount, 2),
            "hour": hour,
            "distance_from_home_km": round(distance, 2),
            "transactions_last_24h": transactions,
            "international": international,
            "merchant_risk": round(merchant_risk, 2),
            "is_fraud": is_fraud
        })

    df = pd.DataFrame(data)
    df.to_csv("sample_transactions.csv", index=False)

    print("Transaction dataset generated successfully!")
    print("Total transactions:", len(df))
    print("Fraudulent transactions:", df["is_fraud"].sum())
    print("Normal transactions:", (df["is_fraud"] == 0).sum())

if __name__ == "__main__":
    generate_dataset()

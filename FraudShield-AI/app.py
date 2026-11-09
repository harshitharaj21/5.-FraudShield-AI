
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from fraud_model import train_model, predict_transaction

# Page configuration
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
h1 {
    color: #142d4e;
}
h2, h3 {
    color: #24476b;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# Load dataset and train AI model
@st.cache_resource
def load_model():
    return train_model()

@st.cache_data
def load_data():
    return pd.read_csv("sample_transactions.csv")

model, accuracy = load_model()
df = load_data()

# Sidebar
st.sidebar.title("🛡️ FraudShield AI")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select a page",
    [
        "Dashboard",
        "Detect Fraud",
        "Transaction History",
        "About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("AI Model: Active")
st.sidebar.caption("Random Forest Classifier")

# Dashboard
if page == "Dashboard":

    st.title("🛡️ FraudShield AI")
    st.subheader("AI-Powered Financial Fraud Detection System")

    st.write(
        "Monitor financial transactions, identify suspicious "
        "activities and analyze potential fraud using Machine Learning."
    )

    total = len(df)
    fraud = int(df["is_fraud"].sum())
    normal = total - fraud

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", f"{total:,}")
    col2.metric("Normal Transactions", f"{normal:,}")
    col3.metric("Suspicious Transactions", f"{fraud:,}")
    col4.metric("Model Accuracy", f"{accuracy * 100:.1f}%")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Transaction Distribution")

        fig, ax = plt.subplots()
        ax.pie(
            [normal, fraud],
            labels=["Normal", "Suspicious"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Transaction Classification")
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.subheader("Fraud vs Normal Transactions")

        chart_data = pd.DataFrame({
            "Transaction Type": ["Normal", "Suspicious"],
            "Count": [normal, fraud]
        })

        st.bar_chart(
            chart_data,
            x="Transaction Type",
            y="Count"
        )

    st.markdown("---")

    st.subheader("Recent Suspicious Transactions")

    suspicious = df[df["is_fraud"] == 1].head(10)

    st.dataframe(
        suspicious.drop(columns=["is_fraud"]),
        use_container_width=True,
        hide_index=True
    )


# Detect Fraud
elif page == "Detect Fraud":

    st.title("🔍 AI Fraud Detection")
    st.write("Enter transaction details to check its risk level.")

    with st.form("fraud_form"):

        amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=1.0,
            max_value=10000000.0,
            value=25000.0
        )

        hour = st.slider(
            "Transaction Hour",
            min_value=0,
            max_value=23,
            value=2
        )

        distance = st.number_input(
            "Distance From Home (km)",
            min_value=0.0,
            max_value=10000.0,
            value=450.0
        )

        transactions = st.number_input(
            "Transactions in Last 24 Hours",
            min_value=1,
            max_value=100,
            value=12
        )

        international = st.selectbox(
            "International Transaction?",
            ["No", "Yes"]
        )

        merchant_risk = st.slider(
            "Merchant Risk Score",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.05
        )

        submitted = st.form_submit_button(
            "Analyze Transaction",
            use_container_width=True
        )

    if submitted:

        transaction = {
            "amount": amount,
            "hour": hour,
            "distance_from_home_km": distance,
            "transactions_last_24h": transactions,
            "international": 1 if international == "Yes" else 0,
            "merchant_risk": merchant_risk
        }

        result = predict_transaction(model, transaction)

        st.markdown("---")
        st.subheader("AI Analysis Result")

        probability = float(result["fraud_probability"])

        if result["result"] == "Suspicious":
            st.error("⚠️ Suspicious Transaction Detected!")
        else:
            st.success("✅ Transaction Classified as Normal")

        st.metric(
            "Predicted Fraud Probability",
            f"{probability:.2f}%"
        )

        st.progress(probability / 100)

        st.info(
            "This is an AI-generated risk estimate based on "
            "the patterns learned from the sample dataset. "
            "It is not a confirmation of fraud."
        )


# Transaction History
elif page == "Transaction History":

    st.title("📋 Transaction History")

    st.write("Explore the complete sample transaction dataset.")

    filter_type = st.selectbox(
        "Filter Transactions",
        ["All", "Normal", "Suspicious"]
    )

    if filter_type == "Normal":
        filtered = df[df["is_fraud"] == 0]

    elif filter_type == "Suspicious":
        filtered = df[df["is_fraud"] == 1]

    else:
        filtered = df

    st.write(f"Showing {len(filtered)} transactions")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Transactions CSV",
        data=csv,
        file_name="fraud_transactions.csv",
        mime="text/csv"
    )


# About Project
elif page == "About Project":

    st.title("ℹ️ About FraudShield AI")

    st.subheader("Project Overview")

    st.write("""
    FraudShield AI is an AI-powered financial fraud detection
    application developed using Python and Machine Learning.

    It analyzes financial transaction patterns and predicts
    whether a transaction appears normal or suspicious.
    """)

    st.subheader("AI Technology Used")

    st.markdown("""
    - **Machine Learning:** Random Forest Classification.
    - **Pandas:** Transaction data processing.
    - **NumPy:** Numerical operations.
    - **Scikit-learn:** Model training and prediction.
    - **Streamlit:** Interactive web application.
    - **Matplotlib:** Data visualization.
    """)

    st.subheader("Main Features")

    st.markdown("""
    1. Financial transaction monitoring.
    2. AI-based fraud prediction.
    3. Fraud probability estimation.
    4. Transaction history and filtering.
    5. Interactive analytics dashboard.
    6. CSV data export.
    """)

    st.subheader("Practical Benefits")

    st.markdown("""
    - Helps identify potentially suspicious transactions.
    - Supports faster transaction screening.
    - Makes financial transaction patterns easier to understand.
    - Demonstrates how AI can assist financial institutions.
    """)

    st.warning(
        "Educational prototype using synthetic data. "
        "It is not intended for real banking decisions."
    )

    st.caption("Developed as an AI for Finance academic project.")

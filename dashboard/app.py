import streamlit as st
import pandas as pd


DATA_PATH = "data/processed/fraud_ring_classification.csv"


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RISKNET AI",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    return pd.read_csv(DATA_PATH)


df = load_data()


# ==========================================
# HEADER
# ==========================================

st.title("🛡️ RISKNET AI")

st.subheader(
    "AI-Powered Fraud Ring & Risk Intelligence Platform"
)

st.divider()


# ==========================================
# KPI METRICS
# ==========================================

total_customers = len(df)

high_risk = len(
    df[df["final_risk_level"] == "HIGH"]
)

medium_risk = len(
    df[df["final_risk_level"] == "MEDIUM"]
)

low_risk = len(
    df[df["final_risk_level"] == "LOW"]
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    total_customers
)

col2.metric(
    "🔴 High Risk",
    high_risk
)

col3.metric(
    "🟡 Medium Risk",
    medium_risk
)

col4.metric(
    "🟢 Low Risk",
    low_risk
)


st.divider()


# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.header("📊 Risk Distribution")

risk_counts = df["final_risk_level"].value_counts()

st.bar_chart(risk_counts)


# ==========================================
# FRAUD RING DISTRIBUTION
# ==========================================

st.header("🔗 Fraud Ring Types")

ring_counts = df["fraud_ring_type"].value_counts()

st.bar_chart(ring_counts)


st.divider()


# ==========================================
# CUSTOMER INVESTIGATION
# ==========================================

st.header("🔍 Customer Risk Investigation")

customer_id = st.text_input(
    "Enter Customer ID",
    placeholder="Example: CUST100000"
)


if customer_id:

    result = df[
        df["customer_id"].astype(str)
        == customer_id
    ]

    if result.empty:

        st.error("Customer not found.")

    else:

        customer = result.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Risk Score",
            customer["final_risk_score"]
        )

        col2.metric(
            "Risk Level",
            customer["final_risk_level"]
        )

        col3.metric(
            "Fraud Ring",
            customer["fraud_ring_type"]
        )

        st.subheader("⚠️ Risk Explanation")

        st.warning(
            customer["risk_reason"]
        )

        st.subheader("Customer Details")

        st.dataframe(
            result.T,
            use_container_width=True
        )


# ==========================================
# TOP RISK CUSTOMERS
# ==========================================

st.divider()

st.header("🚨 Highest Risk Customers")

top_risk = (
    df.sort_values(
        "final_risk_score",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_risk[
        [
            "customer_id",
            "final_risk_score",
            "final_risk_level",
            "fraud_ring_type",
            "risk_reason"
        ]
    ],
    use_container_width=True
)

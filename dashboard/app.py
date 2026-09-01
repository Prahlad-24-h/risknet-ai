import streamlit as st
import pandas as pd


DATA_PATH = "data/processed/fraud_ring_classification.csv"


st.set_page_config(
    page_title="RISKNET AI",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ RISKNET AI")

st.markdown(
    "### AI-Powered Fraud Ring & Customer Risk Intelligence"
)

st.caption(
    "Combining behavioral rules, machine learning and graph-based fraud detection."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("RISKNET AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Customer Investigation",
        "Fraud Rings",
        "Risk Analysis"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("📊 Risk Overview")

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

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Risk Distribution")

        risk_counts = (
            df["final_risk_level"]
            .value_counts()
        )

        st.bar_chart(risk_counts)

    with col2:

        st.subheader("Fraud Ring Distribution")

        ring_counts = (
            df["fraud_ring_type"]
            .value_counts()
        )

        st.bar_chart(ring_counts)

    st.divider()

    st.subheader("🚨 Highest Risk Customers")

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
                "ring_id"
            ]
        ],
        use_container_width=True
    )


# ============================================================
# CUSTOMER INVESTIGATION
# ============================================================

elif page == "Customer Investigation":

    st.header("🔍 Customer Risk Investigation")

    customer_id = st.text_input(
        "Customer ID",
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

            st.success(
                f"Customer {customer_id} found"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Final Risk Score",
                customer["final_risk_score"]
            )

            col2.metric(
                "Final Risk Level",
                customer["final_risk_level"]
            )

            col3.metric(
                "ML Risk",
                customer["ml_risk_level"]
            )

            col4.metric(
                "Graph Risk",
                customer["graph_risk_level"]
            )

            st.divider()

            st.subheader("🔗 Fraud Network")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Fraud Ring",
                customer["fraud_ring_type"]
            )

            col2.metric(
                "Ring Customers",
                customer["ring_customer_count"]
            )

            col3.metric(
                "Ring Nodes",
                customer["ring_node_count"]
            )

            st.divider()

            st.subheader("🧠 Risk Components")

            risk_components = pd.DataFrame(
                {
                    "Component": [
                        "Rule Risk Score",
                        "Graph Risk Score",
                        "Final Risk Score"
                    ],
                    "Score": [
                        customer["risk_score"],
                        customer["graph_risk_score"],
                        customer["final_risk_score"]
                    ]
                }
            )

            st.bar_chart(
                risk_components.set_index("Component")
            )

            st.subheader("⚠️ Explainable Risk Reason")

            st.warning(
                customer["risk_reason"]
            )

            st.subheader("Customer Information")

            customer_columns = [
                "customer_id",
                "full_name",
                "city",
                "kyc_status",
                "pan_status",
                "identity_match",
                "credit_score",
                "monthly_income_inr",
                "account_age_months",
                "device_id",
                "primary_payment_instrument_id"
            ]

            available_columns = [
                column
                for column in customer_columns
                if column in result.columns
            ]

            st.dataframe(
                result[available_columns],
                use_container_width=True
            )


# ============================================================
# FRAUD RINGS
# ============================================================

elif page == "Fraud Rings":

    st.header("🔗 Fraud Ring Intelligence")

    ring_summary = (
        df.groupby("fraud_ring_type")
        .agg(
            customers=("customer_id", "count"),
            average_risk=("final_risk_score", "mean"),
            maximum_risk=("final_risk_score", "max")
        )
        .reset_index()
    )

    ring_summary["average_risk"] = (
        ring_summary["average_risk"]
        .round(2)
    )

    st.dataframe(
        ring_summary,
        use_container_width=True
    )

    st.subheader("Fraud Ring Types")

    st.bar_chart(
        df["fraud_ring_type"].value_counts()
    )

    st.divider()

    selected_ring = st.selectbox(
        "Select Fraud Ring",
        sorted(
            df["fraud_ring_type"]
            .dropna()
            .unique()
        )
    )

    ring_customers = df[
        df["fraud_ring_type"]
        == selected_ring
    ]

    st.subheader(
        f"Customers in {selected_ring}"
    )

    st.dataframe(
        ring_customers[
            [
                "customer_id",
                "final_risk_score",
                "final_risk_level",
                "ring_id",
                "ring_customer_count",
                "graph_risk_score"
            ]
        ],
        use_container_width=True
    )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header("📈 Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Final Risk Score")

        st.bar_chart(
            df["final_risk_score"]
            .value_counts()
            .sort_index()
        )

    with col2:

        st.subheader("ML Risk Levels")

        st.bar_chart(
            df["ml_risk_level"]
            .value_counts()
        )

    st.divider()

    st.subheader("Risk Level Comparison")

    comparison = pd.crosstab(
        df["ml_risk_level"],
        df["final_risk_level"]
    )

    st.dataframe(
        comparison,
        use_container_width=True
    )

    st.subheader("Dataset Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Final Risk",
        round(
            df["final_risk_score"].mean(),
            2
        )
    )

    col2.metric(
        "Average Graph Risk",
        round(
            df["graph_risk_score"].mean(),
            2
        )
    )

    col3.metric(
        "Average Rule Risk",
        round(
            df["risk_score"].mean(),
            2
        )
    )

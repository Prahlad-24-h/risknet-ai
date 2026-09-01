from fastapi import FastAPI, HTTPException
import pandas as pd


DATA_PATH = "data/processed/fraud_ring_classification.csv"


app = FastAPI(
    title="RISKNET AI",
    description="AI-powered fraud ring and customer risk detection API",
    version="1.0.0"
)


def load_results():

    try:
        return pd.read_csv(DATA_PATH)

    except FileNotFoundError:

        return None


@app.get("/")
def home():

    return {
        "project": "RISKNET AI",
        "status": "running",
        "service": "Fraud Risk Detection API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/customers")
def get_customers():

    df = load_results()

    if df is None:
        raise HTTPException(
            status_code=500,
            detail="Risk dataset not found"
        )

    return {
        "count": len(df),
        "customers": df[
            [
                "customer_id",
                "final_risk_score",
                "final_risk_level",
                "fraud_ring_type"
            ]
        ].to_dict(orient="records")
    }


@app.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    df = load_results()

    if df is None:
        raise HTTPException(
            status_code=500,
            detail="Risk dataset not found"
        )

    result = df[
        df["customer_id"].astype(str)
        == customer_id
    ]

    if result.empty:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return result.iloc[0].to_dict()

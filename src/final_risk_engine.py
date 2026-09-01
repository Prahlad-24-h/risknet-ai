import pandas as pd
import joblib

from src.data_loader import load_data


FEATURE_PATH = "data/processed/customer_risk_features.csv"
PREDICTION_PATH = "data/processed/ml_predictions.csv"
MODEL_PATH = "models/risk_model.pkl"


def load_ml_predictions():

    df = pd.read_csv(PREDICTION_PATH)

    return df


def calculate_final_score(df):

    df = df.copy()

    # Start with ML risk score
    df["final_risk_score"] = df["risk_score"]

    # -----------------------------------------
    # ML risk contribution
    # -----------------------------------------

    df.loc[
        df["ml_risk_level"] == "HIGH",
        "final_risk_score"
    ] += 10

    df.loc[
        df["ml_risk_level"] == "MEDIUM",
        "final_risk_score"
    ] += 5

    # -----------------------------------------
    # Chargeback risk
    # -----------------------------------------

    df.loc[
        df["chargeback_rate"] >= 0.10,
        "final_risk_score"
    ] += 10

    # -----------------------------------------
    # Card testing / decline behaviour
    # -----------------------------------------

    df.loc[
        df["decline_rate"] >= 0.30,
        "final_risk_score"
    ] += 10

    # -----------------------------------------
    # Coupon abuse behaviour
    # -----------------------------------------

    df.loc[
        df["promo_rate"] >= 0.50,
        "final_risk_score"
    ] += 10

    # Maximum score
    df["final_risk_score"] = df[
        "final_risk_score"
    ].clip(upper=100)

    # -----------------------------------------
    # Final risk level
    # -----------------------------------------

    df["final_risk_level"] = "LOW"

    df.loc[
        df["final_risk_score"] >= 30,
        "final_risk_level"
    ] = "MEDIUM"

    df.loc[
        df["final_risk_score"] >= 60,
        "final_risk_level"
    ] = "HIGH"

    # -----------------------------------------
    # Fraud ring indicators
    # -----------------------------------------

    df["coupon_ring_flag"] = (
        df["promo_rate"] >= 0.50
    )

    df["card_testing_flag"] = (
        df["decline_rate"] >= 0.30
    )

    df["chargeback_ring_flag"] = (
        df["chargeback_rate"] >= 0.10
    )
    def generate_reason(row):

        reasons = []

        if row["ml_risk_level"] == "HIGH":
            reasons.append("ML model detected high risk")

        if row["promo_rate"] >= 0.50:
            reasons.append("high coupon usage")

        if row["decline_rate"] >= 0.30:
            reasons.append("high transaction decline rate")

        if row["chargeback_rate"] >= 0.10:
            reasons.append("high chargeback rate")

        if not reasons:
            reasons.append("normal transaction behaviour")

        return "; ".join(reasons)

    df["risk_reason"] = df.apply(
        generate_reason,
        axis=1
    )
    return df


def main():

    df = load_ml_predictions()

    result = calculate_final_score(df)

    output_path = "data/processed/final_risk_results.csv"

    result.to_csv(
        output_path,
        index=False
    )

    print("\n================================")
    print("       RISKNET AI ENGINE")
    print("================================\n")

    print(
        result[
            [
                "customer_id",
                "final_risk_score",
                "final_risk_level",
                "risk_reason"
            ]
        ]
        .sort_values(
            "final_risk_score",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

    print(
        "\nSaved:",
        output_path
    )
if __name__ == "__main__":
    main()

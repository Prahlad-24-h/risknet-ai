import pandas as pd


ML_PATH = "data/processed/ml_predictions.csv"
GRAPH_PATH = "data/processed/graph_risk_results.csv"
OUTPUT_PATH = "data/processed/final_risk_results.csv"


def load_data():

    ml = pd.read_csv(ML_PATH)
    graph = pd.read_csv(GRAPH_PATH)

    return ml, graph


def build_final_risk():

    ml, graph = load_data()

    # Keep one graph record per customer
    graph = graph.drop_duplicates(
        subset=["customer_id"]
    )

    # Combine ML and graph information
    df = ml.merge(
        graph,
        on="customer_id",
        how="left"
    )

    # Missing graph information means
    # no detected ring
    df["graph_risk_score"] = (
        df["graph_risk_score"]
        .fillna(0)
    )

    df["graph_risk_level"] = (
        df["graph_risk_level"]
        .fillna("LOW")
    )

    # --------------------------------
    # Final score
    # --------------------------------

    df["final_risk_score"] = (
        df["risk_score"]
        + df["graph_risk_score"] * 0.30
    )

    # ML contribution
    df.loc[
        df["ml_risk_level"] == "HIGH",
        "final_risk_score"
    ] += 10

    df.loc[
        df["ml_risk_level"] == "MEDIUM",
        "final_risk_score"
    ] += 5

    df["final_risk_score"] = (
        df["final_risk_score"]
        .clip(upper=100)
        .round(2)
    )

    # --------------------------------
    # Final level
    # --------------------------------

    df["final_risk_level"] = "LOW"

    df.loc[
        df["final_risk_score"] >= 30,
        "final_risk_level"
    ] = "MEDIUM"

    df.loc[
        df["final_risk_score"] >= 60,
        "final_risk_level"
    ] = "HIGH"

    # --------------------------------
    # Explainability
    # --------------------------------

    def reason(row):

        reasons = []

        if row["ml_risk_level"] == "HIGH":
            reasons.append("ML high risk")

        if row["graph_risk_score"] > 0:
            reasons.append(
                "linked to potential fraud ring"
            )

        if row["promo_rate"] >= 0.50:
            reasons.append("coupon abuse behaviour")

        if row["decline_rate"] >= 0.30:
            reasons.append("card testing behaviour")

        if row["chargeback_rate"] >= 0.10:
            reasons.append("chargeback behaviour")

        if not reasons:
            reasons.append(
                "normal transaction behaviour"
            )

        return "; ".join(reasons)

    df["risk_reason"] = df.apply(
        reason,
        axis=1
    )

    return df


def main():

    print("\n================================")
    print("       RISKNET AI ENGINE")
    print("================================\n")

    df = build_final_risk()

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        df[
            [
                "customer_id",
                "final_risk_score",
                "final_risk_level",
                "graph_risk_level",
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

    print("\nSaved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

from src.features.customer_features import build_customer_features


def calculate_risk_scores():

    df = build_customer_features().copy()

    df["risk_score"] = 0

    # ---------------------------------------------
    # Transaction activity
    # ---------------------------------------------

    df.loc[
        df["transaction_count"] >= 50,
        "risk_score"
    ] += 15

    # ---------------------------------------------
    # Decline behaviour
    # ---------------------------------------------

    df.loc[
        df["decline_rate"] >= 0.30,
        "risk_score"
    ] += 20

    # ---------------------------------------------
    # Chargeback behaviour
    # ---------------------------------------------

    df.loc[
        df["chargeback_rate"] >= 0.10,
        "risk_score"
    ] += 30

    # ---------------------------------------------
    # Promotion behaviour
    # ---------------------------------------------

    df.loc[
        df["promo_rate"] >= 0.50,
        "risk_score"
    ] += 20

    # ---------------------------------------------
    # High transaction value
    # ---------------------------------------------

    df.loc[
        df["total_transaction_amount"] >= 1000000,
        "risk_score"
    ] += 15

    # Maximum 100
    df["risk_score"] = df["risk_score"].clip(
        upper=100
    )

    # ---------------------------------------------
    # Risk category
    # ---------------------------------------------

    df["risk_level"] = "LOW"

    df.loc[
        df["risk_score"] >= 30,
        "risk_level"
    ] = "MEDIUM"

    df.loc[
        df["risk_score"] >= 60,
        "risk_level"
    ] = "HIGH"

    return df


if __name__ == "__main__":

    df = calculate_risk_scores()

    print("\n================================")
    print("       RISK SCORE ENGINE")
    print("================================\n")

    print(
        df[
            [
                "customer_id",
                "risk_score",
                "risk_level",
                "transaction_count",
                "decline_rate",
                "chargeback_rate",
                "promo_rate",
            ]
        ]
        .sort_values(
            "risk_score",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

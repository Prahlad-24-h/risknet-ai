import pandas as pd


INPUT_PATH = "data/processed/final_risk_results.csv"
OUTPUT_PATH = "data/processed/fraud_ring_classification.csv"


def classify_ring(row):

    promo = row.get("promo_rate", 0)
    decline = row.get("decline_rate", 0)
    chargeback = row.get("chargeback_rate", 0)
    graph = row.get("graph_risk_score", 0)

    fraud_types = []

    # Coupon / referral abuse
    if promo >= 0.50:
        fraud_types.append("COUPON_REFERRAL_ABUSE")

    # Card testing
    if decline >= 0.30:
        fraud_types.append("CARD_TESTING")

    # Chargeback / COD fraud
    if chargeback >= 0.10:
        fraud_types.append("CHARGEBACK_COD")

    # Graph relationship
    if graph > 0 and fraud_types:
        return " + ".join(fraud_types)

    if graph > 0:
        return "SUSPICIOUS_NETWORK"

    if fraud_types:
        return " + ".join(fraud_types)

    return "NO_RING"


def main():

    df = pd.read_csv(INPUT_PATH)

    df["fraud_ring_type"] = df.apply(
        classify_ring,
        axis=1
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n================================")
    print("      FRAUD RING CLASSIFIER")
    print("================================\n")

    print(
        df[
            [
                "customer_id",
                "fraud_ring_type",
                "final_risk_score",
                "final_risk_level"
            ]
        ]
        .sort_values(
            "final_risk_score",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

    print("\nRing distribution:\n")

    print(
        df["fraud_ring_type"]
        .value_counts()
    )

    print("\nSaved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

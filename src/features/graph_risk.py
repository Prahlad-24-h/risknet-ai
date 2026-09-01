import pandas as pd

from src.features.fraud_components import find_fraud_components


def calculate_graph_risk():

    rings = find_fraud_components()

    results = []

    for ring in rings:

        customer_count = ring["customer_count"]
        node_count = ring["node_count"]

        # Base graph risk
        score = 0

        if customer_count >= 3:
            score += 30

        if customer_count >= 5:
            score += 20

        if node_count >= 8:
            score += 20

        score = min(score, 100)

        if score >= 60:
            level = "HIGH"

        elif score >= 30:
            level = "MEDIUM"

        else:
            level = "LOW"

        for customer in ring["customers"]:

            results.append(
                {
                    "customer_id": customer,
                    "ring_id": ring["ring_id"],
                    "ring_customer_count": customer_count,
                    "ring_node_count": node_count,
                    "graph_risk_score": score,
                    "graph_risk_level": level,
                }
            )

    return pd.DataFrame(results)


if __name__ == "__main__":

    df = calculate_graph_risk()

    output_path = "data/processed/graph_risk_results.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("\n================================")
    print("       GRAPH RISK")
    print("================================\n")

    print(
        df.head(20).to_string(index=False)
    )

    print(
        "\nSaved:",
        output_path
    )

import networkx as nx
import pandas as pd

from src.features.fraud_graph import build_fraud_graph


OUTPUT_PATH = "data/processed/network_metrics.csv"


def calculate_network_metrics():

    graph = build_fraud_graph()

    results = []

    for node in graph.nodes:

        node_type = graph.nodes[node].get(
            "node_type"
        )

        if node_type != "customer":
            continue

        results.append(
            {
                "customer_id": node,
                "network_degree": graph.degree(node),
                "network_centrality": nx.degree_centrality(
                    graph
                ).get(node, 0),
            }
        )

    return pd.DataFrame(results)


def main():

    df = calculate_network_metrics()

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n================================")
    print("       NETWORK METRICS")
    print("================================\n")

    print(
        df.sort_values(
            "network_degree",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

    print("\nSaved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

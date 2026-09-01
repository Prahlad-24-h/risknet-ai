import networkx as nx

from src.features.fraud_graph import build_fraud_graph


def find_fraud_components():

    graph = build_fraud_graph()

    components = []

    for component in nx.connected_components(graph):

        customers = [
            node
            for node in component
            if graph.nodes[node].get("node_type") == "customer"
        ]

        if len(customers) >= 2:

            components.append(
                {
                    "ring_id": len(components) + 1,
                    "customer_count": len(customers),
                    "customers": customers,
                    "node_count": len(component),
                }
            )

    return components


if __name__ == "__main__":

    rings = find_fraud_components()

    print("\n================================")
    print("       FRAUD RINGS")
    print("================================\n")

    print("Potential rings:", len(rings))

    for ring in rings[:10]:

        print(
            f"Ring {ring['ring_id']} | "
            f"Customers: {ring['customer_count']} | "
            f"Nodes: {ring['node_count']}"
        )

        print(
            "Customers:",
            ring["customers"]
        )

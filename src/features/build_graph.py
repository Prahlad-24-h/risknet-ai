import networkx as nx
from src.data_loader import load_data


def build_risk_graph():
    data = load_data()

    customers = data["customers"]
    transactions = data["transactions"]

    graph = nx.Graph()

    # Customer nodes
    for _, customer in customers.iterrows():
        customer_id = customer["customer_id"]

        graph.add_node(
            customer_id,
            node_type="customer",
            risk_ring=customer.get("synthetic_ring", "None"),
        )

    # Relationship nodes from transactions
    for _, txn in transactions.iterrows():
        customer_id = txn["customer_id"]

        device_id = txn.get("device_id")
        payment_id = txn.get("payment_instrument_id")

        if pd_not_empty(device_id):
            graph.add_node(
                device_id,
                node_type="device",
            )

            graph.add_edge(
                customer_id,
                device_id,
                relationship="USES_DEVICE",
            )

        if pd_not_empty(payment_id):
            graph.add_node(
                payment_id,
                node_type="payment_instrument",
            )

            graph.add_edge(
                customer_id,
                payment_id,
                relationship="USES_PAYMENT_INSTRUMENT",
            )

    return graph


def pd_not_empty(value):
    return value is not None and str(value) != "nan"


if __name__ == "__main__":
    graph = build_risk_graph()

    print("\n=== RISKNET GRAPH ===")
    print(f"Nodes : {graph.number_of_nodes():,}")
    print(f"Edges : {graph.number_of_edges():,}")

    customer_nodes = [
        n for n, data in graph.nodes(data=True)
        if data.get("node_type") == "customer"
    ]

    device_nodes = [
        n for n, data in graph.nodes(data=True)
        if data.get("node_type") == "device"
    ]

    payment_nodes = [
        n for n, data in graph.nodes(data=True)
        if data.get("node_type") == "payment_instrument"
    ]

    print(f"Customers          : {len(customer_nodes):,}")
    print(f"Devices            : {len(device_nodes):,}")
    print(f"Payment instruments: {len(payment_nodes):,}")

import networkx as nx

from src.data_loader import load_data


def build_fraud_graph():

    data = load_data()

    customers = data["customers"]
    transactions = data["transactions"]

    graph = nx.Graph()

    # Add customers
    for _, row in customers.iterrows():

        customer_id = str(row["customer_id"])

        graph.add_node(
            customer_id,
            node_type="customer"
        )

    # Add transaction relationships
    for _, row in transactions.iterrows():

        customer_id = str(row["customer_id"])

        # Device relationship
        if "device_id" in row.index:

            device_id = str(row["device_id"])

            graph.add_node(
                device_id,
                node_type="device"
            )

            graph.add_edge(
                customer_id,
                device_id,
                relationship="uses_device"
            )

        # Payment relationship
        if "payment_id" in row.index:

            payment_id = str(row["payment_id"])

            graph.add_node(
                payment_id,
                node_type="payment"
            )

            graph.add_edge(
                customer_id,
                payment_id,
                relationship="uses_payment"
            )

        # Address relationship
        if "address_id" in row.index:

            address_id = str(row["address_id"])

            graph.add_node(
                address_id,
                node_type="address"
            )

            graph.add_edge(
                customer_id,
                address_id,
                relationship="uses_address"
            )

    return graph


if __name__ == "__main__":

    G = build_fraud_graph()

    print("\n================================")
    print("       FRAUD GRAPH")
    print("================================\n")

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

from collections import defaultdict
from src.data_loader import load_data


def valid(value):
    return value is not None and str(value) != "nan"


def find_shared_entities():

    data = load_data()
    customers = data["customers"]

    device_groups = defaultdict(list)
    payment_groups = defaultdict(list)

    # Group customers by device and payment instrument
    for _, row in customers.iterrows():

        customer_id = row["customer_id"]

        device_id = row.get("device_id")
        payment_id = row.get("primary_payment_instrument_id")

        if valid(device_id):
            device_groups[device_id].append(customer_id)

        if valid(payment_id):
            payment_groups[payment_id].append(customer_id)

    results = []

    # Shared devices
    for device_id, members in device_groups.items():

        if len(members) >= 3:

            results.append({
                "entity_type": "device",
                "entity_id": device_id,
                "customer_count": len(members),
                "customers": members,
            })

    # Shared payment instruments
    for payment_id, members in payment_groups.items():

        if len(members) >= 3:

            results.append({
                "entity_type": "payment_instrument",
                "entity_id": payment_id,
                "customer_count": len(members),
                "customers": members,
            })

    return results


def print_results(results):

    print("\n================================")
    print(" RISKNET SHARED ENTITY DETECTOR")
    print("================================\n")

    print(f"Potential shared groups: {len(results)}\n")

    for result in results[:20]:

        print("--------------------------------")
        print(f"Type       : {result['entity_type']}")
        print(f"Entity     : {result['entity_id']}")
        print(f"Customers  : {result['customer_count']}")
        print(
            "Members    :",
            ", ".join(result["customers"][:10])
        )

        if result["customer_count"] > 10:
            print("             ...")


if __name__ == "__main__":

    results = find_shared_entities()

    print_results(results)

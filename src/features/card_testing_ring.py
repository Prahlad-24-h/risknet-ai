from collections import defaultdict
from src.data_loader import load_data


def detect_card_testing_rings():

    data = load_data()
    customers = data["customers"]
    transactions = data["transactions"]

    # --------------------------------------------------
    # Group customers by shared device
    # --------------------------------------------------

    device_groups = defaultdict(list)

    for _, row in customers.iterrows():

        customer_id = row["customer_id"]
        device_id = row.get("device_id")

        if device_id is not None and str(device_id) != "nan":
            device_groups[device_id].append(customer_id)

    # --------------------------------------------------
    # Calculate transaction behaviour
    # --------------------------------------------------

    tx_stats = {}

    for customer_id, group in transactions.groupby("customer_id"):

        transaction_count = len(group)

        declined = 0
        tiny_transactions = 0

        if "transaction_status" in group.columns:
            declined = (
                group["transaction_status"]
                .astype(str)
                .str.lower()
                .isin(["declined", "failed"])
                .sum()
            )

        if "amount_inr" in group.columns:
            tiny_transactions = (
                group["amount_inr"] <= 500
            ).sum()

        decline_rate = (
            declined / transaction_count
            if transaction_count else 0
        )

        tiny_rate = (
            tiny_transactions / transaction_count
            if transaction_count else 0
        )

        tx_stats[customer_id] = {
            "transaction_count": transaction_count,
            "declined": declined,
            "decline_rate": decline_rate,
            "tiny_transactions": tiny_transactions,
            "tiny_rate": tiny_rate,
        }

    results = []

    # --------------------------------------------------
    # Analyze shared-device clusters
    # --------------------------------------------------

    for device_id, members in device_groups.items():

        if len(members) < 5:
            continue

        total_transactions = 0
        total_declined = 0
        total_tiny = 0

        for customer_id in members:

            stats = tx_stats.get(
                customer_id,
                {
                    "transaction_count": 0,
                    "declined": 0,
                    "tiny_transactions": 0,
                },
            )

            total_transactions += stats["transaction_count"]
            total_declined += stats["declined"]
            total_tiny += stats["tiny_transactions"]

        if total_transactions == 0:
            continue

        decline_rate = total_declined / total_transactions
        tiny_rate = total_tiny / total_transactions

        score = 0
        reasons = []

        # Shared device
        if len(members) >= 10:
            score += 30
            reasons.append("many customers share the same device")

        else:
            score += 15
            reasons.append("multiple customers share the same device")

        # Tiny transactions
        if tiny_rate >= 0.70:
            score += 35
            reasons.append("very high tiny-transaction rate")

        elif tiny_rate >= 0.40:
            score += 20
            reasons.append("elevated tiny-transaction rate")

        # Declines
        if decline_rate >= 0.50:
            score += 35
            reasons.append("very high decline rate")

        elif decline_rate >= 0.25:
            score += 20
            reasons.append("elevated decline rate")

        score = min(score, 100)

        if score >= 50:

            results.append({
                "ring_type": "CARD_TESTING_RING",
                "device_id": device_id,
                "customer_count": len(members),
                "customers": members,
                "transaction_count": total_transactions,
                "tiny_rate": round(tiny_rate, 3),
                "decline_rate": round(decline_rate, 3),
                "risk_score": score,
                "reasons": reasons,
            })

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return results


def print_results(results):

    print("\n================================")
    print("    CARD TESTING RING DETECTOR")
    print("================================\n")

    print(f"Card testing candidates: {len(results)}\n")

    for i, ring in enumerate(results[:20], 1):

        print("--------------------------------")
        print(f"Candidate        : CT-{i:03d}")
        print(f"Ring Type        : {ring['ring_type']}")
        print(f"Device           : {ring['device_id']}")
        print(f"Customers        : {ring['customer_count']}")
        print(f"Transactions     : {ring['transaction_count']}")
        print(f"Tiny Tx Rate     : {ring['tiny_rate'] * 100:.1f}%")
        print(f"Decline Rate     : {ring['decline_rate'] * 100:.1f}%")
        print(f"Risk Score       : {ring['risk_score']}/100")

        print("Reasons:")

        for reason in ring["reasons"]:
            print(f"  - {reason}")

        print("Customers:")
        print("  ", ", ".join(ring["customers"][:10]))

        if ring["customer_count"] > 10:
            print("   ...")


if __name__ == "__main__":

    results = detect_card_testing_rings()
    print_results(results)

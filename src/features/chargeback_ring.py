from collections import defaultdict
from src.data_loader import load_data


def detect_chargeback_rings():

    data = load_data()

    customers = data["customers"]
    transactions = data["transactions"]

    device_groups = defaultdict(list)

    for _, row in customers.iterrows():

        customer_id = row["customer_id"]
        device_id = row.get("device_id")

        if device_id is not None and str(device_id) != "nan":
            device_groups[device_id].append(customer_id)

    tx_stats = {}

    for customer_id, group in transactions.groupby("customer_id"):

        total = len(group)

        chargebacks = 0

        if "chargeback_flag" in group.columns:
            chargebacks = (
                group["chargeback_flag"]
                .astype(str)
                .str.lower()
                .eq("yes")
                .sum()
            )

        chargeback_rate = (
            chargebacks / total
            if total else 0
        )

        tx_stats[customer_id] = {
            "transactions": total,
            "chargebacks": chargebacks,
            "chargeback_rate": chargeback_rate,
        }

    results = []

    for device_id, members in device_groups.items():

        if len(members) < 5:
            continue

        total_transactions = 0
        total_chargebacks = 0

        for customer_id in members:

            stats = tx_stats.get(
                customer_id,
                {
                    "transactions": 0,
                    "chargebacks": 0,
                },
            )

            total_transactions += stats["transactions"]
            total_chargebacks += stats["chargebacks"]

        if total_transactions == 0:
            continue

        chargeback_rate = (
            total_chargebacks /
            total_transactions
        )

        score = 0
        reasons = []

        # Shared device
        if len(members) >= 10:
            score += 35
            reasons.append(
                "many customers share the same device"
            )
        else:
            score += 15
            reasons.append(
                "multiple customers share the same device"
            )

        # Chargebacks
        if chargeback_rate >= 0.30:
            score += 65
            reasons.append(
                "very high chargeback rate"
            )

        elif chargeback_rate >= 0.15:
            score += 45
            reasons.append(
                "elevated chargeback rate"
            )

        elif chargeback_rate >= 0.05:
            score += 25
            reasons.append(
                "chargeback activity detected"
            )

        score = min(score, 100)

        if score >= 50:

            results.append({
                "ring_type": "CHARGEBACK_RING",
                "device_id": device_id,
                "customer_count": len(members),
                "customers": members,
                "transaction_count": total_transactions,
                "chargebacks": total_chargebacks,
                "chargeback_rate": round(
                    chargeback_rate, 3
                ),
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
    print("      CHARGEBACK RING DETECTOR")
    print("================================\n")

    print(
        f"Chargeback candidates: {len(results)}\n"
    )

    for i, ring in enumerate(results[:20], 1):

        print("--------------------------------")
        print(f"Candidate        : CB-{i:03d}")
        print(f"Ring Type        : {ring['ring_type']}")
        print(f"Device           : {ring['device_id']}")
        print(f"Customers        : {ring['customer_count']}")
        print(f"Transactions     : {ring['transaction_count']}")
        print(f"Chargebacks      : {ring['chargebacks']}")
        print(
            f"Chargeback Rate  : "
            f"{ring['chargeback_rate'] * 100:.1f}%"
        )
        print(f"Risk Score       : {ring['risk_score']}/100")

        print("Reasons:")

        for reason in ring["reasons"]:
            print(f"  - {reason}")

        print("Customers:")
        print("  ", ", ".join(ring["customers"][:10]))

        if ring["customer_count"] > 10:
            print("   ...")


if __name__ == "__main__":

    results = detect_chargeback_rings()
    print_results(results)

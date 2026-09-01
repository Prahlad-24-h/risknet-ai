from collections import defaultdict
from src.data_loader import load_data


def detect_coupon_rings():

    data = load_data()

    customers = data["customers"]
    transactions = data["transactions"]

    # --------------------------------------------------
    # 1. Group customers by device
    # --------------------------------------------------

    device_groups = defaultdict(list)

    for _, row in customers.iterrows():

        customer_id = row["customer_id"]
        device_id = row.get("device_id")

        if device_id is not None and str(device_id) != "nan":
            device_groups[device_id].append(customer_id)

    # --------------------------------------------------
    # 2. Calculate transaction/promotion behaviour
    # --------------------------------------------------

    tx_stats = {}

    for customer_id, group in transactions.groupby("customer_id"):

        transaction_count = len(group)

        promo_count = 0

        if "promo_used" in group.columns:
            promo_count = (
                group["promo_used"]
                .astype(str)
                .str.lower()
                .eq("yes")
                .sum()
            )

        promo_rate = (
            promo_count / transaction_count
            if transaction_count > 0
            else 0
        )

        tx_stats[customer_id] = {
            "transaction_count": transaction_count,
            "promo_count": promo_count,
            "promo_rate": promo_rate,
        }

    # --------------------------------------------------
    # 3. Identify suspicious shared-device groups
    # --------------------------------------------------

    results = []

    for device_id, members in device_groups.items():

        # Need multiple accounts on the same device
        if len(members) < 5:
            continue

        total_transactions = 0
        total_promos = 0

        for customer_id in members:

            stats = tx_stats.get(
                customer_id,
                {
                    "transaction_count": 0,
                    "promo_count": 0,
                    "promo_rate": 0,
                },
            )

            total_transactions += stats["transaction_count"]
            total_promos += stats["promo_count"]

        promo_rate = (
            total_promos / total_transactions
            if total_transactions > 0
            else 0
        )

        # --------------------------------------------------
        # 4. Calculate a simple risk score
        # --------------------------------------------------

        score = 0
        reasons = []

        # Shared device
        if len(members) >= 10:
            score += 40
            reasons.append("many customers share the same device")

        elif len(members) >= 5:
            score += 25
            reasons.append("multiple customers share the same device")

        # Promotion behaviour
        if promo_rate >= 0.70:
            score += 40
            reasons.append("very high promotion usage")

        elif promo_rate >= 0.40:
            score += 25
            reasons.append("elevated promotion usage")

        # Transaction volume
        if total_transactions >= 50:
            score += 20
            reasons.append("high transaction activity")

        elif total_transactions >= 20:
            score += 10
            reasons.append("elevated transaction activity")

        # Cap score
        score = min(score, 100)

        # Only report meaningful candidates
        if score >= 50:

            results.append({
                "ring_type": "COUPON_RING",
                "device_id": device_id,
                "customer_count": len(members),
                "customers": members,
                "transaction_count": total_transactions,
                "promo_count": total_promos,
                "promo_rate": round(promo_rate, 3),
                "risk_score": score,
                "reasons": reasons,
            })

    # Highest-risk first
    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return results


def print_results(results):

    print("\n================================")
    print("      COUPON RING DETECTOR")
    print("================================\n")

    print(f"Coupon ring candidates: {len(results)}\n")

    for i, ring in enumerate(results[:20], 1):

        print("--------------------------------")
        print(f"Candidate        : CR-{i:03d}")
        print(f"Ring Type        : {ring['ring_type']}")
        print(f"Device           : {ring['device_id']}")
        print(f"Customers        : {ring['customer_count']}")
        print(f"Transactions     : {ring['transaction_count']}")
        print(f"Promo Usage      : {ring['promo_rate'] * 100:.1f}%")
        print(f"Risk Score       : {ring['risk_score']}/100")

        print("Reasons:")

        for reason in ring["reasons"]:
            print(f"  - {reason}")

        print("Customers:")

        print(
            "  ",
            ", ".join(ring["customers"][:10])
        )

        if ring["customer_count"] > 10:
            print("   ...")


if __name__ == "__main__":

    results = detect_coupon_rings()

    print_results(results)

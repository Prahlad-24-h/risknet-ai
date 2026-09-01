from src.features.coupon_ring import detect_coupon_rings
from src.features.card_testing_ring import detect_card_testing_rings
from src.features.chargeback_ring import detect_chargeback_rings


def run_risk_engine():

    coupon = detect_coupon_rings()
    card_testing = detect_card_testing_rings()
    chargeback = detect_chargeback_rings()

    all_rings = []

    for ring in coupon:
        ring["category"] = "Coupon Abuse"
        all_rings.append(ring)

    for ring in card_testing:
        ring["category"] = "Card Testing"
        all_rings.append(ring)

    for ring in chargeback:
        ring["category"] = "Chargeback"
        all_rings.append(ring)

    all_rings.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return all_rings


if __name__ == "__main__":

    results = run_risk_engine()

    print("\n================================")
    print("       RISKNET AI ENGINE")
    print("================================\n")

    print(
        f"Total ring candidates: {len(results)}\n"
    )

    for i, ring in enumerate(results[:20], 1):

        print("--------------------------------")
        print(f"Rank       : {i}")
        print(f"Category   : {ring['category']}")
        print(f"Ring       : {ring['ring_type']}")
        print(f"Device     : {ring['device_id']}")
        print(f"Customers  : {ring['customer_count']}")
        print(f"Risk Score : {ring['risk_score']}/100")

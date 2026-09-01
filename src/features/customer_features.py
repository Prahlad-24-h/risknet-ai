import pandas as pd
from src.data_loader import load_data


def build_customer_features():

    data = load_data()

    customers = data["customers"].copy()
    transactions = data["transactions"].copy()

    # ---------------------------------------------
    # Transaction statistics
    # ---------------------------------------------

    transaction_stats = transactions.groupby(
        "customer_id"
    ).agg(
        transaction_count=("customer_id", "count"),
        total_transaction_amount=("amount_inr", "sum"),
        average_transaction_amount=("amount_inr", "mean"),
    ).reset_index()

    # ---------------------------------------------
    # Decline statistics
    # ---------------------------------------------

    if "transaction_status" in transactions.columns:

        declined = transactions[
            transactions["transaction_status"]
            .astype(str)
            .str.lower()
            .isin(["declined", "failed"])
        ]

        decline_stats = declined.groupby(
            "customer_id"
        ).size().reset_index(
            name="declined_transactions"
        )

    else:

        decline_stats = pd.DataFrame(
            columns=[
                "customer_id",
                "declined_transactions"
            ]
        )

    # ---------------------------------------------
    # Chargeback statistics
    # ---------------------------------------------

    if "chargeback_flag" in transactions.columns:

        chargeback_stats = transactions.groupby(
            "customer_id"
        )["chargeback_flag"].apply(
            lambda x: (
                x.astype(str)
                .str.lower()
                .eq("yes")
                .sum()
            )
        ).reset_index(
            name="chargeback_count"
        )

    else:

        chargeback_stats = pd.DataFrame(
            columns=[
                "customer_id",
                "chargeback_count"
            ]
        )

    # ---------------------------------------------
    # Promotion statistics
    # ---------------------------------------------

    if "promo_used" in transactions.columns:

        promo_stats = transactions.groupby(
            "customer_id"
        )["promo_used"].apply(
            lambda x: (
                x.astype(str)
                .str.lower()
                .eq("yes")
                .sum()
            )
        ).reset_index(
            name="promo_count"
        )

    else:

        promo_stats = pd.DataFrame(
            columns=[
                "customer_id",
                "promo_count"
            ]
        )

    # ---------------------------------------------
    # Merge everything
    # ---------------------------------------------

    features = customers.merge(
        transaction_stats,
        on="customer_id",
        how="left"
    )

    features = features.merge(
        decline_stats,
        on="customer_id",
        how="left"
    )

    features = features.merge(
        chargeback_stats,
        on="customer_id",
        how="left"
    )

    features = features.merge(
        promo_stats,
        on="customer_id",
        how="left"
    )

    # ---------------------------------------------
    # Fill missing values
    # ---------------------------------------------

    numeric_columns = [
        "transaction_count",
        "total_transaction_amount",
        "average_transaction_amount",
        "declined_transactions",
        "chargeback_count",
        "promo_count",
    ]

    for column in numeric_columns:

        if column in features.columns:
            features[column] = features[column].fillna(0)

    # ---------------------------------------------
    # Derived risk indicators
    # ---------------------------------------------

    features["decline_rate"] = (
        features["declined_transactions"]
        / features["transaction_count"].replace(0, 1)
    )

    features["chargeback_rate"] = (
        features["chargeback_count"]
        / features["transaction_count"].replace(0, 1)
    )

    features["promo_rate"] = (
        features["promo_count"]
        / features["transaction_count"].replace(0, 1)
    )

    return features


if __name__ == "__main__":

    features = build_customer_features()

    print("\n================================")
    print("     CUSTOMER FEATURE ENGINE")
    print("================================\n")

    print("Customers:", len(features))
    print("Features :", len(features.columns))

    print("\nColumns:")
    print(list(features.columns))

    print("\nSample:")
    print(features.head())

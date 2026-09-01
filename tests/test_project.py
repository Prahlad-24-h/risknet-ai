import pandas as pd


DATA_PATH = "data/processed/fraud_ring_classification.csv"


def test_dataset_exists():

    df = pd.read_csv(DATA_PATH)

    assert len(df) > 0


def test_required_columns():

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "customer_id",
        "ring_id",
        "final_risk_score",
        "final_risk_level",
        "fraud_ring_type"
    ]

    for column in required_columns:
        assert column in df.columns


def test_risk_levels():

    df = pd.read_csv(DATA_PATH)

    valid_levels = {
        "LOW",
        "MEDIUM",
        "HIGH"
    }

    assert set(
        df["final_risk_level"].dropna().unique()
    ).issubset(valid_levels)


def test_customer_ids():

    df = pd.read_csv(DATA_PATH)

    assert df["customer_id"].notna().all()

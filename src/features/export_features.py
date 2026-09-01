from src.features.risk_score import calculate_risk_scores


def export_features():

    df = calculate_risk_scores()

    output_path = "data/processed/customer_risk_features.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print("\n================================")
    print("       FEATURE EXPORT")
    print("================================")

    print(f"\nSaved: {output_path}")
    print(f"Rows : {len(df)}")
    print(f"Cols : {len(df.columns)}")


if __name__ == "__main__":
    export_features()

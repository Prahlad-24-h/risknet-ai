import pandas as pd
import joblib


DATA_PATH = "data/processed/customer_risk_features.csv"
MODEL_PATH = "models/risk_model.pkl"


def predict_risk():

    data = pd.read_csv(DATA_PATH)

    saved = joblib.load(MODEL_PATH)

    model = saved["model"]
    encoder = saved["encoder"]
    features = saved["features"]

    X = data[features]

    predictions = model.predict(X)

    data["ml_risk_level"] = encoder.inverse_transform(
        predictions
    )

    print("\n================================")
    print("       ML RISK PREDICTION")
    print("================================\n")

    print(
        data[
            [
                "customer_id",
                "ml_risk_level"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )
    output_path = "data/processed/ml_predictions.csv"

    data.to_csv(
        output_path,
        index=False
    )

    print("\nPredictions saved to:", output_path)

    return data


if __name__ == "__main__":
    predict_risk()

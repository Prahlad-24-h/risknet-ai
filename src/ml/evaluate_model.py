import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


DATA_PATH = "data/processed/customer_risk_features.csv"
MODEL_PATH = "models/risk_model.pkl"


def evaluate_model():

    df = pd.read_csv(DATA_PATH)

    saved = joblib.load(MODEL_PATH)

    model = saved["model"]
    encoder = saved["encoder"]
    features = saved["features"]

    X = df[features]
    y = encoder.transform(df["risk_level"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("\n================================")
    print("       MODEL EVALUATION")
    print("================================\n")

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


if __name__ == "__main__":
    evaluate_model()

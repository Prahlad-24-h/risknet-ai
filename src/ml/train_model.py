import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib


DATA_PATH = "data/processed/customer_risk_features.csv"
MODEL_PATH = "models/risk_model.pkl"


def train_model():

    # Load processed customer features
    df = pd.read_csv(DATA_PATH)

    print("\n================================")
    print("       RISKNET AI - ML")
    print("================================\n")

    print("Dataset shape:", df.shape)

    # Target
    target = "risk_level"

    # Features used by the model
    feature_columns = [
        "transaction_count",
        "total_transaction_amount",
        "average_transaction_amount",
        "declined_transactions",
        "chargeback_count",
        "promo_count",
        "decline_rate",
        "chargeback_rate",
        "promo_rate",
    ]

    X = df[feature_columns]
    y = df[target]

    # Convert LOW/MEDIUM/HIGH into numbers
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    print("\nRisk classes:")
    for number, label in enumerate(encoder.classes_):
        print(number, "=", label)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        random_state=42,
        stratify=y_encoded
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples :", len(X_test))

    # Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nAccuracy:", round(accuracy, 4))

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        )
    )

    # Save model
    joblib.dump(
        {
            "model": model,
            "encoder": encoder,
            "features": feature_columns
        },
        MODEL_PATH
    )

    print("\nModel saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()

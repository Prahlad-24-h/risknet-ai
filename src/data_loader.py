from pathlib import Path
import pandas as pd


DATA_FILE = Path(
    "data/raw/AI_Risk_Manager_Synthetic_Dataset_v2.xlsx"
)


def load_data():
    customers = pd.read_excel(
        DATA_FILE,
        sheet_name="Customers"
    )

    kyc = pd.read_excel(
        DATA_FILE,
        sheet_name="KYC"
    )

    loans = pd.read_excel(
        DATA_FILE,
        sheet_name="Loans"
    )

    transactions = pd.read_excel(
        DATA_FILE,
        sheet_name="Transactions"
    )

    risk_profiles = pd.read_excel(
        DATA_FILE,
        sheet_name="Risk_Profiles"
    )

    return {
        "customers": customers,
        "kyc": kyc,
        "loans": loans,
        "transactions": transactions,
        "risk_profiles": risk_profiles,
    }


if __name__ == "__main__":
    data = load_data()

    print("\n=== RISKNET AI DATASET ===\n")

    for name, df in data.items():
        print(f"{name:15} : {len(df):,} rows")

    print("\nCustomers columns:")
    print(data["customers"].columns.tolist())

    print("\nTransaction columns:")
    print(data["transactions"].columns.tolist())

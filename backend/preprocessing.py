import pandas as pd

def preprocess_data(df):
    df = df.copy()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Clean category names
    df["category"] = df["category"].str.strip().str.title()

    # Ensure amount is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Drop rows with invalid amount
    df = df.dropna(subset=["amount"])

    return df

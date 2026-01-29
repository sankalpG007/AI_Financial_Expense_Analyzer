import pandas as pd

REQUIRED_COLUMNS = {"date", "category", "amount", "description"}

def load_expense_data(csv_file):
    """
    Load and validate expense CSV file
    """
    df = pd.read_csv(csv_file)

    # Check required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df

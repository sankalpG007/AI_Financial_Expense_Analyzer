import pandas as pd

REQUIRED_COLUMNS = {"date", "category", "amount", "description"}


def load_expense_data(file):
    """
    Load and validate expense data from CSV or Excel
    """
    filename = file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file)

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format. Upload CSV or Excel.")

    # Normalize column names (important UX improvement)
    df.columns = [c.strip().lower() for c in df.columns]

    # Check required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df

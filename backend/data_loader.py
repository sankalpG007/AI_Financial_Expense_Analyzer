import pandas as pd


def load_expense_data(file):

    # -----------------------------------
    # READ FILE
    # -----------------------------------

    if str(file).endswith(".csv"):
        df = pd.read_csv(file)

    elif str(file).endswith(".xlsx"):
        df = pd.read_excel(file)

    else:
        raise ValueError(
            "Unsupported file format"
        )

    # -----------------------------------
    # STANDARDIZE COLUMN NAMES
    # -----------------------------------

    df.columns = [
        col.lower().strip()
        for col in df.columns
    ]

    # -----------------------------------
    # AUTO-DETECT DATE COLUMN
    # -----------------------------------

    date_keywords = [
        "date",
        "transaction date",
        "time"
    ]

    amount_keywords = [
        "amount",
        "debit",
        "expense",
        "price",
        "cost"
    ]

    category_keywords = [
        "category",
        "merchant",
        "type"
    ]

    # Detect columns
    date_col = None
    amount_col = None
    category_col = None

    for col in df.columns:

        if any(k in col for k in date_keywords):
            date_col = col

        if any(k in col for k in amount_keywords):
            amount_col = col

        if any(k in col for k in category_keywords):
            category_col = col

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not amount_col:
        raise ValueError(
            "No amount column detected"
        )

    # -----------------------------------
    # RENAME TO STANDARD FORMAT
    # -----------------------------------

    rename_map = {}

    if date_col:
        rename_map[date_col] = "date"

    if amount_col:
        rename_map[amount_col] = "amount"

    if category_col:
        rename_map[category_col] = "category"

    df = df.rename(columns=rename_map)

    # -----------------------------------
    # CREATE MISSING CATEGORY
    # -----------------------------------

    if "category" not in df.columns:
        df["category"] = "Other"

    # -----------------------------------
    # CREATE MISSING DATE
    # -----------------------------------

    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today()

    return df
import pandas as pd


def load_expense_data(file):
    """
    Load expense data from:
    - CSV file path
    - Excel file path
    - Streamlit UploadedFile
    """

    # Get filename when available
    filename = getattr(file, "name", str(file))

    filename = str(filename).lower()

    # CSV
    if filename.endswith(".csv"):
        df = pd.read_csv(file)

    # Excel
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload a CSV or XLSX file."
        )

    # Standardize column names
    df.columns = [
        str(col).lower().strip()
        for col in df.columns
    ]

    # Possible column names
    date_keywords = [
        "date",
        "transaction date",
        "time",
    ]

    amount_keywords = [
        "amount",
        "debit",
        "expense",
        "price",
        "cost",
    ]

    category_keywords = [
        "category",
        "merchant",
        "type",
    ]

    # --------------------------------------------------
    # Detect Date Column
    # --------------------------------------------------

    date_column = None

    for col in df.columns:
        if any(keyword in col for keyword in date_keywords):
            date_column = col
            break

    # --------------------------------------------------
    # Detect Amount Column
    # --------------------------------------------------

    amount_column = None

    for col in df.columns:
        if any(keyword in col for keyword in amount_keywords):
            amount_column = col
            break

    if amount_column is None:
        raise ValueError(
            "Could not find an amount column. "
            "Use a column such as Amount, Expense, Debit, Price or Cost."
        )

    # --------------------------------------------------
    # Detect Category Column
    # --------------------------------------------------

    category_column = None

    for col in df.columns:
        if any(keyword in col for keyword in category_keywords):
            category_column = col
            break

    # --------------------------------------------------
    # Rename Columns
    # --------------------------------------------------

    rename_map = {
        amount_column: "amount",
    }

    if date_column:
        rename_map[date_column] = "date"

    if category_column:
        rename_map[category_column] = "category"

    df = df.rename(columns=rename_map)

    # --------------------------------------------------
    # Missing Category
    # --------------------------------------------------

    if "category" not in df.columns:
        df["category"] = "Other"

    # --------------------------------------------------
    # Missing Date
    # --------------------------------------------------

    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today()

    return df
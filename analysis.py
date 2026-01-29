def total_spending(df):
    """
    Calculate total expense
    """
    return df["amount"].sum()


def category_spending(df):
    """
    Calculate spending per category
    """
    category_totals = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    return category_totals


def monthly_spending(df):
    """
    Calculate monthly spending trend
    """
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")

    monthly_totals = (
        df.groupby("month")["amount"]
        .sum()
    )
    return monthly_totals

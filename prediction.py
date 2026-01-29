import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month_expense(df):
    """
    Predict next month's total expense using Linear Regression
    (with safety checks)
    """
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby("month")["amount"].sum().reset_index()
    monthly["month_index"] = np.arange(len(monthly))

    X = monthly[["month_index"]]
    y = monthly["amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_X = X.iloc[[-1]] + 1
    prediction = model.predict(next_X)[0]

    # Safety: expenses cannot be negative
    prediction = max(prediction, 0)

    return round(prediction, 2)

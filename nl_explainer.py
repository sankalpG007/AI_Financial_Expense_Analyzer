def explain_data(df, anomalies, prediction):
    explanations = []

    total = df["amount"].sum()
    top_category = df.groupby("category")["amount"].sum().idxmax()

    explanations.append(
        f"You spent a total of ₹{total:,.2f}. "
        f"Your highest spending category is '{top_category}'."
    )

    if not anomalies.empty:
        explanations.append(
            f"I detected {len(anomalies)} unusual transactions. "
            "These could be one-time large expenses or irregular spending."
        )
    else:
        explanations.append(
            "Your spending looks consistent with no major anomalies detected."
        )

    explanations.append(
        f"Based on past trends, your estimated expense next month is around ₹{prediction:,.2f}."
    )

    explanations.append(
        "Tip: Review high-frequency categories to identify saving opportunities."
    )

    return explanations

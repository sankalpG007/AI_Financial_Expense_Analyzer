def generate_insights(df):
    """
    Generate AI-like insights based on spending patterns
    """
    insights = []

    total_spent = df["amount"].sum()
    category_totals = df.groupby("category")["amount"].sum()

    # Insight 1: Category percentage analysis
    for category, amount in category_totals.items():
        percentage = (amount / total_spent) * 100

        if percentage > 40:
            insights.append(
                f"⚠️ You spend {percentage:.1f}% on {category}. "
                f"This is quite high and could be reduced."
            )
        elif percentage > 25:
            insights.append(
                f"📌 {category} accounts for {percentage:.1f}% of your spending."
            )
        elif percentage < 10:
            insights.append(
                f"✅ Your spending on {category} is well controlled "
                f"({percentage:.1f}%)."
            )

    # Insight 2: Highest spending category
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()

    insights.append(
        f"💡 Your highest spending category is {top_category} "
        f"with a total of ₹{top_amount:.2f}."
    )

    return insights

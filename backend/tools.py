# tools.py

def generate_budget_plan(data):

    highest_category = max(
        data["category_spending"],
        key=data["category_spending"].get
    )

    amount = data["category_spending"][
        highest_category
    ]

    return (
        f"Your highest spending category is "
        f"{highest_category} (₹{amount:.2f}).\n\n"
        f"Recommended Budget Plan:\n"
        f"- Reduce {highest_category} spending by 15%\n"
        f"- Track weekly expenses\n"
        f"- Set monthly spending limits\n"
        f"- Save at least 20% income monthly"
    )


def explain_anomalies(data):

    count = data["anomaly_count"]

    if count == 0:
        return "No unusual transactions detected."

    return (
        f"I detected {count} unusual transactions.\n"
        f"These may include sudden high expenses "
        f"or irregular spending patterns."
    )


def financial_summary(data):

    total = data["total_spending"]

    prediction = data["prediction"]

    return (
        f"Financial Summary:\n\n"
        f"- Total Spending: ₹{total:.2f}\n"
        f"- Predicted Next Month: ₹{prediction:.2f}\n"
        f"- Anomalies Found: {data['anomaly_count']}"
    )

def autonomous_financial_advisor(data):

    category_data = data["category_spending"]

    total = data["total_spending"]

    insights = []

    # -------------------------
    # Detect high spending
    # -------------------------

    for category, amount in category_data.items():

        percentage = (
            amount / total
        ) * 100

        if percentage > 25:

            insights.append(
                f"⚠️ High spending detected in "
                f"{category} ({percentage:.1f}%)."
            )

    # -------------------------
    # Prediction warning
    # -------------------------

    prediction = data["prediction"]

    if prediction > total / 6:

        insights.append(
            "📈 Your future spending trend "
            "is increasing."
        )

    # -------------------------
    # Savings suggestions
    # -------------------------

    highest_category = max(
        category_data,
        key=category_data.get
    )

    insights.append(
        f"💡 Reducing {highest_category} "
        f"expenses by 15% could improve "
        f"your monthly savings significantly."
    )

    # -------------------------
    # Financial health
    # -------------------------

    anomaly_count = data["anomaly_count"]

    if anomaly_count > 5:

        insights.append(
            "🚨 Multiple unusual transactions detected."
        )

    return "\n".join(insights)

def multi_step_financial_reasoning(data):

    reasoning_steps = []

    category_data = data["category_spending"]

    total = data["total_spending"]

    prediction = data["prediction"]

    anomaly_count = data["anomaly_count"]

    # ---------------------------------
    # STEP 1 — Analyze spending
    # ---------------------------------

    reasoning_steps.append(
        "STEP 1️⃣: Financial data analyzed successfully."
    )

    # ---------------------------------
    # STEP 2 — Detect highest spending
    # ---------------------------------

    highest_category = max(
        category_data,
        key=category_data.get
    )

    highest_amount = category_data[
        highest_category
    ]

    reasoning_steps.append(
        f"STEP 2️⃣: Highest spending detected in "
        f"{highest_category} "
        f"(₹{highest_amount:.2f})."
    )

    # ---------------------------------
    # STEP 3 — Detect anomalies
    # ---------------------------------

    if anomaly_count > 0:

        reasoning_steps.append(
            f"STEP 3️⃣: Found "
            f"{anomaly_count} unusual transactions."
        )

    else:

        reasoning_steps.append(
            "STEP 3️⃣: No unusual transactions detected."
        )

    # ---------------------------------
    # STEP 4 — Future trend analysis
    # ---------------------------------

    avg_monthly = total / 6

    if prediction > avg_monthly:

        reasoning_steps.append(
            "STEP 4️⃣: Future spending trend "
            "appears to be increasing."
        )

    else:

        reasoning_steps.append(
            "STEP 4️⃣: Future spending trend "
            "looks stable."
        )

    # ---------------------------------
    # STEP 5 — Generate action plan
    # ---------------------------------

    reasoning_steps.append(
        f"STEP 5️⃣: Recommended actions:\n"
        f"- Reduce {highest_category} expenses by 15%\n"
        f"- Set monthly category budgets\n"
        f"- Track weekly expenses\n"
        f"- Review unusual transactions regularly"
    )

    # ---------------------------------
    # STEP 6 — Savings estimate
    # ---------------------------------

    estimated_savings = highest_amount * 0.15

    reasoning_steps.append(
        f"STEP 6️⃣: Estimated monthly savings "
        f"potential: ₹{estimated_savings:.2f}"
    )

    return "\n\n".join(reasoning_steps)
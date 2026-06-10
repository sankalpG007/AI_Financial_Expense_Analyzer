from goal_manager import (
    save_goal,
    load_goal,
    calculate_progress
)

def agent_router(message, analysis_data):

    msg = message.lower()

    # SAVE GOAL

    if "save" in msg and "goal" in msg:

        import re

        numbers = re.findall(r"\d+", msg)

        if len(numbers) >= 2:

            amount = int(numbers[0])
            months = int(numbers[1])

            save_goal(amount, months)

            return f"""
🎯 Goal Saved

Target:
₹{amount}

Duration:
{months} months
"""

    # GOAL PROGRESS

    if "how am i doing" in msg:

        goal = load_goal()

        if not goal:
            return "No goal found."

        progress = calculate_progress(
            goal,
            analysis_data
        )

        return f"""
🎯 Goal Progress

Goal:
₹{progress['goal']}

Months:
{progress['months']}

Required/Month:
₹{progress['required_per_month']}

Projected Savings:
₹{progress['projected_savings']}

Status:
{progress['status']}
"""

    # HIGHEST SPENDING

    if "highest" in msg and "spending" in msg:

        category = max(
            analysis_data["category_spending"],
            key=analysis_data["category_spending"].get
        )

        amount = analysis_data["category_spending"][category]

        return f"""
Highest spending category:

{category}

₹{amount}
"""

    # PREDICTION

    if "prediction" in msg:

        return f"""
Predicted next month spending:

₹{analysis_data["prediction"]}
"""

    # ANOMALIES

    if "anomal" in msg:

        return f"""
Detected anomalies:

{analysis_data["anomaly_count"]}
"""

    # SUMMARY

    if "summary" in msg:

        category = max(
            analysis_data["category_spending"],
            key=analysis_data["category_spending"].get
        )

        return f"""
Total Spending:
₹{analysis_data["total_spending"]}

Highest Category:
{category}

Prediction:
₹{analysis_data["prediction"]}
"""

    return None
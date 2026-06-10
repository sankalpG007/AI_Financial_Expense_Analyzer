import json
import os

GOAL_FILE = "goal.json"


def save_goal(amount, months):

    goal_data = {
        "amount": amount,
        "months": months
    }

    with open(GOAL_FILE, "w") as f:
        json.dump(goal_data, f)

    return True


def load_goal():

    if not os.path.exists(GOAL_FILE):
        return None

    with open(GOAL_FILE, "r") as f:
        return json.load(f)


def calculate_progress(goal, analysis_data):

    monthly_spending = analysis_data[
        "monthly_spending"
    ]

    avg_monthly_spending = (
        sum(monthly_spending.values())
        / len(monthly_spending)
    )

    estimated_savings_per_month = (
        50000 - avg_monthly_spending
    )

    projected_savings = (
        estimated_savings_per_month
        * goal["months"]
    )

    status = "On Track"

    if projected_savings < goal["amount"]:
        status = "Behind Target"

    return {
        "goal": goal["amount"],
        "months": goal["months"],
        "required_per_month":
            round(
                goal["amount"] /
                goal["months"],
                2
            ),
        "projected_savings":
            round(
                projected_savings,
                2
            ),
        "status": status
    }
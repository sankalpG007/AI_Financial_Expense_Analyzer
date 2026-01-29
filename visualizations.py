import matplotlib.pyplot as plt


def plot_category_spending(category_data):
    """
    Pie chart for category-wise spending
    """
    fig, ax = plt.subplots()

    category_data.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        ax=ax
    )

    ax.set_title("Category-wise Spending Distribution")
    ax.set_ylabel("")  # Remove y-label

    plt.tight_layout()
    return fig


def plot_monthly_spending(monthly_data):
    """
    Line chart for monthly spending trend
    """
    fig, ax = plt.subplots()

    monthly_data.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Expense")

    plt.tight_layout()
    return fig

import matplotlib.pyplot as plt

def plot_monthly_spending_with_anomalies(monthly_data, anomaly_months):
    fig, ax = plt.subplots()

    # Plot normal line
    monthly_data.plot(
        kind="line",
        marker="o",
        ax=ax,
        color="blue",
        label="Monthly Spending"
    )

    # Highlight anomaly months
    for month in monthly_data.index:
        if month in anomaly_months:
            ax.scatter(
                month,
                monthly_data.loc[month],
                color="red",
                s=100,
                label="Anomaly" if "Anomaly" not in ax.get_legend_handles_labels()[1] else ""
            )

    ax.set_title("Monthly Spending Trend (Anomalies Highlighted)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Expense")
    ax.legend()

    plt.tight_layout()
    return fig

def highlight_anomaly_categories(df, anomalies):
    """
    Return categories that contain anomalies
    """
    return anomalies["category"].value_counts()

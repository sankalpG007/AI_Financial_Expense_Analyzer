import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Add backend directory to Python path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from data_loader import load_expense_data
from preprocessing import preprocess_data
from analysis import total_spending, category_spending, monthly_spending
from prediction import predict_next_month_expense
from anomaly_detection import detect_anomalies
from insights import generate_insights
from tools import (
    financial_summary,
    generate_budget_plan,
    explain_anomalies,
    multi_step_financial_reasoning,
    autonomous_financial_advisor,
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Financial Expense Analyzer",
    page_icon="💰",
    layout="wide",
     initial_sidebar_state="expanded",
)

st.title("💰 AI Financial Expense Analyzer")
st.caption(
    "Machine Learning powered expense analytics, forecasting, "
    "anomaly detection and financial intelligence."
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.sidebar.header("📂 Upload Expense Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or XLSX file",
    type=["csv", "xlsx"],
    help="Upload an expense dataset containing Date, Amount and Category information.",
)

if uploaded_file is None:
    st.info("👈 Upload an expense CSV or XLSX file from the sidebar to begin.")

    st.markdown("### Supported data")

    st.markdown(
        """
        Your dataset should contain columns representing:

        - **Date**
        - **Amount / Expense / Debit / Price / Cost**
        - **Category / Merchant / Type**

        The system automatically detects and standardizes these columns.
        """
    )

    st.stop()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_expense_data(uploaded_file)
    df = preprocess_data(df)

except Exception as e:
    st.error(f"❌ Error processing file: {e}")
    st.stop()


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

total = total_spending(df)
category_data = category_spending(df)
monthly_data = monthly_spending(df)
prediction = predict_next_month_expense(df)
anomalies = detect_anomalies(df)
insights = generate_insights(df)

analysis_data = {
    "total_spending": total,
    "category_spending": category_data.to_dict()
        if isinstance(category_data, pd.Series)
        else category_data,
    "prediction": prediction,
    "anomaly_count": len(anomalies),
}


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.success(
    f"✅ Successfully processed {len(df):,} transactions."
)

st.divider()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Spending",
        f"₹{total:,.2f}",
    )

with col2:
    st.metric(
        "Transactions",
        f"{len(df):,}",
    )

with col3:
    st.metric(
        "Anomalies",
        f"{len(anomalies):,}",
    )

with col4:
    st.metric(
        "Predicted Next Month",
        f"₹{prediction:,.2f}",
    )


# --------------------------------------------------
# PROCESSED DATA
# --------------------------------------------------

st.divider()

with st.expander("📋 View Processed Data"):
    st.dataframe(
        df,
        width="stretch",
    )


# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("💳 Category Spending")

if isinstance(category_data, pd.Series):
    st.bar_chart(category_data)
else:
    st.dataframe(
        category_data,
        width="stretch",
    )


# --------------------------------------------------
# MONTHLY ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("📅 Monthly Spending")

if isinstance(monthly_data, pd.Series):
    st.line_chart(monthly_data)
else:
    st.dataframe(
        monthly_data,
        width="stretch",
    )


# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

st.divider()

st.subheader("🚨 Anomaly Detection")

if len(anomalies) > 0:
    st.warning(
        f"Detected {len(anomalies)} potentially unusual transactions."
    )

    st.dataframe(
        anomalies,
        width="stretch",
    )
else:
    st.success("No unusual transactions detected.")


# --------------------------------------------------
# FINANCIAL INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("💡 Financial Insights")

if isinstance(insights, (list, tuple)):
    for insight in insights:
        st.write(f"• {insight}")
else:
    st.write(insights)


# --------------------------------------------------
# TOOL AUGMENTATION
# --------------------------------------------------

st.divider()

st.subheader("🛠️ Financial Tool Augmentation")
st.caption(
    "Use specialized financial tools to generate summaries, "
    "budgets, anomaly explanations and multi-step reasoning."
)

tool_col1, tool_col2 = st.columns(2)

with tool_col1:

    if st.button("📋 Generate Financial Summary", width="stretch"):
        try:
            result = financial_summary(analysis_data)
            st.write(result)
        except Exception as e:
            st.error(f"Tool error: {e}")

    if st.button("💰 Generate Budget Plan", width="stretch"):
        try:
            result = generate_budget_plan(analysis_data)
            st.write(result)
        except Exception as e:
            st.error(f"Tool error: {e}")


with tool_col2:

    if st.button("🚨 Explain Anomalies", width="stretch"):
        try:
            result = explain_anomalies(analysis_data)
            st.write(result)
        except Exception as e:
            st.error(f"Tool error: {e}")

    if st.button("🧠 Financial Reasoning", width="stretch"):
        try:
            result = multi_step_financial_reasoning(analysis_data)
            st.write(result)
        except Exception as e:
            st.error(f"Tool error: {e}")

# --------------------------------------------------
# FINANCIAL ADVISOR
# --------------------------------------------------

st.divider()

st.subheader("🤖 Financial AI Advisor")

if st.button(
    "Generate Financial Advisor Report",
    width="stretch",
):

    try:
        advisor = autonomous_financial_advisor(analysis_data)

        st.write(advisor)

    except Exception as e:
        st.error(f"Advisor error: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built with Python • Pandas • NumPy • Scikit-learn • "
    "Streamlit • Flask REST API • Tool Augmentation"
)
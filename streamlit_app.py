import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Add backend directory to Python path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
load_dotenv(BACKEND_DIR / ".env")

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from data_loader import load_expense_data
from preprocessing import preprocess_data
from analysis import total_spending, category_spending, monthly_spending
from prediction import predict_next_month_expense
from anomaly_detection import detect_anomalies
from insights import generate_insights
from nlp_engine import (
    train_expense_classifier, predict_expense_category,
    process_financial_query, semantic_transaction_search,
)
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
# NLP INTELLIGENCE MODULE
# --------------------------------------------------

st.divider()
st.header("🧠 NLP Intelligence")
st.caption(
    "Traditional NLP classification, intent detection, entity extraction, "
    "and embedding-based transaction search."
)

nlp_tab1, nlp_tab2, nlp_tab3 = st.tabs([
    "Expense Classifier", "Natural Language Assistant", "Semantic Search"
])

with nlp_tab1:
    st.markdown("#### Transaction description classification")
    if "description" not in df.columns:
        st.warning(
            "This dataset has no Description column. Upload data with transaction "
            "descriptions to use the NLP classifier."
        )
    else:
        st.caption(
            "The uploaded Category column provides training labels. The model uses "
            "TF-IDF features and Logistic Regression."
        )
        with st.form("nlp_classifier_form"):
            transaction_text = st.text_input(
                "Enter a transaction description",
                placeholder="e.g. Uber ride to office",
            )
            classify_clicked = st.form_submit_button("Classify transaction")
        if classify_clicked:
            try:
                with st.spinner("Training the lightweight text classifier..."):
                    classifier_bundle = train_expense_classifier(df)
                    prediction_result = predict_expense_category(
                        classifier_bundle, transaction_text
                    )
                st.success(f"Predicted category: **{prediction_result['category']}**")
                if prediction_result["confidence"] is not None:
                    st.metric("Model confidence", f"{prediction_result['confidence']:.1%}")
                st.caption(
                    f"Trained on {classifier_bundle['training_samples']} labelled transactions. "
                    "Confidence is a model score, not a guarantee."
                )
                if classifier_bundle["metrics"]:
                    metrics = classifier_bundle["metrics"]
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Holdout accuracy", f"{metrics['accuracy']:.1%}")
                    m2.metric("Precision (weighted)", f"{metrics['precision_weighted']:.1%}")
                    m3.metric("Recall (weighted)", f"{metrics['recall_weighted']:.1%}")
                    m4.metric("F1 (weighted)", f"{metrics['f1_weighted']:.1%}")
                    st.caption(
                        f"Holdout evaluation: {metrics['test_samples']} rows. "
                        "Small or imbalanced datasets can produce unstable metrics."
                    )
                else:
                    st.info("Not enough examples per category for a reliable holdout evaluation.")
            except Exception as exc:
                st.error(f"Classifier could not run: {exc}")

with nlp_tab2:
    st.markdown("#### Ask questions in natural language")
    st.caption(
        "A lightweight intent router extracts entities and calls deterministic Python analytics. "
        "Gemini remains the optional fallback for questions outside the supported intents."
    )
    if "nlp_chat_history" not in st.session_state:
        st.session_state.nlp_chat_history = []
    for item in st.session_state.nlp_chat_history:
        with st.chat_message(item["role"]):
            st.write(item["content"])
    with st.form("nlp_query_form", clear_on_submit=True):
        nlp_question = st.text_input(
            "Your question",
            placeholder="How much did I spend on Food?",
        )
        ask_clicked = st.form_submit_button("Ask")
    if ask_clicked and nlp_question.strip():
        routed = process_financial_query(nlp_question, df, analysis_data)
        answer = routed["answer"]
        if answer is None:
            if os.getenv("GEMINI_API_KEY"):
                try:
                    from llm import ask_llm
                    answer = ask_llm(nlp_question, analysis_data)
                except Exception as exc:
                    answer = f"Gemini fallback unavailable: {exc}"
            else:
                answer = (
                    "I couldn't map that question to a supported financial intent. "
                    "Try asking for a summary, category spending, forecast, anomalies, "
                    "monthly trend, or matching transactions."
                )
        st.session_state.nlp_chat_history.append({"role": "user", "content": nlp_question})
        st.session_state.nlp_chat_history.append({"role": "assistant", "content": answer})
        st.rerun()
    if st.session_state.nlp_chat_history:
        last_user = next((x["content"] for x in reversed(st.session_state.nlp_chat_history) if x["role"] == "user"), "")
        if last_user:
            routed = process_financial_query(last_user, df, analysis_data)
            with st.expander("Inspect NLP interpretation"):
                st.write("**Detected intent:**", routed["intent"])
                st.json(routed["entities"])

with nlp_tab3:
    st.markdown("#### Search transactions by meaning")
    st.caption(
        "Uses Gemini embeddings when GEMINI_API_KEY is configured; otherwise it "
        "falls back to TF-IDF cosine similarity."
    )
    if "description" not in df.columns:
        st.warning("Add a Description column to your uploaded data to enable transaction search.")
    else:
        with st.form("semantic_search_form"):
            semantic_query = st.text_input(
                "What kind of transaction are you looking for?",
                placeholder="food delivery, supermarket purchases, travel costs...",
            )
            search_clicked = st.form_submit_button("Search transactions")
        if search_clicked and semantic_query.strip():
            try:
                search_result = semantic_transaction_search(df, semantic_query, top_k=5)
                st.caption(f"Retrieval method: {search_result['method']}")
                if search_result["results"]:
                    result_df = pd.DataFrame(search_result["results"])

                    result_df["similarity"] = result_df["similarity"].map(lambda x: f"{x:.3f}")
                    st.dataframe(result_df, width="stretch", hide_index=True)
                else:
                    st.info("No transaction descriptions were available to search.")
            except Exception as exc:
                st.error(f"Semantic search failed: {exc}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built with Python • Pandas • NumPy • Scikit-learn • "
    "Streamlit • Flask REST API • Tool Augmentation"
)
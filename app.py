import streamlit as st
if "messages" not in st.session_state:
    st.session_state.messages = []

from data_loader import load_expense_data
from preprocessing import preprocess_data
from analysis import total_spending, category_spending, monthly_spending
from insights import generate_insights
from prediction import predict_next_month_expense
from visualizations import plot_category_spending, plot_monthly_spending
from anomaly_detection import detect_anomalies, anomaly_months
from visualizations import plot_monthly_spending_with_anomalies
from export_utils import anomalies_to_csv
from pdf_report import anomalies_to_pdf
from nl_explainer import explain_data

st.set_page_config(
    page_title="AI Financial Expense Analyzer",
    layout="wide"
)

st.title("💰 AI Financial Expense Analyzer")
st.write("Upload your expense CSV/Excel file to analyze spending patterns.")

uploaded_file = st.file_uploader(
    "📂 Upload Expense File (CSV or Excel)",
    type=["csv", "xlsx"]
)

st.info(
    "📌 Supported formats: CSV (.csv) or Excel (.xlsx)\n"
    "Required columns: date, category, amount, description\n"
    "Date format: YYYY-MM-DD"
)
SAMPLE_CSV = """date,category,amount,description
2025-01-02,Food,250,Lunch at restaurant
2025-01-05,Transport,120,Metro ticket
2025-01-07,Shopping,1800,Clothes purchase
2025-01-10,Food,300,Dinner
2025-01-15,Entertainment,500,Movie night
2025-02-03,Food,270,Lunch
2025-02-06,Transport,150,Cab ride
2025-02-10,Shopping,2200,Shoes
2025-02-15,Entertainment,700,Concert
2025-02-20,Bills,3500,Electricity bill
"""

st.download_button(
    label="⬇️ Download Sample CSV",
    data=SAMPLE_CSV,
    file_name="sample_expenses.csv",
    mime="text/csv"
)



if uploaded_file is not None:
        st.subheader("⚙️ Anomaly Detection Settings")

        sensitivity = st.slider(
            "Anomaly Sensitivity",
            min_value=0.05,
            max_value=0.30,
            value=0.10,
            step=0.05,
            help="Higher value detects more unusual expenses"
        )

        st.caption(
            f"🔍 Current sensitivity: {sensitivity} "
            f"({'Strict' if sensitivity <= 0.1 else 'Moderate' if sensitivity <= 0.2 else 'Aggressive'})"
        )

        try:
            df = load_expense_data(uploaded_file)
            df = preprocess_data(df)

            anomalies = detect_anomalies(df, contamination=sensitivity)

            st.success("File uploaded and processed successfully!")

            st.subheader("📄 Data Preview")
            st.dataframe(df)

            st.subheader("📊 Expense Analysis")
            total = total_spending(df)
            st.metric("Total Spending", f"₹{total:,.2f}")

            col1, col2 = st.columns(2)

            with col1:
                st.pyplot(plot_category_spending(category_spending(df)))

            with col2:
                months_with_anomalies = anomaly_months(df, contamination=sensitivity)

                st.pyplot(
                    plot_monthly_spending_with_anomalies(
                        monthly_spending(df),
                        months_with_anomalies
                    )
                )


            st.subheader("🧠 AI Insights")
            for insight in generate_insights(df):
                st.info(insight)

            st.subheader("🔮 Expense Prediction")
            prediction = predict_next_month_expense(df)
            st.success(f"Predicted Next Month Expense: ₹{prediction:,.2f}")

        except Exception as e:
            st.error(f"Error: {e}")

    # ---------- ANOMALY SECTION ----------
        st.subheader("📌 Categories with Unusual Spending")

        if anomalies.empty:
            st.success("No unusual spending detected 🎉")
            st.info("Tip: Large or irregular expenses will appear here.")

        else:
            st.warning("Unusual spending detected:")
            st.bar_chart(anomalies["category"].value_counts())

            st.subheader("⬇️ Download Anomaly Report")

            # CSV download
            csv_data = anomalies_to_csv(anomalies)
            st.download_button(
                label="📥 Download Anomaly Report (CSV)",
                data=csv_data,
                file_name="anomaly_report.csv",
                mime="text/csv"
            )

            # PDF download
            pdf_file = anomalies_to_pdf(anomalies)
            st.download_button(
                label="📄 Download Anomaly Report (PDF)",
                data=pdf_file,
                file_name="anomaly_report.pdf",
                mime="application/pdf"
            )

        
        st.divider()
        st.subheader("💬 Chat with your data")

        if st.button("🧹 Clear Chat", key="clear_chat_btn"):
            st.session_state.messages = []
            st.rerun()

        # Show previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input at the very bottom
        user_prompt = st.chat_input(
            "Ask things like: Explain my data, Where am I spending most, Why anomalies?"
        )

        if user_prompt:
            st.session_state.messages.append({
                "role": "user",
                "content": user_prompt
            })

            with st.chat_message("user"):
                st.markdown(user_prompt)

            explanations = explain_data(df, anomalies, prediction)
            ai_response = "\n".join([f"• {line}" for line in explanations])

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })

            with st.chat_message("assistant"):
                st.markdown(ai_response)
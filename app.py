import streamlit as st

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
st.write("Upload your expense CSV file to analyze spending patterns.")

uploaded_file = st.file_uploader(
    "📂 Upload Expense File (CSV or Excel)",
    type=["csv", "xlsx"]
)

st.info(
    "📌 Supported formats: CSV (.csv) or Excel (.xlsx)\n"
    "Required columns: date, category, amount, description\n"
    "Date format: YYYY-MM-DD"
)
with open("sample_data/expenses.csv", "r") as f:
    st.download_button(
        label="⬇️ Download Sample CSV",
        data=f,
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
                months_with_anomalies = anomaly_months(df)

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

            st.subheader("💬 Ask the AI about your data")

            user_query = st.text_input(
                "Ask a question (e.g. 'Explain my data', 'Where am I spending most?')"
            )
            if user_query:
                explanations = explain_data(df, anomalies, prediction)

                st.markdown("### 🧠 AI Explanation")
                for line in explanations:
                    st.write("•", line)



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

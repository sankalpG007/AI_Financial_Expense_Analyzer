# 💰 AI Financial Expense Analyzer

An end-to-end **AI-powered financial analytics application** that helps users analyze expenses, detect unusual spending patterns, and forecast future expenses — all through an interactive Streamlit dashboard.

This project combines **data analysis, machine learning, anomaly detection, and modern UI/UX** to simulate a real-world fintech analytics tool.

---

## 🚀 Features

### 📊 Expense Analysis
- Total spending overview
- Category-wise expense breakdown
- Monthly spending trends

### 🤖 AI Insights
- Automatically generated insights from spending data
- Highlights dominant expense categories and trends

### 🔮 Expense Forecasting
- Predicts next month’s expenses using:
  - Linear Regression
  - Smoothed (rolling-average) forecasting
- Handles real-world constraints (no negative predictions)

### 🚨 Anomaly Detection (Advanced)
- Detects unusual or suspicious expenses using **Isolation Forest**
- **User-controlled sensitivity slider** to adjust strictness
- Anomalies highlighted directly on charts

### 📈 Visual Intelligence
- Pie charts for category spending
- Time-series charts with anomaly markers
- Category anomaly frequency charts

### 📄 Export Reports
- Download anomaly reports as:
  - **CSV** (for analysis)
  - **PDF** (for stakeholders)

---

## 🛠️ Tech Stack

| Layer | Technologies |
|------|-------------|
| Language | Python |
| UI | Streamlit |
| Data | Pandas, NumPy |
| ML | Scikit-learn (Linear Regression, Isolation Forest) |
| Visualization | Matplotlib |
| Reporting | ReportLab (PDF export) |

---

## 📂 Project Structure
AI_Financial_Expense_Analyzer/
│
├── app.py # Streamlit application
├── data_loader.py # CSV loading & validation
├── preprocessing.py # Data cleaning & processing
├── analysis.py # Core expense analytics
├── insights.py # AI-generated insights
├── prediction.py # Expense forecasting models
├── anomaly_detection.py # ML anomaly detection
├── visualizations.py # Charts & plots
├── export_utils.py # CSV export
├── pdf_report.py # PDF report generation
├── sample_data/
│ └── expenses.csv
├── requirements.txt
└── README.md

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/AI_Financial_Expense_Analyzer.git
cd AI_Financial_Expense_Analyzer

python -m venv venv
venv\Scripts\activate   # Windows

Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run app.py
Future Improvements
Cloud deployment (Streamlit Cloud / AWS)
User authentication
Database-backed expense storage
Category-level forecasting
LLM-powered natural language financial advice

👨‍💻 Author
Sankalp Satendra Singh
MCA (AI/ML) | Data Analytics Intern
Interested in AI, ML, Data Science, and FinTech

#Why This Project Matters
This project demonstrates:
Real-world ML problem solving
Explainable AI decisions
Strong data storytelling
End-to-end product thinking

#HOW TO DESCRIBE THIS ON RESUME (BONUS)

AI Financial Expense Analyzer
Built an end-to-end financial analytics dashboard using Python, Streamlit, and ML. Implemented anomaly detection with Isolation Forest, interactive sensitivity tuning, expense forecasting, and automated CSV/PDF reporting.


# 💰 AI Financial Expense Analyzer

An AI-powered financial analytics platform that analyzes expense data, detects unusual transactions, forecasts future spending, generates financial insights, and provides AI-assisted financial recommendations.

## 🚀 Features

- 📂 Upload CSV and Excel expense files
- 🧹 Automated data loading and preprocessing
- 📊 Category-wise spending analysis
- 📈 Monthly spending trend analysis
- 🤖 Expense forecasting using Scikit-learn
- 🚨 Anomaly detection using Isolation Forest
- 💡 Automated financial insights
- 🧠 Rule-based financial tools and reasoning
- 🤖 Gemini-powered financial assistant
- 🧠 NLP expense classification using TF-IDF + Logistic Regression
- 🧭 Natural-language intent detection and financial entity extraction
- 🔎 Transaction similarity search using Gemini embeddings with TF-IDF fallback
- 💬 Conversational REST API
- 🌐 Flask REST API
- 📊 Interactive Streamlit dashboard
- 🎯 Financial goal and budget support

## 🏗️ Architecture

```text
                 AI Financial Expense Analyzer
                            │
             ┌──────────────┴──────────────┐
             │                             │
       Streamlit UI                  Flask REST API
             │                             │
             └──────────────┬──────────────┘
                            ↓
                   Reusable Python Modules
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
      Analytics          ML Models         Tool Layer
          │                 │                 │
    Pandas / NumPy    Linear Regression   Financial Tools
                      Isolation Forest    Reasoning Engine
                                                │
                                                ↓
                                           Gemini LLM

                     NLP Intelligence Layer
             ┌──────────────┼────────────────┐
             ↓              ↓                ↓
       TF-IDF Classifier  Intent + NER   Gemini Embeddings
       Logistic Regression  Patterns     Cosine Similarity

🧠 AI & Machine Learning
Expense Forecasting

Uses Scikit-learn LinearRegression to estimate the next month's spending based on historical monthly expense data.

Anomaly Detection

Uses Scikit-learn IsolationForest to identify unusual transactions based on transaction amounts.

Gemini Financial Assistant

Gemini is used to generate natural-language financial assistance using structured financial analysis as context.

### NLP Intelligence

- **Expense classification:** TF-IDF (unigrams + bigrams) converts transaction descriptions into text features; Logistic Regression predicts the category. The uploaded `category` column is used as the training label.
- **Intent detection:** A lightweight, explainable intent router identifies requests such as spending summary, category spending, forecast, anomaly search, monthly trend, and semantic transaction search.
- **Entity extraction:** Pattern- and dictionary-based extraction identifies amounts, category names, time periods, and merchant phrases. This is lightweight rule-based extraction, not a trained NER model.
- **Semantic transaction search:** The system requests text embeddings from Gemini (`gemini-embedding-001`) and ranks transaction descriptions with cosine similarity. If the Gemini embedding service or API key is unavailable, it falls back to TF-IDF cosine similarity; the UI reports which method was used.
- **Gemini fallback:** Questions outside the supported deterministic intents can be passed to the existing Gemini assistant when `GEMINI_API_KEY` is configured.

The classifier learns from the uploaded file, so useful predictions require a `description` column and meaningful labelled examples in `category`. The included sample data is small and intended for demonstration. Holdout metrics are shown when the class distribution permits evaluation; do not treat metrics from a small sample as production performance.

The system also contains deterministic rule-based tools for:

Financial summaries
Budget recommendations
Anomaly explanations
Financial reasoning
Financial advisor recommendations
🔧 Technology Stack
Backend
Python
Flask
Flask-CORS
Pandas
NumPy
Scikit-learn
OpenPyXL
AI
Google Gemini API
Scikit-learn
Rule-based financial tools
Frontend
Streamlit
HTML
CSS
JavaScript
Chart.js
Deployment Support
Gunicorn
Render configuration
📁 Project Structure
AI_Financial_Expense_Analyzer/
│
├── backend/
│   ├── agent.py
│   ├── analysis.py
│   ├── anomaly_detection.py
│   ├── app.py
│   ├── data_loader.py
│   ├── goal_manager.py
│   ├── insights.py
│   ├── llm.py
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── tools.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── render.yaml
│   └── templates/
│
├── sample_data/
│   └── expenses.csv
│
├── streamlit_app.py
├── .gitignore
└── readme.md
⚙️ Installation

Clone the repository:

git clone https://github.com/sankalpG007/AI_Financial_Expense_Analyzer.git
cd AI_Financial_Expense_Analyzer

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r backend/requirements.txt
🔑 Gemini API Configuration

Create a .env file inside the backend directory:

GEMINI_API_KEY=your_api_key_here

Never commit the .env file to Git.

▶️ Run the Streamlit Dashboard

From the project root:

streamlit run streamlit_app.py

The dashboard will be available locally at:

http://localhost:8501

Upload a CSV or Excel expense file and use the dashboard to view:

Spending KPIs
Category analysis
Monthly trends
Anomalies
Financial insights
Budget recommendations
Financial reasoning
AI financial advice
🌐 Run the Flask REST API

From the project root:

python backend/app.py

The API will run locally at:

http://127.0.0.1:5000
Analyze Expenses
POST /analyze

Upload an expense file using the file field.

Example:

curl -X POST \
  -F "file=@sample_data/expenses.csv" \
  http://127.0.0.1:5000/analyze
Financial Assistant
POST /chat

NLP endpoints (upload a file through `/analyze` first):

Classify a transaction description:

```bash
curl -X POST http://127.0.0.1:5000/nlp/classify \
  -H "Content-Type: application/json" \
  -d '{"description":"Uber ride to office"}'
```

Understand a financial question:

```bash
curl -X POST http://127.0.0.1:5000/nlp/query \
  -H "Content-Type: application/json" \
  -d '{"message":"How much did I spend on Food last month?"}'
```

Search transaction descriptions:

```bash
curl -X POST http://127.0.0.1:5000/nlp/search \
  -H "Content-Type: application/json" \
  -d '{"query":"food delivery and restaurant expenses"}'
```

Example:

curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"What is my highest spending category?\"}" \
  http://127.0.0.1:5000/chat
📊 Supported Expense Data

The application can process CSV and Excel files containing fields representing:

Date
Amount
Category
Description (recommended for NLP classification and transaction search)

The data loader performs flexible column detection and preprocessing before analysis. Description columns can be named Description, Transaction Description, Narration, Details or Note.

🔄 Processing Workflow
Upload Expense File
        ↓
Data Loading
        ↓
Data Preprocessing
        ↓
Analytics
        ↓
┌───────────────────────────────┐
│ Category Analysis             │
│ Monthly Spending              │
│ Expense Forecasting            │
│ Anomaly Detection              │
└───────────────────────────────┘
        ↓
Financial Insights
        ↓
Tool Augmentation
        ↓
Gemini Financial Assistant
🎯 Project Highlights

This project demonstrates practical implementation of:

Python-based data processing
Machine learning pipelines
REST API development
Interactive data applications
Tool-based financial analysis
LLM API integration
Structured AI reasoning
CSV and Excel data ingestion
Modular backend architecture
⚠️ Notes

Forecasting performance depends on the amount and quality of historical expense data provided. The included sample dataset is intended for demonstrating the application's workflow rather than benchmarking model accuracy.

👨‍💻 Author

Sankalp Singh

AI/ML Developer | Python | Machine Learning | Applied AI Systems


from tools import autonomous_financial_advisor
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import os
from llm import ask_llm
from tools import multi_step_financial_reasoning
from data_loader import load_expense_data
from preprocessing import preprocess_data
from analysis import total_spending, category_spending, monthly_spending
from prediction import predict_next_month_expense
from anomaly_detection import detect_anomalies
from insights import generate_insights
from flask_cors import CORS
from tools import (
    generate_budget_plan,
    explain_anomalies,
    financial_summary
)
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Add this global variable here
latest_analysis = {}
chat_memory = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    
    global chat_memory
    global latest_analysis

    data = request.json

    user_message = data.get(
        "message",
        ""
    ).lower()

    # ---------------------------
    # SAVE USER MESSAGE
    # ---------------------------

    chat_memory.append({
        "role": "user",
        "message": user_message
    })

    response_text = ""

    # ---------------------------
    # NO DATA YET
    # ---------------------------

    if not latest_analysis:
        from agent import agent_router

        agent_reply = agent_router(
            user_message,
            latest_analysis
        )

        if agent_reply:

            response_text = agent_reply

        response_text = (
            "Please upload an expense file first."
        )

    # ---------------------------
    # EXPLAIN CHART
    # ---------------------------

    elif response_text == "" and (
        "chart" in user_message
        or "graph" in user_message
        or "trend" in user_message
    ):

        highest_category = max(
            latest_analysis["category_spending"],
            key=latest_analysis[
                "category_spending"
            ].get
        )

        response_text = (
            f"The charts show that your highest "
            f"spending category is "
            f"{highest_category}. "
            f"Your monthly spending trend also "
            f"shows changes across months."
        )

    # ---------------------------
    # HIGHEST SPENDING
    # ---------------------------

    elif response_text == "" and (
        "highest" in user_message
        or "most spending" in user_message
    ):

        highest_category = max(
            latest_analysis["category_spending"],
            key=latest_analysis[
                "category_spending"
            ].get
        )

        amount = latest_analysis[
            "category_spending"
        ][highest_category]

        response_text = (
            f"Your highest spending category "
            f"is {highest_category} "
            f"with ₹{amount:.2f} spent."
        )

    # ---------------------------
    # PREDICTION
    # ---------------------------

    elif response_text == "" and (
        "prediction" in user_message
        or "future" in user_message
        or "next month" in user_message
    ):

        response_text = (
            f"Your predicted next month expense "
            f"is ₹{latest_analysis['prediction']:.2f}."
        )

    # ---------------------------
    # SAVE MONEY
    # ---------------------------

   

    # ---------------------------
    # ANOMALIES
    # ---------------------------

    elif response_text == "" and (
        "anomaly" in user_message
        or "unusual" in user_message
    ):

        response_text = (
            f"I detected "
            f"{latest_analysis['anomaly_count']} "
            f"unusual transactions in your data."
        )

    # ---------------------------
    # GREETING
    # ---------------------------

    elif response_text == "" and (
        "hi" in user_message
        or "hello" in user_message
    ):

        response_text = (
            "Hello 👋 I am your AI Financial Assistant. "
            "Ask me about your expenses, trends, "
            "predictions, or savings."
        )

        # ---------------------------
    # FINANCIAL SUMMARY TOOL
    # ---------------------------

    elif response_text == "" and (
        "summary" in user_message
        or "report" in user_message
        or "overview" in user_message
    ):

        response_text = financial_summary(
            latest_analysis
        )

    # ---------------------------
    # BUDGET TOOL
    # ---------------------------

    elif response_text == "" and (
        "budget" in user_message
        or "saving plan" in user_message
        or "financial plan" in user_message
    ):

        response_text = generate_budget_plan(
            latest_analysis
        )

    # ---------------------------
    # ANOMALY TOOL
    # ---------------------------

    elif response_text == "" and (
        "anomaly" in user_message
        or "unusual" in user_message
        or "fraud" in user_message
    ):

        response_text = explain_anomalies(
            latest_analysis
        )


    # ---------------------------
    # REAL LLM RESPONSE
    # ---------------------------

    if response_text == "":

        try:

            response_text = ask_llm(
                user_message,
                latest_analysis
            )

        except Exception as e:

            print("LLM ERROR:", str(e))

            response_text = (
                f"AI Error: {str(e)}"
            )

    # ---------------------------
    # SAVE AI RESPONSE
    # ---------------------------

    chat_memory.append({
        "role": "assistant",
        "message": response_text
    })

    return jsonify({
        "response": response_text,
        "memory_size": len(chat_memory)
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        print("Request received")
        
        file = request.files["file"]
        print("Filename:", file.filename)
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        print("File saved:", filepath)
        
        # -------------------------
        # LOAD DATA
        # -------------------------
        df = load_expense_data(filepath)
        print("Data loaded")
        
        df = preprocess_data(df)
        print("Data preprocessed")
        
        # -------------------------
        # ANALYSIS
        # -------------------------
        total = total_spending(df)
        print("Total calculated")
        
        # CATEGORY
        category_series = category_spending(df)
        category_data = {
            str(k): float(v)
            for k, v in category_series.items()
        }
        
        # MONTHLY
        monthly_series = monthly_spending(df)
        monthly_data = {
            str(k): float(v)
            for k, v in monthly_series.items()
        }
        
        # PREDICTION
        prediction = predict_next_month_expense(df)
        print("Prediction completed")
        
        # ANOMALIES
        anomalies = detect_anomalies(df)
        print("Anomalies detected")
        
        # INSIGHTS
        insights = generate_insights(df)
        print("Insights generated")
        
        agent_advice = autonomous_financial_advisor({
            "category_spending": category_data,
            "total_spending": total,
            "prediction": prediction,
            "anomaly_count": len(anomalies)
        })

        reasoning_output = multi_step_financial_reasoning({
            "category_spending": category_data,
            "total_spending": total,
            "prediction": prediction,
            "anomaly_count": len(anomalies)
        })

        # -------------------------
        # FINAL RESPONSE
        # -------------------------
        response = {
            "total_spending": float(total),
            "category_spending": category_data,
            "monthly_spending": monthly_data,
            "agent_advice": agent_advice,
            "reasoning": reasoning_output,
            "prediction": (
                0 if prediction != prediction
                else float(prediction)
            ),
            "insights": [str(i) for i in insights],
            "anomaly_count": int(len(anomalies))
        }
        
        print(response)
        
        # Add this to update the global latest_analysis
        global latest_analysis
        latest_analysis = response
        
        return jsonify(response)
        
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
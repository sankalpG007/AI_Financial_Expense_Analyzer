from urllib import response

from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import os

from data_loader import load_expense_data
from preprocessing import preprocess_data
from analysis import total_spending, category_spending, monthly_spending
from prediction import predict_next_month_expense
from anomaly_detection import detect_anomalies
from insights import generate_insights
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        print("Request received")

        file = request.files["file"]

        print("Filename:", file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

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

        # -------------------------
        # FINAL RESPONSE
        # -------------------------

        response = {

            "total_spending": float(total),

            "category_spending": category_data,

            "monthly_spending": monthly_data,

            "prediction": (
                0 if prediction != prediction
                else float(prediction)
            ),

            "insights": [str(i) for i in insights],

            "anomaly_count": int(len(anomalies))
        }

        print(response)

        return jsonify(response)

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True)
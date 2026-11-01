"""Lightweight NLP features for the AI Financial Expense Analyzer.

Traditional NLP: TF-IDF + Logistic Regression for expense classification.
Query understanding: intent rules + lightweight entity extraction.
Embeddings: Gemini text embeddings when configured, with TF-IDF similarity fallback.
"""

import os
import re
from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def _clean_text(value):
    text = str(value or "").lower().strip()
    text = re.sub(r"[^a-z0-9₹.\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def train_expense_classifier(df):
    """Train a TF-IDF + Logistic Regression classifier from labelled transactions.

    The uploaded dataset's category column acts as the training label. Metrics are
    calculated on a holdout split when the dataset has enough examples per class.
    The final model is then fitted on all labelled rows for prediction.
    """
    if "description" not in df.columns:
        raise ValueError(
            "Your file needs a Description column to train the NLP classifier. "
            "Add transaction descriptions such as 'Uber ride' or 'grocery store'."
        )
    if "category" not in df.columns:
        raise ValueError("A Category column is required as the classifier's training label.")

    data = df[["description", "category"]].copy()
    data["description"] = data["description"].fillna("").map(_clean_text)
    data["category"] = data["category"].fillna("").astype(str).str.strip()
    data = data[(data["description"] != "") & (data["category"] != "")]

    if data["category"].nunique() < 2 or len(data) < 6:
        raise ValueError("At least 6 labelled descriptions across 2 or more categories are needed.")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True,
            stop_words="english",
        )),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])

    # Evaluate only when every evaluated class has at least two examples.
    counts = data["category"].value_counts()
    evaluable = data[data["category"].isin(counts[counts >= 2].index)]
    metrics = None
    if evaluable["category"].nunique() >= 2 and len(evaluable) >= 10:
        try:
            x_train, x_test, y_train, y_test = train_test_split(
                evaluable["description"],
                evaluable["category"],
                test_size=0.25,
                random_state=42,
                stratify=evaluable["category"],
            )
            evaluation_model = Pipeline([
                ("tfidf", TfidfVectorizer(
                    ngram_range=(1, 2), max_features=5000,
                    sublinear_tf=True, stop_words="english",
                )),
                ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
            ])
            evaluation_model.fit(x_train, y_train)
            predictions = evaluation_model.predict(x_test)
            metrics = {
                "accuracy": float(accuracy_score(y_test, predictions)),
                "precision_weighted": float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
                "recall_weighted": float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
                "f1_weighted": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
                "test_samples": int(len(y_test)),
            }
        except ValueError:
            # Very small/imbalanced datasets may not support a reliable holdout split.
            metrics = None

    pipeline.fit(data["description"], data["category"])
    return {
        "model": pipeline,
        "metrics": metrics,
        "training_samples": int(len(data)),
        "categories": sorted(data["category"].unique().tolist()),
    }


def predict_expense_category(model_bundle, description):
    text = _clean_text(description)
    if not text:
        raise ValueError("Enter a transaction description first.")
    model = model_bundle["model"]
    category = str(model.predict([text])[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(model.predict_proba([text]).max())
    return {"category": category, "confidence": confidence}


def extract_entities(message, categories=None):
    """Extract useful financial entities using lightweight patterns and dictionaries."""
    original = str(message or "")
    lowered = original.lower()
    entities = {"amount": None, "category": None, "period": None, "merchant": None}

    amount_match = re.search(r"(?:₹|rs\.?\s*|inr\s*)(\d+(?:,\d{3})*(?:\.\d{1,2})?)", lowered)
    if amount_match:
        entities["amount"] = float(amount_match.group(1).replace(",", ""))

    category_values = list(categories) if categories is not None else []
    for category in sorted(category_values, key=len, reverse=True):
        if re.search(r"\b" + re.escape(str(category).lower()) + r"\b", lowered):
            entities["category"] = str(category)
            break

    period_patterns = [
        (r"\b(last month|previous month)\b", "last_month"),
        (r"\b(this month|current month)\b", "this_month"),
        (r"\b(last week|previous week)\b", "last_week"),
        (r"\b(this week|current week)\b", "this_week"),
    ]
    for pattern, value in period_patterns:
        if re.search(pattern, lowered):
            entities["period"] = value
            break
    if entities["period"] is None:
        month_names = "january february march april may june july august september october november december".split()
        for month in month_names:
            if re.search(r"\b" + month + r"\b", lowered):
                entities["period"] = month
                break

    merchant_match = re.search(r"\b(?:at|from|merchant)\s+([a-z][a-z0-9&' -]{1,35})", lowered)
    if merchant_match:
        entities["merchant"] = merchant_match.group(1).strip(" .?!")

    return entities


def detect_intent(message, categories=None):
    """Classify common finance questions into a small, explainable intent set."""
    text = _clean_text(message)
    if any(term in text for term in ("hello", "hi", "hey")) and len(text.split()) <= 3:
        return "greeting"
    if any(term in text for term in ("similar transaction", "find transaction", "search transaction", "delivery expense", "merchant", "payment at", "transactions matching")) or ("find" in text and "transaction" in text):
        return "semantic_search"
    if any(term in text for term in ("anomaly", "anomalies", "unusual", "suspicious", "irregular")):
        return "anomaly_search"
    if any(term in text for term in ("predict", "forecast", "next month", "future spending")):
        return "expense_prediction"
    if any(term in text for term in ("highest", "most spending", "top category", "spent the most")):
        return "highest_category"
    if any(term in text for term in ("compare", "monthly trend", "month by month", "spending trend")):
        return "monthly_trend"
    if any(term in text for term in ("how much", "spending on", "spent on", "category")):
        return "category_spending"
    category_values = list(categories) if categories is not None else []
    if any(str(category).lower() in text for category in category_values) and any(term in text for term in ("spend", "expense", "cost", "paid")):
        return "category_spending"
    if any(term in text for term in ("summary", "overview", "total spending", "total expense", "report")):
        return "spending_summary"
    return "unknown"


def _gemini_embeddings(texts):
    """Return Gemini embeddings, or None if credentials/service are unavailable."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts,
        )
        vectors = [item.values for item in response.embeddings]
        return vectors
    except Exception as exc:
        print("Gemini embedding unavailable; using TF-IDF fallback:", exc)
        return None


def semantic_transaction_search(df, query, top_k=5):
    """Search descriptions by meaning using Gemini embeddings when available.

    If Gemini embeddings cannot be reached, a TF-IDF cosine-similarity fallback is
    used. The response states which retrieval method actually ran.
    """
    if "description" not in df.columns:
        raise ValueError("The uploaded data needs a Description column for transaction search.")
    descriptions = df["description"].fillna("").astype(str).tolist()
    valid = [(i, value.strip()) for i, value in enumerate(descriptions) if value.strip()]
    if not valid:
        return {"method": "none", "results": []}

    indices, texts = zip(*valid)
    vectors = _gemini_embeddings([str(query)] + list(texts))
    if vectors is not None and len(vectors) == len(texts) + 1:
        scores = cosine_similarity([vectors[0]], vectors[1:])[0]
        method = "Gemini embeddings + cosine similarity"
    else:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = vectorizer.fit_transform(list(texts) + [str(query)])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        method = "TF-IDF cosine similarity fallback"

    ranked = sorted(zip(indices, scores), key=lambda item: item[1], reverse=True)[:max(1, int(top_k))]
    results = []
    for index, score in ranked:
        row = df.iloc[index]
        results.append({
            "date": str(row.get("date", "")),
            "description": str(row.get("description", "")),
            "category": str(row.get("category", "Other")),
            "amount": float(row.get("amount", 0)),
            "similarity": float(score),
        })
    return {"method": method, "results": results}


def process_financial_query(message, df, analysis_data):
    """Run intent/entity extraction and route common requests to Python analytics."""
    categories = df["category"].dropna().astype(str).unique().tolist() if "category" in df else []
    intent = detect_intent(message, categories)
    entities = extract_entities(message, categories)
    category_data = analysis_data.get("category_spending", {})

    if intent == "greeting":
        answer = "Hello! Ask me about spending summaries, categories, forecasts, anomalies or matching transactions."
    elif intent == "spending_summary":
        answer = (
            f"Total spending: ₹{analysis_data.get('total_spending', 0):,.2f}\n"
            f"Transactions: {len(df):,}\n"
            f"Predicted next-month spending: ₹{analysis_data.get('prediction', 0):,.2f}\n"
            f"Unusual transactions: {analysis_data.get('anomaly_count', 0)}"
        )
    elif intent == "highest_category":
        if category_data:
            category = max(category_data, key=category_data.get)
            answer = f"Your highest spending category is {category}: ₹{category_data[category]:,.2f}."
        else:
            answer = "There is no category spending data available yet."
    elif intent == "category_spending":
        category = entities.get("category")
        if category and category in category_data:
            filtered = df.copy()
            period = entities.get("period")
            if period and "date" in filtered.columns:
                dates = pd.to_datetime(filtered["date"], errors="coerce")
                if period in ("last_month", "this_month") and dates.notna().any():
                    reference_month = dates.max().to_period("M")
                    target_month = reference_month - 1 if period == "last_month" else reference_month
                    filtered = filtered[dates.dt.to_period("M") == target_month]
                elif period in ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"):
                    month_number = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"].index(period) + 1
                    filtered = filtered[dates.dt.month == month_number]
            category_rows = filtered[filtered["category"].astype(str).str.lower() == category.lower()]
            amount = float(category_rows["amount"].sum())
            period_label = f" during {entities['period'].replace('_', ' ')}" if entities.get("period") else ""
            answer = f"Your spending on {category}{period_label} is ₹{amount:,.2f} across {len(category_rows)} transactions."
        else:
            answer = "I couldn't identify a category. Try asking about one of: " + ", ".join(categories)
    elif intent == "expense_prediction":
        answer = f"Your estimated next-month spending is ₹{analysis_data.get('prediction', 0):,.2f}. This is a model-based estimate, not a guarantee."
    elif intent == "anomaly_search":
        answer = f"The existing Isolation Forest model flagged {analysis_data.get('anomaly_count', 0)} potentially unusual transactions for review."
    elif intent == "monthly_trend":
        monthly = df.assign(month=pd.to_datetime(df["date"]).dt.to_period("M").astype(str)).groupby("month")["amount"].sum().sort_index()
        if len(monthly) >= 2:
            answer = "Monthly spending (latest months):\n" + "\n".join(f"{month}: ₹{amount:,.2f}" for month, amount in monthly.tail(6).items())
        elif len(monthly) == 1:
            answer = f"Only one month is present: {monthly.index[0]} — ₹{monthly.iloc[0]:,.2f}. More history is needed for comparison."
        else:
            answer = "No monthly transaction history is available."
    elif intent == "semantic_search":
        search = semantic_transaction_search(df, message, top_k=5)
        if search["results"]:
            answer = f"Matching transactions ({search['method']}):\n" + "\n".join(
                f"{r['date']} | {r['description']} | {r['category']} | ₹{r['amount']:,.2f}"
                for r in search["results"]
            )
        else:
            answer = "I couldn't find transaction descriptions to search."
    else:
        answer = None

    return {
        "intent": intent,
        "entities": entities,
        "answer": answer,
    }

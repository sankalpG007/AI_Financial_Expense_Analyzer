from dotenv import load_dotenv
from pathlib import Path
import os
from google import genai

# Load the backend-local .env file regardless of the directory used to launch Flask.
load_dotenv(Path(__file__).resolve().parent / ".env")


def ask_llm(user_message, analysis_data):
    """Use Gemini for a short natural-language explanation when configured."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "Gemini is not configured. Add GEMINI_API_KEY to backend/.env. "
            "The deterministic NLP intents and Python financial tools are still available."
        )

    highest_category = "Unknown"
    if analysis_data.get("category_spending"):
        highest_category = max(
            analysis_data["category_spending"],
            key=analysis_data["category_spending"].get,
        )

    prompt = f"""
You are a careful financial analysis assistant. Use only the supplied data.
Do not invent transactions, totals, or financial facts. Keep the answer under 100 words.

Total Spending: ₹{analysis_data.get('total_spending', 0)}
Predicted Next Month Spending: ₹{analysis_data.get('prediction', 0)}
Highest Spending Category: {highest_category}
Potentially Unusual Transactions: {analysis_data.get('anomaly_count', 0)}

User Question: {user_message}
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text or "Gemini returned an empty response."
    except Exception as exc:
        print("LLM ERROR:", exc)
        return (
            "AI Assistant temporarily unavailable. "
            + analysis_data.get("agent_advice", "No additional financial advice available.")
        )

def get_gemini_api_key():
    api_key = get_gemini_api_key()

    if api_key:
        return api_key

    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

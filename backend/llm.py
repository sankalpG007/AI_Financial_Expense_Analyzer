from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("LLM LOADED SUCCESSFULLY")

def ask_llm(user_message, analysis_data):

    highest_category = "Unknown"

    if analysis_data.get("category_spending"):
        highest_category = max(
            analysis_data["category_spending"],
            key=analysis_data["category_spending"].get
        )

    prompt = f"""
    You are a professional financial advisor.

    Total Spending:
    ₹{analysis_data.get('total_spending',0)}

    Prediction:
    ₹{analysis_data.get('prediction',0)}

    Highest Category:
    {highest_category}

    User Question:
    {user_message}

    Answer in less than 100 words.
    """

    try:

        print("ASK_LLM CALLED")
        print("QUESTION:", user_message)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("LLM RESPONSE:")
        print(response.text)

        return response.text

    except Exception as e:

        print("LLM ERROR:", e)

        return (
            "⚠️ AI Assistant temporarily unavailable.\n\n"
            + analysis_data.get(
                "agent_advice",
                "No financial advice available."
            )
        )
from llm import ask_llm

analysis_data = {
    "total_spending": 10000,
    "prediction": 12000,
    "category_spending": {
        "Shopping": 5000
    },
    "agent_advice": "Reduce shopping expenses"
}

print(
    ask_llm(
        "How can I improve my finances?",
        analysis_data
    )
)
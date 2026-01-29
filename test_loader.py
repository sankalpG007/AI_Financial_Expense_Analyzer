from data_loader import load_expense_data
from preprocessing import preprocess_data
from prediction import predict_next_month_expense

df = load_expense_data("sample_data/expenses.csv")
df = preprocess_data(df)

prediction = predict_next_month_expense(df)
print("PREDICTED NEXT MONTH EXPENSE:", prediction)

from data_loader import load_expense_data
from preprocessing import preprocess_data
from anomaly_detection import detect_anomalies

df = load_expense_data("sample_data/expenses.csv")
df = preprocess_data(df)

anomalies = detect_anomalies(df)

print("ANOMALOUS EXPENSES:")
print(anomalies)

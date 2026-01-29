from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.1):
    """
    Detect anomalous expenses using Isolation Forest
    contamination controls sensitivity
    """
    df = df.copy()

    X = df[["amount"]]

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(X)

    anomalies = df[df["anomaly"] == -1]
    return anomalies


def anomaly_months(df, contamination=0.1):
    """
    Return months that contain anomalous expenses
    """
    anomalies = detect_anomalies(df, contamination)
    anomalies["month"] = anomalies["date"].dt.to_period("M")
    return set(anomalies["month"])

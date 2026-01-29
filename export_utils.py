import pandas as pd
from io import StringIO


def anomalies_to_csv(anomalies_df):
    """
    Convert anomalies DataFrame to CSV string
    """
    csv_buffer = StringIO()
    anomalies_df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

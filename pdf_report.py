from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def anomalies_to_pdf(anomalies_df):
    """
    Generate PDF report for anomalies
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Anomalous Expense Report")

    c.setFont("Helvetica", 10)
    y = height - 90

    for _, row in anomalies_df.iterrows():
        text = f"{row['date']} | {row['category']} | ₹{row['amount']} | {row['description']}"
        c.drawString(50, y, text)
        y -= 15

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

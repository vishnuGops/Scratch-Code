import yfinance as yf
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


def fetch_stock_data(ticker):
    # Fetch stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    return stock.history(period="100d")


def format_decimal(value, decimals=2):
    return f"{value:.{decimals}f}"


def generate_pdf_report(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a list to hold the flowables (elements) of the document
    elements = []

    # Create a title
    title = Paragraph("Stock Report", styles["Title"])
    elements.append(title)

    # Create a table
    table_data = [['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    for index, row in data.iterrows():
        table_data.append([str(index),
                           format_decimal(row['Open']),
                           format_decimal(row['High']),
                           format_decimal(row['Low']),
                           format_decimal(row['Close']),
                           str(row['Volume'])])  # Keeping volume as integer
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)

    # Build the PDF document
    doc.build(elements)


# Fetch stock data for a specific ticker
ticker = "AAPL"
stock_data = fetch_stock_data(ticker)

# Generate PDF report using the fetched data
generate_pdf_report(stock_data, f"{ticker}_stock_report.pdf")

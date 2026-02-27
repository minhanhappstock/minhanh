import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ====== CẤU HÌNH ======
STOCK_SYMBOL = "FPT"
EMAIL_SENDER = "GMAIL_CUA_BAN"
EMAIL_PASSWORD = "APP_PASSWORD_16_KY_TU"
EMAIL_RECEIVER = "GMAIL_CUA_BAN"
# =======================
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from flask import Flask
import os

app = Flask(__name__)


def get_stock_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=FPT"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]
        return price
    else:
        return None


def send_email(price):
    if price is None:
        return "API error"

    today = datetime.now().strftime("%d-%m-%Y")

    html_content = f"""
    <h2>Báo cáo giá cổ phiếu FPT</h2>
    <p>Ngày: {today}</p>
    <p>Giá hiện tại: <b>{price}</b></p>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = "Báo cáo cổ phiếu FPT"
    msg["From"] = "YOUR_EMAIL@gmail.com"
    msg["To"] = "YOUR_EMAIL@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("YOUR_EMAIL@gmail.com", "YOUR_APP_PASSWORD")
        server.send_message(msg)

    return "Email sent successfully!"


@app.route("/")
def home():
    price = get_stock_price()
    result = send_email(price)
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

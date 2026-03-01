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
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from flask import Flask
import os

app = Flask(__name__)


def get_stock_price():
    url = "https://finance.vietstock.vn/FPT-ctcp-fpt.htm"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.select_one(".price")

    if price_tag:
        return price_tag.text.strip()

    return None


def send_email(price):
    if price is None:
        return "Không lấy được giá"

    today = datetime.now().strftime("%d-%m-%Y")

    html_content = f"""
    <h2>Báo cáo giá cổ phiếu FPT</h2>
    <p>Ngày: {today}</p>
    <p>Giá hiện tại: <b>{price}</b></p>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = "Báo cáo cổ phiếu FPT"
    msg["From"] = "info.lienanh@gmail.com"
    msg["To"] = "info.lienanh@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("info.lienanh@gmail.com", "minhanhapp123")
        server.send_message(msg)

    return "Email sent successfully!"


@app.route("/")
def home():
    price = get_stock_price()
    return send_email(price)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

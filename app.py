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


def get_stock_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=FPT"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]
        return price
    else:
        print("API error")
        return None


def send_email(price):
    if price is None:
        print("No price to send")
        return

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
        server.login("info.lienanh@gmail.com", "minanhapp123")
        server.send_message(msg)


if __name__ == "__main__":
    price = get_stock_price()
    send_email(price)

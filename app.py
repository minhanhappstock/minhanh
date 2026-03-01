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
    try:
        # API miễn phí (demo key)
        url = "https://financialmodelingprep.com/api/v3/quote/FPT.VN?apikey=demo"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Status code:", response.status_code)
            return None

        data = response.json()

        if len(data) > 0:
            return data[0]["price"]

    except Exception as e:
        print("ERROR:", e)

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

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("info.lienanh.com", "minhanhapp123")
            server.send_message(msg)

        return "Email sent successfully!"

    except Exception as e:
        print("Email error:", e)
        return "Lỗi gửi email"


@app.route("/")
def home():
    price = get_stock_price()
    return send_email(price)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

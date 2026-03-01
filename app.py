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
    import requests

    try:
        url = "https://iboard-query.ssi.com.vn/v2/stock/quote"
        params = {
            "symbol": "FPT",
            "page": 1,
            "size": 1
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Status:", response.status_code)
            return None

        data = response.json()

        if data and "data" in data and len(data["data"]) > 0:
            return data["data"][0]["lastPrice"]

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

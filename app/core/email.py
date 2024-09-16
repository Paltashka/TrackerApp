import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(to_email: str, subject: str, body: str):
    try:
        server = smtplib.SMTP(os.getenv("MAIL_SERVER"), os.getenv("MAIL_PORT"))
        if os.getenv("MAIL_TLS"):
            server.starttls()

        server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))

        msg = MIMEText(body, 'html')
        msg['From'] = os.getenv("MAIL_FROM")
        msg['To'] = to_email
        msg['Subject'] = subject

        server.send_message(msg)

        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

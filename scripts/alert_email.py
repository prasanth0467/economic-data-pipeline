import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "majjiprasanthreddy@gmail.com"
APP_PASSWORD = "rfcymhbkclkdouuy"
RECEIVER_EMAIL = "majjiprasanthreddy@gmail.com"


def send_failure_email(step_name, error_message):
    msg = EmailMessage()
    msg["Subject"] = f"❌ Data Pipeline Failed: {step_name}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(f"""
Pipeline step failed.

Step: {step_name}

Error:
{error_message}
""")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

import smtplib
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_NAME


def send_email(to_email, subject, body):
    if not to_email:
        return

    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        # Simulated mode: no real SMTP configured yet. Print instead of failing,
        # so the rest of the app keeps working while you set up credentials.
        print(f"[email:simulated] to={to_email} subject={subject!r}\n{body}\n")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
    except Exception as e:
        print(f"[email:error] failed to send to {to_email}: {e}")

import os
import requests


RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv(
    "EMAIL_FROM",
    "HostelCare <onboarding@resend.dev>"
)


def send_email(to_email, subject, body):
    if not to_email:
        return

    if not RESEND_API_KEY:
        print(
            f"[email:simulated] to={to_email} "
            f"subject={subject!r}\n{body}\n"
        )
        return

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": EMAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "text": body,
            },
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        print(
            f"[email:sent] to={to_email} "
            f"message_id={data.get('id')}"
        )

    except requests.RequestException as e:
        print(f"[email:error] failed to send to {to_email}: {e}")

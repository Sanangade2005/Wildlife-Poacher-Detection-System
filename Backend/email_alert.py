import smtplib
from email.message import EmailMessage
from config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_TO
)

def send_poacher_alert(frame_path, ranger_id, detected_time, reason):
    msg = EmailMessage()
    msg["Subject"] = "🚨 Poacher Detected Alert"
    msg["From"] = EMAIL_USERNAME
    msg["To"] = EMAIL_TO

    msg.set_content(
        f"""
🚨 POACHER DETECTED 🚨

Ranger ID   : {ranger_id}
Time        : {detected_time}
Reason      : {reason}

Immediate action required.
"""
    )

    with open(frame_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="jpeg",
            filename=frame_path.split("/")[-1]
        )

    # ✅ CORRECT WAY FOR PORT 587
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()          # 🔑 THIS IS REQUIRED
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)

# emailer.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content

def send_email(recipient, body_string):
    sender = os.getenv("SENDER_EMAIL")
    api_key = os.getenv("SENDGRID_API_KEY")

    if not sender or not api_key:
        print("❌ Missing environment variables. Check your .env file.")
        return

    subject = "Daily Value: Tennessee News"

    # Use the pre-formatted string directly for plain text
    text_body = body_string

    # Create an HTML version by replacing newline characters with <br> tags
    # This makes it look correct in an HTML email client.
    html_body = body_string.replace("\n\n", "<br><br>").replace("\n", "<br>")

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        plain_text_content=text_body,
        html_content=html_body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Sent to {recipient} (Status: {response.status_code})")

        # Log the send
        with open("send_log.txt", "a", encoding="utf-8") as log:
            log.write(f"Sent to {recipient} | Status: {response.status_code}\n")

    except Exception as e:
        print(f"❌ Error sending to {recipient}: {e}")
# emailer.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(recipient, articles):
    sender = os.getenv("SENDER_EMAIL")
    api_key = os.getenv("SENDGRID_API_KEY")

    if not sender or not api_key:
        print("❌ Missing environment variables. Check your .env file.")
        return

    subject = "Daily Value: Tennessee News"
    body = "Here are today's top Tennessee stories:\n\n"

    for article in articles:
        title = article.get("title", "Untitled")
        summary = article.get("summary", "")
        url = article.get("url", "")
        body += f"{title}\n{summary}\nRead more: {url}\n\n"

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Sent to {recipient} (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error sending to {recipient}: {e}")
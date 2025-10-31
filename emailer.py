# emailer.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(recipient, articles):
    sender = os.getenv("SENDER_EMAIL")  # e.g., dailyvalue.news@gmail.com
    subject = "Daily Value: Tennessee News"
    body = "Here are today's top Tennessee stories:\n\n"

    for article in articles:
        body += f"{article['title']}\n{article['summary']}\nRead more: {article['url']}\n\n"

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"✅ Sent to {recipient} (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error sending to {recipient}: {e}")

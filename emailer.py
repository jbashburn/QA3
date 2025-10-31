# emailer.py

import smtplib
import os

def send_email(recipient, articles):
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_API_KEY")  # App password or email API key

    subject = "Daily Value: Tennessee News"
    body = "Here are today's top Tennessee stories:\n\n"

    for article in articles:
        body += f"{article['title']}\n{article['summary']}\nRead more: {article['url']}\n\n"

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message)
        print(f"✅ Sent to {recipient}")
    except Exception as e:
        print(f"❌ Error sending to {recipient}: {e}")
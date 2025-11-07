# emailer.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime

# --- UPDATE THE FUNCTION DEFINITION ---
def send_email(recipient, articles_list, subject="Daily Value: AI-Powered News Stories"):
    """
    Builds a professional HTML email from the list of articles
    and sends it via SendGrid.
    """
    sender = os.getenv("SENDER_EMAIL")
    api_key = os.getenv("SENDGRID_API_KEY")
    if not sender or not api_key:
        print("❌ Missing environment variables. Check your .env file.")
        return
    
    today_date = datetime.date.today().strftime("%B %d, %Y")

    # --- 1. Build Plain Text Fallback ---
    # Update the header
    text_body = f"Today's Top Business News\n{today_date}\n\n"
    for article in articles_list:
        text_body += f"📰 {article.get('title', 'Untitled')}\n"
        text_body += f"{article.get('summary', 'No summary.')}\n"
        text_body += f"Read more: {article.get('url', '#')}\n\n"
        text_body += "-"*60 + "\n"

    # --- 2. Build Professional HTML Body ---
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center" style="padding: 20px 0;">
                    <table width="600" border="0" cellspacing="0" cellpadding="0" style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                        
                        <tr>
                            <td align="center" style="background-color: #2196F3; color: white; padding: 30px 20px;">
                                <h1 style="margin: 0; font-size: 25px;">Daily Value News</h1>
                                <p style="margin: 5px 0 0; font-size: 16px;">Your AI-Powered Business & Finance Newsletter for {today_date}</p>
                            </td>
                        </tr>

                        """

    for article in articles_list:
        title = article.get('title', 'Untitled')
        summary = article.get('summary', 'No summary.')
        url = article.get('url', '#')

        html_body += f"""
                        <tr>
                            <td style="padding: 30px 20px; border-bottom: 1px solid #eee;">
                                <h2 style="margin: 0 0 10px; font-size: 22px;">
                                    <a href="{url}" style="color: #333; text-decoration: none;">{title}</a>
                                </h2>
                                <p style="margin: 0 0 20px; font-size: 14px; line-height: 1.5; color: #555;">
                                    {summary}
                                </p>
                                <a href="{url}" style="color: #2196F3; text-decoration: none; font-weight: bold; font-size: 16px;">
                                    Read Full Article &rarr;
                                </a>
                            </td>
                        </tr>
        """

    # --- THIS IS THE FIX: Added 'f' to the line below ---
    html_body += f"""
                        <tr>
                            <td align="center" style="background-color: #f9f9f9; color: #777; padding: 20px; font-size: 12px;">
                                <p style="margin: 0;">&copy; {datetime.date.today().year} Daily Value News. All rights reserved.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # --- 3. Create and Send Mail ---
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject, # <-- This now uses the passed-in subject
        plain_text_content=text_body,
        html_content=html_body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Sent to {recipient} (Status: {response.status_code})")

        # --- THIS IS THE TIMESTAMP FIX ---
        # 1. Get the current timestamp
        now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        with open("send_log.txt", "a", encoding="utf-8") as log:
            # 2. Write the new log format
            log.write(f"{now} | Sent to {recipient} | Status: {response.status_code}\n")

    except Exception as e:
        print(f"❌ Error sending to {recipient}: {e}")
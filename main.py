# main.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Securely access API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")  # Optional if using SMTP

# Import your custom modules
import database
import fetch_news
import summarize
import emailer

def generate_newsletter():
    """Returns the formatted newsletter content as a string."""
    articles = fetch_news.get_tennessee_news(NEWS_API_KEY)
    summarized_articles = summarize.summarize_articles(articles, OPENAI_API_KEY)

    # Format the newsletter body
    email_body = ""
    for item in summarized_articles:
        title = item.get("title", "Untitled")
        summary = item.get("summary", "")
        url = item.get("url", "")
        email_body += f"📰 {title}\n\n{summary}\nRead more: {url}\n\n{'-'*60}\n\n"

    return email_body

def run_newsletter():
    # Step 1: Generate newsletter content
    email_body = generate_newsletter()

    # Step 2: Get subscriber emails from the database
    subscribers = database.get_subscribers()

    # Step 3: Send the newsletter to each subscriber
    for email in subscribers:
        emailer.send_email(email, email_body)

    print("✅ Daily Value newsletter sent successfully!")

if __name__ == "__main__":
    run_newsletter()
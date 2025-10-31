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

def run_newsletter():
    # Step 1: Fetch Tennessee news
    articles = fetch_news.get_tennessee_news(NEWS_API_KEY)

    # Step 2: Summarize articles using OpenAI
    summarized_articles = summarize.summarize_articles(articles, OPENAI_API_KEY)

    # Step 3: Get subscriber emails from the database
    subscribers = database.get_subscribers()

    # Step 4: Send the newsletter to each subscriber
    for email in subscribers:
        emailer.send_email(email, summarized_articles)

    print("✅ Daily Value newsletter sent successfully!")

if __name__ == "__main__":
    run_newsletter()

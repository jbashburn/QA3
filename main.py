# main.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Securely access API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Import your custom modules
import database
import fetch_news
import summarize
import emailer

def generate_newsletter():
    """Fetches and summarizes fresh articles every time."""
    articles = fetch_news.get_business_news(NEWS_API_KEY)
    summarized_articles = summarize.summarize_articles(articles, OPENAI_API_KEY)
    return summarized_articles

def run_newsletter():
    articles_list = generate_newsletter()
    if not articles_list:
        print("❌ No articles found. Newsletter not sent.")
        return

    subscribers = database.get_subscribers()
    if not subscribers:
        print("❌ No subscribers found. Newsletter not sent.")
        return

    # --- DEFINE THE SUBJECT ---
    subject = "Today's Top Business News"
    for email in subscribers:
        # --- PASS THE SUBJECT ---
        emailer.send_email(email, articles_list, subject)
    print(f"✅ Business newsletter sent to {len(subscribers)} subscribers!")

if __name__ == "__main__":
    run_newsletter()

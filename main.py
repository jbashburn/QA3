# main.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Securely access API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY") 

# Import your custom modules
import database
import fetch_news
import summarize
import emailer

def generate_newsletter():
    """Fetches and summarizes articles, returning a LIST of dicts."""
    articles = fetch_news.get_tennessee_news(NEWS_API_KEY)
    # This list now contains 'title', 'url', and 'summary'
    summarized_articles = summarize.summarize_articles(articles, OPENAI_API_KEY)
    return summarized_articles # <-- FIX: Return the list directly

def run_newsletter():
    # Step 1: Generate newsletter content (this is now a list)
    articles_list = generate_newsletter()

    if not articles_list:
        print("❌ No articles found. Newsletter not sent.")
        return

    # Step 2: Get subscriber emails from the database
    subscribers = database.get_subscribers()
    if not subscribers:
        print("❌ No subscribers found. Newsletter not sent.")
        return

    # Step 3: Send the newsletter to each subscriber
    # We pass the full list of articles to the emailer
    for email in subscribers:
        emailer.send_email(email, articles_list)

    print(f"✅ Daily Value newsletter sent to {len(subscribers)} subscribers!")

if __name__ == "__main__":
    run_newsletter()
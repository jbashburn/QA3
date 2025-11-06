
# fetch_news.py
import requests
import datetime  # <-- CHANGED from 'time' to 'datetime'
import random    # <-- NEW: for random keyword selection

def get_business_news(api_key):
    """
    Fetches RELEVANT business articles from top-tier domains
    by combining a domain filter with a keyword search and a
    powerful cache-buster.
    """

    # Use the /everything endpoint (it's the only one that supports 'q' and 'domains')
    url = "https://newsapi.org/v2/everything"

    # --- 1. THE DOMAIN FILTER ---
    your_domains = "bloomberg.com,forbes.com,businessinsider.com,economist.com,reuters.com"

    # --- 2. THE QUALITY FILTER ---
    keyword_options = [
        '"business"', '"finance"', '"markets"', '"economy"',
        '"stocks"', '"wall street"', '"entrepreneurship"', '"startups"',
        '"inflation"', '"interest rates"', '"corporate earnings"'
    ]
    your_keywords = random.choice(keyword_options)  # <-- NEW: random keyword each time

    # --- 3. THE REFRESH FIX (Forces new articles) ---
    # This creates a 100% unique string every time.
    cache_buster = datetime.datetime.now().isoformat()

    params = {
        "q": your_keywords,       # <-- Add keywords
        "domains": your_domains,  # <-- Add domains
        "language": "en",
        "searchIn": "title",      # <-- Search titles for max relevance
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key,
        "t": cache_buster         # <-- Add the unique cache buster
    }

    response = requests.get(url, params=params)
    data = response.json()
    articles = []

    if data.get("status") == "ok":
        for item in data["articles"]:
            articles.append({
                "title": item["title"],
                "url": item["url"],
                "content": item["description"] or ""
            })
    else:
        print(f"❌ Error fetching news: {data.get('message')}")
    return articles

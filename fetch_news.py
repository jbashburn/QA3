# fetch_news.py

import requests
import random # <-- IMPORT RANDOM

def get_business_news(api_key):
    """
    Fetches the latest articles directly from a list of top-tier
    business and finance domains.
    """
    
    # Use the /everything endpoint
    url = "https://newsapi.org/v2/everything"
    
    # Define your high-quality domains
    your_domains = "bloomberg.com,forbes.com,businessinsider.com,economist.com"
    
    # --- THIS IS THE FIX ---
    # Ask for a different page (1-5) each time to get new content
    page_to_fetch = random.randint(1, 5)

    params = {
        "domains": your_domains, 
        "language": "en",
        "sortBy": "publishedAt", 
        "pageSize": 5, 
        "page": page_to_fetch, # <-- ADD THE RANDOM PAGE
        "apiKey": api_key 
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
# fetch_news.py
import requests
import datetime
import random  

def get_business_news(api_key):
    """
    Fetches RELEVANT business articles from top-tier domains
    by combining a domain filter with a keyword search and a
    powerful cache-buster.
    """

    url = "https://newsapi.org/v2/everything"

    # --- 1. THE DOMAIN FILTER ---
    your_domains = "forbes.com,businessinsider.com,cnbc.com,wsj.com,bloomberg.com"

    # --- 2. THE QUALITY FILTER ---
    keyword_options = [
        '"business"', '"finance"', '"markets"', '"economy"',
        '"stocks"', '"wall street"', '"entrepreneurship"', '"startups"',
        '"inflation"', '"interest rates"', 
        '"corporate earnings"', '"investing"'  
    ]
    
    # 1. Randomly pick 3 keywords from the list
    chosen_keywords = random.sample(keyword_options, 3) 
    
    # 2. Join those 3 random keywords with " OR "
    your_keywords = " OR ".join(chosen_keywords)

    # --- 3. THE REFRESH FIX (Forces new articles) ---
    cache_buster = datetime.datetime.now().isoformat()

    params = {
        "q": your_keywords,       # <-- Sends the new random "OR" string
        "domains": your_domains,
        "language": "en",
        "searchIn": "title",    
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key,
        "t": cache_buster       
    }

    response = requests.get(url, params=params)
    data = response.json()
    articles = []

    if data.get("status") == "ok":
        for item in data["articles"]:
            articles.append({
                "title": item["title"],
                "url": item["url"],
                "content": item["description"] or "",
                "source": item["source"]["name"]  
            })
    else:
        print(f"❌ Error fetching news: {data.get('message')}")
    return articles
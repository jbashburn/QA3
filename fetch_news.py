# fetch_news.py

import requests

def get_tennessee_news(api_key):
    
    # --- NEW: More specific keywords and phrases ---
    # We will search for these terms in the article *titles*.
    # Quoted phrases are more specific.
    keywords = [
        "Tennessee",
        "Nashville",
        "Memphis",
        "Knoxville",
        "Chattanooga",
        '"Middle Tennessee"',
        '"East Tennessee"',
        '"West Tennessee"',
        # We add the paper names as keywords. If a TV station
        # writes an article *about* the Tennessean, we'll find it.
        '"The Tennessean"',
        '"TN Tribune"',
        '"Herald-Citizen"',
        '"Upper Cumberland"'
    ]
    
    # Join with " OR "
    query = " OR ".join(keywords)

    url = "https://newsapi.org/v2/everything"
    params = {
        # --- FIX: Using 'q' and 'searchIn' ---
        "q": query,
        "searchIn": "title", # Only find matches in the headline
        
        "language": "en",
        "sortBy": "publishedAt", # Get the newest articles
        "pageSize": 5,
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
                "content": item["content"] or item["description"]
            })
    else:
        # This will print the error message from NewsAPI if something fails
        print(f"❌ Error fetching news: {data.get('message')}")

    return articles
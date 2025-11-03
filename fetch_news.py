# fetch_news.py

import requests

def get_tennessee_news(api_key):
    
    keywords = [
        "Tennessee", "Nashville", "Memphis", "Knoxville", "Chattanooga",
        '"Middle Tennessee"', '"East Tennessee"', '"West Tennessee"',
        '"The Tennessean"', '"TN Tribune"', '"Herald-Citizen"', '"Upper Cumberland"'
    ]
    query = " OR ".join(keywords)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "searchIn": "title", # Only find matches in the headline
        "language": "en",
        "sortBy": "publishedAt",
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
                # <-- Removed urlToImage line -->
            })
    else:
        print(f"❌ Error fetching news: {data.get('message')}")

    return articles
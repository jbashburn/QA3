# fetch_news.py

import requests

def get_tennessee_news(api_key):
    # Keywords to filter Tennessee news
    keywords = ["Tennessee", "Memphis", "Nashville", "Knoxville", "Chattanooga", "Clarksville", "Jackson TN"]
    query = " OR ".join(keywords)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,  # Limit to 5 articles for simplicity
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
        print("❌ Error fetching news:", data.get("message"))

    return articles
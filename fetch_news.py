# fetch_news.py

import requests

def get_tennessee_news(api_key): # This 'api_key' variable is the one we need to use
    """
    Fetches Tennessee news by searching titles for a broad list of keywords.
    """
    
    keywords = [
        # State & Regions
        "Tennessee", '"Middle Tennessee"', '"East Tennessee"', '"West Tennessee"', '"Upper Cumberland"',
        
        # Major Cities
        "Nashville", "Memphis", "Knoxville", "Chattanooga", "Murfreesboro", "Franklin",
        "Johnson City", "Gatlinburg",
        
        # State-Specific Topics
        '"Smoky Mountains"', '"TVA"', '"Bill Lee"',
        
        # Sports Teams
        '"Tennessee Titans"', '"Nashville Predators"', '"Memphis Grizzlies"', '"Tennessee Vols"'
    ]
    query = " OR ".join(keywords)

    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": query,
        "searchIn": "title",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        
        # --- THIS IS THE FIX ---
        # Use the 'api_key' variable passed into the function
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
        # If it fails, this will print the real error (like 'apiKeyInvalid')
        print(f"❌ Error fetching news: {data.get('message')}")

    return articles
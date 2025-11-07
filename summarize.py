# summarize.py

from openai import OpenAI # <-- Import the new 'OpenAI' class

def summarize_articles(articles, api_key):
    
    # --- FIX ---
    # Initialize the client with the API key
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI client: {e}")
        return [] # Return empty list if client fails
    
    summaries = []

    for article in articles:
        content = article["content"]
        if not content:
            continue  # Skip if there's no content to summarize

        try:
            # --- FIX ---
            # This is the new syntax for making an API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes news articles."},
                    {"role": "user", "content": f"Summarize this article in an engaging way, in 4-5 sentences:\n\n{content}"}
                ],
                max_tokens=150,
                temperature=0.5
            )

            # --- FIX ---
            # This is the new syntax for parsing the response
            summary = response.choices[0].message.content.strip()
            
            summaries.append({
                "title": article["title"],
                "url": article["url"],
                "summary": summary
            })

        except Exception as e:
            # Print the specific article title that failed
            print(f"❌ Error summarizing article '{article.get('title', 'Unknown')}': {e}")

    return summaries
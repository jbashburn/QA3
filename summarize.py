# summarize.py

import openai

def summarize_articles(articles, api_key):
    openai.api_key = api_key
    summaries = []

    for article in articles:
        content = article["content"]
        if not content:
            continue  # Skip if there's no content to summarize

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                    {"role": "user", "content": f"Summarize this article in 3-4 sentences:\n\n{content}"}
                ],
                max_tokens=150,
                temperature=0.5
            )

            summary = response["choices"][0]["message"]["content"].strip()
            summaries.append({
                "title": article["title"],
                "url": article["url"],
                "summary": summary
            })

        except Exception as e:
            print(f"Error summarizing article: {e}")

    return summaries

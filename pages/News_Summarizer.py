import streamlit as st
import requests
from decouple import config

# Load API keys from environment variables
news_api_key = config("NEWSAPI_KEY")
openai_api_key = config("OPENAI_API_KEY")


# Function to fetch news articles from NewsAPI
def fetch_news(query):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "apiKey": news_api_key,
        "language": "en",
        "pageSize": 5,
        "sortBy": "relevancy",
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles
    else:
        return None


# Function to summarize text using OpenAI API
def summarize_text(text):
    api_url = "https://api.openai.com/v1/chat/completions"

    # Prepare the prompt for the API request
    prompt = f"""
        Summarize the following text:\n\n{text}\n\nSummary:
    """

    # Set up the request payload and headers
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    # Send the request to OpenAI API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        return "Failed to summarize the text."


# Streamlit app layout
st.title("News Fetcher and Summarizer")

# Input for news topic
query = st.text_input(
    "Enter a topic to search news for:", "Artificial Intelligence AND technology"
)

if st.button("Fetch and Summarize News"):
    if query:
        st.write(f"Fetching news articles related to '{query}'...")

        # Fetch news articles
        articles = fetch_news(query)
        if articles:
            for i, article in enumerate(articles, start=1):
                st.subheader(f"Article {i}: {article['title']}")
                st.write(article["description"])
                st.write(f"[Read more]({article['url']})")

                # Summarize the article content
                summary = summarize_text(article["content"] or article["description"])
                st.write(f"**Summary:** {summary}")
        else:
            st.error("Failed to retrieve news. Please try again.")

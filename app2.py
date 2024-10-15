import streamlit as st
import nltk
from textblob import TextBlob
import requests

nltk.download('punkt')

def fetch_news(query,api_key,num_articles=5):
    url= f"https://gnews.io/api/v4/search?q={query}&token={api_key}&lang=en&max={num_articles}"
    res=requests.get(url)
    data=res.json()

    if 'articles' in data:
        articles=data['articles']
    else:
        st.error("No article found ,sorry!")
        articles=[]
    return articles

def sentiment_analysis(text):
    blob=TextBlob(text)
    score=blob.sentiment.polarity
    return score

def main():
    st.title("News Sentiment Analysis App")

    api_key = '21f708cabb4908f3505767839b4b4bf8'
    # Query input
    query = st.text_input("Enter a topic you want to analyze (e.g., 'Tesla stock'):")

    if st.button("Analyze Sentiment"):
        if api_key and query:
            articles = fetch_news(query, api_key)

            if articles:
                total_sentiment = 0
                num_articles = len(articles)

                # Analyze sentiment for each article
                for article in articles:
                    title = article['title']
                    description = article['description']
                    full_text = title + ' ' + description

                    sentiment = sentiment_analysis(full_text)
                    total_sentiment += sentiment

                # Calculate average sentiment
                average_sentiment = total_sentiment / num_articles if num_articles > 0 else 0
                final_sentiment_label = 'Positive' if average_sentiment > 0 else 'Negative' if average_sentiment < 0 else 'Neutral'

                st.write(f"Average Sentiment Score for '{query}': {average_sentiment:.2f} ({final_sentiment_label})")
            else:
                st.error("No articles found.")
        else:
            st.error("Please enter a query.")

if __name__ == "__main__":
    main()




import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

# Set page configuration
st.set_page_config(
    page_title="Company News Sentiment Analysis", page_icon="📰", layout="wide"
)

# Main header
st.title("Company News Sentiment Analysis")
st.markdown(
    "📈 Get sentiment analysis of news articles with Hindi text-to-speech summaries"
)

# Sidebar for inputs
st.sidebar.header("Search Parameters")

# User Input for Searching News
companies = [
    "Apple",
    "Google",
    "Microsoft",
    "Amazon",
    "Meta",
    "Tesla",
    "Nvidia",
    "Netflix",
]
company_choice = st.sidebar.selectbox("Select a company", companies)
custom_company = st.sidebar.text_input("Or enter a custom company name")

# Use custom company if provided, otherwise use the selected one
query = custom_company if custom_company else company_choice

# Search button
search_button = st.sidebar.button("🔍 Analyze Company News")

# Initialize session state
if "news_df" not in st.session_state:
    st.session_state.news_df = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = {}


# Function to fetch news data
def fetch_news_data(company):
    try:
        # Call API to fetch the news
        response = requests.get(f"{API_URL}/news/{company}")
        if response.status_code == 200:
            articles = response.json()
            st.session_state.news_df = pd.DataFrame(articles)

            # Generate Hindi audio for summaries
            for i, article in enumerate(articles):
                if "summary" in article:
                    audio_response = requests.post(
                        f"{API_URL}/generate_audio/", json={"text": article["summary"]}
                    )
                    if audio_response.status_code == 200:
                        audio_filename = f"{company}_article_{i}.mp3"
                        with open(audio_filename, "wb") as f:
                            f.write(audio_response.content)
                        st.session_state.audio_files[i] = audio_filename

            return True
        else:
            st.error(f"Failed to fetch news: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False


# Execute search when button is clicked
if search_button:
    with st.spinner(f"Analyzing news for {query}..."):
        success = fetch_news_data(query)
        if success:
            st.success(f"Found {len(st.session_state.news_df)} articles for {query}")

# Display results if available
if st.session_state.news_df is not None and not st.session_state.news_df.empty:
    news_df = st.session_state.news_df

    # Display sentiment distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = news_df["sentiment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=sentiment_counts.index, y=sentiment_counts.values, palette="coolwarm", ax=ax
    )
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    st.pyplot(fig)

    # Display sentiment scores
    st.subheader("Sentiment Scores by Article")
    sorted_df = news_df.sort_values(by="sentiment_score", ascending=False)

    # Create a more readable plot by shortening article titles
    sorted_df["short_title"] = sorted_df["title"].apply(
        lambda x: x[:30] + "..." if len(x) > 30 else x
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = sns.barplot(
        x="sentiment_score", y="short_title", data=sorted_df, palette="viridis", ax=ax
    )

    # Add article index to make it easier to reference
    for i, p in enumerate(bars.patches):
        bars.annotate(
            f"#{i + 1}",
            (p.get_width() + 0.01, p.get_y() + p.get_height() / 2),
            ha="left",
            va="center",
            fontsize=9,
        )

    plt.xlabel("Sentiment Score")
    plt.ylabel("Article")
    plt.tight_layout()
    st.pyplot(fig)

    # Create a legend/index below the chart
    st.markdown("#### Article Index")
    for i, (idx, row) in enumerate(sorted_df.iterrows()):
        st.markdown(f"**#{i + 1}**: {row['title']}")

    # Display articles
    st.subheader("News Articles")

    # Create tabs for articles
    tabs = st.tabs([f"Article {i + 1}" for i in range(len(news_df))])

    # Display article details in each tab
    for i, (tab, idx) in enumerate(zip(tabs, news_df.index)):
        article = news_df.iloc[i]
        with tab:
            st.markdown(f"### {article['title']}")
            st.markdown(f"**Source**: {article['url']}")
            if "publish_date" in article:
                st.markdown(f"**Date**: {article['publish_date']}")

            # Summary
            st.markdown("#### Summary")
            st.write(article["summary"])

            # Display Hindi audio for this article if available
            if i in st.session_state.audio_files:
                st.audio(st.session_state.audio_files[i], format="audio/mp3")
                st.caption("▶️ Listen to Hindi summary of this article")

            # Topics
            if "topics" in article:
                st.markdown("#### Topics")
                st.write(article["topics"])

            # Sentiment
            st.markdown(f"**Sentiment**: {article['sentiment']}")
            st.markdown(f"**Sentiment Score**: {article['sentiment_score']:.2f}")

            # Link to full article
            st.markdown(f"[Read Full Article]({article['url']})")

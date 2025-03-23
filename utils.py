import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
from transformers import pipeline
import nltk
from gtts import gTTS
from deep_translator import GoogleTranslator
import stanza

# Download nltk data
nltk.download('punkt')

# Initialize models
summarizer = pipeline("summarization", model="google/pegasus-xsum")
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Initialize Stanza for entity extraction
try:
    nlp = stanza.Pipeline("en")
except:
    stanza.download("en")
    nlp = stanza.Pipeline("en")

def get_nytimes_articles(company, num_articles=10):
    """Extract article links from NYTimes"""
    search_url = f"https://www.nytimes.com/search?query={company}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print("Failed to retrieve NYTimes search results")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        for link in soup.find_all('a', href=True):
            url = link['href']
            if url.startswith("/202"):  # Only considering articles with proper date format
                full_url = "https://www.nytimes.com" + url
                if full_url not in articles:
                    articles.append(full_url)
                if len(articles) >= num_articles:
                    break

        return articles
    except Exception as e:
        print(f"Error fetching NYTimes articles: {e}")
        return []

def get_sentiment(text):
    """Analyze sentiment of text with meaningful labels"""
    if not text.strip():
        return "Neutral"  # Handle empty texts
    
    result = sentiment_model(text[:512])[0]
    sentiment_labels = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
    return sentiment_labels.get(result['label'], "Neutral")

def get_sentiment_score(text):
    """Get numerical sentiment score"""
    if not text or text.strip() == "":
        return 0  # Neutral
    
    result = sentiment_model(text[:512])[0]
    score = result['score']
    label = result['label']
    
    # Convert to score between 0-1
    if label == "LABEL_2":  # Positive
        return score
    elif label == "LABEL_0":  # Negative
        return -score
    else:  # Neutral
        return 0

def extract_entities_stanza(text):
    """Extract meaningful business-related entities using Stanza"""
    if not text.strip():
        return "No relevant topics detected"
    
    doc = nlp(text)
    relevant_entities = {ent.text for ent in doc.ents if ent.type in ["ORG", "PRODUCT", "MONEY", "GPE"]}
    return ", ".join(relevant_entities) if relevant_entities else "No relevant topics detected"

def summarize_article(url):
    """Summarize an article and extract metadata"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Generate summary
        summary_text = summarizer(article.text, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] if article.text else "Summary not available"
        
        # Get sentiment and score
        sentiment = get_sentiment(article.text)
        sentiment_score = get_sentiment_score(article.text)
        
        # Extract topics/entities
        topics = extract_entities_stanza(article.text)
        
        # Create article data dictionary
        summary_data = {
            "title": article.title,
            "authors": ", ".join(article.authors) if article.authors else "Unknown",
            "publish_date": article.publish_date.strftime("%Y-%m-%d") if article.publish_date else "Unknown",
            "summary": summary_text,
            "full_text": article.text,
            "url": url,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "topics": topics
        }
        return summary_data
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def fetch_company_news(company):
    """Fetch and process news articles for a company"""
    articles = get_nytimes_articles(company)
    if not articles:
        print("No articles found.")
        return pd.DataFrame()

    summaries = []
    for url in articles:
        summary = summarize_article(url)
        if summary:
            summaries.append(summary)

    return pd.DataFrame(summaries)

def generate_tts(text, filename="output.mp3"):
    """Convert text to Hindi speech"""
    try:
        # Translate text to Hindi
        translated_text = GoogleTranslator(source="en", target="hi").translate(text)
        
        # Convert translated text to speech
        tts = gTTS(text=translated_text, lang="hi")
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating TTS: {e}")
        # Create a fallback audio if translation fails
        tts = gTTS(text="Translation failed", lang="en")
        tts.save(filename)
        return filename
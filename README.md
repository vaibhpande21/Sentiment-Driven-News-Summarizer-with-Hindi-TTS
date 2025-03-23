# 📰 News Summarization and Sentiment Analysis with Hindi TTS

## 📌 Overview
This web-based application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## 🎯 Features
- **News Extraction**: Fetches and summarizes news articles about a company.
- **Sentiment Analysis**: Categorizes news articles as Positive, Negative, or Neutral.
- **Comparative Analysis**: Analyzes sentiment trends across multiple articles.
- **Hindi Text-to-Speech (TTS)**: Converts summaries into Hindi audio.
- **User Interface**: Simple web app built with Streamlit.
- **API-Based Architecture**: FastAPI for backend and Streamlit/Gradio for frontend.
- **Deployment**: Hosted on Hugging Face Spaces.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Web Scraping**: BeautifulSoup, Newspaper3k
- **NLP Models**: Transformers (Google Pegasus-XSum, CardiffNLP Roberta)
- **Speech Generation**: Google Text-to-Speech (gTTS)
- **Data Processing**: Pandas, Stanza
- **Deployment**: Hugging Face Spaces

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/news-sentiment-tts.git
cd news-sentiment-tts
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the FastAPI Backend
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 4️⃣ Run the Streamlit Frontend
```bash
streamlit run app.py
```

## 🌐 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/news/{company}` | Fetches and summarizes news articles about a company. |
| `POST` | `/generate_audio/` | Converts text into Hindi speech. |

## 📌 Expected Output
- **News Summary**: Extracted title, summary, and metadata.
- **Sentiment Report**: Categorization of news articles.
- **Comparative Analysis**: Insights into how media coverage varies.
- **Hindi Audio Output**: Playable audio summarizing the sentiment report.

## 📢 Deployment on Hugging Face Spaces
[![Deploy to Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face-blue?logo=huggingface)](https://huggingface.co/spaces/your-deployment-link)



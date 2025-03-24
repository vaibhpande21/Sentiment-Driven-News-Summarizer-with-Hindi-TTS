# 📰 News Summarization and Sentiment Analysis with Hindi TTS

## 📌 Overview
This web-based application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## 🎯 Features
- **News Extraction**: Fetches and summarizes news articles about a company.
- **Sentiment Analysis**: Categorizes news articles as Positive, Negative, or Neutral.
- **Comparative Analysis**: Analyzes sentiment trends across multiple articles.
- **Hindi Text-to-Speech (TTS)**: Converts summaries into Hindi audio.
- **User Interface**: Simple web app built with Streamlit.
- **API-Based Architecture**: FastAPI for backend and Streamlit for frontend.
- **Deployment**: Hosted on Hugging Face Spaces.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Web Scraping**: BeautifulSoup, Newspaper3k
- **NLP Models**:
  - **Summarization**: Google Pegasus-XSum
  - **Sentiment Analysis**: CardiffNLP Roberta
- **Speech Generation**: Google Text-to-Speech (gTTS)
- **Data Processing**: Pandas, Stanza
- **Deployment**: Hugging Face Spaces

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vaibhpande21/Sentiment-Driven-News-Summarizer-with-Hindi-TTS.git
cd Sentiment-Driven-News-Summarizer-with-Hindi-TTS
```

### 2️⃣ Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate it (Mac/Linux)
venv\Scripts\activate  # Activate it (Windows)
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Backend
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 5️⃣ Run the Streamlit Frontend
```bash
streamlit run app.py
```

## 🌐 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/news/{company}` | Fetches and summarizes news articles about a company. |
| `POST` | `/generate_audio/` | Converts text into Hindi speech. |

### Example API Calls
#### **Fetch News Summary**
```bash
curl -X GET "http://127.0.0.1:8000/news/Tesla"
```
**Response:**
```json
{
  "company": "Tesla",
  "articles": [
    {
      "title": "Tesla Achieves Record Sales",
      "summary": "Tesla's quarterly sales hit a new record, boosting stock prices.",
      "sentiment": "Positive"
    }
  ]
}
```

#### **Convert Text to Hindi Speech**
```bash
curl -X POST "http://127.0.0.1:8000/generate_audio/" -H "Content-Type: application/json" -d '{"text": "यह एक समाचार सारांश है।"}'
```

## 📌 Expected Output
- **News Summary**: Extracted title, summary, and metadata.
- **Sentiment Report**: Categorization of news articles.
- **Comparative Analysis**: Insights into how media coverage varies.
- **Hindi Audio Output**: Playable audio summarizing the sentiment report.

## 📣 Deployment on Hugging Face Spaces
[![Deploy to Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face-blue?logo=huggingface)](https://huggingface.co/spaces/Vaibh21/news-sentiment-tts)

## 📸 Screenshots
*(Consider adding images or GIFs of your app UI for better visualization.)*

---
Feel free to suggest further enhancements! 🚀

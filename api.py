from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import fetch_company_news, generate_tts

# Initialize FastAPI app
app = FastAPI(
    title="News Sentiment Analysis API",
    description="API for company news sentiment analysis with Hindi TTS",
)


class TextRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "News Sentiment Analysis API is running"}


@app.get("/news/{company}")
async def get_news(company: str):
    """
    Fetch news articles based on a company name

    Args:
        company (str): Company name to search for

    Returns:
        List of news articles with sentiment analysis
    """
    df = fetch_company_news(company)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No news found for {company}")

    return df.to_dict(orient="records")


@app.post("/generate_audio/")
async def generate_audio(data: TextRequest):
    """
    Generate Hindi TTS audio from text

    Args:
        data (TextRequest): Object containing text to convert to speech

    Returns:
        Audio file in MP3 format
    """
    text = data.text
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    # Generate a unique filename
    filename = f"hindi_summary_{hash(text) % 10000}.mp3"
    filepath = generate_tts(text, filename)

    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)

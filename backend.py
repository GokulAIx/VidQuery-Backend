from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.proxies import WebshareProxyConfig # Import the proxy configuration
import os # Import the os module to access environment variables

app = FastAPI()

# Retrieve proxy credentials from environment variables
# Use .getenv() with a default value to avoid errors if the variable is not set
WEBSHARE_USER = os.getenv("WEBSHARE_USER")
WEBSHARE_PASS = os.getenv("WEBSHARE_PASS")

# Initialize YouTubeTranscriptApi with Webshare proxy configuration
# This ensures all requests made by ytt_api are routed through Webshare
try:
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=WEBSHARE_USER,
            proxy_password=WEBSHARE_PASS,
        )
    )
except Exception as e:
    # Log or handle the error appropriately if proxy configuration fails
    print(f"Error initializing YouTubeTranscriptApi with proxy: {e}")
    # You might want to consider how your application should behave if proxies cannot be initialized
    # For example, raise an exception to prevent transcript requests without proxies
    ytt_api = YouTubeTranscriptApi() # Fallback to no proxy if initialization fails


def Trans(video_id: str):
    try:
        # Use the pre-configured ytt_api instance
        transcript = ytt_api.fetch(video_id)
        final_transcripts = " ".join(chunk.text for chunk in transcript)
        return final_transcripts
    except TranscriptsDisabled:
        return None

@app.get("/transcript/{video_id}")
async def get_transcript(video_id: str):
    transcript_text = Trans(video_id)
    if transcript_text is None:
        raise HTTPException(
            status_code=404,
            detail="Transcripts are disabled for this video."
        )
    return transcript_text

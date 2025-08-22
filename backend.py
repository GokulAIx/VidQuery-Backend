from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS for your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize YouTubeTranscriptApi with Webshare rotating proxies
proxy_username = os.getenv("WEBSHARE_USER")
proxy_password = os.getenv("WEBSHARE_PASS")

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=proxy_username,
        proxy_password=proxy_password,
        filter_ip_locations=["us", "de"]  # Optional: restrict countries
    )
)

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        # Fetch transcript through Webshare proxies
        transcript_data = ytt_api.fetch(video_id)
        final_transcript = " ".join([chunk["text"] for chunk in transcript_data])
        return final_transcript
    except TranscriptsDisabled:
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

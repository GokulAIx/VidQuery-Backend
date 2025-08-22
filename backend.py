from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

app = FastAPI()

# Allow CORS for your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        final_transcript = " ".join(chunk.text for chunk in transcript)
        return {"transcript": final_transcript}
    except TranscriptsDisabled:
        return {"transcript": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

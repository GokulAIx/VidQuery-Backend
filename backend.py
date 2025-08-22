from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

app = FastAPI()

def Trans(video_id: str):
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
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
    return {"transcript": transcript_text}

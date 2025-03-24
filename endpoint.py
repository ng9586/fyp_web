from fastapi import FastAPI, HTTPException
from app.main import download_audio, transcribe_audio, get_video_subtitles
from pydantic import BaseModel

app = FastAPI()

# 添加根 URL 处理函数
@app.get("/")
async def root():
    return {"message": "Welcome to YouTube Transcriber"}

class URLPayload(BaseModel):
    url: str

@app.post("/transcribe/")
async def transcribe_audio_endpoint(payload: URLPayload):
    """從 YouTube 影片下載字幕並返回"""
    try:
        url = payload.url
        
        # 直接從影片中提取字幕
        subtitles = get_video_subtitles(url)  
        
        # 如果影片沒有字幕，則拋出錯誤
        if not subtitles:
            raise HTTPException(status_code=404, detail="No subtitles found for this video.")
        
        return {"subtitles": subtitles}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

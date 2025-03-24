from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import yt_dlp as youtube_dl
import openai
import os
import time

app = FastAPI()

# 設定 OpenAI API 密鑰
# openai.api_key = 'your-openai-api-key'

class YouTubeURL(BaseModel):
    url: str
    language: str

def download_audio(url):
    """下載 YouTube 影片音訊並返回音訊文件路徑"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',  # 設定音訊格式為 mp3
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join('downloads', f"{info['id']}.mp3")

def transcribe_audio(audio_path):
    """使用 Whisper 轉錄音訊"""
    with open(audio_path, 'rb') as f:
        transcription = openai.Audio.transcribe("whisper-1", f)
    return transcription['text']

@app.post("/transcribe")
async def transcribe(youtube_url: YouTubeURL):
    """從 YouTube 影片轉錄音訊"""
    try:
        audio_path = download_audio(youtube_url.url)
        transcription = transcribe_audio(audio_path)
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket 端點
@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket, youtube_url: YouTubeURL):
    await websocket.accept()
    try:
        audio_path = download_audio(youtube_url.url)
        transcription = transcribe_audio(audio_path)
        
        # 當轉錄過程進行時，可以更新進度（例如分步驟）
        for i in range(1, 11):
            await websocket.send_text(f"Progress: {i * 10}%")
            time.sleep(1)  # 模擬延遲
        
        await websocket.send_text(f"Transcription completed: {transcription}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")

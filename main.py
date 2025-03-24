import yt_dlp as youtube_dl
import os
from fastapi import HTTPException

# Function to download the audio from YouTube
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

# Function to transcribe audio using speech_recognition
def transcribe_audio(audio_path):
    """使用本地音訊轉錄方法"""
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)  # 讀取音訊
        # 使用 Google Web 服務進行語音識別
        transcription = recognizer.recognize_google(audio)
        return transcription
    except Exception as e:
        raise Exception(f"Error during transcription: {str(e)}")

# Function to extract subtitles from YouTube
def get_video_subtitles(url):
    """從 YouTube 影片中提取字幕"""
    ydl_opts = {
        'quiet': True,  # 不輸出過多訊息
        'subtitles': True,  # 提取字幕
        'subtitleslangs': ['en'],  # 指定要提取的字幕語言（這裡是英語，視需求可更改）
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # 下載字幕文件保存路徑
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            # 提取視頻資訊
            info = ydl.extract_info(url, download=False)
            
            # 檢查是否有字幕
            if 'subtitles' in info and 'en' in info['subtitles']:
                # 如果有字幕，返回字幕
                subtitle_url = info['subtitles']['en'][0]['url']
                
                # 下載字幕內容
                subtitle = ydl.urlopen(subtitle_url).read().decode('utf-8')
                return subtitle
            else:
                # 如果沒有字幕，返回 None
                return None
        except Exception as e:
            raise Exception(f"無法提取字幕: {str(e)}")

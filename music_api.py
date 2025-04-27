from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with specific origins like ["http://localhost"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class SongRequest(BaseModel):
    song_name: str

def download_music_as_m4a(song_name):
    search_query = f"ytsearch1:{song_name}"
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=True)
        filename = f"{info.get('title', 'Unknown Title')}.m4a"
        return filename

@app.post("/download_music")
def download_music(request: SongRequest):
    filename = download_music_as_m4a(request.song_name)
    return {"message": "✅ Downloaded", "file": filename}

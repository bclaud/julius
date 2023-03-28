from fastapi import FastAPI, Body
from pydantic import BaseModel
import uvicorn
import os
import yt_dlp
from multiprocessing import Process

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


    
def main ():
    uvicorn.run(app=app, port=8000)

if __name__ == "__main__":
    main()

def download_video(url, output_name=None):
    # Create a yt-dlp options dictionary
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s'
    }

    # If an output name is specified, use it
    if output_name:
        ydl_opts['outtmpl'] = output_name

    # Create a yt-dlp object with options
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Download the video
    with ydl:
        ydl.download([url])

    # If an output name is not specified, rename the downloaded video to remove any special characters
    if not output_name:
        video_info = ydl.extract_info(url, download=False)
        title = video_info.get('title', 'video').replace('/', '-')
        ext = video_info.get('ext', 'mp4')
        filename = f"{title}.{ext}"
        os.rename(filename, filename.replace('.', '_'))

class MyUrl(BaseModel):
    url: str



def start_background_job(url, output_name=None):
  p = Process(target=download_video, args=(url, output_name))
  p.start()



@app.post("/download/")
def download_video_router(url: MyUrl = Body(...)):
    print(url.url)
    start_background_job(url.url)
    return "ok"
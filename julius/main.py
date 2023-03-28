from fastapi import FastAPI, Body
import uvicorn

import julius


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run(app=app, port=8000)


if __name__ == "__main__":
    main()


@app.post("/download/")
def download_video_router(chat_request: julius.schemas.ChatVideoRequest = Body(...)):
    julius.video_download.job_download_video(chat_request.video_url)

    return "ok"

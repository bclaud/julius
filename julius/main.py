from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI, Body
import uvicorn
import telebot

import julius
from julius.settings import Settings

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()

bot = telebot.TeleBot(get_settings().bot_token)

@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": "Hello World", "App-name": settings.app_name}


def main():
    uvicorn.run(app=app, port=8000)


if __name__ == "__main__":
    main()


@app.post("/download/")
def download_video_router(chat_request: julius.schemas.ChatVideoRequest = Body(...)):
    julius.video_download.job_download_video(chat_request.video_url)

    return "ok"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['download'])
def sign_handler(message):
    text = "Provide the video url you want to download"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

bot.infinity_polling()



from pydantic import BaseSettings


class Settings(BaseSettings):
    # reads all env vars
    app_name: str = "Julius-bot"
    bot_token: str = "token_mock"



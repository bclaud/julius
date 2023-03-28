from pydantic import BaseModel


class ChatVideoRequest(BaseModel):
    video_url: str
    user: str
    filename: str

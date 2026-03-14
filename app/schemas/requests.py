from pydantic import BaseModel


class AppMessageRequest(BaseModel):
    user_id: str
    text: str

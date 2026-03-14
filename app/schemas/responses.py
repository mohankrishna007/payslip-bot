from pydantic import BaseModel


class SessionStatusResponse(BaseModel):
    state: str
    has_session: bool


class AppMessageResponse(BaseModel):
    reply: str
    state: str


class AppUploadResponse(BaseModel):
    reply: str
    state: str

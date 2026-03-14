"""In-app chat router — protocol adapter for WebChannel."""

import logging
from pathlib import Path

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import AppMessageRequest, AppMessageResponse, AppUploadResponse, SessionStatusResponse
from app.services.conversation.channel import WebChannel
from app.services.conversation.messages import GENERIC_ERROR
from app.services.conversation.state import get_state
from app.services.session.store import get_session

router = APIRouter(prefix="/app", tags=["in-app chat"])
log = logging.getLogger("salarybot.chat")
_templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")
_channel = WebChannel()


@router.post("/message", response_model=AppMessageResponse, summary="Send a text message")
async def send_message(body: AppMessageRequest):
    try:
        reply = await _channel.on_text(body.user_id, body.text)
    except Exception:
        log.exception("Error handling message for user %s", body.user_id)
        reply = GENERIC_ERROR
    return AppMessageResponse(reply=reply, state=get_state(body.user_id).value)


@router.post("/upload", response_model=AppUploadResponse, summary="Upload a payslip for analysis")
async def upload_payslip(user_id: str = Form(...), file: UploadFile = File(...)):
    try:
        data = await file.read()
        reply = await _channel.on_upload(user_id, data)
    except Exception:
        log.exception("Error handling upload for user %s", user_id)
        reply = GENERIC_ERROR
    return AppUploadResponse(reply=reply, state=get_state(user_id).value)


@router.get("/session/{user_id}", response_model=SessionStatusResponse, summary="Get current session state")
async def session_status(user_id: str):
    return SessionStatusResponse(state=get_state(user_id).value, has_session=get_session(user_id) is not None)


@router.get("/ui", response_class=HTMLResponse, include_in_schema=False)
async def ui(request: Request):
    return _templates.TemplateResponse("chat.html", {"request": request})

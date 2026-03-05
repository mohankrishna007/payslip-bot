from pydantic import BaseModel


# --- Request models ---

class ConsentRequest(BaseModel):
    user_id: str


class ChatRequest(BaseModel):
    user_id: str
    message: str


class CheckRequest(BaseModel):
    user_id: str


# --- Response models ---

class HealthResponse(BaseModel):
    status: str
    provider: str


class ConsentResponse(BaseModel):
    detail: str


class AnalyzeResponse(BaseModel):
    data: dict


class ChatResponse(BaseModel):
    reply: str


class DeductionResult(BaseModel):
    field: str
    expected: float | None
    actual: float | None
    status: str  # "ok" | "flag"


class CheckResponse(BaseModel):
    results: list[DeductionResult]


class SlipEvent(BaseModel):
    id: int
    user_id: str
    processed_at: str
    provider_used: str
    language: str


class HistoryResponse(BaseModel):
    events: list[SlipEvent]

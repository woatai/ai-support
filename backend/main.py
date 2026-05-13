import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.llm_client import get_customer_service_reply


app = FastAPI(title="AI Support")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message 不能为空")

    try:
        reply = get_customer_service_reply(message)
    except requests.exceptions.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"调用大模型失败：{exc}") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="大模型返回格式异常") from exc

    return ChatResponse(reply=reply)

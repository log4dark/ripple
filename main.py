from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from api.websocket import router as ws_router
from api.upload import router as upload_router
from utils.log import setup_logger

logger = setup_logger(name="main")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def redirect_to_ui():
    logger.info("🔁 클라이언트가 index.html 요청")
    return RedirectResponse(url="/static/index.html")

# API 라우터 등록
app.include_router(ws_router)
app.include_router(upload_router)

logger.info("🚀 STT FastAPI 서버 시작됨.")

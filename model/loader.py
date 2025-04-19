from faster_whisper import WhisperModel
from config.settings import get_settings
from utils.log import setup_logger

logger = setup_logger("model")

model = None

def get_model():
    global model
    if model:
        return model

    settings = get_settings()

    logger.info(f"🔧 모델 로딩 중: {settings.WHISPER_MODEL}")
    logger.info(f"📦 디바이스: {settings.WHISPER_DEVICE}, 연산: {settings.WHISPER_COMPUTE_TYPE}")

    model = WhisperModel(
        settings.WHISPER_MODEL,
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE,
        download_root=settings.WHISPER_MODEL_DIR
    )

    logger.info("✅ 모델 로딩 완료")
    return model


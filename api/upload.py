# api/upload.py
# - 업로드된 파일 → 저장 → VAD 전처리 → STT 추론 → 텍스트 반환

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4

from utils.log import setup_logger
from model.loader import get_model
from model.transcribe import upload_transcribe
from preprocess.audio.vad import split_voiced, save_wave
from postprocess.pipeline import run_full_postprocess

router = APIRouter()
logger = setup_logger("upload")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/stt/upload")
async def upload_and_transcribe(file: UploadFile = File(...)):
    filename = f"{uuid4()}.wav"
    filepath = os.path.join(UPLOAD_DIR, filename)

    try:
        # 📥 1. 업로드 파일 저장
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"📤 WAV 업로드 성공: {filename}")

        # ✂️ 2. VAD 전처리
        voiced_audio, sample_rate = split_voiced(filepath)
        vad_filename = filename.replace(".wav", "_voiced.wav")
        vad_filepath = os.path.join(UPLOAD_DIR, vad_filename)

        # 💾 3. 전처리된 음성 저장
        save_wave(vad_filepath, voiced_audio, sample_rate)
        logger.info(f"🔊 VAD 전처리 완료: {vad_filename} ({len(voiced_audio)} bytes)")

        # 🤖 4. STT 처리
        model = get_model()
        segments, raw_result = upload_transcribe(model, vad_filepath)

        # 🎯 5. 후처리
        final_result = run_full_postprocess(raw_result, apply_kobart=False)

        logger.info(f"📄 STT 결과 (원문): {raw_result[:50]}...")
        logger.info(f"🎯 후처리 결과: {final_result[:50]}...")

        return JSONResponse({
            "raw": raw_result,
            "text": final_result,
            "filename": vad_filename
        })

    except Exception as e:
        logger.error(f"🚨 업로드 실패: {file.filename} | 오류: {str(e)}")
        return JSONResponse({"error": "파일 저장 또는 처리 실패"}, status_code=500)

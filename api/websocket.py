# api/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os
import numpy as np
from datetime import datetime

from utils.log import setup_logger
from model.loader import get_model
from model.transcribe import stream_transcribe
from preprocess.audio.vad import is_speech_frame, save_wave

router = APIRouter()
logger = setup_logger("websocket")

AUDIO_DIR = "temp_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

SAMPLE_RATE = 16000
FRAME_MS = 30
CHUNK_SECONDS = 5
OVERLAP_SECONDS = 0.5

FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)
OVERLAP_SIZE = int(SAMPLE_RATE * OVERLAP_SECONDS)
SILENCE_TRIGGER_FRAMES = int(500 / FRAME_MS)  # 500ms = 17 frames

model = get_model()

@router.websocket("/ws/stt/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    filename = f"{datetime.now():%Y%m%d_%H%M%S}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    all_audio = bytearray()
    pcm_buffer = np.array([], dtype=np.int16)
    current_chunk = []
    silence_count = 0
    prev_tail = np.array([], dtype=np.int16)

    logger.info(f"🎙️ WebSocket 연결 수립됨 → {filename}")

    try:
        while True:
            data = await websocket.receive_bytes()
            all_audio.extend(data)

            samples = np.frombuffer(data, dtype=np.int16)
            pcm_buffer = np.concatenate((pcm_buffer, samples))

            while len(pcm_buffer) >= FRAME_SIZE:
                frame = pcm_buffer[:FRAME_SIZE]
                pcm_buffer = pcm_buffer[FRAME_SIZE:]

                current_chunk.append(frame)

                if is_speech_frame(frame.tobytes(), SAMPLE_RATE):
                    silence_count = 0
                else:
                    silence_count += 1

                # STT 트리거 조건 (무음 or 최대 청크 길이 도달)
                total_duration_ms = len(current_chunk) * FRAME_MS
                if silence_count >= SILENCE_TRIGGER_FRAMES or total_duration_ms >= CHUNK_SECONDS * 1000:
                    logger.debug("[청크 처리 시작] ----------------------------")

                    current = np.concatenate(current_chunk)
                    full_input = np.concatenate([prev_tail, current]) if prev_tail.size else current
                    prev_tail = current[-OVERLAP_SIZE:]

                    segments, _ = stream_transcribe(model, full_input, sr=SAMPLE_RATE)

                    # 중복 제거
                    result_texts = []
                    last_end = 0.0
                    for seg in segments:
                        if seg.start >= last_end - 0.3:
                            result_texts.append(seg.text)
                            last_end = seg.end
                        else:
                            logger.debug(f"중복 제거됨: {seg.start:.2f}-{seg.end:.2f} → {seg.text}")

                    result_text = " ".join(result_texts).strip()
                    if result_text:
                        logger.info(f"실시간 STT 결과: {result_text[:50]}...")
                        await websocket.send_text(result_text)

                    logger.debug("[청크 처리 완료] ----------------------------\n")
                    current_chunk = []
                    silence_count = 0

    except WebSocketDisconnect:
        logger.warning(f"❗ WebSocket 연결 끊김 → {filename}")
        try:
            save_wave(filepath, all_audio, SAMPLE_RATE)
            logger.info(f"💾 WAV 저장 완료 → {filepath} ({len(all_audio)} bytes)")
        except Exception as e:
            logger.error(f"🚨 WAV 저장 실패 → {filepath} | 오류: {e}")


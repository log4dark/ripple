# model/transcribe.py

import time
import tempfile
import soundfile as sf
import numpy as np
import math
from config.settings import get_settings
from utils.log import setup_logger

logger = setup_logger("transcribe")

def stream_transcribe(model, audio_chunk: np.ndarray, sr: int = 16000):
    """실시간 STT용 추론 (WebSocket 처리 chunk 단위)"""
    start = time.perf_counter()

    # RMS 체크
    if audio_chunk.dtype != np.float32:
        audio_chunk = audio_chunk.astype(np.float32) / 32768.0

    rms = np.sqrt(np.mean(audio_chunk ** 2))
    dbfs = 20 * math.log10(rms + 1e-10)

    logger.debug(f"[stream] RMS: {rms:.6f}, dBFS: {dbfs:.2f} dB")

    if dbfs < -40:
        logger.debug(f"[stream] 입력이 너무 작습니다 (dBFS: {dbfs:.2f} dB)")
        elapsed = (time.perf_counter() - start) * 1000
        logger.debug(f"[stream] 추론 생략됨, 시간: {elapsed:.2f} ms")
        return [], ""

    #
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio_chunk, sr)
        temp_path = tmp.name

    # 추론
    segments, info = model.transcribe(
        temp_path,
        beam_size=3,             # 너무 낮은 beam은 반복 발생 확률을 높이고, 너무 높으면 속도 저하 -> 3~5정도 
        language="ko",
        vad_filter=False,
        temperature=0.4,         # → randomness 추가로 반복 완화
    )

    # 세그먼트 조합~~~
    segments = list(segments)
    texts = [s.text for s in segments]
    result = " ".join(texts).strip()
    #result = suppress_repetition(filter_short_repetitions(result)) # 후처리 추가

    elapsed = (time.perf_counter() - start) * 1000
    logger.info(f"[stream] STT 추론 시간: {elapsed:.2f} ms")

    if not result:
        logger.info("[stream] STT 결과 없음 (무음 또는 인식 실패)")

    return segments, result

def upload_transcribe(model, wav_path: str):
    """WAV 파일 경로 기반 추론 (업로드용)"""
    start = time.perf_counter()

    segments, info = model.transcribe(
        wav_path,
        beam_size=5,
        language="ko",
        vad_filter=False,
        temperature=0.4,
        no_speech_threshold=0.95,
        condition_on_previous_text=True,
    )

    # Segment 로그 찍기 (어디서 잘렸는지 보기 위함)
    segments = list(segments)
    for i, seg in enumerate(segments):
        logger.debug(f"[Segment {i}] {seg.start:.2f}s ~ {seg.end:.2f}s | no_speech_prob: {seg.no_speech_prob:.2f}, avg_logprob: {seg.avg_logprob:.2f} | {seg.text}")

    # 텍스트 조합
    texts = [s.text for s in segments]
    result = " ".join(texts).strip()

    elapsed = (time.perf_counter() - start) * 1000
    logger.info(f"[upload] STT 추론 시간: {elapsed:.2f} ms")

    return segments, result


### TEST ######################################################################
# repeat suppression 후처리 로직 추가
# - result에 대해 단순한 N-gram 반복 제거 필터를 추가해.
def suppress_repetition(text, max_repeat=5):
    words = text.split()
    filtered = []
    prev = ""
    repeat_count = 0
    for word in words:
        if word == prev:
            repeat_count += 1
            if repeat_count < max_repeat:
                filtered.append(word)
        else:
            repeat_count = 1
            filtered.append(word)
        prev = word
    return " ".join(filtered)

# 단일 음절 반복 필터
# - ["어", "우", "음", "음음음음음"] 같은 반복 제거
import re

def filter_short_repetitions(text):
    # 3번 이상 반복된 단일 음절
    return re.sub(r'(\b\w{1})\1{3,}', r'\1', text)

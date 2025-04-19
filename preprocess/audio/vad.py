# preprocess/audio/vad.py

import webrtcvad
import numpy as np
import wave
import os

# 📥 WAV 읽기
def read_wave(path):
    with wave.open(path, 'rb') as wf:
        assert wf.getsampwidth() == 2  # 16-bit
        assert wf.getnchannels() == 1  # mono
        assert wf.getframerate() in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, wf.getframerate()

# 💾 WAV 저장
def save_wave(path, audio_bytes, sample_rate):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

# 📦 업로드용 VAD 전처리 → 음성 있는 구간만 필터링
def split_voiced(path, aggressiveness=2, frame_duration_ms=30):
    audio, sample_rate = read_wave(path)
    vad = webrtcvad.Vad(aggressiveness) # 0(민감) ~ 3(덜 민감)
    frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # byte 단위
    segments = []

    for i in range(0, len(audio), frame_size):
        frame = audio[i:i + frame_size]
        if len(frame) < frame_size:
            break
        if vad.is_speech(frame, sample_rate):
            segments.append(frame)

    voiced_audio = b''.join(segments)
    return voiced_audio, sample_rate

# 🔄 실시간 프레임용 VAD → bool 반환
def is_speech_frame(frame_bytes, sample_rate, aggressiveness=2):
    vad = webrtcvad.Vad(aggressiveness)
    return vad.is_speech(frame_bytes, sample_rate)

# 🛠 실시간 프레임 생성 유틸
def frame_generator(pcm_array, sample_rate, frame_duration_ms=30):
    frame_size = int(sample_rate * frame_duration_ms / 1000)
    for i in range(0, len(pcm_array), frame_size):
        frame = pcm_array[i:i + frame_size]
        if len(frame) < frame_size:
            break
        yield frame


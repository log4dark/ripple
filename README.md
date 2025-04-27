# 🌀 ripple - Real-Time Korean STT Server

**ripple**은 OpenAI Whisper와 CTranslate2 기반으로 구축된 **한국어 실시간 음성 인식 (STT) 서버**입니다.  

---

## ✨ 제공 기능

- 🎤 **입력**
  - 실시간: chunk (100ms), PCM 스트리밍
  - 배치: WAV 파일 업로드

- 🎛 **오디오 전처리**
  - VAD (음성 구간 검출)

- 🧠 **STT 모델 추론**
  - faster-whisper + CTranslate2 + CPU 기반 고속 추론

- 📦 **사용 모델**
  - [seastar105/whisper-medium-ko-zeroth](https://huggingface.co/seastar105/whisper-medium-ko-zeroth)
  - [SungBeom/whisper-small-ko](https://huggingface.co/SungBeom/whisper-small-ko)

- 🚀 **모델 성능 최적화**
  - None

- 🔄 **실시간 Streaming 모드**
  - 0.5초 단위 chunk 오버랩 처리 (Sliding Window) 및 중복 제거

- 🛠 **텍스트 후처리**
  - None

---

## 🧩 프로젝트 구조

<pre>
ripple/
├── api/              # FastAPI STT 라우터
├── model/            # Whisper 모델 로딩 및 추론
├── preprocess/audio/ # 오디오 전처리 (VAD 등)
├── static/           # Web UI (index.html, stt.js)
├── whisper/          # [❗Git 제외] CTranslate2 모델 디렉토리
├── config/, utils/   # 설정 및 로깅 유틸
├── main.py           # FastAPI 앱 진입점
└── INSTALL.md        # 설치 가이드
</pre>

---

## ⚙️ 빠른 시작

### (선택) 1. Conda 환경 생성 & 패키지 설치

```bash
conda create -n ripple python=3.10 -y
conda activate ripple
pip install -r requirements.txt
```

### 2. Whisper 모델 변환 및 설치

> HuggingFace 모델을 받아 CTranslate2 포맷으로 변환 후 `whisper/` 디렉토리에 위치시켜야 합니다.

```bash
ct2-transformers-converter \
  --model SungBeom/whisper-small-ko \
  --output_dir ./whisper/ct2-whisper-small-ko-int8 \
  --quantization int8
```

### 3. 서버 실행

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

웹 UI 접속: [http://localhost:8000](http://localhost:8000)

---

## 📬 API 요약

| 메서드 | 엔드포인트     | 설명                      |
|--------|----------------|---------------------------|
| POST   | `/stt/upload`  | WAV 파일 업로드로 STT 실행 |
| WS     | `/ws/stt`      | WebSocket 실시간 STT 처리  |

---

## 📄 설치 가이드

설치 및 환경 구성에 대한 자세한 내용은 👉 [INSTALL.md](./INSTALL.md) 파일을 참고하세요.

---

## 📎 참고 프로젝트

- [OpenAI Whisper](https://github.com/openai/whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)

---

## 🤝 기여 또는 문의

- 담당자: **BS**
- 에러 로그: `logs/error.log`, `logs/debug.log` 참고
- Pull Request 및 Issue 환영

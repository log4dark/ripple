# 🌀 ripple - Real-Time Korean STT Server

**ripple**은 OpenAI Whisper와 CTranslate2 기반으로 구축된 **한국어 실시간 음성 인식 (STT) 서버**입니다.  
FastAPI 백엔드와 WebSocket 스트리밍, 후처리 모듈을 통해 **정확하고 자연스러운 텍스트 변환**을 제공합니다.

---

## 🎯 주요 기능

- 🎤 **실시간 STT**: 마이크 음성을 WebSocket으로 스트리밍
- 📁 **파일 업로드 STT**: WAV 파일 업로드로 텍스트 추출
- 🎛 **전처리 & 후처리 포함**:
  - VAD (음성 구간 검출)
  - 띄어쓰기, 맞춤법 보정
  - 구두점 자동 삽입
  - 중복 제거 및 문장 템플릿화
- 🌐 **웹 UI**: index.html + stt.js로 브라우저에서 직접 테스트 가능
- ⚡ **CTranslate2 기반 고속 추론** (INT8 모델 지원)

---

## 🧩 프로젝트 구조

<pre>
ripple/
├── api/              # FastAPI STT 라우터
├── model/            # Whisper 모델 로딩 및 추론
├── postprocess/      # 텍스트 후처리 (맞춤법, 구두점 등)
├── preprocess/audio/ # 오디오 전처리 (VAD 등)
├── static/           # Web UI (index.html, stt.js)
├── whisper/          # [❗Git 제외] CTranslate2 모델 디렉토리
├── config/, utils/   # 설정 및 로깅 유틸
├── main.py           # FastAPI 앱 진입점
└── INSTALL.md        # 설치 가이드
</pre>

---

## ⚙️ 빠른 시작

### 1. Conda 환경 생성 & 패키지 설치

```bash
conda create -n ripple python=3.10 -y
conda activate ripple
pip install -r requirements.txt
```

### 2. Whisper 모델 변환 및 설치

> HuggingFace 모델을 받아 CTranslate2 포맷으로 변환 후 `whisper/` 디렉토리에 위치시켜야 합니다.

```bash
ct2-transformers-converter \
  --model ghost613/whisper-large-v3-turbo \
  --output_dir ./whisper/ct2-whisper-large-v3-turbo-korean-int8 \
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
- [PyKoSpacing](https://github.com/haven-jeon/PyKoSpacing)
- [Hanspell](https://github.com/ssut/py-hanspell)

---

## 🤝 기여 또는 문의

- 담당자: **BS**
- 에러 로그: `logs/error.log`, `logs/debug.log` 참고
- Pull Request 및 Issue 환영
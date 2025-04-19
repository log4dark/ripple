# 🛠 설치 가이드: Ripple STT 서버 (Conda 환경 기준)

이 문서는 Ripple STT 프로젝트를 Conda 가상환경에서 실행하기 위한 설치 절차를 안내합니다.

---

## ✅ Conda 환경 구성

Anaconda 또는 Miniconda가 설치되어 있어야 합니다.

```bash
conda create -n ripple python=3.10 -y
conda activate ripple
```

---

## 📦 필수 패키지 설치

```bash
pip install -r requirements.txt
```

> `torch`는 GPU 환경에 따라 수동 설치를 권장합니다. 아래를 참고하세요.

---

## 🚀 GPU/CPU 환경별 torch 설치

### ✅ CPU-only 환경

```bash
pip install torch==2.1.0+cpu torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### ✅ CUDA 11.8 환경 (예시)

```bash
pip install torch==2.1.0+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> CUDA 버전에 맞는 패키지를 설치하세요.

---

## 🔧 TensorFlow 설치 (PyKoSpacing용)

`pykospacing` 모듈 사용 시 TensorFlow 설치가 필요합니다.

### ✅ 일반 환경

```bash
pip install tensorflow==2.11
```

### ✅ macOS Apple Silicon (M1/M2/M3)

```bash
pip install tensorflow-macos==2.11
```

> 경우에 따라 `tensorflow-metal`을 함께 설치해 성능을 높일 수 있습니다.

---

## 🧠 모델 및 리소스 구성

`whisper/` 디렉토리에 미리 변환된 CT2 모델을 위치시킵니다:

```
whisper/
├── ct2-whisper-large-v3-turbo-korean-int8/
├── ct2-whisper-medium-ko-zeroth-int8/
└── ct2-whisper-small-ko-int8/
```

모델은 HuggingFace에서 다운로드 후 `ct2-transformers-converter`로 변환하세요.

---

## 🧪 테스트

후처리 모듈 테스트:

```bash
python -m postprocess.run_test
```

또는:

```bash
python postprocess/run_test.py
```

---

## 📁 프로젝트 구조 요약

```
Work/stt/ripple/
├── api/                # FastAPI 엔드포인트
├── model/              # Whisper 모델 추론 모듈
├── postprocess/        # 텍스트 후처리
├── preprocess/audio/   # 오디오 전처리 (VAD)
├── whisper/            # 모델 디렉토리 (Git 제외)
├── uploads/, temp_audio/  # 임시 저장소
└── utils/              # 로깅 및 공용 유틸
```

---

## 🤝 문의

- 담당자: BS
- 시스템 오류는 `logs/debug.log` 또는 `logs/error.log`에서 확인하세요
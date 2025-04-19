# utils/log.py

import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setup_logger(name="app", log_dir="logs", level=logging.DEBUG):
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일 경로
    debug_log = os.path.join(log_dir, "debug.log")
    error_log = os.path.join(log_dir, "error.log")

    # 포맷
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")

    # ✅ 1. Debug 로그: 파일 용량 + 날짜 기준 회전
    debug_handler = TimedRotatingFileHandler(
        debug_log,
        when="midnight",            # 자정 기준 회전
        interval=1,
        backupCount=7,              # 7일치 보관
        encoding="utf-8",
        utc=False                   # 한국 시간 기준
    )
    debug_handler.namer = lambda name: name.replace(".log", "") + ".log"
    debug_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)

    # ✅ 추가 용량 기준 회전
    size_rotate_handler = RotatingFileHandler(
        debug_log,
        maxBytes=100 * 1024 * 1024,  # 100MB
        backupCount=7,
        encoding="utf-8"
    )
    size_rotate_handler.setFormatter(formatter)
    size_rotate_handler.setLevel(logging.DEBUG)

    # ✅ 2. Error 로그 핸들러 (오직 ERROR 이상)
    error_handler = TimedRotatingFileHandler(
        error_log,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=False
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # ✅ 3. 콘솔 출력
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    #console.setLevel(logging.INFO)
    console.setLevel(logging.DEBUG)

    # ✅ Logger 등록
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(debug_handler)
    logger.addHandler(size_rotate_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console)
    logger.propagate = False

    return logger


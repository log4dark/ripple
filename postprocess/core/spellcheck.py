# preprocess/text/spellcheck.py

from pykospacing import Spacing
from hanspell import spell_checker
from utils.log import setup_logger

logger = setup_logger("spellcheck")  # 로거 초기화

spacing = Spacing()

def apply_spacing(text: str) -> str:
    """PyKoSpacing으로 띄어쓰기 보정"""
    try:
        corrected = spacing(text)
        logger.debug(f"🔤 띄어쓰기 보정 완료\n  ⤷ 입력: {text}\n  ⤷ 결과: {corrected}")
        return corrected
    except Exception as e:
        logger.error(f"❌ 띄어쓰기 보정 오류: {e}")
        return text

def apply_spellcheck(text: str) -> str:
    """Hanspell로 맞춤법 검사 및 교정"""
    try:
        result = spell_checker.check(text)
        logger.debug(f"📝 맞춤법 검사 완료\n  ⤷ 입력: {text}\n  ⤷ 결과: {result.checked}")
        return result.checked
    except Exception as e:
        logger.error(f"❌ 맞춤법 검사 오류: {e}")
        return text

def correct_text(text: str, spacing_first=True) -> str:
    """
    전체 맞춤법 보정 파이프라인
    spacing_first=True면 띄어쓰기 → 맞춤법 순서
    """
    #logger.info(f"📥 원문 입력 수신: {text}")
    if spacing_first:
        text = apply_spacing(text)
        #text = apply_spellcheck(text)
    else:
        #text = apply_spellcheck(text)
        text = apply_spacing(text)
    #logger.info(f"📤 최종 교정 결과: {text}")
    return text


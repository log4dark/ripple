import re
from utils.log import setup_logger

logger = setup_logger("punctuation")

def insert_punctuation(text: str) -> str:
    """
    한국어 일반 문장용 구두점 삽입기 (마침표, 쉼표, 물음표, 느낌표 포함)
    """

    logger.debug(f"insert_korean_punctuation start: {text}")

    # ✅ 1. 질문문 처리: 인가요, 습니까 → ?
    text = re.sub(r"(인가요|입니까|습니까)(?![?])", r"\1?", text)

    # ✅ 2. 감탄문 처리: 대단하다 → !
    text = re.sub(r"(정말 대단하다|대박이다|좋다|멋지다)(?![!])", r"\1!", text)

    # ✅ 3. 종결 표현 뒤에 마침표 (없을 때만)
    sentence_ends = ["니다", "다", "요"]
    for ending in sentence_ends:
        pattern = rf"({ending})(?![.?!\w])"
        text = re.sub(pattern, r"\1.", text)

    # ✅ 4. 쉼표 처리
    comma_rules = [
        (" 그리고", ", 그리고"),
        (" 그러나", ", 그러나"),
        (" 하지만", ", 하지만"),
        (" 또는", ", 또는"),
        (" 혹은", ", 혹은"),
        (" 및", ", 및"),
    ]
    for before, after in comma_rules:
        text = text.replace(before, after)

    # ✅ 5. 중복 마침표 제거
    text = re.sub(r"([.?!]){2,}", r"\1", text)

    # ✅ 6. 마침표 뒤 공백 정리
    text = re.sub(r"([.?!])(?=[^\s\n])", r"\1 ", text)

    logger.debug(f"insert_korean_punctuation end: {text}")
    return text

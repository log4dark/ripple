from utils.log import setup_logger

logger = setup_logger("normalize")

def normalize_numbers(text: str) -> str:
    """
    숫자 및 오인식 단어 정규화 + 의미기반 치환
    예: 일 번 → 1번, 선발 → 3번 등
    """
    rules = {
        "에이티": "KT",
        "케이티": "KT",
        "기가 인턴에": "기가 인터넷",
        "기가인턴 에": "기가 인터넷",     # ✅ 이거 추가
        "기가인턴에": "기가 인터넷",      # ✅ 이것도 함께 추가
        "시시티비": "CCTV",
        "티비": "TV",
        "유선상품은": "유선 상품은",
        "일 번": "1번",
        "이 번": "2번",
        "선발": "3번",
        "상발": "3번",
        "에이아이로봇": "AI 로봇",
        "에이 아이 로봇": "AI 로봇",
        "창업고객": "창업 고객",
        "가계매장": "가게 매장",
        "입력시간이 지났습니다": "입력 시간이 지났습니다",
        "이용판법": "이용 방법",
        "별표로 눌러주세요": "별표를 눌러주세요",
        "차 끌고 가야지 차로 가면 시 키로인데": "왜 차 끌고 가야지 그러니까 차로 가면 1kg인데"
    }

    logger.debug(f"normalize_numbers start: {text}")

    for wrong, correct in rules.items():
        text = text.replace(wrong, correct)

    logger.debug(f"normalize_numbers end: {text}")
    return text

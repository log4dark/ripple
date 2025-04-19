import re

def apply_templates(text: str) -> str:
    """
    의미 단위로 정해진 템플릿에 맞춰 문장을 구조화함
    - 예: 번호 선택 안내를 하나의 포맷 문장으로 통일
    """
    # 번호 선택 안내 패턴 감지 및 정형화
    if "유선 상품은 1번" in text and "2번" in text and "3번" in text:
        text = re.sub(
            r"유선 상품은 1번.*?2번.*?3번.*?(눌러주세요)?",
            "기가 인터넷, TV 등 유선 상품은 1번, 하이오더, AI 로봇, CCTV 등 창업 고객, 매장 상품은 2번, 휴대폰은 3번을 눌러주세요.",
            text
        )

    return text

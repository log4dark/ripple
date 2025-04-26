from postprocess.core.normalize import normalize_numbers
from postprocess.core.punctuation import insert_punctuation
from utils.log import setup_logger

logger = setup_logger("pipeline")

def run_full_postprocess(text: str, apply_kobart=False) -> str:
    logger.info("STT 후처리 파이프라인 시작")
    logger.debug(f"원문ㅓ:\n{text}")

    # 1. 띄어쓰기 및 맞춤법 보정
    #text = correct_text(text)

    # 2. 숫자 및 단어 의미 치환
    text = normalize_numbers(text)

    # 3. 템플릿 기반 문장 정형화
    #text = apply_templates(text)

    # 4. 구두점 삽입
    text = insert_punctuation(text)

    # 5. 중복 문장 제거
    #text = remove_repetitions(text)

    # 6. KoBART 문장 정리 (선택적)
    #if apply_kobart:
    #    logger.info("✨ KoBART 문장 정리 적용")
    #    text = kobart_summarize(text)

    logger.info("STT 후처리 파이프라인 완료")
    logger.debug(f"최종 결과:\n{text}")
    return text


if __name__ == "__main__":
    raw = """에이티 고객센터입니다 기가 인턴에 티비 등 유선 상품은 일 번 하이 오더 에이아이로봇 시시티비 등 창업고객 가게매장 상품은 이 번 휴대폰은 선발을 눌러주세요 다시 듣기는 별표로 눌러주세요 입력시간이 지났습니다 기가 인턴에 티비 등 유선 상품은 일 번 하이 오더 에이아이로봇 시시티비 등 창업고객 가게매장 상품은 이 번 휴대폰은 선발을 눌러주세요 다시 듣기는 별표로 눌러주세요 차 끌고 가야지 입력시간이 지났습니다 기가 인턴에 티비 등 유선 상품은 일 번 하이 오더 에이아이로봇 시시티비 등 창업고객 가게매장 상품은 이 번 휴대폰은 선발을 눌러주세요 다시 듣기는 별표로 눌러주세요 입력시간이 지났습니다 죄송합니다 이용방법을 확인 후 다시 걸어 주시기 바랍니다 감사합니다 케이티는 항상 고객님과 함께하겠습니다"""
    #raw = """에이째 유 플러스 모바일 고객센터입니다 지금 연결하신 번호는 유선전화 무제한에 해당되지 않는 부가통화입니다 무료통화 휴대폰 일 네 사로 이용하시기 바랍니다 상담 받으실 전화번호 열 한 자리 번호와 우물정자를 눌러 주십시오 가입하지 않은 고객께서는 별표를 눌러 주십시오 두 컨티니우 인 앵글리시 플리스 프레스 파운드 입력 시간이 경고되었습니다 상담 받으실 전화번호 열 한 자리 번호와 우물정자를 눌러 주십시오 가입하지 않은 고객께서는 별표를 눌러 주십시오 두 컨티니우 인 앵글리시 플리스 프레스 파운드 입력 시간이 경고되었습니다 상담 받으실 전화번호 열 한 자리 번호와 우물정자를 눌러 주십시오 가입하지 않은 고객께서는 별표를 눌러 주십시오 두 컨티니우 인 앵글리시 플리스 프레스 파운드 사용 방법을 확인하신 후 다시 걸어 주십시오"""

    #cleaned = run_full_postprocess(raw)
    cleaned = run_full_postprocess(raw, apply_kobart=False)
    #print(cleaned)

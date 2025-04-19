from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

# 모델 & 토크나이저 불러오기
tokenizer = PreTrainedTokenizerFast.from_pretrained("digit82/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")

def kobart_summarize(text):
    # 인코딩
    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)

    # 생성
    summary_ids = model.generate(
        input_ids,
        max_length=128,
        num_beams=4,
        early_stopping=True
    )

    # 디코딩
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 예시 문장
raw = "에이티 고객센터입니다 기가인턴 에 티비 등 유선상품은 일 번 하이 오더 에이아이로봇 시시티비 등 창업고객 가게매장 상품은 이 번 휴대폰은 선발을 눌러주세요"

# 실행
result = kobart_summarize(raw)
print("KoBART 정리 결과:", result)


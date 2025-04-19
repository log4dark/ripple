from transformers import T5Tokenizer, T5ForConditionalGeneration

# 모델과 토크나이저 불러오기
tokenizer = T5Tokenizer.from_pretrained("KETI-AIR/ke-t5-small")
model = T5ForConditionalGeneration.from_pretrained("KETI-AIR/ke-t5-small")

def t5_summarize(text: str) -> str:
    """
    T5 모델을 이용한 문장 정리 (명령형 prefix 사용)
    예: "문장 정리: ~" → 자연스러운 문장 생성
    """
    prefix = "문장 정리: "
    input_text = prefix + text

    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    output_ids = model.generate(
        input_ids,
        max_length=128,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


if __name__ == "__main__":
    sample = "에이티 고객센터입니다 기가인턴 에 티비 등 유선상품은 일 번 하이 오더 에이아이로봇 시시티비 등 창업고객 가게매장 상품은 이 번 휴대폰은 선발을 눌러주세요"
    print("📝 T5 정리 결과:", t5_summarize(sample))


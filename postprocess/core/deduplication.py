def remove_repetitions(text: str) -> str:
    """문장 중복 제거 (간단한 rule 기반)"""
    import re
    sentences = [s.strip() for s in re.split(r'[.\n]', text) if s.strip()]
    seen = set()
    result = []
    for sentence in sentences:
        if sentence not in seen:
            result.append(sentence)
            seen.add(sentence)
    return ". ".join(result) + "."

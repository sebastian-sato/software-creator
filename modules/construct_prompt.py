def construct_prompt(text_prompt: str) -> list[dict[str, str]]:
    return [{"role":"user","content":text_prompt}]
def if_str_empty_prompt_user(val: str, prompt: str) -> str:
    if val in (None, ""):
        return input(prompt + ": ")
    else:
        return val

def replace_special_characters(text: str) -> str:
    text = text.replace("[SIGINT]", SIGINT)
    text = text.replace("[ESCAPE]", ESCAPE)
    text = text.replace("[END]", END_TRANSMISSION)
    text = text.replace("[UP]", UP)
    text = text.replace("[DOWN]", DOWN)
    text = text.replace("[LEFT]", LEFT)
    text = text.replace("[RIGHT]", RIGHT)
    text = text.replace("[DONE]","")
    text = text.replace("[WAIT]","")
    text = text.replace("`","")
    return text

def between_substr(text: str, a: str, b: str):
    start = text.find(a)
    cut = text[start+len(a):]
    end = cut.find(b)
    cut = cut[:end]
    return cut

def strip_comments(jsonc):
    without_single_line = re.sub(r'(\/\/.*)', '', jsonc) # Remove single line comments
    json = re.sub(r'(\/\**.*\*\/)', '', without_single_line, flags=re.DOTALL) # Remove multi line comments
    return json

def resolve_nonexistent_directories(path):
    folders = path.split("/")[:-1]
    for i in range(len(folders)):
        os.system("mkdir " + "/".join(folders[:i+1]))
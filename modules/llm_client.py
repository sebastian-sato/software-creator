URL = f"http://{SERVER_IP}:{PORT}/{SERVICE_NAME}"

def generate(chat: list[dict], max_tokens: int=4000) -> dict:
    return sendAndRecieve(data={"payload":{"messages":chat}}, url=URL, password=PASSWORD, max_tokens=max_tokens)

def sendAndRecieve(data: dict, url: str, password: str, max_tokens: int=500) -> dict: # Apparently you can do static type checking in Python with mypy, neat!
    try:
        data["pass"] = password
        data["max_tokens"] = max_tokens
        return requests.post(url=url, json=data, timeout=60).json()
    except:
        print("Failed to connect to LLM server! Make sure you entered the correct information in config.json, or check your internet connection!")
        raise ConnectionError

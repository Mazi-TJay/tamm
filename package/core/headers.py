def headers(token: str):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://taman.fun",
        "Referer": "https://taman.fun/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Wallet": token,
    }
    return headers

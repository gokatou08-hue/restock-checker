import requests
import json
import os

URL = "https://www.stormst.com/products/detail/646"
KEYWORD = "<html"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

html = requests.get(URL, headers=headers).text
now = KEYWORD in html

with open("state.json", "r") as f:
    state = json.load(f)

before = state["in_stock"]

if not before and now:
    requests.post(
        WEBHOOK,
        json={"content": f"🎉 @everyone 再入荷しました！\n{URL}"}
    )
    print("再入荷通知を送信しました")
else:
    print("変化なし")

state["in_stock"] = now
with open("state.json", "w") as f:
    json.dump(state, f)




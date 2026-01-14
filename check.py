import requests, json, os

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 設定読み込み
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

items = config["items"]

# state初期化
if not os.path.exists("state.json"):
    state = {item["name"]: False for item in items}
    with open("state.json", "w") as f:
        json.dump(state, f)

with open("state.json", "r") as f:
    state = json.load(f)

for item in items:
    name = item["name"]
    url = item["url"]
    keyword = item["keyword"]

    html = requests.get(url, headers=HEADERS, timeout=15).text
    now = keyword in html
    before = state.get(name, False)

    if not before and now:
        requests.post(WEBHOOK, json={
            "content": f"🎉 **{name}** が再入荷しました！\n{url}"
        })

    state[name] = now

with open("state.json", "w") as f:
    json.dump(state, f)

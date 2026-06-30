import json
import requests

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def send(msg):
    requests.post(config["discord_webhook"], json={"content": msg})

def get_price(item_name):
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={item_name}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except:
        return None

    if not data.get("success"):
        return None

    price = data.get("lowest_price")
    if not price:
        return None

    price = (
        price.replace("zł", "")
        .replace("$", "")
        .replace(",", ".")
        .strip()
    )

    try:
        return float(price)
    except:
        return None


for item in config["items"]:
    name = item["url_name"]
    price = get_price(name)

    if price is None:
        send(f"STEAM: {name} = ❌ brak danych (None)")
    else:
        send(f"STEAM: {name} = {price}")

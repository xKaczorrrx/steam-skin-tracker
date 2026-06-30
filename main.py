import json
import requests
import urllib.parse

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def send(msg):
    requests.post(config["discord_webhook"], json={"content": msg})

def get_price(item_name):
    url_name = urllib.parse.quote(item_name)

    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={url_name}"

    r = requests.get(url)
    data = r.json()

    if not data.get("success"):
        return None

    price = data.get("lowest_price")
    if not price:
        return None

    price = price.replace("zł", "").replace("$", "").replace(",", ".").strip()

    try:
        return float(price)
    except:
        return None


for item in config["items"]:
    name = item["url_name"]
    price = get_price(name)

    send(f"STEAM: {name} = {price}")

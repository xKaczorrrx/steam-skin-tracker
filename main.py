import json
import requests
import urllib.parse

with open("config.json", "r") as f:
    config = json.load(f)

WEBHOOK = config["https://discord.com/api/webhooks/1521552130920681564/SZd5mTBSMWum4q5rWD3OdXzOPVaTu2lCLtQpx_vXeFpa3qsVt1Q57kWc6jtzwRfxwzU7"]

def get_price(name):
    url = f"https://steamcommunity.com/market/priceoverview/?currency=6&appid=730&market_hash_name={urllib.parse.quote(name)}"
    r = requests.get(url).json()

    if r.get("success"):
        price = r.get("lowest_price") or r.get("median_price")
        if price:
            return float(price.replace("zł","").replace(" ","").replace(",","."))
    return None

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

for item in config["items"]:
    price = get_price(item["url_name"])
    if price and price >= item["price_limit"]:
        send(f"🔔 {item['name']}\n💰 {price} zł\n🎯 próg: {item['price_limit']} zł")

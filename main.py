import json
import requests
import urllib.parse
import time

with open("config.json", "r") as f:
    config = json.load(f)

WEBHOOK = config["discord_webhook"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

last_prices = {}

def get_price(name):
    url = f"https://steamcommunity.com/market/priceoverview/?currency=6&appid=730&market_hash_name={urllib.parse.quote(name)}"
    r = requests.get(url, headers=HEADERS).json()

    if r.get("success"):
        price = r.get("lowest_price") or r.get("median_price")
        if price:
            price = price.replace("zł", "").replace(" ", "").replace(",", ".")
            try:
                return float(price)
            except:
                return None
    return None

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

while True:
    for item in config["items"]:
        name = item["url_name"]
        price = get_price(name)

        if price is None:
            continue

        last = last_prices.get(name)

        if last is not None and price > last:
            send(f"📈 CENA WZROSŁA!\n{item['name']}\n💰 {last} → {price} zł")

        if price >= item["price_limit"]:
            send(f"🔔 {item['name']}\n💰 {price} zł\n🎯 próg: {item['price_limit']} zł")

        last_prices[name] = price

    time.sleep(300)

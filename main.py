import requests
import urllib.parse

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1521552130920681564/SZd5mTBSMWum4q5rWD3OdXzOPVaTu2lCLtQpx_vXeFpa3qsVt1Q57kWc6jtzwRfxwzU7"

items = [
    {
        "name": "AK-47 Redline",
        "url_name": "AK-47 | Redline (Field-Tested)",
        "price_limit": 160
    },
    {
        "name": "USP-S | Cyrex",
        "url_name": "USP-S | Cyrex (Minimal Wear)",
        "price_limit": 63
    },
    {
        "name": "P90 | Reef Grief",
        "url_name": "P90 | Reef Grief (Factory New)",
        "price_limit": 10
    }
]


def get_price(market_name):
    url_name = urllib.parse.quote(market_name, safe="")

    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={url_name}"

    r = requests.get(url, timeout=10)
    data = r.json()

    print("RAW:", data)

    if data.get("success") and data.get("lowest_price"):
        price_str = data["lowest_price"].replace("zł", "").replace(",", ".").strip()
        return float(price_str)
    else:
        return None


def send_discord(name, price, limit):
    msg = {
        "content": f"🚨 PROG PRZEKROCZONY!\n{name}\n💰 {price} zł\n🎯 próg: {limit} zł"
    }
    requests.post(DISCORD_WEBHOOK, json=msg)


def main():
    for item in items:
        price = get_price(item["url_name"])

        if price is None:
            print(f"{item['name']} = ❌ brak danych")
            continue

        print(f"{item['name']} = {price} zł")

        if price <= item["price_limit"]:
            send_discord(item["name"], price, item["price_limit"])


if __name__ == "__main__":
    main()

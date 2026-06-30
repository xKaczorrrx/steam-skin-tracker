import json
import requests

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

def get_price(url_name: str):
    # na razie test
    return 1.0

def send(msg: str):
    webhook = config["discord_webhook"]
    requests.post(webhook, json={"content": msg})

for item in config["items"]:
    name = item["url_name"]
    price = get_price(name)

    send(f"TEST: {name} = {price}")

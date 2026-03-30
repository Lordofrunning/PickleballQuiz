import requests
import csv

url = "https://thepickleballstudio.notion.site/api/v3/queryCollection"

payload = {
    "collectionId": "3c5f9880-81b2-4ace-b83c-46374c8281c0",
    "collectionViewId": "15aa3cef-c76a-80b9-b4ba-000c2df1ede5",
    "loader": {
        "limit": 1000
    }
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("Fetching paddles...")

r = requests.post(url, json=payload, headers=headers)

data = r.json()

blocks = data["recordMap"]["block"]

paddles = []

for block_id, block in blocks.items():

    value = block.get("value", {})
    props = value.get("properties", {})

    if not props:
        continue

    paddle = {
        "brand": props.get("o{Nq", [[""]])[0][0] if "o{Nq" in props else "",
        "model": props.get("{S<Z", [[""]])[0][0] if "{S<Z" in props else "",
        "price": props.get("`R^P", [[""]])[0][0] if "`R^P" in props else "",
        "swing_weight": props.get("Lfds", [[""]])[0][0] if "Lfds" in props else "",
        "twist_weight": props.get("KmOn", [[""]])[0][0] if "KmOn" in props else ""
    }

    if paddle["model"]:
        paddles.append(paddle)

print("Paddles found:", len(paddles))

with open("paddles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["brand","model","price","swing_weight","twist_weight"]
    )
    writer.writeheader()
    writer.writerows(paddles)

print("Saved paddles.csv")
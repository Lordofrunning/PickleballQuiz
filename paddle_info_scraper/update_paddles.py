import requests
import csv
import json

url = "https://thepickleballstudio.notion.site/api/v3/queryCollection?src=initial_load"

# Authentication cookies from browser session
# Get these from: DevTools > Network > queryCollection request > Headers > Cookie
NOTION_COOKIES = {
    "notion_browser_id": "a1220f43-7128-4266-ae7b-5a43608f1928",
    "device_id": "332d872b-594c-81f8-8bd6-003b6bec109f",
    "notion_check_cookie_consent": "false"
}

payload = {
    "collectionView": {
        "id": "15aa3cef-c76a-80b9-b4ba-000c2df1ede5",
        "spaceId": ""
    },
    "collectionViewBlock": {
        "id": "5bdf3ee7-52c9-40eb-a864-a81bc3281164",
        "spaceId": ""
    },
    "clientType": "notion_app",
    "isFullScreen": True,
    "isMobile": False,
    "userTimeZone": "America/Denver"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Content-Type": "application/json",
    "notion-client-version": "23.13.20260330.1621",
    "origin": "https://thepickleballstudio.notion.site",
    "referer": "https://thepickleballstudio.notion.site/5bdf3ee752c940eba864a81bc3281164?v=15aa3cefc76a80b9b4ba000c2df1ede5"
}

print("Fetching all paddles (with pagination)...")

all_paddles = []
all_records = {"block": {}, "__version__": 3}
offset = 0
page = 1

while True:
    # Create payload for this page with offset
    current_payload = payload.copy()
    current_payload["offset"] = offset
    
    print(f"  Fetching page {page} (offset {offset})...")
    r = requests.post(url, json=current_payload, headers=headers, cookies=NOTION_COOKIES)
    
    if r.status_code != 200:
        print(f"ERROR: Status {r.status_code}")
        break
    
    data = r.json()
    
    if "recordMap" not in data or "block" not in data["recordMap"]:
        print(f"ERROR: No data on page {page}")
        break
    
    # Merge records
    all_records["block"].update(data["recordMap"]["block"])
    
    # Get block IDs for this page
    block_ids = []
    if "result" in data and "reducerResults" in data["result"]:
        reducer_results = data["result"]["reducerResults"]
        if "collection_group_results" in reducer_results:
            collection_results = reducer_results["collection_group_results"]
            block_ids = collection_results.get("blockIds", [])
            has_more = collection_results.get("hasMore", False)
            print(f"    Got {len(block_ids)} paddles, hasMore={has_more}")
    
    if not has_more or not block_ids:
        break
    
    page += 1
    offset += 50
    if page > 15:  # Safety limit (15 * 50 = 750 paddles)
        print("Reached page limit, stopping")
        break

records = all_records

paddles = []

# Extract all paddles from all pages
for block_id in records["block"].keys():
    if block_id == "__version__":
        continue
        
    block = records["block"][block_id]
    
    value = block.get("value", {}).get("value", {})
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
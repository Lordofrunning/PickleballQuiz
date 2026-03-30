import requests
import csv
import json

url = "https://thepickleballstudio.notion.site/api/v3/queryCollection?src=initial_load"

# Authentication cookies from browser session
# NOTE: Cookies will expire! If script fails, extract fresh cookies:
# 1. Open https://thepickleballstudio.notion.site in your browser
# 2. Press F12 > Network tab
# 3. Scroll down on the page to trigger a queryCollection request
# 4. Find the request "queryCollection" in Network tab
# 5. Click it > Headers section > scroll down to "Cookie" header
# 6. Copy the cookie values and update NOTION_COOKIES below with:
#    - notion_browser_id
#    - device_id  
#    - notion_check_cookie_consent
# 7. Save and run the script again
NOTION_COOKIES = {
    "notion_browser_id": "a1220f43-7128-4266-ae7b-5a43608f1928",
    "device_id": "332d872b-594c-81f8-8bd6-003b6bec109f",
    "notion_check_cookie_consent": "false"
}

payload = {
    "clientType": "notion_app",
    "collectionView": {
        "id": "15aa3cef-c76a-80b9-b4ba-000c2df1ede5",
        "spaceId": "506f2e06-5b8c-449b-8da1-caa63bc40912"
    },
    "source": {
        "type": "collection",
        "id": "3c5f9880-81b2-4ace-b83c-46374c8281c0",
        "spaceId": "506f2e06-5b8c-449b-8da1-caa63bc40912"
    },
    "loader": {
        "userTimeZone": "America/Denver",
        "archiveStatus": "NON_ARCHIVED",
        "searchQuery": "",
        "sort": [
            {
                "property": "o{Nq",
                "direction": "ascending"
            }
        ],
        "propertyAggregations": [
            {
                "type": "aggregation",
                "aggregation": {
                    "property": "title",
                    "aggregator": "count"
                }
            }
        ],
        "reducers": {
            "collection_group_results": {
                "type": "results",
                "limit": 50
            }
        }
    }
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Content-Type": "application/json",
    "notion-client-version": "23.13.20260330.1621",
    "origin": "https://thepickleballstudio.notion.site",
    "referer": "https://thepickleballstudio.notion.site/5bdf3ee752c940eba864a81bc3281164?v=15aa3cefc76a80b9b4ba000c2df1ede5"
}

print("Fetching all paddles (incrementally loading)...")

all_records = {"block": {}, "__version__": 3}
current_limit = 50
page = 1

while True:
    print(f"  Fetching with limit {current_limit}...")
    
    # Update limit in payload for this request
    current_payload = {
        "clientType": payload["clientType"],
        "collectionView": payload["collectionView"],
        "source": payload["source"],
        "loader": {
            "userTimeZone": payload["loader"]["userTimeZone"],
            "archiveStatus": payload["loader"]["archiveStatus"],
            "searchQuery": payload["loader"]["searchQuery"],
            "sort": payload["loader"]["sort"],
            "propertyAggregations": payload["loader"]["propertyAggregations"],
            "reducers": {
                "collection_group_results": {
                    "type": "results",
                    "limit": current_limit
                }
            }
        }
    }
    
    r = requests.post(url, json=current_payload, headers=headers, cookies=NOTION_COOKIES)
    
    if r.status_code != 200:
        print(f"ERROR: Status {r.status_code}")
        break
    
    data = r.json()
    
    if "recordMap" not in data or "block" not in data["recordMap"]:
        print(f"ERROR: No data at limit {current_limit}")
        break
    
    # Merge records
    new_blocks = data["recordMap"]["block"]
    all_records["block"].update(new_blocks)
    
    # Get result info
    block_ids = []
    has_more = False
    if "result" in data and "reducerResults" in data["result"]:
        reducer_results = data["result"]["reducerResults"]
        if "collection_group_results" in reducer_results:
            collection_results = reducer_results["collection_group_results"]
            block_ids = collection_results.get("blockIds", [])
            has_more = collection_results.get("hasMore", False)
    
    print(f"    Got {len(new_blocks)} blocks, blockIds count={len(block_ids)}, total blocks={len(all_records['block'])}, hasMore={has_more}")
    
    if not has_more or not block_ids:
        print("    No more results")
        break
    
    page += 1
    current_limit += 50  # Increase limit by 50 each time
    if current_limit > 1000:  # Safety limit
        print("Reached max limit, stopping")
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
        "weight": props.get("C{vB", [[""]])[0][0] if "C{vB" in props else "",
        "core_thickness_mm": props.get("bEnc", [[""]])[0][0] if "bEnc" in props else "",
        "grip_length": props.get("fSUz", [[""]])[0][0] if "fSUz" in props else "",
        "rpm": props.get("kKLs", [[""]])[0][0] if "kKLs" in props else "",
        "shape": props.get("RLTk", [[""]])[0][0] if "RLTk" in props else "",
        "face_material": props.get("Sk;V", [[""]])[0][0] if "Sk;V" in props else "",
        "core_material": props.get("lvSm", [[""]])[0][0] if "lvSm" in props else "",
        "swing_weight": props.get("Lfds", [[""]])[0][0] if "Lfds" in props else "",
        "twist_weight": props.get("KmOn", [[""]])[0][0] if "KmOn" in props else ""
    }

    if paddle["model"]:
        paddles.append(paddle)

print("Paddles found:", len(paddles))

with open("paddles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["brand","model","price","weight","core_thickness_mm","grip_length","rpm","shape","face_material","core_material","swing_weight","twist_weight","year"]
    )
    writer.writeheader()
    writer.writerows(paddles)

print("Saved paddles.csv")
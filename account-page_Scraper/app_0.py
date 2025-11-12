from parsel import Selector
import requests
import json
import time
import json
import json
from datetime import datetime
def get_data(url):
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.108", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    max_try = 3
    err_list = None
    response = None

    for i in range(max_try):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                response = resp
                break
            else:
                err_list = Exception(f"Non-200 status code: {resp.status_code}")
        except Exception as e:
            err_list = e
            time.sleep(1)

    if response is None:
        raise err_list if err_list else Exception("Request failed")

    selector = Selector(text=response.text)
    
    scripts = selector.css('script[type="application/json"][data-content-len]::text').getall()
    return scripts

urls = [
    "https://www.facebook.com/LeonardoDiCaprio",
    "https://www.facebook.com/zuck",
    "https://www.facebook.com/cristiano",
    "https://web.facebook.com/leomessi"
]

all_profiles = []  # সব প্রোফাইলের ডেটা রাখবে

for url in urls:
    print(f"\n🔍 Processing: {url}")
    script = get_data(url)



    def contains_best_description(obj):
        """Recursively check if 'best_description' exists anywhere inside a JSON object"""
        if isinstance(obj, dict):
            if "aggregated_ranges" in obj:
                return True
            return any(contains_best_description(v) for v in obj.values())
        elif isinstance(obj, list):
            return any(contains_best_description(i) for i in obj)
        return False

    # Step 2: Each item might be a string, so convert each to proper JSON if needed
    parsed_data = []
    for item in script:
        if isinstance(item, str):
            try:
                parsed_data.append(json.loads(item))
            except json.JSONDecodeError:
                continue
        elif isinstance(item, dict):
            parsed_data.append(item)



    import json
    filtered = [item for item in parsed_data if contains_best_description(item)]
    data = filtered 


    def find_value(obj, target_path):
        """Recursively find value in nested JSON, ignoring numeric indexes"""
        if not target_path:
            return None

        key = target_path[0]

        # If current object is dict
        if isinstance(obj, dict):
            if key in obj:
                if len(target_path) == 1:
                    return obj[key]
                return find_value(obj[key], target_path[1:])
            # search inside all values (for dynamic numeric keys)
            for v in obj.values():
                result = find_value(v, target_path)
                if result is not None:
                    return result

        # If current object is list
        elif isinstance(obj, list):
            for item in obj:
                result = find_value(item, target_path)
                if result is not None:
                    return result

        return None


    # ===============================
    # 🔹 1. Profile URL + Name extract
    # ===============================

    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "url"
    ]

    user_url = find_value(data, path)

    if user_url:
        print("✅ User URL:", user_url)

        try:
            profile_name = user_url.strip("/").split("/")[-1]
            print("🏷️ Profile Name:", profile_name)
        except Exception:
            print("⚠️ Couldn't extract profile name from URL.")
    else:
        print("⚠️ User URL not found.")




    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "profile_social_context",
        "content"
    ]

    content = find_value(data, path)

    # Following Text
    if isinstance(content, list) and len(content) > 1:
        following_text = content[1].get("text", {}).get("text")
        print("✅ Following Text:", following_text)
    else:
        print("⚠️ Following not found.")

    # Followers Text
    if isinstance(content, list) and len(content) > 0:
        followers_text = content[0].get("text", {}).get("text")
        print("✅ Followers:", followers_text)
    else:
        print("⚠️ Followers not found.")



    # ===============================
    # 🔹 3. Collection ID extract
    # ===============================

    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "profile_tabs",
        "profile_user",
        "timeline_nav_app_sections",
        "edges"
    ]

    edges = find_value(data, path)

    if isinstance(edges, list) and edges:
        node_id = edges[0].get("node", {}).get("all_collections", {}).get("nodes", [])[0].get("id")
        print("✅ First Collection ID:", node_id)
    else:
        print("⚠️ No collection ID found.")

    path = [
        "result",
        "data",
        "user",
        "id"
    ]

    user_id = find_value(data, path)

    if user_id:
        print("✅ User ID:", user_id)
    else:
        print("⚠️ User ID not found.")


    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "profile_picture_for_sticky_bar",
        "uri"
    ]

    profile_pic_url = find_value(data, path)

    if profile_pic_url:
        print("✅ Profile Picture URL:", profile_pic_url)
    else:
        print("⚠️ Profile Picture URL not found.")    



    profile_social_uri = find_value(data, path)

    if profile_social_uri:
        print("✅ Profile Social followers URI:", profile_social_uri)
    else:
        print("⚠️ Social Context URI not found.")    


    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "profile_social_context",
        "content"
    ]

    content_list = find_value(data, path)

    if isinstance(content_list, list) and len(content_list) > 1:
        uri_value = content_list[1].get("uri")
        if uri_value:
            print("✅ Profile Following", uri_value)
        else:
            print("⚠️ URI key not found in Following")

    path = [
        "result",
        "data",
        "user",
        "profile_header_renderer",
        "user",
        "profile_social_context",
        "content"
    ]

    content_list = find_value(data, path)

    if isinstance(content_list, list) and len(content_list) > 1:
        uris_value = content_list[0].get("uri")
        if uris_value:
            print("✅ Profile Following", uris_value)
        else:
            print("⚠️ URI key not found in Following")
    

    output_data = {
        "user_url": user_url,
        "profile_name": profile_name if user_url else None,
        "followers": followers_text if 'followers_text' in locals() else None,
        "following": following_text if 'following_text' in locals() else None,
        "followers_uri":  uris_value,
        "following_uri": uri_value,
        "collection_id": node_id if 'node_id' in locals() else None,
        "user_id": user_id,
        "profile_picture_url": profile_pic_url
    }


    
    all_data = []
    all_data.append(output_data)

 
    all_profiles.append(output_data)

    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=4)

    print(f"\n💾 Saved {len(all_profiles)} profiles to output.json successfully!")




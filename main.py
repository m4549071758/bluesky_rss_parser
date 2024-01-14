import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

did = "YOUR_DID_HERE" # did:plc:xxxxxxxxxxxxxxxx 
url = f"https://bsky.app/profile/{did}/rss"

response = requests.get(url)

if response.status_code == 200:
    # XMLパース
    root = ET.fromstring(response.content)

    # アイテムストア
    items = []

    for item in root.findall(".//item"):
        link = item.find("link").text
        pub_date_str = item.find("pubDate").text

        # 時間情報の抽出
        pub_date_parts = pub_date_str.split()
        day, month, year, time = pub_date_parts[0], pub_date_parts[1], pub_date_parts[2], pub_date_parts[3]

        # 月を略語表記から数値表記に変換
        month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        month = month_dict[month]

        # datetimeオブジェクトに変換し、timedeltaで日本時間に変更
        pub_date = datetime.strptime(f"{year}-{month}-{day} {time}", "%y-%m-%d %H:%M") + timedelta(hours=9)
        formatted_pub_date = pub_date.strftime("%Y-%m-%d %H:%M")

        # 画像のみの場合など、descriptionが存在しない場合は"No description available"を挿入
        description_element = item.find("description")
        description = description_element.text if description_element is not None else "No description available"

        items.append({"link": link, "description": description, "pub_date": formatted_pub_date})

    # 各アイテムをpub_dateの降順にソート
    sorted_items = sorted(items, key=lambda x: x["pub_date"], reverse=True)

    for item in sorted_items:
        print(f"Link: {item['link']}")
        print(f"Description: {item['description']}")
        print(f"Pub Date (JST): {item['pub_date']}")
        print("-" * 40)

else:
    print(f"データの取得に失敗しました。 ステータスコード: {response.status_code}")

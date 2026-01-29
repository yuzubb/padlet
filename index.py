import requests
import xml.etree.ElementTree as ET
import time

# 提供されたフィードURL
FEED_URL = "https://padlet.com/padlets/hdkwd3vuxun3qzr2/feed.xml?token=TTNCSFVEQkhTVmN3WlhSYVR6QnpZVWN3VVhBNU5WSlBaM1pFUkdWc2RETm1OM0pYWVRacFkyVllSM2RyVWxOdGRucHBRWEEwTjFFMFdUTnRjbkJQWmxrMksxbFpUVmhRWW1neFRsVndNbk53U21RNFFtVnlhVEpoWm5JM2JIVnZTbTFsYlhOU2NUSkpORms5TFMxVVVIaHlOblJXYjFsRlkyOXFOWFZTZUVJck5FTlJQVDA9LS05MDEwNzA2MmU1YjhkYTkzMzQ1OGU2MjFlMjFiZjIxODRhOTJjNDBi"

# 名前空間の定義
NS = {'atom': 'http://www.w3.org/2005/Atom'}

def get_post_ids():
    try:
        response = requests.get(FEED_URL, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        # entryタグ内の id をすべて取得してセットで返す
        entries = root.findall('atom:entry', NS)
        posts = {}
        for entry in entries:
            post_id = entry.find('atom:id', NS).text
            title = entry.find('atom:title', NS).text or "無題"
            posts[post_id] = title
        return posts
    except Exception as e:
        print(f"取得エラー: {e}")
        return None

def main():
    print("--- Padlet監視開始 ---")
    known_posts = get_post_ids()
    
    if known_posts is None:
        print("初期データの取得に失敗しました。終了します。")
        return

    print(f"現在の投稿数: {len(known_posts)}")

    while True:
        time.sleep(60)  # 60秒ごとにチェック
        current_posts = get_post_ids()
        
        if current_posts is not None:
            # 既知のIDリストにない新しいIDを探す
            new_ids = set(current_posts.keys()) - set(known_posts.keys())
            
            if new_ids:
                print(f"\n【新着通知】{len(new_ids)} 件の新しい投稿があります！")
                for nid in new_ids:
                    print(f"・タイトル: {current_posts[nid]}")
                known_posts = current_posts
            else:
                print(".", end="", flush=True) # 変化なしの目印

if __name__ == "__main__":
    main()

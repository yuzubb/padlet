from urllib.request import Request, urlopen
import xml.dom.minidom
import json

# 設定
FEED_URL = "https://padlet.com/padlets/hdkwd3vuxun3qzr2/feed.xml?token=TTNCSFVEQkhTVmN3WlhSYVR6QnpZVWN3VVhBNU5WSlBaM1pFUkdWc2RETm1OM0pYWVRacFkyVllSM2RyVWxOdGRucHBRWEEwTjFFMFdUTnRjbkJQWmxrMksxbFpUVmhRWW1neFRsVndNbk53U21RNFFtVnlhVEpoWm5JM2JIVnZTbTFsYlhOU2NUSkpORms5TFMxVVVIaHlOblJXYjFsRlkyOXFOWFZTZUVJck5FTlJQVDA9LS05MDEwNzA2MmU1YjhkYTkzMzQ1OGU2MjFlMjFiZjIxODRhOTJjNDBi"

def handler(request):
    try:
        # フィード取得
        req = Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            xml_str = response.read()
        
        dom = xml.dom.minidom.parseString(xml_str)
        entries = dom.getElementsByTagName('entry')
        
        current_posts = []
        for entry in entries:
            title_node = entry.getElementsByTagName('title')[0].firstChild
            title = title_node.nodeValue if title_node else "無題"
            current_posts.append(title)

        # ログへの出力（VercelのDashboardから確認可能）
        print(f"Check successful. Found {len(current_posts)} posts.")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "ok", "count": len(current_posts), "latest": current_posts[0] if current_posts else None}, ensure_ascii=False)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

from urllib.request import Request, urlopen
import xml.dom.minidom
import json
import time
from http.server import BaseHTTPRequestHandler

FEED_URL = "https://padlet.com/padlets/hdkwd3vuxun3qzr2/feed.xml?token=TTNCSFVEQkhTVmN3WlhSYVR6QnpZVWN3VVhBNU5WSlBaM1pFUkdWc2RETm1OM0pYWVRacFkyVllSM2RyVWxOdGRucHBRWEEwTjFFMFdUTnRjbkJQWmxrMksxbFpUVmhRWW1neFRsVndNbk53U21RNFFtVnlhVEpoWm5JM2JIVnZTbTFsYlhOU2NUSkpORms5TFMxVVVIaHlOblJXYjFsRlkyOXFOWFZTZUVJck5FTlJQVDA9LS05MDEwNzA2MmU1YjhkYTkzMzQ1OGU2MjFlMjFiZjIxODRhOTJjNDBi"

def fetch_padlet():
    try:
        req = Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=5) as response:
            dom = xml.dom.minidom.parseString(response.read())
            entries = dom.getElementsByTagName('entry')
            posts = []
            for entry in entries:
                p_id = entry.getElementsByTagName('id')[0].firstChild.nodeValue
                t_node = entry.getElementsByTagName('title')[0].firstChild
                title = t_node.nodeValue if t_node else "無題"
                posts.append({"id": p_id, "title": title})
            return posts
    except:
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 初回取得
        initial_posts = fetch_padlet()
        if initial_posts is None:
            self.send_response(500)
            self.end_headers()
            return

        # Vercelのタイムアウトを考慮し、約8秒間 1秒おきにループ
        new_posts = []
        for _ in range(8):
            time.sleep(1)
            current_posts = fetch_padlet()
            if current_posts and len(current_posts) > len(initial_posts):
                # 増えた分の差分を特定
                old_ids = {p['id'] for p in initial_posts}
                new_posts = [p for p in current_posts if p['id'] not in old_ids]
                break
        
        # レスポンス送信
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        # ブラウザ側でキャッシュされないように設定
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()

        res = {
            "new_arrivals": new_posts,
            "has_new": len(new_posts) > 0,
            "current_count": len(current_posts) if 'current_posts' in locals() else len(initial_posts),
            "timestamp": time.time()
        }
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))

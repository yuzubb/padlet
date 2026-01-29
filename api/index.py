from urllib.request import Request, urlopen
import xml.dom.minidom
import json
from http.server import BaseHTTPRequestHandler

# トークン付きフィードURL
FEED_URL = "https://padlet.com/padlets/hdkwd3vuxun3qzr2/feed.xml?token=TTNCSFVEQkhTVmN3WlhSYVR6QnpZVWN3VVhBNU5WSlBaM1pFUkdWc2RETm1OM0pYWVRacFkyVllSM2RyVWxOdGRucHBRWEEwTjFFMFdUTnRjbkJQWmxrMksxbFpUVmhRWW1neFRsVndNbk53U21RNFFtVnlhVEpoWm5JM2JIVnZTbTFsYlhOU2NUSkpORms5TFMxVVVIaHlOblJXYjFsRlkyOXFOWFZTZUVJck5FTlJQVDA9LS05MDEwNzA2MmU1YjhkYTkzMzQ1OGU2MjFlMjFiZjIxODRhOTJjNDBi"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Padletフィードを取得
            req = Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=10) as response:
                xml_data = response.read()

            dom = xml.dom.minidom.parseString(xml_data)
            entries = dom.getElementsByTagName('entry')

            posts = []
            for entry in entries:
                # 必要な情報を抽出
                post_id = entry.getElementsByTagName('id')[0].firstChild.nodeValue
                title_node = entry.getElementsByTagName('title')[0].firstChild
                title = title_node.nodeValue if title_node else "無題"
                
                # 更新時刻 (updatedタグ)
                updated_node = entry.getElementsByTagName('updated')[0].firstChild
                updated = updated_node.nodeValue if updated_node else ""

                posts.append({
                    "id": post_id,
                    "title": title,
                    "updated": updated
                })

            # JSONでレスポンスを返す
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response_data = {
                "status": "success",
                "count": len(posts),
                "latest_post": posts[0] if posts else None,
                "all_posts": posts
            }
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

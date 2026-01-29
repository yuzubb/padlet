from urllib.request import Request, urlopen
import xml.dom.minidom
import json
from http.server import BaseHTTPRequestHandler

FEED_URL = "https://padlet.com/padlets/hdkwd3vuxun3qzr2/feed.xml?token=UzNwSFpHWXdWSGRqZGpKYWJYUnpjVkZKY0Vnd2EwbHBXV3hrT1VnemJrbDZkV3RzTVhnemQza3ZiR3RFVTJocWMwc3JiRVl3UkRVeFJtczJMeXRRZWs0d1ozSk1lRUpRV2sxTlZHcEphMmhJZUhSRlUwOTJSM2RxZFVrelVtRTVjbWxKTWpaMVRtZEtVRkU5TFMxSlJIRnJNSGsyVTFKWFpVWkJOa3hhVmswMFVVVjNQVDA9LS0xY2E5NWFlOTQwZDllNGU1NDMyNjgzZDc0ZDY5NmRlZWQxN2Y0Y2E5"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            req = Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=10) as response:
                dom = xml.dom.minidom.parseString(response.read())
            
            entries = dom.getElementsByTagName('entry')
            posts = []
            for entry in entries:
                # 投稿者情報 (author)
                author_node = entry.getElementsByTagName('author')[0]
                author_name = author_node.getElementsByTagName('name')[0].firstChild.nodeValue
                # アイコンURL（Padletのフィードに含まれる場合）
                try:
                    icon_url = author_node.getElementsByTagName('uri')[0].firstChild.nodeValue
                except:
                    icon_url = "https://padlet.com/favicon.ico"

                # コンテンツ
                title = entry.getElementsByTagName('title')[0].firstChild.nodeValue if entry.getElementsByTagName('title')[0].firstChild else "無題"
                content = entry.getElementsByTagName('content')[0].firstChild.nodeValue if entry.getElementsByTagName('content')[0].firstChild else ""
                updated = entry.getElementsByTagName('updated')[0].firstChild.nodeValue

                posts.append({
                    "id": entry.getElementsByTagName('id')[0].firstChild.nodeValue,
                    "author": author_name,
                    "author_icon": icon_url,
                    "title": title,
                    "content": content, # HTML形式で入っていることが多い
                    "updated": updated
                })

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(posts, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

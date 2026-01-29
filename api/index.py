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
                xml_data = response.read()
            
            dom = xml.dom.minidom.parseString(xml_data)
            items = dom.getElementsByTagName('item')
            
            posts = []
            for item in items:
                # 各要素のテキストを取得する補助関数
                def get_text(tag_name):
                    nodes = item.getElementsByTagName(tag_name)
                    if nodes and nodes[0].firstChild:
                        return nodes[0].firstChild.nodeValue
                    return ""

                posts.append({
                    "id": get_text("guid"),
                    "author": get_text("author") or "匿名",
                    "title": get_text("title") or "(無題)",
                    "content": get_text("description"),
                    "date": get_text("pubDate"),
                    "link": get_text("link")
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

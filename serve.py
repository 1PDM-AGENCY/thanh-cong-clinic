import http.server
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(("", 8090), handler)
print(f"Serving at http://localhost:8090")
httpd.serve_forever()

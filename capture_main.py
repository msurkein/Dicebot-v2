import http.server
import socketserver
import time
PORT = 8000

class CaptureHandler(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("OK GO\n".encode("UTF8"))

    def do_POST(self):
        cl = self.headers.get("Content-Length")
        b = []
        while len(b) < int(cl):
            b += self.rfile.read(256)
        img_data = b[0:int(cl)]
        with open("test_{}.jpg".format(time.time_ns()), "wb") as jpg_tst:
            jpg_tst.write(bytes(img_data))
        self.send_response(200)
        self.end_headers()
        print("OK")


Handler = CaptureHandler

with socketserver.TCPServer(("", PORT), Handler, False) as httpd:
    print("serving at port", PORT)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    httpd.serve_forever()
    print("OK GO")
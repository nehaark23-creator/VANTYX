import io
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import pandas as pd

from pipeline import process, make_payload


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open("dashboard.html", "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self):
        if self.path != "/triage":
            self._send(404, b"Not found", "text/plain")
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            raw = pd.read_csv(io.BytesIO(self.rfile.read(n)),
                              encoding_errors="replace")
            out = process(raw)
            body = json.dumps(make_payload(out), ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json")
        except Exception as e:
            body = json.dumps({"error": str(e)}).encode("utf-8")
            self._send(400, body, "application/json")


if __name__ == "__main__":
    print("Open http://localhost:8000  (Ctrl+C to stop)")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
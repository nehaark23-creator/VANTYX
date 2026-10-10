import io, json, os
import pandas as pd
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pipeline import process
from build_dashboard import to_rows


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):
        try:
            body = open("dashboard.html", "rb").read()
        except FileNotFoundError:
            body = b"Run: python build_dashboard.py first"
        self._send(200, body, "text/html; charset=utf-8")


    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            raw = pd.read_csv(io.BytesIO(self.rfile.read(n)), encoding_errors="replace")
            body = json.dumps(to_rows(process(raw)), separators=(",", ":")).encode()
            self._send(200, body, "application/json")
        except Exception as e:
            self._send(400, str(e).encode(), "text/plain")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Serving on http://localhost:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
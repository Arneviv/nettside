from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs

ENTRIES = []  # enkel minneliste (ikke persistent)

class handler(BaseHTTPRequestHandler):
    def _send(self, code=200, obj=None):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if obj is not None:
            self.wfile.write(json.dumps(obj, ensure_ascii=False).encode())

    def do_GET(self):
        self._send(200, {"ok": True, "entries": ENTRIES})

    def do_POST(self):
        n = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(n).decode()
        try:
            data = json.loads(raw) if raw else {}
        except Exception:
            data = {k: v[0] for k, v in parse_qs(raw).items()}

        msg = (data.get('msg') or '').strip()
        if not msg:
            return self._send(400, {"ok": False, "error": "mangler msg"})

        ENTRIES.append(msg)
        self._send(200, {"ok": True, "count": len(ENTRIES)})

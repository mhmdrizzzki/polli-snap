"""Polli Snap - optional local backend.

The live app is fully client-side (index.html) and calls the Pollinations
image API directly with the visitor's own key (BYOP):

    POST https://gen.pollinations.ai/v1/images/generations
    {"model": "flux", "prompt": "...", "n": 1, "size": "1024x1024"}

This server exists only for local development: it serves index.html and can
proxy a generation if you prefer not to expose your key in the browser.

    python3 server_snap.py            # http://localhost:8000
    GET /api?q=<prompt>               # legacy helper, returns {url} for a prompt

Note: the old GET https://gen.pollinations.ai/<prompt>?model=flux endpoint was
removed upstream (returns 404). This file uses the current v1 endpoint.
"""
import json
import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

POLLINATIONS_IMAGES = "https://gen.pollinations.ai/v1/images/generations"
POLLINATIONS_CLASSIC = "https://image.pollinations.ai/prompt/"


def classic_url(prompt, seed=42):
    """Free, keyless endpoint. Returns a direct JPEG URL."""
    from urllib.parse import quote
    return POLLINATIONS_CLASSIC + quote(prompt) + "?width=768&height=768&seed=%s&nologo=true" % seed


def generate(prompt, api_key, model="flux", size="1024x1024"):
    """Call the current Pollinations image endpoint. Returns (ok, payload)."""
    body = json.dumps({"model": model, "prompt": prompt, "n": 1, "size": size}).encode()
    req = urllib.request.Request(
        POLLINATIONS_IMAGES,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
            "User-Agent": "polli-snap",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return True, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return False, json.loads(e.read() or b"{}")
        except Exception:
            return False, {"error": {"message": "HTTP %s" % e.code}}
    except Exception as exc:
        return False, {"error": {"message": str(exc)}}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api":
            prompt = parse_qs(u.query).get("q", [""])[0].strip()
            if not prompt:
                return self.respond_json({"error": "empty prompt"})
            key = os.environ.get("POLLINATIONS_API_KEY", "")
            if not key:
                # keyless path: the free classic endpoint serves the JPEG directly
                return self.respond_json({"url": classic_url(prompt), "mode": "classic"})
            ok, payload = generate(prompt, key)
            if not ok:
                return self.respond_json(payload)
            item = (payload.get("data") or [{}])[0]
            return self.respond_json({"url": item.get("url", ""), "raw": payload})
        path = "index.html" if u.path in ("/", "/index.html") else u.path.lstrip("/")
        try:
            with open(path, "rb") as f:
                data = f.read()
        except Exception:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        ctype = "text/html" if path.endswith(".html") else "text/plain"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def respond_json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print("Polli Snap -> http://localhost:%d" % port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()

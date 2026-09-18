# Polli Snap - Text to Image Meme Maker

Fast text-to-image meme generator powered by the **Pollinations image API**.

## Pollinations integration

This app **calls the Pollinations image API** directly:

- **`index.html`** — client: sends the typed prompt to the local `/api` endpoint and renders the returned image in the page.
- **`server_snap.py`** — backend: builds the Pollinations image request and returns the generated-image URL.

The actual Pollinations API call lives in `server_snap.py`:

```python
POLLINATIONS_IMAGE_BASE = "https://gen.pollinations.ai/"
image_url = POLLINATIONS_IMAGE_BASE + quote(prompt) + "?model=flux&nologo=true"
```

Every generation uses `model=flux` on `gen.pollinations.ai`, so the image you see is produced by Pollinations.

## Run locally

```bash
python3 server_snap.py   # serves on :8892
# open http://localhost:8892
```

## Try it

1. Type a meme prompt (or tap a preset), hit Generate.
2. `index.html` fetches `/api?q=<prompt>`.
3. `server_snap.py` builds the Pollinations `gen.pollinations.ai/<prompt>?model=flux` URL.
4. The generated image is shown inline.

Live demo: Polli Snap (image category, no login needed).

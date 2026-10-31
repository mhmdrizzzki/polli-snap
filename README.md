# Polli Snap — Text to Image Meme Maker

Fast text-to-image meme generator powered by the **Pollinations image API**.

[![Made with Pollinations](https://pollinations.ai/badge-made-with.svg)](https://pollinations.ai)

Live: **https://mhmdrizzzki.github.io/polli-snap/** — works with no key, no login.

## How it calls Pollinations

Two paths, same picture. The app picks one per request:

**1. Free, keyless (default)** — the browser loads the JPEG straight from the classic endpoint:

```js
https://image.pollinations.ai/prompt/<url-encoded prompt>?width=768&height=768&seed=<seed>&nologo=true
```

Rate-limited per IP by Pollinations (one image at a time, ~45s apart). No key, no account.

**2. Keyed (optional)** — paste an `sk_...` key from [enter.pollinations.ai](https://enter.pollinations.ai)
into the key field to use every model with no per-IP limit:

```js
POST https://gen.pollinations.ai/v1/images/generations
{ "model": "flux", "prompt": "<prompt>", "n": 1, "size": "1024x1024", "seed": <seed> }
Authorization: Bearer <sk_...>
```

The key stays in `sessionStorage` for that tab and is sent only to `gen.pollinations.ai`.
If a keyed request fails, the app falls back to the free endpoint automatically.

## Run locally

```bash
python3 -m http.server 8000     # static app
# or, with the optional Python proxy:
POLLINATIONS_API_KEY=sk_... python3 server_snap.py
```

## Files

- `index.html` — the whole app (UI + Pollinations API call, client-side BYOP)
- `server_snap.py` — optional local proxy for development; not required for the live app

## Note on the old endpoint

Earlier versions used `GET https://gen.pollinations.ai/<prompt>?model=flux`. That
endpoint was removed upstream (it now returns `404`), which is why image generation
stopped working. This version uses the keyless classic endpoint by default and
`POST /v1/images/generations` when a key is supplied.

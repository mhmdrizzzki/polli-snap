# Polli Snap — Text to Image Meme Maker

Fast text-to-image meme generator powered by the **Pollinations image API**.

[![Made with Pollinations](https://pollinations.ai/badge-made-with.svg)](https://pollinations.ai)

Live: **https://mhmdrizzzki.github.io/polli-snap/**

## Pollinations integration

The app calls the current Pollinations image endpoint directly from the browser,
using the visitor's own key (BYOP — you pay your own Pollen):

**`index.html`**

```js
const r = await fetch('https://gen.pollinations.ai/v1/images/generations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + apiKey,
  },
  body: JSON.stringify({ model: 'flux', prompt, n: 1, size: '1024x1024' }),
});
const { data } = await r.json();
img.src = data[0].url;
```

Model: `flux` · Endpoint: `POST https://gen.pollinations.ai/v1/images/generations`

### Getting a key

Paste an `sk_...` key from [enter.pollinations.ai](https://enter.pollinations.ai)
into the key field at the top of the page. The key is kept in `sessionStorage` for
that tab only and is never sent anywhere except `gen.pollinations.ai`.

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

Earlier versions used `GET https://gen.pollinations.ai/<prompt>?model=flux`.
That endpoint was removed upstream (it now returns `404`), which is why image
generation stopped working. This version uses `POST /v1/images/generations`.

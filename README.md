# jarvisguthrie.com

Website for Jarvis Guthrie — minister, founder of [Saved By Grace House](https://savedbygracehouse.com),
and author of *Step Out of the Boat*. Main call to action: order/reserve the book, with a stated
mission of getting it into every prison in the country.

## Stack

Plain HTML, CSS, and minimal JS — no frameworks or npm dependencies. Same architecture as
[savedbygracehouse.com](https://github.com/chadburmeister/saved-by-grace-house):

```
bodies/              Page content fragments (index, 404)
static/assets/       styles.css, main.js
static/images/       favicon.svg (swap in real photos/logo here)
build.py             Assembles pages with shared header/footer, writes sitemap/robots/llms.txt
pages.py             Per-page titles, meta descriptions, keywords
vercel.json          Build settings, headers, clean URLs
public/              Generated output (git-ignored, rebuilt on every deploy)
```

## Local build

```bash
python3 build.py
python3 -m http.server 8000 --directory public
```

## Deploy

Vercel runs `python3 build.py` automatically on every push (see `vercel.json`). No manual build
step needed.

## TODO before this is fully live

- [ ] Real portrait/family photos and Grace House photo (currently placeholder frames in the hero,
      book, "Why It's Personal," and Grace House spotlight sections)
- [ ] Real book cover art (currently a styled text mockup in the Book section)
- [ ] Formspree (or similar) endpoint — replace `YOUR_FORM_ID` in `bodies/index.html`'s reserve form
- [ ] Point jarvisguthrie.com's DNS at Vercel (currently forwarding via Squarespace)
- [ ] apple-touch-icon / PNG favicon variants (only an SVG favicon exists today)
- [ ] og:image for social share previews

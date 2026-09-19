#!/usr/bin/env python3
"""
Local generator for jarvisguthrie.com.
Assembles plain static HTML into ./public/ from body fragments in ./bodies/.
The REPO ships only the generated plain HTML — no build step on Vercel beyond this script.
"""
import json, pathlib, datetime, shutil

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "public"
BODIES = HERE / "bodies"
STATIC = HERE / "static"
SITE = "https://www.jarvisguthrie.com"
V = "1"

NAV = [
    ("/", "Home", "index"),
    ("/#story", "My Story", ""),
    ("/#ministry", "Ministry", ""),
    ("/#grace-house", "Saved By Grace House", ""),
    ("/#speaking", "Speaking", ""),
    ("/#connect", "Contact", ""),
]

PERSON_LD = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": SITE + "/#jarvis",
    "name": "Jarvis Guthrie",
    "url": SITE + "/",
    "jobTitle": ["Minister", "Author", "Founder"],
    "description": ("Jarvis Guthrie is an ordained minister, prison and reentry chaplain, fatherhood advocate, "
                     "and founder of Saved By Grace House in Jacksonville, Florida. He is the author of "
                     "Step Out of the Boat."),
    "worksFor": {"@type": "Organization", "name": "Saved By Grace House", "url": "https://savedbygracehouse.com"},
    "sameAs": ["https://savedbygracehouse.com"],
}

BOOK_LD = {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "Step Out of the Boat",
    "author": {"@type": "Person", "name": "Jarvis Guthrie"},
    "url": SITE + "/#book",
    "description": ("A memoir by Jarvis Guthrie of prison, purpose, and the leap of faith that changed "
                     "everything — written to reach incarcerated men across America."),
    "bookFormat": "https://schema.org/Paperback",
    "workExample": {"@type": "Book", "isbn": "", "bookEdition": "First Edition"},
}


def head(page):
    ld_blocks = "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(b, separators=(",", ":"))
        for b in page.get("ld", [PERSON_LD, BOOK_LD] if page["file"] == "index" else [])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<meta name="keywords" content="{page['kw']}">
<link rel="canonical" href="{SITE}{page['path']}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Jarvis Guthrie">
<meta property="og:title" content="{page['og_title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{SITE}{page['path']}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{page['og_title']}">
<meta name="twitter:description" content="{page['desc']}">
<meta name="theme-color" content="#002548">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;1,400;1,500&family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={V}">
{ld_blocks}
</head>
<body>
"""


def header(active):
    links = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'      <a href="{href}"{cur}>{label}</a>')
    links = "\n".join(links)
    return f"""<a class="sr" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-header__bar">
    <a class="brand" href="/" aria-label="Jarvis Guthrie — home">
      <span class="brand__mark">JG</span>
      <span class="brand__text">
        <span class="brand__name">JARVIS GUTHRIE</span>
        <span class="brand__sub">MINISTER &amp; AUTHOR</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
      <a class="btn btn--gold" href="/#book">Order the Book</a>
    </nav>
  </div>
</header>

<main id="main">
"""


FOOTER = """</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand"><span class="brand__mark" style="width:38px;height:38px;font-size:13px">JG</span><span>JARVIS GUTHRIE</span></div>
        <p>Minister, mentor, and founder of Saved By Grace House — a Christ-centered shared living community in Jacksonville, Florida. Author of <em>Step Out of the Boat</em>.</p>
        <p class="footer-verse" style="margin-top:16px">&ldquo;An ambassador in bonds.&rdquo;<br>Ephesians 6:20</p>
      </div>
      <div>
        <h4>Explore</h4>
        <div class="footer-links">
          <a href="/#book">The Book</a>
          <a href="/#story">My Story</a>
          <a href="/#ministry">Ministry</a>
          <a href="/#speaking">Speaking</a>
        </div>
      </div>
      <div>
        <h4>Connect</h4>
        <div class="footer-links">
          <a href="https://savedbygracehouse.com" target="_blank" rel="noopener">Saved By Grace House &rarr;</a>
          <a href="/#connect">Contact</a>
          <a href="tel:+19042367081">(904) 236-7081</a>
        </div>
      </div>
      <div>
        <h4>Get The Book</h4>
        <div class="footer-links">
          <a href="/#book">Reserve Your Copy</a>
          <a href="/#book">Sponsor Copies for Prisons</a>
          <a href="/#connect">Bulk / Chaplain Orders</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Jarvis Guthrie. All rights reserved.</span>
      <span>Jacksonville, FL &middot; In partnership with <a href="https://savedbygracehouse.com" target="_blank" rel="noopener" style="color:#B7C8D8">Saved By Grace House</a></span>
    </div>
  </div>
</footer>

<script src="/assets/main.js?v=%s"></script>
</body>
</html>
""" % (V,)


LLMS_TXT = """# Jarvis Guthrie

> Jarvis Guthrie is an ordained minister, prison and reentry chaplain, fatherhood advocate, and
> founder of Saved By Grace House in Jacksonville, Florida. He is the author of the forthcoming
> book "Step Out of the Boat."

## Quick facts

- **Name:** Jarvis Guthrie
- **Roles:** Ordained minister (2024), prison/reentry chaplain, fatherhood advocate, founder of
  Saved By Grace House, author.
- **Book:** "Step Out of the Boat" — a memoir of prison, purpose, and faith, written with the goal
  of reaching incarcerated men across the United States through chaplains and reentry programs.
  The book takes its title from Jarvis's answer, in a podcast interview, to what he would tell
  himself on the morning he woke up handcuffed to a hospital bed at eighteen: "Step out of the
  boat. Put all your faith and trust in God."
- **Location:** Jacksonville, Florida.
- **Background:** Incarcerated 2012–2014 after a single drunken mistake at eighteen. Encountered
  God during his sentence; received his calling to ministry on May 13, 2013, after a three-day
  fast. Released April 2, 2014. Ordained a minister in September 2024.
- **Ministry work:** Weekly prison ministry at Lake City Correctional Institution; death row
  ministry at Florida State Prison (started January 2022). Mentoring men, fatherhood advocacy,
  and family support work tied to the child welfare and criminal justice systems.
- **Saved By Grace House:** A Christ-centered shared living / sober living home in Jacksonville,
  Florida, founded and run by Jarvis and his wife, Jennifer. https://savedbygracehouse.com
- **Contact:** (904) 236-7081

## Usage

This content may be quoted and cited. Please link back to https://www.jarvisguthrie.com.
"""


def build(pages):
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True, exist_ok=True)
    for sub in ("assets", "images"):
        src = STATIC / sub
        if src.exists():
            shutil.copytree(src, ROOT / sub)

    for p in pages:
        body = (BODIES / (p["file"] + ".html")).read_text()
        html = head(p) + header(p["nav"]) + body + FOOTER
        (ROOT / (p["file"] + ".html")).write_text(html)
        print("wrote", p["file"] + ".html", len(html), "bytes")

    today = datetime.date.today().isoformat()
    urls = []
    for p in pages:
        if p["file"] == "404":
            continue
        urls.append(
            f"  <url>\n    <loc>{SITE}{p['path']}</loc>\n    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{p.get('freq','monthly')}</changefreq>\n    <priority>{p.get('prio','0.8')}</priority>\n  </url>"
        )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap)

    ai_agents = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User",
                 "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
                 "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot",
                 "CCBot", "cohere-ai", "Meta-ExternalAgent", "Amazonbot", "DuckAssistBot"]
    robots = ["# Jarvis Guthrie — jarvisguthrie.com",
              "# Minister, author of Step Out of the Boat, founder of Saved By Grace House.",
              "# Search engines and AI answer engines are welcome to index and cite this site.",
              "", "User-agent: *", "Allow: /", ""]
    for a in ai_agents:
        robots += ["User-agent: %s" % a, "Allow: /", ""]
    robots += ["Sitemap: %s/sitemap.xml" % SITE, ""]
    (ROOT / "robots.txt").write_text("\n".join(robots))

    (ROOT / "llms.txt").write_text(LLMS_TXT)
    print("wrote sitemap.xml + robots.txt + llms.txt")


if __name__ == "__main__":
    from pages import PAGES
    build(PAGES)

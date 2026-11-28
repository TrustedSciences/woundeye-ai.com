# CLAUDE.md — WoundEye site (www.woundeye-ai.com)

Static marketing site for WoundEye. Plain HTML/CSS/JS; pushing to `main` redeploys the live site.

## How to work

- Page content lives in `build/pages/<page>.html`. The shared header, menu, "Return" links,
  Explore cards, CTA band and footer live in `build/build.py`.
- **Never hand-edit the generated files** (`index.html`, `404.html`, `<page>/index.html`,
  `sitemap.xml`). Edit `build/pages/*` or `build/build.py`, then run:
  `python3 build/build.py`
- Preview: `python3 -m http.server 8000`, then open http://127.0.0.1:8000
  (run it in a separate Terminal tab so Claude Code stays free).
- Commit the source and the regenerated HTML together, then push to `main`.
- Keep `build/build.py` standard-library only and Python 3.8+ compatible
  (no backslashes inside f-string expressions). Write files as UTF-8 with `\n` line endings.
- Links in page fragments use root paths (`/images/...`); the build makes them relative.
  `404.html` keeps root paths on purpose.

## Wording rules (strict)

- Never say "AI", "artificial intelligence", "agents" or "AI-powered" in site copy, animations
  or captions. Use: **Precision Routing, Worklists, and Clinician Coordination**.
- Never write "WoundSolutionsAI". The company name in the footer is "Wound Solutions AI"
  (legal name, leave as is).
- Brand: **Wound*Eye*** (with "Eye" italicised in the logo/title).
- Statistics need a source: add a footnote linking to `/references/#ref-N`.
- FAQ answers must stay clinically accurate and conservative (seek urgent care for
  signs of infection, etc.). Don't add medical claims without a citation.

## Design rules

- "Sand and ink" style, matching wounds-ai.com.
- **No skewed or rotated images or cards.** Animations may fade or slide only.
- Workflow animations (`js/flow.js`): background is the original #354765 lightened 15%
  (grid #3D517D); product boxes stay cream; the Precision Routing circle is blue #1A55C4.
  If you change the animation background, re-check that the cream boxes stay cream.
- Animations pause when off-screen (IntersectionObserver) — keep that behaviour.

## Handoff package

A developer zip (`woundeye-website.zip`) is made from this repo minus `netlify.toml`,
`.gitignore` and this repo README/CLAUDE.md, with its own handover README.
The handoff package must not mention GitHub or Netlify.

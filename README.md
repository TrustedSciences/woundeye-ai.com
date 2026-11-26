# woundeye-ai.com

Rebuild of [woundeye.com](https://www.woundeye.com), deployed with Netlify at **https://www.woundeye-ai.com**.

## Structure

```
.
├── index.html        # Home page
├── 404.html          # Custom "not found" page
├── css/styles.css    # Site styles
├── js/main.js        # Site scripts
├── images/           # Photos, logos, icons
├── assets/docs/      # PDFs and other downloads
├── robots.txt
└── netlify.toml      # Netlify settings (publish dir, redirects, headers)
```

New pages go in the root as `page-name.html` (or `page-name/index.html` for clean URLs).

## Deployment

Netlify watches the `main` branch. Every push to `main` redeploys the live site automatically;
pull requests get their own preview URL.

- No build step — plain HTML/CSS/JS.
- Domain: `www.woundeye-ai.com` (primary), `woundeye-ai.com` redirects to it.

## Local preview

Open `index.html` in a browser, or run `npx serve .` from this folder.

## Pages and how they are built

The site has a short home page plus separate pages for its key areas:

| Page | URL |
|---|---|
| Home | `/` |
| How it works | `/how-it-works/` |
| Interactive body map | `/body-map/` |
| AssureStage | `/assurestage/` |
| Patients & caregivers | `/patients-caregivers/` |
| Clinicians | `/clinicians/` |
| Employers & health plans | `/employers-health-plans/` |
| References | `/references/` |

Each page's content lives in `_build/pages/<page>.html`. The shared header, menu,
"Return" links, Explore cards and footer live in `_build/build.py`. After editing,
run `python3 _build/build.py` from the repo root and commit the generated HTML.

#!/usr/bin/env python3
"""Build the WoundEye site.

Each page's main content lives in build/pages/<slug>.html. This script wraps
it in the shared header, menu and footer and writes the published HTML:
  home -> index.html, 404 -> 404.html, every other page -> <slug>/index.html
It also writes sitemap.xml.

All internal links and asset paths in the output are relative, so the site
works from the top level of a domain or from any subfolder. Write them in the
page files as root paths (for example /images/logo.png or /body-map/); the
build converts them.

Run from the site folder:  python3 build/build.py
Needs Python 3.8 or later and nothing else (standard library only).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGES = os.path.join(HERE, 'pages')
SITE = 'https://www.woundeye-ai.com'

USE_CASES = [
    ('patients-caregivers', 'Patients &amp; caregivers'),
    ('clinicians', 'Clinicians'),
    ('employers-health-plans', 'Employers &amp; health plans'),
]

# slug: (browser title, description, menu key, back link, uses animation)
META = {
    'home': ('WoundEye — Catch it early. Heal it sooner.',
             "Photograph a wound at home. A clinician reviews it and sends plain-language guidance back the same day. iOS, Android and web.",
             None, None, False),
    'how-it-works': ('How it works | WoundEye',
                     'From your mobile to a clinician’s answer: capture, locate, clinical review and same-day guidance, plus the five platform modules and integrations.',
                     'how', 'main', False),
    'body-map': ('Interactive body map | WoundEye',
                 'Tap the body, open the close-up and pin the exact wound site, so every wound is tracked visit after visit.',
                 'body', 'main', False),
    'assurestage': ('AssureStage Clinical Wound Assessments | WoundEye',
                    'The certified wound specialists behind every WoundEye answer: type and stage, infection screening and follow-up.',
                    'assure', 'main', False),
    'patients-caregivers': ('For patients and caregivers | WoundEye',
                            'Photograph a wound at home and get a certified wound specialist’s answer the same day.',
                            'who', 'uses', True),
    'clinicians': ('For clinicians | WoundEye',
                   'From worklist to signed assessment: precision routing handles intake so clinicians focus on clinical judgement.',
                   'who', 'uses', True),
    'employers-health-plans': ('For employers and health plans | WoundEye',
                               'Two paths for the same wound: seen late at high cost, or seen the same day with WoundEye.',
                               'who', 'uses', True),
    'references': ('References | WoundEye', 'Sources for the figures used on the WoundEye site.', None, 'main', False),
    '404': ('Page not found | WoundEye', 'The page you were looking for has moved or does not exist.', None, None, False),
}

CURRENT = ' aria-current="page"'


def cur(on):
    return CURRENT if on else ''

FEATURES = [
    ('how-it-works', 'How it works', 'From your mobile to a clinician’s answer',
     'Capture, locate, clinical review and same-day guidance — plus the platform and integrations.',
     '/images/screen-carer-home.jpg', 'phone'),
    ('body-map', 'Interactive body map', 'Every wound gets an exact address',
     'Tap the body, open the close-up and pin the exact spot, visit after visit.',
     '/images/map-heel-sole.jpg', 'plate'),
    ('assurestage', 'AssureStage', 'The clinicians behind every answer',
     'Certified wound specialists determine type and stage, screen for infection and set the follow-up.',
     '/images/flow/assurestage-logo.png', 'logo'),
]
USE_CASE_CARDS = [
    ('patients-caregivers', 'Patients &amp; caregivers', 'Send a photo from home and get a specialist’s answer the same day.'),
    ('clinicians', 'Clinicians', 'A worklist of photos that need your judgement — and a signed record of every decision.'),
    ('employers-health-plans', 'Employers &amp; health plans', 'Catch wounds while they are small, before they become costly episodes.'),
]


def nav(current_key, slug):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == current_key else ''
        return f'      <a href="{href}"{cur}>{label}</a>'
    who_cur = ' current' if current_key == 'who' else ''
    drop = '\n'.join(
        '          <a href="/%s/"%s>%s</a>' % (s, cur(s == slug), n)
        for s, n in USE_CASES)
    return f'''    <nav class="nav" id="site-nav" aria-label="Main">
{item('/how-it-works/', 'How it works', 'how')}
{item('/body-map/', 'Body map', 'body')}
{item('/assurestage/', 'AssureStage', 'assure')}
      <div class="nav-drop{who_cur}">
        <button type="button" aria-expanded="false" aria-haspopup="true">Who it&rsquo;s for <svg class="caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
        <div class="drop-panel">
{drop}
          <a class="drop-all" href="/#use-cases">All use cases</a>
        </div>
      </div>
      <a href="/#why">Why it matters</a>
      <a href="/#faq">FAQ</a>
      <a class="btn-ink" href="https://app.woundeye.com/">Sign in</a>
    </nav>'''


def page_top(slug, back):
    if back == 'uses':
        tabs = '\n'.join(
            '        <a href="/%s/"%s>%s</a>' % (s, cur(s == slug), n) for s, n in USE_CASES)
        return f'''  <div class="page-top">
    <div class="wrap page-top-row">
      <a class="back-link" href="/#use-cases"><span aria-hidden="true">←</span> Return to use cases</a>
      <nav class="uc-switch" aria-label="Use cases">
{tabs}
      </nav>
    </div>
  </div>
'''
    if back == 'main':
        return '''  <div class="page-top">
    <div class="wrap page-top-row">
      <a class="back-link" href="/"><span aria-hidden="true">←</span> Return to main menu</a>
    </div>
  </div>
'''
    return ''


def feature_card(s, kicker, title, text, img, kind):
    media = (f'<div class="fc-media fc-{kind}"><img src="{img}" alt="" loading="lazy"></div>')
    return f'''        <a class="feature-card" href="/{s}/">
          {media}
          <div class="fc-body">
            <p class="kicker">{kicker}</p>
            <h3>{title}</h3>
            <p>{text}</p>
            <span class="fc-more">Explore <span aria-hidden="true">→</span></span>
          </div>
        </a>'''


def explore(exclude=None, home=False):
    feats = '\n'.join(feature_card(*f) for f in FEATURES if f[0] != exclude)
    ucs = '\n'.join(
        f'''        <a class="uc-card" href="/{s}/"><span class="uc-label">{n}</span><span class="uc-text">{t}</span><span class="fc-more">See the workflow <span aria-hidden="true">→</span></span></a>'''
        for s, n, t in USE_CASE_CARDS if s != exclude)
    head = ('<p class="kicker">Explore WoundEye</p>\n          <h2>The parts that make WoundEye work</h2>'
            if home else '<p class="kicker">Keep exploring</p>\n          <h2>More about WoundEye</h2>')
    lede = ('<p class="lede">Each one has its own page — open the one you need, then come straight back.</p>'
            if home else '')
    return f'''  <section class="section explore" id="explore">
    <div class="wrap">
      <div class="section-head">
        <div>
          {head}
        </div>
        {lede}
      </div>
      <div class="feature-grid">
{feats}
      </div>
      <p class="uc-cards-head">Built for</p>
      <div class="uc-cards">
{ucs}
      </div>
    </div>
  </section>'''


CTA = '''  <section class="cta-band">
    <div class="wrap">
      <h2>Bring expert wound assessment to wherever the wound is.</h2>
      <div class="btn-row">
        <a class="btn btn-ink" href="mailto:access@woundeye.com">Request access</a>
        <a class="btn btn-line" href="https://app.woundeye.com/">Sign in</a>
      </div>
    </div>
  </section>'''

FOOTER = '''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/"><img src="/images/logo.png" alt="" width="32" height="32"><span class="brand-name">Wound<em>Eye</em></span></a>
        <p class="mt-1">Timely human wound care advice — capture, assessment and tracking on any phone.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/how-it-works/">How it works</a></li>
          <li><a href="/body-map/">Interactive body map</a></li>
          <li><a href="/assurestage/">AssureStage</a></li>
          <li><a href="/#security">Trust &amp; security</a></li>
          <li><a href="/references/">References</a></li>
        </ul>
      </div>
      <div>
        <h4>Who it&rsquo;s for</h4>
        <ul>
          <li><a href="/patients-caregivers/">Patients &amp; caregivers</a></li>
          <li><a href="/clinicians/">Clinicians</a></li>
          <li><a href="/employers-health-plans/">Employers &amp; health plans</a></li>
        </ul>
      </div>
      <div>
        <h4>Get started</h4>
        <ul>
          <li><a href="https://app.woundeye.com/">Sign in</a></li>
          <li><a href="mailto:access@woundeye.com">access@woundeye.com</a></li>
          <li><a href="https://www.wounds-ai.com">Wound Solutions AI</a></li>
        </ul>
      </div>
    </div>
    <p class="foot-legal">WoundEye is a wellness product. It does not diagnose, treat, cure or prevent any disease, and it is not a substitute for professional medical advice. Always consult a qualified clinician about a wound.</p>
    <p class="foot-legal">© <span id="year">2026</span> Wound Solutions AI. Site by Simon Lee &amp; Associates LLC</p>
  </div>
</footer>'''


def build(slug):
    title, desc, key, back, anim = META[slug]
    with open(os.path.join(PAGES, slug + '.html'), encoding='utf-8') as f:
        body = f.read().rstrip()
    url = SITE + ('/' if slug == 'home' else f'/{slug}/')
    if slug == 'home':
        body = body.replace('<!--EXPLORE-->', explore(home=True))
    elif slug == '404':
        pass
    else:
        tail = '' if slug == 'references' else '\n\n' + explore(exclude=slug) + '\n\n' + CTA
        body = page_top(slug, back) + '\n' + body + tail
    scripts = ('<script src="/js/flow.js"></script>\n' if anim else '') + '<script src="/js/main.js"></script>'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#ECE3D1">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/images/logo.png" type="image/png">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE}/images/photo-hero-feet.webp">
  <meta property="og:url" content="{url}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Caladea:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body id="top" class="page-{slug}">
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="WoundEye home">
      <img src="/images/logo.png" alt="" width="32" height="32">
      <span class="brand-name">Wound<em>Eye</em></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
{nav(key, slug)}
  </div>
</header>

<main id="main">
{body}
</main>

{FOOTER}

{scripts}
</body>
</html>
'''
    if slug == 'home':
        out, depth = os.path.join(ROOT, 'index.html'), 0
    elif slug == '404':
        # Hosts show the 404 page at whatever address was mistyped, so it keeps
        # root paths (/css/styles.css) instead of relative ones.
        out, depth = os.path.join(ROOT, '404.html'), None
    else:
        out, depth = os.path.join(ROOT, slug, 'index.html'), 1
    if depth is not None:
        html = relative(html, depth)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Always UTF-8 with Unix line endings, on every operating system.
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    return out


ROOT_PATH = re.compile(r'(\b(?:href|src)=")/(?!/)([^"]*)"')


def relative(html, depth):
    """Turn root paths like /images/x.png into paths relative to the page."""
    prefix = '../' * depth

    def fix(m):
        path = prefix + m.group(2)
        if path == '':
            path = './'
        elif path.startswith('#'):
            path = './' + path
        return m.group(1) + path + '"'
    return ROOT_PATH.sub(fix, html)


def sitemap():
    urls = [SITE + '/'] + [SITE + '/' + s + '/' for s in META if s not in ('home', '404')]
    body = ''.join('  <url><loc>%s</loc></url>\n' % u for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n')
    out = os.path.join(ROOT, 'sitemap.xml')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml)
    return out


if __name__ == '__main__':
    for s in META:
        print('built', os.path.relpath(build(s), ROOT))
    print('built', os.path.relpath(sitemap(), ROOT))

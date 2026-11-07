"""Génère le site statique anywhere.swiffle-grid.com à partir de _grids.json.
Usage : python _build.py   (réécrit index.html, */index.html, style.css, copy.js, CNAME)
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = 'https://github.com/arnaudlbdc/swiffle-grid-anywhere'
VER = '1.17'
LOADER = (
    '<script src="https://demo.swiffle-grid.com/wp-content/plugins/swiffle-grid-embed-data-anywhere/js/swiffle_embed_loader.js?v=' + VER + '" '
    'data-src="https://demo.swiffle-grid.com/wp-content/plugins/swiffle-grid-embed-data-anywhere-pro/js/swifflegridpro.js?v=' + VER + '" '
    'data-cache-version="' + VER + '"></script>'
)
# Settings panel next to the grid ("With setup bar" option of the embed code panel, plugin 1.17).
BAR = (
    '<script src="https://demo.swiffle-grid.com/wp-content/plugins/swiffle-grid-embed-data-anywhere/js/swiffle_setup_bar.js?v=' + VER + '" data-swiffle-setup-bar></script>\n'
    '<script src="https://demo.swiffle-grid.com/wp-content/plugins/swiffle-grid-embed-data-anywhere-pro/js/swiffle_setup_bar_pro.js?v=' + VER + '" data-swiffle-setup-bar></script>'
)

# slug, menu label, title, intro
PAGES = [
    ('sheets', 'Sheets', 'A Google Sheet as cards',
     'The cards below are rows of a public Google Sheet. Edit a cell in the sheet and this page shows the change on the next load.'),
    ('woo', 'Woo', 'A WooCommerce shop on a site without WordPress',
     'Products, prices, options and the cart come from the WooCommerce shop of demo.swiffle-grid.com. Checkout happens on that shop.'),
    ('rss', 'RSS', 'An RSS feed as cards',
     'The latest articles of The New York Times RSS feed, shown as cards and kept up to date.'),
    ('youtube', 'YouTube', 'A YouTube channel as cards',
     'The latest videos of the NASA Goddard YouTube channel, read from its public feed. A click plays the video.'),
    ('pokeapi', 'PokeAPI', 'A public REST API as cards',
     'Data from the public PokeAPI, fetched through a custom connector on the WordPress side.'),
    ('france-travail', 'France Travail', 'Job offers from an official API',
     'Job offers from the France Travail API (the French public employment service), through a custom connector.'),
    ('glimmerlings', 'Glimmerlings', 'Another custom API',
     'Cards built from a small custom API, through a connector written in PHP on the WordPress side.'),
]
MENU = [p for p in PAGES if p[0] in ('sheets', 'woo', 'rss', 'youtube')]
API = [p for p in PAGES if p[0] in ('pokeapi', 'france-travail', 'glimmerlings')]


def url(slug, prefix):
    return prefix + ('' if slug == 'sheets' else slug + '/')


def page(slug, label, title, intro, grids):
    prefix = './' if slug == 'sheets' else '../'
    g = grids[slug]
    snippet = LOADER + '\n<swiffle-grid datak="' + g['datak'] + '"></swiffle-grid>'
    src_file = 'index.html' if slug == 'sheets' else slug + '/index.html'
    nav = ''.join(
        f'<a href="{url(s, prefix)}"{" class=\"on\"" if s == slug else ""}>{html.escape(l)}</a>' for s, l, _, _ in MENU
    )
    nav += '<span class="sub">API:</span>' + ''.join(
        f'<a href="{url(s, prefix)}"{" class=\"on\"" if s == slug else ""}>{html.escape(l)}</a>' for s, l, _, _ in API
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} | Swiffle Grid, without WordPress</title>
<meta name="description" content="{html.escape(intro)}">
<link rel="stylesheet" href="{prefix}style.css">
{LOADER}
</head>
<body>
<div class="proof">This site is hosted on <strong>GitHub Pages</strong>: plain HTML, no WordPress, no PHP. Every grid comes from <a href="https://demo.swiffle-grid.com/">demo.swiffle-grid.com</a>. <a href="{REPO}">See the code</a></div>
<header><a class="brand" href="{prefix}">Swiffle Grid <span>anywhere</span></a><nav>{nav}</nav></header>
<main>
<h1>{html.escape(title)}</h1>
<p class="intro">{html.escape(intro)}</p>
<p class="links"><a href="{g['demo']}">Same grid on the WordPress site</a> | <a href="{REPO}/blob/main/{src_file}">View this page's source</a></p>
<p class="try">Try the settings panel: the grid reloads with each change, and <strong>Copy this embed code</strong> gives you the code with your settings.</p>
<swiffle-grid data-setup-bar datak="{g['datak']}"></swiffle-grid>
{BAR}
<section class="code">
<h2>Code to paste</h2>
<p>This is all this page contains to show the grid above. Paste it in any HTML page (Webflow, Shopify, Wix, a static site): the script line is needed only once per page.</p>
<button class="copy" type="button" data-target="code-{slug}">Copy the code</button>
<pre id="code-{slug}">{html.escape(snippet)}</pre>
<p class="note">To show your own grid on your own site, the WordPress site that holds the data must allow the address of the page where you paste the code. <a href="https://swiffle-grid.com/en/understanding-remote-embed-authorization/">How it works</a></p>
</section>
</main>
<footer>Built with <a href="https://wordpress.org/plugins/swiffle-grid-embed-data-anywhere/">Swiffle Grid</a>, free on WordPress.org | <a href="https://swiffle-grid.com/">swiffle-grid.com</a></footer>
<script src="{prefix}copy.js"></script>
</body>
</html>
'''


CSS = '''*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#1d2330;background:#f6f7fb}
a{color:#4b3bd6}
.proof{background:#220d6b;color:#fff;font-size:.9rem;padding:10px 16px;text-align:center}
.proof a{color:#10d8e4}
header{background:#fff;border-bottom:1px solid #e4e7ee;padding:12px 16px;display:flex;flex-wrap:wrap;gap:10px 24px;align-items:center;justify-content:space-between}
.brand{font-weight:700;font-size:1.15rem;text-decoration:none;color:#220d6b}
.brand span{color:#6c5cf2;font-weight:400}
nav{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}
nav a{text-decoration:none;color:#444;padding:4px 2px;border-bottom:2px solid transparent}
nav a.on{color:#220d6b;border-bottom-color:#6c5cf2}
nav .sub{color:#999;font-size:.85rem;margin-left:6px}
main{max-width:1200px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:1.7rem;margin:.2rem 0 .4rem}
.intro{color:#4b5263;margin:.2rem 0 .6rem}
.links{font-size:.9rem;margin:0 0 20px}
.try{font-size:.95rem;margin:0 0 14px;padding:10px 14px;background:#f3f0ff;border-radius:8px}
.code{margin-top:40px;background:#fff;border:1px solid #e4e7ee;border-radius:10px;padding:16px 20px}
.code h2{margin:0 0 6px;font-size:1.2rem}
.code pre{white-space:pre-wrap;word-break:break-all;background:#1d2330;color:#e6e9ef;border-radius:8px;padding:14px;font-size:.78rem;max-height:220px;overflow:auto}
.copy{background:#6c5cf2;color:#fff;border:0;border-radius:6px;padding:8px 14px;font-size:.95rem;cursor:pointer}
.note{font-size:.88rem;color:#5d6675}
footer{text-align:center;font-size:.85rem;color:#777;padding:24px 16px}
'''

JS = '''document.querySelectorAll('button.copy').forEach(function (b) {
  b.addEventListener('click', function () {
    var t = document.getElementById(b.dataset.target).textContent;
    navigator.clipboard.writeText(t).then(function () {
      var old = b.textContent; b.textContent = 'Copied'; setTimeout(function () { b.textContent = old; }, 1500);
    });
  });
});
'''


def main():
    grids = json.load(open(os.path.join(ROOT, '_grids.json'), encoding='utf-8'))
    for slug, label, title, intro in PAGES:
        d = ROOT if slug == 'sheets' else os.path.join(ROOT, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(page(slug, label, title, intro, grids))
    for name, txt in (('style.css', CSS), ('copy.js', JS), ('CNAME', 'anywhere.swiffle-grid.com\n')):
        with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
    print('ok', len(PAGES), 'pages')


main()

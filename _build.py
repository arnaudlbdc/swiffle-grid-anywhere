"""Fabrique les 6 pages du site anywhere.swiffle-grid.com.

Ce programme ne contient AUCUN texte ni style du site. Tout se modifie dans des fichiers ordinaires :
  _template/page.html  le modèle d'une page (HTML simple, avec des repères {{...}})
  _pages.json          la liste des démos : titre, phrase d'intro, menu, CodePen, Google Site
  _grids.json          le code (datak) de chaque grille et sa page sur demo
  style.css, copy.js   le style et le script, modifiés directement (ce programme n'y touche pas)

Usage : python _build.py   (réécrit index.html et */index.html, rien d'autre)
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = 'https://github.com/arnaudlbdc/swiffle-grid-anywhere'
DEMO = 'https://demo.swiffle-grid.com/wp-content/plugins/'
GSITE = 'https://sites.google.com/view/swiffle-grid-shop-on-gsheet/'


def read(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return f.read()


def main():
    conf = json.loads(read('_pages.json'))
    grids = json.loads(read('_grids.json'))
    template = read('_template/page.html')
    v = conf['plugin_version']
    loader = (f'<script src="{DEMO}swiffle-grid-embed-data-anywhere/js/swiffle_embed_loader.js?v={v}" '
              f'data-src="{DEMO}swiffle-grid-embed-data-anywhere-pro/js/swifflegridpro.js?v={v}" '
              f'data-cache-version="{v}"></script>')
    setup_bar = (f'<script src="{DEMO}swiffle-grid-embed-data-anywhere/js/swiffle_setup_bar.js?v={v}" data-swiffle-setup-bar></script>\n'
                 f'<script src="{DEMO}swiffle-grid-embed-data-anywhere-pro/js/swiffle_setup_bar_pro.js?v={v}" data-swiffle-setup-bar></script>')

    for p in conf['pages']:
        slug = p['slug']
        home = slug == 'sheets'
        prefix = './' if home else '../'
        g = grids[slug]

        def link(q):
            on = ' class="on"' if q['slug'] == slug else ''
            return f'<a href="{prefix}{"" if q["slug"] == "sheets" else q["slug"] + "/"}"{on}>{html.escape(q["menu"])}</a>'

        nav = ''.join(link(q) for q in conf['pages'] if q['group'] == 'main')
        nav += '<span class="sub">API:</span>' + ''.join(link(q) for q in conf['pages'] if q['group'] == 'api')

        src_file = 'index.html' if home else slug + '/index.html'
        buttons = [('b-wp', g['demo'], 'See on the WordPress site')]
        if p.get('codepen'):
            buttons.append(('b-cp', 'https://codepen.io/swiffle-grid/pen/' + p['codepen'], 'See on CodePen'))
        if p.get('google_site'):
            buttons.append(('b-gs', GSITE + p['google_site'], 'See on Google Site'))
        buttons.append(('b-src', f'{REPO}/blob/main/{src_file}', "View this page's source"))

        values = {
            'TITLE': html.escape(p['title']),
            'INTRO': html.escape(p['intro']),
            'PREFIX': prefix,
            'ASSETS_VERSION': conf['assets_version'],
            'LOADER': loader,
            'SETUP_BAR': setup_bar,
            'REPO': REPO,
            'NAV': nav,
            'BUTTONS': ''.join(f'<a class="{c}" href="{html.escape(u)}">{html.escape(t)}</a>' for c, u, t in buttons),
            'DATAK': g['datak'],
            'SLUG': slug,
            'SNIPPET': html.escape(loader + '\n<swiffle-grid datak="' + g['datak'] + '"></swiffle-grid>'),
        }
        out = template
        for k, val in values.items():
            out = out.replace('{{' + k + '}}', val)

        d = ROOT if home else os.path.join(ROOT, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
    print('ok', len(conf['pages']), 'pages')


main()

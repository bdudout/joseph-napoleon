#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble le site statique : content/<langue>/<page>.html (corps seul) + gabarit commun → <langue>/<page>.html.
Chaque fichier de contenu commence par un commentaire JSON : <!-- {"title": "...", "description": "..."} -->.
La page « letter » reçoit en plus le tableau ligne à ligne généré depuis data/ (marqueur <!-- LETTER-TABLE -->).
Usage : python3 tools/build.py   (depuis la racine du dépôt)"""
import json, os, re, html, hashlib
from letter_table import letter_table

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PAGES = ['index', 'history', 'method', 'letter', 'sources']
LANGS = {
    'fr': dict(code='fr', label='Français', brand='La lettre chiffrée du roi Joseph',
               nav=['Accueil', "L'histoire", 'La méthode', 'La lettre', 'Sources'], theme='Basculer le thème clair/sombre',
               footer='© 2026 Brice Dudout, avec Claude (Anthropic). Textes, données et code : <a href="https://creativecommons.org/licenses/by/4.0/deed.fr">CC BY 4.0</a> (exceptions : <a href="https://github.com/bdudout/joseph-napoleon/blob/main/NOTICE.md">NOTICE</a>). Cryptogramme : planche de J. Vilcoq, <i>Revue historique des Armées</i>, 1969 (Persée), d\'après l\'original des Archives nationales. Table du Grand Chiffre : photographies de J.-F. Bouchaudy (Service historique de la Défense). Travaux antérieurs : S. Tomokiyo (Cryptiana) ; Daniel Bourdeau (CC BY 4.0). <a href="sources.html">Toutes les sources</a>. Contact : <a href="https://www.linkedin.com/in/brice-dudout" rel="author noopener">LinkedIn</a>.',
               langs='Langue'),
    'en': dict(code='en', label='English', brand="King Joseph's cipher letter",
               nav=['Home', 'The history', 'The method', 'The letter', 'Sources'], theme='Toggle light/dark theme',
               footer='© 2026 Brice Dudout, with Claude (Anthropic). Text, data and code: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> (exceptions: <a href="https://github.com/bdudout/joseph-napoleon/blob/main/NOTICE.md">NOTICE</a>). Cryptogram: plate from J. Vilcoq, <i>Revue historique des Armées</i>, 1969 (Persée), after the original in the Archives nationales. Great Cipher table: photographs by J.-F. Bouchaudy (Service historique de la Défense). Prior work: S. Tomokiyo (Cryptiana); Daniel Bourdeau (CC BY 4.0). <a href="sources.html">All sources</a>. Contact: <a href="https://www.linkedin.com/in/brice-dudout" rel="author noopener">LinkedIn</a>.',
               langs='Language'),
}
FLAGS = {'fr': ('fr', 'FR'), 'en': ('gb', 'EN')}
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' "
        "fill='%239b2c1f'/%3E%3Ctext x='16' y='23' font-size='19' text-anchor='middle' fill='%23f7f3ea' font-family='serif'%3EJ%3C/text%3E%3C/svg%3E")

TEMPLATE = '''<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{alternates}
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="icon" href="{icon}">
</head>
<body>
<header class="site-header"><div class="inner">
  <a class="brand" href="index.html"><span class="seal seal-j">J</span> {brand}</a>
  <nav class="menu">
{nav}
  </nav>
  <nav class="lang-switch" aria-label="{langs}">
    <details>
{switch}
    </details>
  </nav>
  <button class="theme-toggle" type="button" aria-label="{theme}">◐</button>
</div></header>

<main>
{body}
</main>

<footer class="site-footer"><div class="inner">
  {footer}
</div></footer>
<script src="../assets/js/site.js"></script>
</body>
</html>
'''


def bust(page):
    """Ajoute ?v=<empreinte> aux CSS/JS locaux pour que les navigateurs rechargent les fichiers modifiés."""
    def rep(m):
        path = os.path.normpath(os.path.join(ROOT, 'fr', m.group(2)))
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10] if os.path.exists(path) else None
        return m.group(1) + m.group(2) + ('?v=' + h if h else '') + m.group(3)
    return re.sub(r'((?:href|src)=")(\.\./assets/(?:css|js)/[^"?]+)(")', rep, page)


def build():
    n = 0
    for lang, L in LANGS.items():
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for page in PAGES:
            src = os.path.join(ROOT, 'content', lang, page + '.html')
            if not os.path.exists(src):
                continue
            raw = open(src, encoding='utf-8').read()
            m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', raw, re.S)
            meta = json.loads(m.group(1)) if m else {}
            body = raw[m.end():] if m else raw
            if '<!-- LETTER-TABLE -->' in body:
                body = body.replace('<!-- LETTER-TABLE -->', letter_table(lang))
            nav = '\n'.join('    <a href="%s.html"%s>%s</a>' % (p, ' aria-current="page"' if p == page else '', L['nav'][i])
                            for i, p in enumerate(PAGES))
            switch = ('      <summary title="%s" aria-label="%s — %s"><img class="flag" src="../assets/img/flags/%s.svg" width="20" height="15" alt="">'
                      '<span class="lc">%s</span></summary>\n      <ul>\n' % (L['langs'], L['langs'], L['label'], FLAGS[lang][0], FLAGS[lang][1]))
            switch += '\n'.join('        <li><a href="../%s/%s.html" hreflang="%s" lang="%s" data-lang="%s"%s>'
                                '<img class="flag" src="../assets/img/flags/%s.svg" width="20" height="15" alt=""><span>%s</span></a></li>'
                                % (l, page, LL['code'], LL['code'], l, ' aria-current="true"' if l == lang else '', FLAGS[l][0], LL['label'])
                                for l, LL in LANGS.items())
            switch += '\n      </ul>'
            alternates = '\n'.join('<link rel="alternate" hreflang="%s" href="../%s/%s.html">' % (LL['code'], l, page) for l, LL in LANGS.items())
            out = TEMPLATE.format(code=L['code'], title=html.escape(meta.get('title', L['brand'])),
                                  description=html.escape(meta.get('description', '')), alternates=alternates,
                                  icon=ICON, brand=L['brand'], nav=nav, langs=L['langs'], switch=switch,
                                  theme=L['theme'], body=body.rstrip(), footer=L['footer'])
            open(os.path.join(ROOT, lang, page + '.html'), 'w', encoding='utf-8').write(bust(out))
            n += 1
    print(n, 'pages générées')


if __name__ == '__main__':
    build()

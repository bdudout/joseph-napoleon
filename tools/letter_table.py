# -*- coding: utf-8 -*-
"""Tableau ligne à ligne de la page « La lettre » : groupes du cryptogramme (planche de Vilcoq), valeur lue dans la
table de 1812, lecture. Données : data/cryptogramme-planche-vilcoq.txt, data/table-1812-entrees.json, data/lecture.json."""
import json, os, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SPECIAL = {'un point': '.', 'point et virgule': ';', 'alinéa': '¶'}
T = {'fr': dict(line='Ligne', groups='Groupes chiffrés et valeurs de la table', reading='Lecture',
                fix='Corrigé sur la planche (transcription en ligne : %s)', doubt='Douteux : %s'),
     'en': dict(line='Line', groups='Cipher groups and table values', reading='Reading (French)',
                fix='Corrected from the plate (online transcription: %s)', doubt='Uncertain: %s')}


def letter_table(lang):
    d = lambda p: os.path.join(ROOT, 'data', p)
    lines = [l.split() for l in open(d('cryptogramme-planche-vilcoq.txt'), encoding='utf-8') if l.strip()]
    tab = json.load(open(d('table-1812-entrees.json'), encoding='utf-8'))
    lec = json.load(open(d('lecture.json'), encoding='utf-8'))
    L = T[lang]
    out = ['<div class="table-wrap wide"><table class="letter"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>'
           % (L['line'], L['groups'], L['reading'])]
    for i, groups in enumerate(lines, 1):
        toks = []
        for j, g in enumerate(groups):
            v = tab.get(g, '?')
            shown = SPECIAL.get(v, v.split(',')[0].rstrip('?'))
            cls, title = ['tok'], [v]
            c = lec['corrections_transcription'].get('%d:%d' % (i, j))
            if c: cls.append('fix'); title.append(L['fix'] % c[0])
            if g in lec['douteux']: cls.append('doubt'); title.append(L['doubt'] % lec['douteux'][g][lang])
            toks.append('<span class="%s" title="%s"><b>%s</b><i>%s</i></span>'
                        % (' '.join(cls), html.escape(' — '.join(title)), g, html.escape(shown)))
        out.append('<tr><td class="ln">%d</td><td class="toks">%s</td><td class="rd" lang="fr">%s</td></tr>'
                   % (i, ''.join(toks), html.escape(lec['lignes_fr'][i - 1])))
    out.append('</tbody></table></div>')
    return '\n'.join(out)

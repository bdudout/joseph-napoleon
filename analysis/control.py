#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle par permutations : vraisemblance en français (4-grammes de caractères) du texte décodé avec la table du
Grand Chiffre de 1812, comparée à 1 000 décodages obtenus en mélangeant les numéros de la même table.
Le modèle de langue doit être appris sur un texte indépendant du cryptogramme. Dans ce travail : les lettres de Berthier
de décembre 1812 imprimées par A. Chuquet (1812. La guerre de Russie, 3e série, 1912), texte OCR non redistribué ici.
Usage : python3 analysis/control.py TEXTE_DE_REFERENCE.txt"""
import json, math, os, random, re, sys, unicodedata
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SPECIAL = {'un point', 'point et virgule', 'alinéa'}


def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s)


train = norm(open(sys.argv[1], encoding='utf-8').read())
N = 4
grams = Counter(train[i:i + N] for i in range(len(train) - N + 1))
ctx = Counter(train[i:i + N - 1] for i in range(len(train) - N + 2))


def score(text):
    t = norm(text)
    lp = sum(math.log((grams[t[i:i + N]] + 0.1) / (ctx[t[i:i + N - 1]] + 0.1 * 26)) for i in range(len(t) - N + 1))
    return lp / max(1, len(t) - N + 1)


def decode(tab, ct):
    out = []
    for g in ct:
        e = tab.get(g)
        if e is None: continue
        w = e.split(',')[0]
        if w in SPECIAL or w.startswith('['): continue
        out.append(w.rstrip('?'))
    return ''.join(out)


ct = open(os.path.join(ROOT, 'data', 'cryptogramme-planche-vilcoq.txt'), encoding='utf-8').read().split()
tab = json.load(open(os.path.join(ROOT, 'data', 'table-1812-entrees.json'), encoding='utf-8'))
real = score(decode(tab, ct))
rng = random.Random(1812); keys, vals, ctrl = list(tab), list(tab.values()), []
for _ in range(1000):
    rng.shuffle(vals); ctrl.append(score(decode(dict(zip(keys, vals)), ct)))
ctrl.sort()
print('table du Grand Chiffre : %.3f par caractère' % real)
print('1 000 permutations : médiane %.3f, maximum %.3f, nombre >= réel : %d' % (ctrl[500], ctrl[-1], sum(c >= real for c in ctrl)))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décode le cryptogramme (data/cryptogramme-planche-vilcoq.txt) avec les entrées lues dans la table du Grand Chiffre
de 1812 (data/table-1812-entrees.json) : une ligne par ligne du chiffré, valeur principale de chaque groupe.
Usage : python3 analysis/decode.py   (depuis la racine du dépôt)"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SPECIAL = {'un point': '.', 'point et virgule': ';', 'alinéa': '¶'}
tab = json.load(open(os.path.join(ROOT, 'data', 'table-1812-entrees.json'), encoding='utf-8'))
for i, line in enumerate(open(os.path.join(ROOT, 'data', 'cryptogramme-planche-vilcoq.txt'), encoding='utf-8'), 1):
    vals = [tab.get(g, '??') for g in line.split()]
    print('%02d  %s' % (i, ' '.join(SPECIAL.get(v, v.split(',')[0]) for v in vals)))

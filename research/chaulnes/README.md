# Louis XIV → duc de Chaulnes, Versailles, 10 juillet 1690 — travail en cours (non déchiffré)

Lettre signée *Louis*, contresignée *Colbert* (de Croissy), à l'ambassadeur à Rome pendant l'affaire des bulles.
300 groupes chiffrés en 11 passages, 116 groupes distincts, valeurs de 2 à 535. Transcription vérifiée sur les
photographies par le projet [cyphersolver](https://github.com/dbourdeau/cyphersolver) (`targets/chaulnes/`), reprise ici
dans `ciphertext.txt`. Aucun déchiffrement publié connu (Cryptiana, Klausis 2019, cyphersolver sept. 2026).

## Hypothèse de structure

Les codes de Colbert de Croissy de 1684-1690 reconstruits par Lasry et Tomokiyo (d'Avaux 1684, Béthune et Teil 1689,
Castaignère 1690 ; images de Tomokiyo, page Cryptiana `louisxiv.htm`, déposée dans `sources/chaulnes/` sur `main`)
suivent un même plan :

- les petits nombres (ici < 80) sont des lettres seules, dans l'ordre alphabétique, avec des homophones ;
- au-delà, la table a 10 colonnes (chiffre des unités) et se lit **colonne par colonne** : de haut en bas, puis colonne
  suivante, les initiales avancent dans l'ordre alphabétique ;
- chaque consonne a sa série de syllabes Ca-Ce-Ci-Co-Cu de 10 en 10 dans une même colonne ; les mots de même initiale
  sont placés autour.

Conséquence : en classant les groupes par (colonne, nombre), à partir d'une colonne de départ c0 inconnue, les initiales
des valeurs claires sont croissantes. C'est la contrainte exploitée par `solve.py` et `crib.py`.

## Fichiers

| fichier | rôle |
|---|---|
| `ciphertext.txt` | les 11 passages chiffrés avec le texte clair qui les entoure |
| `ch_parse.py` | lecture de `ciphertext.txt` |
| `build_corpus.py` | extrait du corpus FreEM (`git clone https://github.com/FreEM-corpora/FreEMmax_OA corp/FreEMmax_OA`) la prose 1640-1720 (`fr1640_1720.txt`, 77 Mo) et 1540-1600 (`fr1540_1600.txt`, 12 Mo) |
| `lm6.py` | modèle de langue par caractères (6-grammes) ; `python3 lm6.py fr1640_1720.txt lm1690.pkl` |
| `wlm.py` | modèle par mots (unigrammes + bigrammes, segmentation de Viterbi) ; `python3 wlm.py fr1640_1720.txt wlm1690.pkl` |
| `vocab.py` | alphabet, syllabes, vocabulaire |
| `mkctrl.py` | génère des textes de contrôle chiffrés avec un code de même plan (`ctrl1-3.json`) |
| `solve.py` | recuit simulé sous contrainte d'ordre alphabétique ; `--ctrl ctrlN.json` ou texte réel, `--c0`, `--crib` |
| `crib.py` | test d'un mot ou d'une phrase supposés sur un passage (découpages compatibles avec l'ordre du code) |
| `evalcmp.py` | compare le score de la vraie clé d'un contrôle à celui des solutions trouvées |

Les corpus et les modèles (`*.txt`, `*.pkl`) ne sont pas versionnés : ils se reconstruisent avec les commandes ci-dessus.

## Résultats sur les contrôles (16 octobre 2026)

| essai | groupes justes |
|---|---|
| score par caractères, à l'aveugle | 14-21 % ; les solutions fausses battent la vraie clé |
| score par mots, vocabulaire de 700 mots | 5-8 % ; idem |
| score par mots, 400 mots les plus fréquents | 11-14 % ; **la vraie clé a désormais le meilleur score**, la recherche ne la trouve pas |
| idem avec une phrase connue de 25 groupes fixée | 71 % au total, mais 10-12 % hors de cette phrase |

Conclusion provisoire : 300 groupes ne suffisent pas à l'attaque à l'aveugle ; une phrase connue aide peu à elle seule.
Ce qui débloquerait : la minute (Archives diplomatiques, CP Rome vol. 331-332, « le Roi à Chaulnes, 10 juillet 1690 »)
ou une autre lettre dans le même code avec un déchiffrement.

## Pistes en cours

Voir `PISTES.md`.

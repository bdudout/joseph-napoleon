# Pistes sur la lettre de Chaulnes (16 octobre 2026)

Hypothèses de travail, **non vérifiées**. Notation : `groupe = valeur`.

## 1. « appa… » en fin de P5

Fin de P5, après « …qui sont nommés aux archeveschés et eveschés » : `2 47 49 3 12 381 509 102 433 170` puis un point.

Si les petits nombres sont des lettres en ordre alphabétique, avec une disposition proche du code de Castaignère
(1690 : a = 2, 3 ; e = 14 ; n = 38 ; r = 50, 51 ; s = 53, 54 ; u = 59), alors `2 47 49 3` = a p p a.

Test (`crib.py`) des 64 mots du corpus 1640-1720 commençant par *appa* (fréquence ≥ 5), sous la contrainte d'ordre :
`12` est forcément une lettre comprise entre a et p, ce qui exclut *apparence*, *apparemment*, *appartient*…
Seuls passent :

| mot | valeurs | colonnes de départ possibles |
|---|---|---|
| appaise | 12 = i, 381 = se | toutes |
| appaisa | 12 = i, 381 = sa | toutes |
| appaisent | 12 = i, 381 = sent | toutes |
| appaisera | 12 = i, 381 = se, 509 = ra, ou 381 = sera | 2-9 / toutes |
| appanage | 12 = n, 381 = age | toutes |

## 2. « ne » = 488 (proposition de Thomas Ernst, Klausis 2019)

Avec 488 = ne, la série des n est en colonne 8 : 478 na, 488 ne, 498 ni, 508 no, 518 nu ; 508 (3 fois) = no.
Combinée à *appaise* (381 = se), la colonne de départ est c0 ∈ {2…8}.

## 3. Hypothèse d'ensemble (c0 = 2), compatible avec l'ordre alphabétique

- lettres : 2, 3 = a ; 12 = i ; 47, 49 = p
- colonne 2 : b (122 be … 152 bu), c (172 ce, 182 ci, 192 co)
- colonne 3 : 433 = de
- colonne 8 : 488 = ne, 508 = no
- colonne 0 : soit p (120 pe … 150 pu) + qu (170 que, 180 qui), soit s (170 se, 180 si) avec 381 = sera
- colonne 1 : 381 = se ou sera

Les deux variantes de la colonne 0 sont départagées par le solveur (`solve.py --fixjson hypA.json / hypB.json`).
Résultats : voir la section suivante quand ils seront disponibles.

## 4. Résultats du solveur sur la vraie lettre (c0 = 2, 250 000 itérations, vocabulaire de 400 mots)

| hypothèse fixée | codes fixés | score final |
|---|---|---|
| A : appaise + ne + séries b, c, p, qu, de, no | 24 | −1004 |
| B : appaisera (381 = sera) + ne + séries b, c, s, de, no | 20 | −960 |
| C : appaise + ne seulement (graine 1) | 7 | −643 |
| C : idem (graine 2) | 7 | −623 |

Toutes les sorties sont des suites de mots sans suite (« salade »), aucune lecture. Les hypothèses A et B coûtent plus de
300 points par rapport à C : les séries de syllabes supposées (qu / s en colonne 0, b et c en colonne 2, de = 433) sont
défavorisées. *appaise* et *ne* = 488 ne sont ni confirmés ni contredits. Les deux graines de C divergent : la recherche
ne converge pas, comme sur les contrôles.

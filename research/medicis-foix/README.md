# Catherine de Médicis → Paul de Foix, 15 janvier 1563/4 (BL Add MS 4136, ff. 148v-149 ; DECODE R9241)

> **Mise au point (16 octobre 2026).** Cette lettre est **déjà largement déchiffrée et publiée** : David Potter l'édite
> (correspondance de Paul de Foix, n° 65, Paris, **15 janvier 1563/4**, soit **1564** en style moderne) avec un texte
> clair reconstitué, d'après un autre témoin, TNA SP 70/67, ff. 82-84. Lawrence Beck (avec ChatGPT) a reconstruit la clé
> du témoin de la British Library et l'a contrôlée sur des lettres de 1562 déchiffrées à l'époque (BnF Français 6612) :
> voir `targets/foix1563/beck-preliminary/CURRENT_STATUS.md` dans cyphersolver. Valeurs établies là-bas qui corrigent les
> notes ci-dessous : **70 = tout** (et non *toute*), **N monogramme = ff**, 32 = par, 10 = dict, RX = mm ; *Mauvissière*,
> *prouffict*, *advertirez*, *offert* figurent déjà chez Potter. Pas d'article publié sur ce dossier : les apports
> propres de ce travail sont minces (tests systématiques par modèle de langue ; *cc* proposé dans *a[cc]ompaign[ée]* ;
> 37 lu *me* plutôt que *car*). Les notes ci-dessous sont conservées comme trace de recherche.

## Notes de travail (antérieures à la mise au point)

En attente des photographies (demandées à Daniel Bourdeau). Données et clés dans le dépôt
[cyphersolver](https://github.com/dbourdeau/cyphersolver), `targets/foix1563/` (transcription et clé de L. Beck,
clé de Foix 1565 reconstruite par S. Tomokiyo, `r9241_foix1565key/key_k0.json`).

`dec.py` décode la transcription de Beck (`CYPHERSOLVER=<chemin du clone> python3 dec.py`) en ajoutant les
mots-codes de la clé de 1565 que la clé de Beck laisse vides. Lecture obtenue, sans ajustement sur la lettre :

- 26 = *bien* (4 occurrences) : « dont je voy bien qu'il seroit bien aise de faire son prou[ffi]ct de ce royaulme »,
  « je la luy feiz bien entendre pour luy oster ceste esperance », « je voy bien que son but seroit… »
- 34 = *tant* : « peust avoir tant de faveur », « vous a esté ja tant escript »
- 40 = *faict* : « ayant faict les beaulx [20]ancemens » (20 = av ?)
- 10 = *dict* : « depuis le partement du dict… »
- 70 = *toute*, 82 = *ceulx*, 37 = *car* : à vérifier ; la ligne D0 reste obscure.

À contrôler sur les images : RX, z, 3, 20, 37, 70.

## Tests du 16 octobre 2026 (`med.py`, modèle par mots entraîné sur la prose FreEM 1540-1600)

`med_targets.py SIGNE…` essaie ~300 valeurs (lettres, digrammes, mots fréquents) pour un signe à toutes ses occurrences
et classe les valeurs par score de la lettre entière.

- **Validation** (`med_loo.py`, `med_loo.txt`) : sur les 58 signes connus de 2 occurrences ou plus, valeur masquée puis
  retrouvée au rang 1 dans 45 cas (48 dans le top 3). Fiable pour les signes-lettres, pas pour les mots-codes rares.
- **Mots-codes de la clé de 1565** (`med_targets.txt`) : non confirmés par le texte seul (bien rang 10, tant 37, faict 63,
  dict 63, toute 83, ceulx 108 sur ~300). Leur appui reste l'indépendance de la clé de 1565. 37 : *me* (rang 7) bien
  meilleur que *car* (rang 214) ; la clé de 1565 donne les deux.
- **B1** : `SWASH_2` = **g** (écart de 8,4 avec la 2e valeur) ; avec `CAP_D_BOWL` = *cc* (hypothèse) :
  « avecques grande abondance de langai**g**e a**cc**ompaign[ée] de la dexterité de son esperit » ; la fin *-ée* est sous
  la tache B1:23 et `M_SWASH`.
- **D8** : « depuis le partement du dict de Mar‑i‑ss‑r‑i‑u‑e‑r‑e » : *Mauvissière* (Michel de Castelnau) — lecture déjà
  donnée par Potter, retrouvée ici indépendamment, sans priorité.
- Ouverts : 20 (*au* ? « auancemens »), `N_MONOGRAM`, ligne D0.

Signes à vérifier sur les photos : `ZBAR`, `CAP_D_BOWL`, `M_SWASH`, `N_MONOGRAM`, 20, 37, fin de D8.

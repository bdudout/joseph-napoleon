# La lettre chiffrée du roi Joseph · King Joseph's cipher letter (1812)

**Site : <https://bdudout.github.io/joseph-napoleon/>** (français, English)

Par **Brice Dudout**, en collaboration avec Claude (Anthropic) — licence [CC BY 4.0](LICENSE) (mentions et exceptions : [NOTICE.md](NOTICE.md)).

Un cryptogramme publié en 1969 par J. Vilcoq dans la *Revue historique des Armées* et présenté comme une dépêche du
maréchal Berthier à Napoléon (22 décembre 1812, Archives nationales) se lit avec la table de déchiffrement du
**Grand Chiffre de 1812**, le code des armées françaises d'Espagne. Le texte est, très vraisemblablement, une lettre du
**roi Joseph** à l'Empereur, écrite de Madrid ; une lettre sœur adressée le 23 décembre 1812 au ministre de la Guerre,
imprimée par Du Casse en 1854, recoupe son contenu.

Trois pages, en français et en anglais :

1. **L'histoire** — le contexte (Espagne et Russie, 1812), le texte de la lettre, son auteur ;
2. **La méthode** — les tables essayées, la table du Grand Chiffre, le contrôle par permutations, la relecture sur la
   planche de 1969 (8 groupes corrigés), la lettre sœur ;
3. **La lettre** — les 325 groupes ligne à ligne avec leur valeur dans la table, le texte suivi et sa traduction.

**Priorité** : la clé (Grand Chiffre de Paris) et l'auteur (le roi Joseph) ont été identifiés en premier par **Ilia Chirtulov**
(résultat reçu par S. Tomokiyo le 4 octobre 2026, signalé sur [Cryptiana](https://cryptiana.web.fc2.com/code/unsolved.htm)
le 12 octobre 2026). Ce site est une relecture indépendante qui ajoute la lecture complète ligne à ligne, la relecture du
chiffré sur la planche de 1969 (8 groupes corrigés), un contrôle par permutations et la lettre sœur du 23 décembre 1812.

Ce travail part du cryptogramme recensé par **S. Tomokiyo** sur [Cryptiana](https://cryptiana.web.fc2.com/code/napoleon2.htm)
et de la liste publiée par **Daniel Bourdeau** ([dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver), CC BY 4.0).
La table du Grand Chiffre a été lue sur les photographies publiées par **Jean-François Bouchaudy**
([The codebooks of Napoleon I](http://www.jfbouch.fr/crypto/napoleon/index.html)).

## Structure

```
index.html              page de choix de langue (redirige selon la langue du navigateur)
fr/, en/                pages générées (ne pas éditer à la main)
content/<langue>/       contenu des pages (corps HTML + métadonnées en commentaire JSON)
tools/build.py          assemble content/ + gabarit commun → fr/, en/
tools/letter_table.py   tableau ligne à ligne de la page « La lettre » (depuis data/)
assets/                 feuille de style, script, drapeaux, images
data/                   cryptogramme relu sur la planche, entrées lues dans la table, lecture
analysis/               décodage et contrôle par permutations
```

Mise à jour : éditer `content/fr/*.html` et `content/en/*.html` (même structure dans les deux langues), puis
`python3 tools/build.py`.

## Données

- `data/cryptogramme-planche-vilcoq.txt` : les 325 groupes de la page 3, relus sur la planche de 1969 (Persée) ;
  8 groupes diffèrent de la transcription en ligne (`data/lecture.json`, clé `corrections_transcription`).
- `data/table-1812-entrees.json` : les 226 entrées de la table du Grand Chiffre de 1812 lues pour ce travail
  (graphie de la table ; « ? » = lecture douteuse ; les entrées 851 et 1051 sont cachées par une pliure).
- `data/lecture.json` : lecture ligne à ligne et notes sur les groupes douteux.
- `python3 analysis/decode.py` : décodage ligne à ligne ; `python3 analysis/control.py TEXTE.txt` : contrôle par
  permutations (modèle de langue appris sur un texte de référence indépendant).

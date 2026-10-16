import collections,re
from lm6 import norm
ALPHA='abcdefghilmnopqrstuxyz'   # j->i, v->u, k->c, w->u
AIDX={c:i for i,c in enumerate(ALPHA)}
CONS='bcdfghlmnpqrstux'           # syllable consonants (q = qu, u = v)
VOW='aeiou'
def syl(c,v): return ('qu'+v) if c=='q' else c+v
SYLS=[(c,v,syl(c,v)) for c in CONS for v in VOW]
def words_from_corpus(path,n=700,maxchars=30_000_000,skip=0):
    f=open(path,encoding='utf-8',errors='ignore'); f.seek(skip)
    t=f.read(maxchars)
    toks=[norm(w) for w in re.findall(r"[A-Za-zÀ-ÿſ]+",t)]
    c=collections.Counter(w for w in toks if 2<=len(w)<=12)
    return [w for w,_ in c.most_common(n)]
DOMAIN='bulles bulle evesques evesque archevesques eveschez archeveschez pape sainctete saintete cardinaux cardinal assemblee clerge regale expedition declaration rome chaulnes roy maiesté maieste congregation propositions doctrine eglise ottoboni cibo nommez nomination instances negotiation affaire affaires lettre lettres projet profession foy promesse satisfaction'.split()
SUFF='tion ment ance ence oit oient ant ent on en an ou ont oir eur'.split()

# Médicis -> de Foix: test candidate values for a sign at all its occurrences (word-level LM, 1540-1600)
import os,sys,json,collections,math
os.environ.setdefault('CYPHERSOLVER','cyphersolver')
sys.path.insert(0,'.')
from load import lines,kv,key
from wlm import WLM
from lm6 import norm
from vocab import words_from_corpus
NULL={'XP','T6','TF','MM','POUR','ASSEZ','CAR','QUOG','SEP_SLASH'}
K0NUM={'26':'bien','34':'tant','40':'faict','70':'toute','10':'dict','82':'ceulx','37':'car'}
def base_key(extra=None):
    k={}
    for ln,u in lines:
        for x in u:
            if x in NULL: k[x]=''
            elif x in K0NUM: k[x]=K0NUM[x]
            else:
                v=kv(x); k[x]=None if v in (None,'') else norm(v)
    if extra: k.update(extra)
    return k
# passages: concatenate lines with same letter
PASS=collections.OrderedDict()
for ln,u in lines: PASS.setdefault(ln[0],[]).extend(u)
m=WLM('wlm1560.pkl'); BONUS=1.3
def pieces(seq,k):
    out=[[]]
    for x in seq:
        v=k.get(x)
        if v is None: out.append([])
        else: out[-1].append(v)
    return [''.join(p) for p in out if p]
def score(k):
    s=0.0
    for p,seq in PASS.items():
        for t in pieces(seq,k):
            if t: s+=m.score(t)+BONUS*len(t)
    return s
def render(k):
    return {p:' | '.join(pieces(seq,k)) for p,seq in PASS.items()}
CANDS=None
def cands():
    global CANDS
    if CANDS: return CANDS
    letters=list('abcdefghilmnopqrstuxyz')
    bigr=['ie','en','es','er','re','on','ou','an','qu','de','le','te','nt','ur','it','us','ai','ue','se','ra','ar','ne','ce','me','ec','is','in','oi','ns','st','ll','ss','ff','tz']
    ws=[w for w in words_from_corpus('fr1540_1600.txt',250) if len(w)<=7]
    CANDS=list(dict.fromkeys(['']+letters+bigr+list(K0NUM.values())+['me','luy','par','pour','que','qui','le','la','est','ie','faire','nous','vous','sieur','roy','royne']+ws))
    return CANDS
def test(sign,k=None,top=10):
    k=dict(k or base_key()); res=[]
    for c in cands():
        k[sign]=c; res.append((score(k),c))
    res.sort(reverse=True); return res[:top],res
if __name__=='__main__':
    k=base_key()
    for p,t in render(k).items(): print(p,t)
    unk=collections.Counter(x for _,u in lines for x in u if k.get(x) is None)
    print('unknown',unk)

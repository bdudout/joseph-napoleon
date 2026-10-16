# Test a plaintext crib on a Chaulnes passage under the Croissy column-major alphabetical constraint.
import sys,itertools
from lm6 import norm
from vocab import ALPHA,AIDX,VOW,CONS
from ch_parse import segs
LOW=80
from vocab import SYLS,SUFF,DOMAIN,words_from_corpus
import os,pickle
if os.path.exists('lex.pkl'): LEX=pickle.load(open('lex.pkl','rb'))
else:
    LEX={u for _,_,u in SYLS}|set(SUFF)|{norm(w) for w in DOMAIN}|set(words_from_corpus('fr1640_1720.txt',3000))
    LEX|={v+c for v in 'aeiou' for c in 'nrslmtx'}|{'ou','au','oi','ai','eu','ui','ie','ue','qu'}
    pickle.dump(LEX,open('lex.pkl','wb'))
def rank(g,c0): return ((g%10-c0)%10)*1000+g//10
def consistent(asg,c0s=range(10)):
    # low letters non-decreasing in code
    lows=sorted((g,u) for g,u in asg.items() if g<LOW)
    for (g1,u1),(g2,u2) in zip(lows,lows[1:]):
        if AIDX[u1]>AIDX[u2]: return []
    ok=[]
    for c0 in c0s:
        hs=sorted(((rank(g,c0),g,u) for g,u in asg.items() if g>=LOW))
        if all(AIDX[a[2][0]]<=AIDX[b[2][0]] for a,b in zip(hs,hs[1:])):
            # syllable runs: same consonant CV units must share column/base
            base={}; bad=False
            for _,g,u in hs:
                c=None
                if len(u)==2 and u[0] in CONS and u[1] in VOW: c,v=u[0],u[1]
                elif len(u)==3 and u[:2]=='qu' and u[2] in VOW: c,v='q',u[2]
                if c:
                    b=g-10*VOW.index(v)
                    if base.setdefault(c,b)!=b: bad=True
            if not bad: ok.append(c0)
    return ok
def search(groups,plain,fixed=None,maxlen=12,prefix=True,limit=200000):
    plain=norm(plain); res=[]; n=len(groups)
    def rec(i,j,asg):
        if len(res)>=limit: return
        if j==len(plain) and (prefix or i==n):
            if consistent(asg): res.append((i,dict(asg)))
            return
        if i==n: return
        g=groups[i]
        lens=[1] if g<LOW else range(2,maxlen+1)
        for L in lens:
            if j+L>len(plain): break
            u=plain[j:j+L]
            if g>=LOW and u not in LEX: continue
            if g in asg:
                if asg[g]!=u: continue
                rec(i+1,j+L,asg); continue
            if g>=LOW and u in asg.values(): continue   # one-part code: a high unit has one code
            asg[g]=u
            if consistent(asg): rec(i+1,j+L,asg)
            del asg[g]
    rec(0,0,dict(fixed or {}))
    return res
if __name__=='__main__':
    si=int(sys.argv[1]); phrase=sys.argv[2]
    g=segs[si]['groups']
    print('passage',segs[si]['tag'],'«',segs[si]['pre'][-50:],'»',len(g),'groups')
    r=search(g,phrase)
    print('solutions',len(r))
    for i,asg in r[:15]:
        print(i,'groups:',' '.join(f"{x}={asg[x]}" for x in g[:i]),'| c0',consistent(asg))

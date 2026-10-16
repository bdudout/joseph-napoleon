# char n-gram LM (letters only, no spaces), stupid-backoff, built from period corpus
import re,unicodedata,pickle,math,collections,os,sys
N=6
def norm(t):
    t=unicodedata.normalize('NFD',t.lower())
    t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.replace('ſ','s').replace('j','i').replace('v','u').replace('w','u').replace('k','c')
    return re.sub(r'[^a-z]','',t)
def build(src,out,maxchars=25_000_000):
    t=norm(open(src,encoding='utf-8',errors='ignore').read(maxchars*2))[:maxchars]
    tabs=[None]+[collections.Counter(t[i:i+n] for i in range(len(t)-n+1)) for n in range(1,N+1)]
    tot=len(t); lp={}
    for n in range(1,N+1):
        for g,c in tabs[n].items():
            if n>1 and c<2: continue
            den=tabs[n-1][g[:-1]] if n>1 else tot
            lp[g]=math.log(c/den)
    pickle.dump(lp,open(out,'wb'))
class LM:
    def __init__(s,p): s.lp=pickle.load(open(p,'rb'))
    def score(s,t):
        lp=s.lp; tot=0.0
        for i in range(len(t)):
            pen=0.0
            for n in range(min(N,i+1),0,-1):
                v=lp.get(t[i-n+1:i+1])
                if v is not None: tot+=v+pen; break
                pen-=0.9
            else: tot+=-12
        return tot
if __name__=='__main__':
    build(sys.argv[1],sys.argv[2])

# word-level scorer: Viterbi segmentation into corpus words with unigram+bigram (interpolated) probabilities
import re,collections,math,pickle,sys
from lm6 import norm
def build(src,out,maxchars=40_000_000):
    t=open(src,encoding='utf-8',errors='ignore').read(maxchars)
    toks=[norm(w) for w in re.findall(r"[A-Za-zÀ-ÿſ]+",t)]; toks=[w for w in toks if w]
    uni=collections.Counter(toks); bi=collections.Counter(zip(toks,toks[1:]))
    uni={w:c for w,c in uni.items() if c>=3 and len(w)<=18}
    bi={k:c for k,c in bi.items() if c>=3 and k[0] in uni and k[1] in uni}
    pickle.dump((uni,bi,len(toks)),open(out,'wb'))
class WLM:
    UNK=-14.0
    def __init__(s,p):
        uni,bi,N=pickle.load(open(p,'rb')); s.N=N
        s.lu={w:math.log(c/N) for w,c in uni.items()}
        s.uni=uni; s.bi=bi; s.maxlen=18
    def lp(s,prev,w):
        u=s.uni[w]/s.N
        if prev is not None and prev in s.uni:
            b=s.bi.get((prev,w),0)/s.uni[prev]
            return math.log(0.6*b+0.4*u)
        return math.log(u)
    def score(s,t):
        # Viterbi over (position) keeping best (score,lastword); approximate bigram with best-prev only
        n=len(t); best=[(-1e18,None)]*(n+1); best[0]=(0.0,None)
        lu=s.lu
        for i in range(n):
            sc,pw=best[i]
            if sc<-1e17: continue
            for L in range(1,min(s.maxlen,n-i)+1):
                w=t[i:i+L]
                if w in lu:
                    v=sc+s.lp(pw,w)
                    if v>best[i+L][0]: best[i+L]=(v,w)
            v=sc+s.UNK
            if v>best[i+1][0]: best[i+1]=(v,None)
        return best[n][0]
if __name__=='__main__':
    build(sys.argv[1],sys.argv[2])

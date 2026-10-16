# Synthetic control: column-major alphabetical one-part code (Croissy 1684-1690 design), 300 groups in 11 segments
import random,re,sys,json,collections
from lm6 import norm
from vocab import *
def build_code(rnd,words,c0,lowmax=78,rows=(8,53)):
    # low letters: alphabetical, 2-4 homophones, from 2 up to lowmax
    low={}; n=2
    letfreq='eaisntrulodcmpqfbghxyz'
    for ch in ALPHA:
        k=3 if ch in 'easintr' else (2 if ch in 'uolcdmp' else 1)
        for _ in range(k):
            if n<=lowmax: low[n]=ch; n+=1
        n+=rnd.choice([0,0,1])
    # high table entries in alphabetical order of initial
    ent=[]
    byinit=collections.defaultdict(list)
    for w in words: byinit[w[0]].append(w)
    nslots=(rows[1]-rows[0]+1)*10
    nsyl=len(CONS)*5
    nw=nslots-nsyl-20
    sylset={u for _,_,u in SYLS}
    words=[w for w in dict.fromkeys(SUFF+words) if w not in sylset]
    chosen=set(words[:nw])
    for w in words:
        byinit[w[0]]
    byinit=collections.defaultdict(list)
    for w in words: byinit[w[0]].append(w)
    seq=[]
    for ch in ALPHA:
        ws=[w for w in byinit[ch] if w in chosen]; rnd.shuffle(ws)
        sy=[syl(ch,v) for v in VOW] if ch in CONS else []
        k=rnd.randint(0,len(ws)) if ws else 0
        seq.append((ch,ws[:k],sy,ws[k:]))
    # lay out column-major: fill columns c0,c0+1.. top to bottom; a syllable run must stay within a column (5 consecutive rows)
    nrows=rows[1]-rows[0]+1
    code={}; col=0; row=0
    def put(u):
        nonlocal col,row
        if row>=nrows: col+=1; row=0
        if col>=10: return False
        code[((c0+col)%10)+10*(rows[0]+row)]=u; row+=1; return True
    for ch,pre,sy,post in seq:
        for w in pre: put(w)
        if sy:
            if row+5>nrows: col+=1; row=0
            for s in sy: put(s)
        for w in post: put(w)
    return low,code
def encode(words,low,code,rnd):
    inv={}
    for k,u in code.items(): inv.setdefault(u,[]).append(k)
    linv=collections.defaultdict(list)
    for k,ch in low.items(): linv[ch].append(k)
    out=[]
    for w in words:
        if w in inv and rnd.random()<0.9: out.append(rnd.choice(inv[w])); continue
        i=0
        while i<len(w):
            for L in range(min(6,len(w)-i),1,-1):
                if w[i:i+L] in inv and rnd.random()<0.9: out.append(inv[w[i:i+L]][0]); i+=L; break
            else:
                if w[i] in linv: out.append(rnd.choice(linv[w[i]]))
                i+=1
    return out
def main(seed):
    rnd=random.Random(seed)
    words=words_from_corpus('fr1640_1720.txt',700)
    c0=rnd.randrange(10)
    low,code=build_code(rnd,words,c0)
    f=open('fr1640_1720.txt',encoding='utf-8',errors='ignore'); f.seek(60_000_000+seed*1_000_000); raw=f.read(400000)
    toks=[norm(w) for w in re.findall(r"[A-Za-zÀ-ÿſ]+",raw)]; toks=[t for t in toks if t]
    lens=[25,11,18,8,15,9,141,10,30,24,18]  # Chaulnes segment sizes (groups)
    segs=[]; pos=rnd.randrange(1000)
    for L in lens:
        pre=' '.join(toks[pos:pos+8]); pos+=8
        g=[]; plain=[]
        while len(g)<L:
            e=encode([toks[pos]],low,code,rnd)
            if len(g)+len(e)>L+2: break
            g+=e; plain.append(toks[pos]); pos+=1
        post=' '.join(toks[pos:pos+6]); pos+=6+rnd.randrange(50)
        segs.append(dict(pre=pre,groups=g,post=post,plain=' '.join(plain)))
    json.dump(dict(c0=c0,low={str(k):v for k,v in low.items()},code={str(k):v for k,v in code.items()},segs=segs),open(f'ctrl{seed}.json','w'))
    allg=[x for s in segs for x in s['groups']]
    print('seed',seed,'c0',c0,'groups',len(allg),'distinct',len(set(allg)),'max',max(allg),'low tokens',sum(x<80 for x in allg))
if __name__=='__main__':
    for s in sys.argv[1:]: main(int(s))

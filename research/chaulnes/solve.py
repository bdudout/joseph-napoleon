# Annealer for a column-major alphabetical one-part code (Croissy design).
import random,math,json,sys,collections,time
from lm6 import LM,norm
import wlm as _w
import math as _m
def _lp(self,prev,w):
    u=self.uni[w]/self.N
    if prev is not None and prev in self.uni:
        b=self.bi.get((prev,w),0)/self.uni[prev]; return _m.log(0.98*b+0.02*u)
    return _m.log(u)
_w.WLM.lp=_lp
from vocab import *
LOWMAX=80
class Problem:
    def __init__(s,segs,lm,words,c0,bonus=1.6):
        s.segs=segs; s.lm=lm; s.c0=c0; s.bonus=bonus
        s.ctx=[(norm(' '.join(x['pre'].split()[-3:])),norm(' '.join(x['post'].split()[:2]))) for x in segs]
        s.ctxs=[lm.score(a) for a,b in s.ctx]
        allg=sorted({g for x in segs for g in x['groups']})
        s.low=[g for g in allg if g<LOWMAX]; s.high=sorted([g for g in allg if g>=LOWMAX],key=s.rank)
        s.hpos={g:i for i,g in enumerate(s.high)}; s.lpos={g:i for i,g in enumerate(s.low)}
        s.occ=collections.defaultdict(set)
        for i,x in enumerate(segs):
            for g in x['groups']: s.occ[g].add(i)
        # unit inventory: (unit, initial, kind, cons, vowel)
        units={}
        for c,v,u in SYLS: units[u]=(u[0],'s',c,VOW.index(v))
        for w in list(dict.fromkeys(SUFF+DOMAIN+words)):
            w=norm(w)
            if len(w)>=2 and w not in units: units[w]=(w[0],'w',None,None)
        s.units=units
        s.byinit=collections.defaultdict(list)
        for u,(i,_,_,_) in units.items(): s.byinit[AIDX[i]].append(u)
    def rank(s,g): return ((g%10-s.c0)%10)*1000+g//10
    def dec_seg(s,i,st):
        return ''.join(st[g] for g in s.segs[i]['groups'])
    def seg_score(s,i,st):
        d=s.dec_seg(i,st); a,b=s.ctx[i]
        return s.lm.score(a+d+b)-s.ctxs[i]+s.bonus*len(d)
    def init(s,rnd,fixed=None):
        fixed=fixed or {}
        def ini(u): return AIDX[u[0]]
        def interp(codes,fx):
            n=len(codes); anchors=[(-1,0)]+[(i,ini(fx[g])) for i,g in enumerate(codes) if g in fx]+[(n,len(ALPHA)-1)]
            out=[]
            for i in range(n):
                a=max(x for x in anchors if x[0]<=i); b=min(x for x in anchors if x[0]>=i)
                if a[0]==b[0]: out.append(a[1]); continue
                out.append(a[1]+(b[1]-a[1])*(i-a[0])//(b[0]-a[0]))
            return out
        st={}
        for g,ai in zip(s.low,interp(s.low,fixed)): st[g]=fixed.get(g,ALPHA[ai])
        used=set(fixed.values())
        for g,ai in zip(s.high,interp(s.high,fixed)):
            if g in fixed: st[g]=fixed[g]; continue
            cands=[u for u in s.byinit[ai] if s.units[u][1]=='w' and u not in used]
            if not cands:
                for d in range(1,len(ALPHA)):
                    for aj in (ai-d,ai+d):
                        if 0<=aj<len(ALPHA) and not cands: cands=[u for u in s.byinit[aj] if s.units[u][1]=='w' and u not in used]
            u=rnd.choice(cands[:40]); st[g]=u; used.add(u)
        # occupy run slots implied by fixed syllables
        base={}
        for g,u in fixed.items():
            inf=s.units.get(u)
            if g>=LOWMAX and inf and inf[1]=='s': base[inf[2]]=g-10*inf[3]
        for c,b in base.items():
            for j in range(5):
                if b+10*j in st and b+10*j not in fixed: st[b+10*j]=syl(c,VOW[j])
        return st
    # constraints
    def ok_high(s,st,g,u):
        k=s.hpos[g]; ia=AIDX[s.units[u][0]] if u in s.units else 0
        if k>0:
            p=st[s.high[k-1]]
            if AIDX[p[0] if p[0]!='?' else p[1]]>ia: return False
        if k+1<len(s.high):
            q=st[s.high[k+1]]
            if AIDX[q[0] if q[0]!='?' else q[1]]<ia: return False
        return True
    def run_ok(s,st):
        # syllables of same consonant must share base (code - 10*vowel), and no foreign unit on an occupied run slot
        base={}
        for g in s.high:
            u=st[g]; inf=s.units.get(u)
            if inf and inf[1]=='s':
                b=g-10*inf[3]
                if base.setdefault(inf[2],b)!=b: return False
        slots={}
        for c,b in base.items():
            for j in range(5): slots[b+10*j]=syl(c,VOW[j])
        for g in s.high:
            if g in slots and st[g]!=slots[g]: return False
        return True
def anneal(P,iters,seed,T0=8.0,T1=0.3,log=None,fixed=None):
    rnd=random.Random(seed); fixed=fixed or {}; st=P.init(rnd,fixed)
    scores=[P.seg_score(i,st) for i in range(len(P.segs))]; cur=sum(scores)
    used=collections.Counter(st[g] for g in P.high)
    best=(cur,dict(st))
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        r=rnd.random()
        if r<0.35 and P.low:
            g=rnd.choice(P.low); k=P.lpos[g]
            lo=AIDX[st[P.low[k-1]]] if k>0 else 0; hi=AIDX[st[P.low[k+1]]] if k+1<len(P.low) else len(ALPHA)-1
            if lo>hi: continue
            new={g:ALPHA[rnd.randint(lo,hi)]}
        elif r<0.85:
            g=rnd.choice(P.high); k=P.hpos[g]
            def ini(x): return AIDX[x[0] if x[0]!='?' else x[1]]
            lo=ini(st[P.high[k-1]]) if k>0 else 0; hi=ini(st[P.high[k+1]]) if k+1<len(P.high) else len(ALPHA)-1
            if lo>hi: continue
            ai=rnd.randint(lo,hi)
            if rnd.random()<0.5 and ALPHA[ai] in CONS:
                u=syl(ALPHA[ai],rnd.choice(VOW))
            else:
                c=P.byinit[ai]
                if not c: continue
                u=rnd.choice(c[:rnd.choice([30,100,len(c)])])
            if used[u] and st[g]!=u: continue
            new={g:u}
        else:
            # run move: take a syllable code, shift its whole run to another consonant/vowel phase
            sy=[g for g in P.high if P.units.get(st[g],('', ''))[1]=='s']
            if not sy: continue
            g=rnd.choice(sy); c=P.units[st[g]][2]; v=P.units[st[g]][3]
            members=[h for h in sy if P.units[st[h]][2]==c]
            dv=rnd.choice([-2,-1,1,2]) if rnd.random()<0.5 else 0
            nc=c if dv else rnd.choice(CONS)
            new={}
            for h in members:
                vi=P.units[st[h]][3]+dv
                if not 0<=vi<5: new=None; break
                new[h]=syl(nc,VOW[vi])
            if not new: continue
            if any(used[u] and st[h]!=u and u not in [st[m] for m in members] for h,u in new.items()): continue
        if any(g in fixed for g in new): continue
        old={g:st[g] for g in new}
        st.update(new)
        if not all(P.ok_high(st,g,u) for g,u in new.items() if g>=LOWMAX) or not P.run_ok(st):
            st.update(old); continue
        segs=set().union(*(P.occ[g] for g in new))
        ns={i:P.seg_score(i,st) for i in segs}
        d=sum(ns[i]-scores[i] for i in segs)
        if d>=0 or rnd.random()<math.exp(d/T):
            for i in segs: scores[i]=ns[i]
            cur+=d
            for g in new:
                if g>=LOWMAX: used[old[g]]-=1; used[new[g]]+=1
            if cur>best[0]: best=(cur,dict(st))
        else: st.update(old)
        if log and it%log==0: print(it,round(T,2),round(cur,1),flush=True)
    return best
def accuracy(st,ctrl):
    key={int(k):v for k,v in ctrl['code'].items()}; key.update({int(k):v for k,v in ctrl['low'].items()})
    toks=[g for s in ctrl['segs'] for g in s['groups']]
    return sum(st.get(g)==key[g] for g in toks)/len(toks)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--ctrl'); ap.add_argument('--real',action='store_true'); ap.add_argument('--c0',type=int); ap.add_argument('--iters',type=int,default=200000); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--bonus',type=float,default=1.0); ap.add_argument('--init'); ap.add_argument('--nvoc',type=int,default=400); ap.add_argument('--crib',default=''); ap.add_argument('--fixjson',default=''); ap.add_argument('--tag',default='')
    a=ap.parse_args()
    lm=_w.WLM('wlm1690.pkl'); words=words_from_corpus('fr1640_1720.txt',a.nvoc,skip=45_000_000)
    if a.ctrl:
        ctrl=json.load(open(a.ctrl)); segs=ctrl['segs']
    else:
        from ch_parse import segs
    P=Problem(segs,lm,words,a.c0,a.bonus)
    fixed={}
    if a.crib and a.ctrl:
        tr={int(k):v for k,v in ctrl['code'].items()}; tr.update({int(k):v for k,v in ctrl['low'].items()})
        for si in map(int,a.crib.split(',')):
            for g in segs[si]['groups']: fixed[g]=tr[g]
        for g,u in fixed.items():
            if g>=LOWMAX and u not in P.units: P.units[u]=(u[0],'w',None,None); P.byinit[AIDX[u[0]]].append(u)
        print('fixed',len(fixed),'codes')
    if a.fixjson:
        for k,v in json.load(open(a.fixjson)).items(): fixed[int(k)]=v
        for g,u in fixed.items():
            if g>=LOWMAX and u not in P.units: P.units[u]=(u[0],'w',None,None); P.byinit[AIDX[u[0]]].append(u)
        print('fixed',len(fixed),'codes')
    t=time.time(); sc,st=anneal(P,a.iters,a.seed,log=a.iters//10,fixed=fixed)
    print('time',round(time.time()-t),'score',round(sc,1))
    if a.ctrl:
        print('acc',round(accuracy(st,ctrl),3))
        tr={int(k):v for k,v in ctrl['code'].items()}; tr.update({int(k):v for k,v in ctrl['low'].items()})
        print('true score',round(sum(P.seg_score(i,tr) for i in range(len(segs))),1))
    for i,s in enumerate(segs):
        print('|',P.dec_seg(i,st),'|', s.get('plain',''))
    json.dump({str(k):v for k,v in st.items()},open(f"st_{'ctrl' if a.ctrl else 'real'}_{a.c0}_{a.seed}{a.tag}.json",'w'))

import json,glob,math
from wlm import WLM
from lm6 import norm
m=WLM('wlm1690.pkl')
ctrl=json.load(open('ctrl1.json'))
tr={int(k):v for k,v in ctrl['code'].items()}; tr.update({int(k):v for k,v in ctrl['low'].items()})
segs=ctrl['segs']
def total(st,bonus,lam_bi,prior):
    WLM.lp_orig=getattr(WLM,'lp_orig',WLM.lp)
    def lp(s,prev,w):
        u=s.uni[w]/s.N
        if prev is not None and prev in s.uni:
            b=s.bi.get((prev,w),0)/s.uni[prev]; return math.log(lam_bi*b+(1-lam_bi)*u)
        return math.log(u)
    WLM.lp=lp
    sc=0
    for x in segs:
        pre=norm(' '.join(x['pre'].split()[-3:])); post=norm(' '.join(x['post'].split()[:2]))
        d=''.join(st[g] for g in x['groups'])
        sc+=m.score(pre+d+post)-m.score(pre)+bonus*len(d)
    # codebook prior: rare word entries
    ents={st[g] for g in st if g>=80}
    for e in ents:
        c=m.uni.get(e,1); sc+=prior*min(0,math.log(c/2000))
    return sc
sts=[{int(k):v for k,v in json.load(open(f)).items()} for f in sorted(glob.glob('st_ctrl_2_*.json'))]
for bonus in (0,1,2):
  for lam in (0.6,0.9,0.98):
    for prior in (0,1):
      t=total(tr,bonus,lam,prior); f=[total(s,bonus,lam,prior) for s in sts]
      print(bonus,lam,prior,'true',round(t),'found',[round(x) for x in f],'margin',round(t-max(f)))

from med import *
import sys
k=base_key()
cnt=collections.Counter(x for _,u in lines for x in u)
known=[x for x in cnt if cnt[x]>=2 and x not in NULL and x not in K0NUM and k.get(x)]
hits=0;top3=0;rows=[]
for x in sorted(known,key=lambda x:-cnt[x]):
    top,allr=test(x,k,top=5)
    truth=k[x]; ranks=[c for _,c in allr]
    r=ranks.index(truth)+1 if truth in ranks else None
    hits+=r==1; top3+=(r or 99)<=3
    rows.append((x,cnt[x],truth,r,[c for _,c in top[:3]]))
    print(x,cnt[x],'vrai=',truth,'rang',r,'top3',[c for _,c in top[:3]],flush=True)
print('LOO: rang 1',hits,'/',len(known),' top3',top3)

from med import *
import sys
k=base_key()
for x in sys.argv[1:]:
    top,allr=test(x,k,top=8)
    cur=k.get(x); ranks=[c for _,c in allr]
    print(x,'occ',sum(u.count(x) for _,u in lines),'actuel=',cur,'rang',(ranks.index(cur)+1 if cur in ranks else '-'),'| meilleurs:',[(c,round(s-top[0][0],1)) for s,c in top],flush=True)

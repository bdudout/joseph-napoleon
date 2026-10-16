from load import *
import sys
K0={'26':'BIEN','34':'TANT','40':'FAICT','70':'TOUTE','10':'DICT','82':'CEULX','37':'CAR','XP':'','T6':'','SEP_SLASH':'|','POUR':'','ASSEZ':'','CAR':'','QUOG':'','TF':'','MM':''}
def dec(lbl):
    if lbl in K0: return K0[lbl]
    v=kv(lbl)
    return v if v not in (None,'') else '['+lbl+']'
for ln,u in lines:
    print(ln, ''.join(dec(x) for x in u))

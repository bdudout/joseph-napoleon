import json,collections
import os
B=os.path.join(os.environ.get('CYPHERSOLVER','cyphersolver'),'targets/foix1563/beck-preliminary/data/')
src=json.load(open(B+'source.json')); key=json.load(open(B+'key.json'))['key']
def kv(lbl):
    e=key.get(lbl)
    if e is None: return None
    if isinstance(e,dict): return e.get('value', e.get('plaintext'))
    return e
lines=[(l['line'],[u['label'] for u in l['units']]) for l in src]

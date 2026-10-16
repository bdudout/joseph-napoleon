import csv,os,re,sys,glob
R='corp/FreEMmax_OA/'
idx={}
for p in glob.glob(R+'0_source/**/*.xml',recursive=True): idx.setdefault(os.path.basename(p),p)
def txt(p):
    s=open(p,encoding='utf-8',errors='ignore').read()
    m=re.search(r'<text[\s>].*',s,re.S); s=m.group(0) if m else s
    s=re.sub(r'<(note|teiHeader)[\s\S]*?</\1>',' ',s)
    s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'&[a-z]+;',' ',s)
    return re.sub(r'\s+',' ',s)
for name,lo,hi in [('fr1640_1720',1640,1720),('fr1540_1600',1540,1600)]:
    out=open(f'work/{name}.txt','w'); n=0; files=0
    for r in csv.DictReader(open(R+'TOC.tsv'),delimiter='\t'):
        try: d=int(r['Date'][:4])
        except: continue
        if not(lo<=d<=hi) or r['Form'] not in('prose','mixed') or r['Genre'] in('theatre','poetry'): continue
        p=idx.get(os.path.basename(r['File'].strip()))
        if not p: continue
        t=txt(p); out.write(t+'\n'); n+=len(t); files+=1
    print(name,files,n)

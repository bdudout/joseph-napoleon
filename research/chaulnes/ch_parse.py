import re,collections
segs=[]
for line in open(__import__('os').path.join(__import__('os').path.dirname(__file__),'ciphertext.txt')):
    if not line.startswith('['): continue
    tag,rest=line.split(']',1); parts=rest.split('|')
    # alternate clear / cipher: parts[0] clear, parts[1] cipher, parts[2] clear, ...
    for i in range(1,len(parts),2):
        g=[int(re.sub(r'[_^]','',x)) for x in parts[i].split()]
        segs.append(dict(tag=tag[1:],pre=parts[i-1].strip(),groups=g,post=parts[i+1].strip() if i+1<len(parts) else ''))
allg=[x for s in segs for x in s['groups']]

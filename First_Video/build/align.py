import json, re
from difflib import SequenceMatcher
LEAD=0.35; TAIL=0.6
VOICE_DUR=102.113
asr=json.load(open('asr_parakeet.json'))
beats=json.load(open('beats_src.json'))
# ASR words
W=[]
for seg in asr:
    cur=None
    for t in seg['tokens']:
        if t['t'].startswith(' ') or cur is None:
            if cur: W.append(cur)
            cur={'w':t['t'].strip(),'s':t['s'],'seg_end':seg['b']}
        else: cur['w']+=t['t']
    if cur: W.append(cur)
for i,w in enumerate(W):
    nxt=W[i+1]['s'] if i+1<len(W) else VOICE_DUR
    w['e']=round(min(nxt, w['s']+0.7, w['seg_end']),3)
    w['n']=re.sub(r'[^a-z0-9]','',w['w'].lower())
ASR_SPLIT=[]  # split asr words that glue e.g. 'subtimeline' kept as is
ANCHORS={'edits','resolve','claude','terminal','settings','automation','bridge','mcp','popup','edit','instagram','davinci','apple','silicon','copy','download','workspace','scripts','commands','connected','timeline','subtitles','music','clips','prompt','render','import','vertical','desktop','tools','restart','project','comment','dm','guide','server','enable','code','post','tweak','list','fix','blackmagic','mac','sign','in','running'}
SPOKEN={'1':'ek','2':'do','3':'teen','4':'chaar','/mcp':'slash mcp','dm':'dm','claude':'claude'}
# caption words
C=[]
for bi,(bid,role,line) in enumerate(beats):
    toks=line.split()
    bold=False
    for tk in toks:
        st=tk.startswith('**'); 
        t=tk.replace('**','') 
        b_on = bold or st
        if st: bold=True
        if tk.endswith('**') or tk.rstrip('.,?:!').endswith('**'): 
            en=True
        else: en=False
        disp=re.sub(r'[.,:!]+$','',t)
        if disp.endswith('?'): pass
        key=disp.lower().rstrip('?')
        spoken=SPOKEN.get(key,key)
        C.append({'beat':bid,'bi':bi,'text':disp,'hl':b_on,'key':re.sub(r'[^a-z0-9 ]','',spoken),'punct':t[len(disp):] if len(t)>len(disp) else ''})
        if en: bold=False
# simple phonetic normalisation
def ph(s):
    s=s.replace(' ','')
    s=s.replace('ee','i').replace('oo','u').replace('aa','a').replace('w','v').replace('z','j')
    s=s.replace('ph','f').replace('kh','k').replace('th','t').replace('dh','d').replace('bh','b').replace('ch','c').replace('sh','s').replace('gh','g')
    s=s.replace('y','i').replace('c','k').replace('q','k')
    return s
def sim(a,b):
    if not a or not b: return 0
    return max(SequenceMatcher(None,a,b).ratio(), SequenceMatcher(None,ph(a),ph(b)).ratio())
n,m=len(C),len(W)
import numpy as np
S=np.zeros((n+1,m+1)); P=np.zeros((n+1,m+1),dtype=int)
G=-0.35
for i in range(1,n+1): S[i,0]=S[i-1,0]+G; P[i,0]=1
for j in range(1,m+1): S[0,j]=S[0,j-1]+G; P[0,j]=2
sc={}
for i in range(1,n+1):
    for j in range(1,m+1):
        r=sim(C[i-1]['key'],W[j-1]['n']); sc[(i,j)]=r
        d=S[i-1,j-1]+(r*2-0.9)
        u=S[i-1,j]+G; l=S[i,j-1]+G
        best=max(d,u,l); S[i,j]=best; P[i,j]=0 if best==d else (1 if best==u else 2)
i,j=n,m; pairs={}
while i>0 and j>0:
    if P[i,j]==0: pairs[i-1]=(j-1,sc[(i,j)]); i-=1;j-=1
    elif P[i,j]==1: i-=1
    else: j-=1
# anchors
for k,c in enumerate(C):
    c['asr']=None
    if k in pairs:
        j,r=pairs[k]
        c['asr']=W[j]['w']; c['sim']=round(r,2)
        thr=0.72 if c['key'] in ANCHORS else 0.78
        if r>=thr:
            c['s']=W[j]['s']; c['e']=W[j]['e']; c['anchored']=True
# ensure monotonic anchors
last=-1
for c in C:
    if c.get('anchored'):
        if c['s']<=last: c['anchored']=False; c.pop('s');c.pop('e')
        else: last=c['s']
# interpolate unanchored, weighted by length, between anchors (use speech end ~ VOICE_DUR-0.25)
idx=[k for k,c in enumerate(C) if c.get('anchored')]
bounds=[(-1,0.05)]+[(k,C[k]['s']) for k in idx]+[(len(C),101.82)]
for (ka,ta),(kb,tb) in zip(bounds,bounds[1:]):
    # span from end of anchor ka to tb
    if ka>=0:
        t0=max(C[ka]['s']+0.12, min(C[ka]['e'], tb-0.14*(kb-ka-1)))
        C[ka]['e']=round(t0,3)
    else: t0=ta
    gap=list(range(ka+1,kb))
    if not gap:
        continue
    L=[len(C[g]['key'])+2 for g in gap]; tot=sum(L)
    t=t0; span=max(tb-t0,0.05*len(gap))
    for g,l in zip(gap,L):
        C[g]['s']=round(t,3); t+=span*l/tot; C[g]['e']=round(t,3)
# end times: word end = min(own end, next start)
for k,c in enumerate(C):
    if k+1<len(C): c['e']=round(min(c['e'],C[k+1]['s']) if c['e']>c['s'] else C[k+1]['s'],3)
    if c['e']<=c['s']: c['e']=round(c['s']+0.12,3)
# silence gaps refine beat edges: snap beat start to nearest silence end within 0.4s
sil=[(3.87,4.24),(5.63,6.00),(6.25,6.62),(10.87,11.25),(12.50,12.85),(18.92,19.25),(20.05,20.32),(20.93,21.24),(22.37,22.77),(23.59,23.97),(28.75,29.10),(29.80,30.15),(34.46,34.74),(36.71,37.09),(37.90,38.20),(43.61,43.97),(44.77,45.08),(45.86,46.13),(47.27,47.63),(48.25,48.50),(49.06,49.41),(50.12,50.45),(52.55,52.84),(56.86,57.13),(58.75,59.01),(63.56,63.84),(70.06,70.33),(75.29,75.55),(76.88,77.15),(79.36,79.71),(80.22,80.51),(81.13,81.38),(86.42,86.70),(91.25,91.53),(95.86,96.12),(99.86,100.14),(101.82,102.10)]
B=[]
for bi,(bid,role,line) in enumerate(beats):
    ws=[c for c in C if c['bi']==bi]
    s=ws[0]['s']; e=ws[-1]['e']
    B.append({'id':bid,'role':role,'line':line.replace('**',''),'vs':s,'ve':e})
for bi,b in enumerate(B):
    cand=[se for ss,se in sil if abs(se-b['vs'])<0.45]
    if cand and bi>0:
        ns=min(cand,key=lambda x:abs(x-b['vs']))
        ws=[c for c in C if c['bi']==bi]
        if not ws[0].get('anchored'): ws[0]['s']=ns
        b['vs']=ns
    cand=[ss for ss,se in sil if abs(ss-b['ve'])<0.6]
    if cand:
        b['ve']=min(cand,key=lambda x:abs(x-b['ve']))
for k,c in enumerate(C):
    if k+1<len(C) and c['e']>C[k+1]['s']: c['e']=C[k+1]['s']
for b in B:
    b['start']=round(b['vs']+LEAD,3); b['end']=round(b['ve']+LEAD,3); b['vs']=round(b['vs'],3); b['ve']=round(b['ve'],3)
prev=-1
for c in C:
    if c['s']<prev+0.07: c['s']=round(prev+0.07,3)
    prev=c['s']
for k,c in enumerate(C):
    nx=C[k+1]['s'] if k+1<len(C) else c['e']
    if c['e']<=c['s'] or c['e']>nx: c['e']=round(max(min(nx,c['e']),c['s']+0.07),3)
for c in C:
    c['t0']=round(c['s']+LEAD,3); c['t1']=round(c['e']+LEAD,3)
total=round(VOICE_DUR+LEAD+TAIL,3)
out={'fps':30,'lead_in':LEAD,'tail':TAIL,'voice_duration':VOICE_DUR,'total':total,'asr':'sherpa-onnx parakeet-tdt-0.6b-v3 (faster-whisper models blocked)','beats':B,'words':[{k:c.get(k) for k in ['beat','text','punct','hl','t0','t1','anchored','asr','sim']} for c in C]}
json.dump(out,open('../timeline.json','w'),indent=1,ensure_ascii=False)
print('total',total,'anchored',sum(1 for c in C if c.get('anchored')),'/',len(C))
for b in B: print(b['id'],b['start'],b['end'],round(b['end']-b['start'],2))

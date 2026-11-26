# G2 and voice-intact check: transcribe the final mix, compare English anchor word starts with caption word times.
import json, re, numpy as np, soundfile as sf, sherpa_onnx, librosa
from difflib import SequenceMatcher
T=json.load(open('../timeline.json')); LEAD=T['lead_in']
x,sr=sf.read('../reel/assets/audio/mix.wav'); x=x.mean(1) if x.ndim>1 else x
x=librosa.resample(x.astype('float32'),orig_sr=sr,target_sr=16000); sr=16000
src=open('asr_sherpa.py').read(); sil=eval(src[src.index('sil=')+4:src.index('\n',src.index('sil='))])
cuts=[0.0]+[(a+b)/2+LEAD for a,b in sil]+[len(x)/sr]
p="/opt/asr/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/"
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=p+"encoder.int8.onnx",decoder=p+"decoder.int8.onnx",joiner=p+"joiner.int8.onnx",tokens=p+"tokens.txt",model_type="nemo_transducer",num_threads=4)
W=[];text=[]
for a,b in zip(cuts,cuts[1:]):
    s=rec.create_stream(); s.accept_waveform(sr,x[int(a*sr):int(b*sr)]); rec.decode_stream(s); r=s.result
    text.append(r.text); cur=None
    for t,ts in zip(r.tokens,r.timestamps):
        if t.startswith(' ') or cur is None:
            if cur: W.append(cur)
            cur={'w':t.strip(),'s':a+ts}
        else: cur['w']+=t
    if cur: W.append(cur)
orig=" ".join(s['text'] for s in json.load(open('asr_parakeet.json')))
sim=SequenceMatcher(None,orig.lower().split(),(" ".join(text)).lower().split(),autojunk=False).ratio()
ANCH={'edits','resolve','claude','terminal','settings','automation','bridge','mcp','popup','edit','instagram','copy','download','workspace','scripts','connected','timeline','subtitles','music','commands','render'}
diffs=[]
for w in T['words']:
    k=re.sub(r'[^a-z]','',w['text'].lower())
    if k in ANCH and w['anchored']:
        c=[a for a in W if re.sub(r'[^a-z]','',a['w'].lower()).startswith(k[:4]) and abs(a['s']-w['t0'])<0.5]
        if c:
            best=min(c,key=lambda a:abs(a['s']-w['t0'])); diffs.append(abs(best['s']-w['t0']))
d=np.array(diffs)
res={'voice_transcript_similarity_to_source':round(sim,3),'anchors_compared':len(d),'max_offset_frames':round(float(d.max()*30),2),'mean_offset_frames':round(float(d.mean()*30),2),'within_3_frames':int((d<=0.1+1e-6).sum())}
json.dump(res,open('g2.json','w'),indent=1); print(res)

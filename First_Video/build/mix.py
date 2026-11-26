import json, subprocess, numpy as np, soundfile as sf, pyloudnorm as pyln, sys
SR=48000
R='../reel/assets/'
plan=json.load(open('plan.json')); sfxt=plan['sfx']
T=json.load(open('../timeline.json')); TOTAL=T['total']; LEAD=T['lead_in']
N=int(round(TOTAL*SR))
# voice chain: high-pass 80 Hz, de-ess, 3:1 compression, then -16 LUFS
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','../voice/voiceover.wav','-af',
  'highpass=f=80,deesser=i=0.4,acompressor=threshold=-9dB:ratio=3:attack=15:release=200:makeup=1','-ar','48000','-ac','1','voice_proc.wav'],check=True)
v,_=sf.read('voice_proc.wav'); meter=pyln.Meter(SR)
v=v*10**((-16-meter.integrated_loudness(v))/20)
voice=np.zeros(N); s=int(LEAD*SR); voice[s:s+len(v)]=v[:N-s]
# music bed, sidechain ducked by the voice
m,_=sf.read(R+'music/bed.wav'); m=m.mean(1) if m.ndim>1 else m
mm=np.zeros(N); mm[:min(N,len(m))]=m[:N]
mm=mm*10**((-16-meter.integrated_loudness(mm[:int((TOTAL-2)*SR)]))/20)
win=int(0.02*SR); rms=np.sqrt(np.convolve(voice**2,np.ones(win)/win,'same'))
act=(rms>10**(-42/20)).astype(float)
# attack 40 ms, release 350 ms smoothing
g=np.zeros(N); a1=np.exp(-1/(0.04*SR)); r1=np.exp(-1/(0.35*SR)); z=0.0
for i in range(0,N,48):
    x=act[i]; c=a1 if x>z else r1; z=x+(z-x)*(c**48); g[i:i+48]=z
duck_db=-18*g+(-12)*(1-g)   # 18 dB under the voice while it speaks, 12 dB in the gaps
# music drop to near silence for one line in S12 (from the B12 cut to the hit)
d0=int(plan['cuts']['B12']*SR); d1=int(sfxt['hit']*SR)
ramp=int(0.12*SR)
drop=np.zeros(N); drop[d0:d1]=-26
drop[d0:d0+ramp]=np.linspace(0,-26,ramp); drop[d1-ramp:d1]=np.linspace(-26,0,ramp)
music=mm*10**((duck_db+drop)/20)
# sound moments
def place(name,t,db):
    x,_=sf.read(R+f'sfx/{name}.wav'); x=x.mean(1) if x.ndim>1 else x
    i=int(round(t*SR)); L=min(len(x),N-i); out=np.zeros(N); out[i:i+L]=x[:L]*10**(db/20); return out
fx=np.zeros(N)
moments=[('sting','sting1',-14),('riser','riser',-22),('impact','impact',-15),('click','toggle',-16),('chime','chime1',-17),
         ('whoosh','whoosh',-21),('click','menu_click',-16),('chime','chime2',-17),('hit','hit',-15),('sting','sting2',-14)]
for name,key,db in moments: fx+=place(name,sfxt[key],db)
# loop: tiny fades so nothing clicks at the loop point
fade=int(0.004*SR)
def finish(x,path):
    x=x.copy(); x[:fade]*=np.linspace(0,1,fade); x[-int(0.25*SR):]*=np.linspace(1,0,int(0.25*SR))
    sf.write('pre_'+path.split('/')[-1],np.stack([x,x],1),SR,subtype='FLOAT')
    # gain to -14 LUFS, then a peak limiter (oversampled) keeps true peak under -1 dBTP; linear, so the loudness range stays
    y,_=sf.read('pre_'+path.split('/')[-1]); m_=pyln.Meter(SR); y=y*10**((-13.05-m_.integrated_loudness(y))/20)
    sf.write('pre2.wav',y,SR,subtype='FLOAT')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','pre2.wav','-af','aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=false,aresample=48000','-c:a','pcm_s16le',path],check=True)
finish(voice+music+fx, R+'audio/mix.wav')
finish(voice+fx, R+'audio/mix_nomusic.wav')
print('done')

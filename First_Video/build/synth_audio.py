# Code-made music bed and sound effects (CC0, generated here). 48 kHz.
import numpy as np, soundfile as sf, json
SR=48000; rng=np.random.default_rng(7)
OUT='../reel/assets/'
TOTAL=json.load(open('../timeline.json'))['total']
def env(n,a,d,s=0.0,r=None):
    t=np.arange(n)/SR
    e=np.minimum(1,t/max(a,1e-4))*np.exp(-np.maximum(0,t-a)/max(d,1e-4))
    return e*(1-s)+s
def lp(x,c):  # one-pole lowpass
    a=np.exp(-2*np.pi*c/SR); y=np.zeros_like(x); z=0.0
    for i in range(len(x)): z=(1-a)*x[i]+a*z; y[i]=z
    return y
def lp_fast(x,c):
    from scipy.signal import butter,sosfilt
    return sosfilt(butter(2,c,fs=SR,output='sos'),x)
def hp_fast(x,c):
    from scipy.signal import butter,sosfilt
    return sosfilt(butter(2,c,btype='high',fs=SR,output='sos'),x)
def note(f): return 440*2**((f-69)/12)
# ---------- music bed: 96 BPM warm lofi pad ----------
BPM=96; beat=60/BPM; bar=4*beat
N=int((TOTAL+1)*SR); t=np.arange(N)/SR
mus=np.zeros(N)
prog=[[53,57,60,64],[57,60,64,67],[50,53,57,60],[48,52,55,59]]  # Fmaj7 Am7 Dm7 Cmaj7
bass=[41,45,38,36]
nb=int(np.ceil(TOTAL/bar))+1
pad=np.zeros(N); bs=np.zeros(N); kick=np.zeros(N); hat=np.zeros(N); keys=np.zeros(N)
for b in range(nb):
    c=prog[b%4]; s0=int(b*bar*SR); L=int(bar*SR)
    if s0>=N: break
    L=min(L,N-s0); tt=np.arange(L)/SR
    e=np.minimum(1,tt/0.25)*np.minimum(1,(bar-tt)/0.3)
    for m in c:
        f=note(m)
        pad[s0:s0+L]+=e*(np.sin(2*np.pi*f*tt)+0.5*np.sin(2*np.pi*f*1.003*tt+1)+0.25*np.sin(2*np.pi*2*f*tt))*0.06
    fb=note(bass[b%4])
    for k in range(4):
        ks=s0+int(k*beat*SR); kl=min(int(beat*SR),N-ks)
        if kl<=0: continue
        kt=np.arange(kl)/SR
        bs[ks:ks+kl]+=np.sin(2*np.pi*fb*kt)*np.exp(-kt/0.35)*0.22
        if k in (0,2):
            fk=50+70*np.exp(-kt/0.03)
            kick[ks:ks+kl]+=np.sin(2*np.pi*np.cumsum(fk)/SR)*np.exp(-kt/0.16)*0.5
        # soft keys arpeggio on offbeats
        hs=ks+int(beat/2*SR); hl=min(int(0.08*SR),N-hs)
        if hl>0: hat[hs:hs+hl]+=rng.standard_normal(hl)*np.exp(-np.arange(hl)/SR/0.018)*0.06
        m=c[(k+b)%4]+12; f=note(m); al=min(int(0.6*SR),N-hs)
        if al>0:
            at=np.arange(al)/SR
            keys[hs:hs+al]+=(np.sin(2*np.pi*f*at)+0.3*np.sin(2*np.pi*2*f*at))*np.exp(-at/0.25)*0.05
pad=lp_fast(pad,1800); hat=hp_fast(hat,6000)
mus=pad+bs+kick+hat+keys
mus=lp_fast(mus,9000)
# fades for the loop
fi=int(0.4*SR); fo=int(1.2*SR); mus[:fi]*=np.linspace(0,1,fi); 
end=int(TOTAL*SR); mus[end-fo:end]*=np.linspace(1,0,fo); mus[end:]=0
mus=mus/np.max(np.abs(mus))*0.5
st=np.stack([mus, np.roll(mus,int(0.012*SR))*0.96],1)
sf.write(OUT+'music/bed.wav',st[:end],SR)
# ---------- SFX ----------
def save(n,x):
    x=x/np.max(np.abs(x))*0.7
    f=int(0.004*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f)
    sf.write(OUT+f'sfx/{n}.wav',x,SR)
def bell(f,d=1.2,amp=1):
    n=int(d*SR); tt=np.arange(n)/SR
    return amp*(np.sin(2*np.pi*f*tt+1.2*np.sin(2*np.pi*f*2*tt)*np.exp(-tt/0.3)))*np.exp(-tt/0.45)*np.minimum(1,tt/0.004)
def seq(parts,total):
    x=np.zeros(int(total*SR))
    for at,y in parts:
        s=int(at*SR); L=min(len(y),len(x)-s); x[s:s+L]+=y[:L]
    return x
sting=seq([(0,bell(note(72))),(0.13,bell(note(76))),(0.26,bell(note(79),1.0))],1.3)
save('sting',sting)
# riser 1.1 s noise sweep + impact
n=int(1.1*SR); tt=np.arange(n)/SR
from scipy.signal import butter,sosfilt
ri=rng.standard_normal(n); out=np.zeros(n)
for k in range(10):
    a,b=k*n//10,(k+1)*n//10
    out[a:b]=sosfilt(butter(2,[300+k*500,800+k*900],btype='band',fs=SR,output='sos'),ri[a:b])
ri=out*(tt/tt[-1])**2
save('riser',ri)
n=int(0.7*SR); tt=np.arange(n)/SR
imp=np.sin(2*np.pi*np.cumsum(45+90*np.exp(-tt/0.04))/SR)*np.exp(-tt/0.22)+lp_fast(rng.standard_normal(n),2500)*np.exp(-tt/0.05)*0.5
save('impact',imp)
n=int(0.06*SR); tt=np.arange(n)/SR
clk=hp_fast(rng.standard_normal(n),2000)*np.exp(-tt/0.006)+np.sin(2*np.pi*1800*tt)*np.exp(-tt/0.01)*0.6
save('click',clk)
chime=seq([(0,bell(note(84),0.9,0.8)),(0.09,bell(note(88),1.0))],1.2)
save('chime',chime)
n=int(0.6*SR); tt=np.arange(n)/SR
wn=rng.standard_normal(n); out=np.zeros(n)
for k in range(12):
    a,b=k*n//12,(k+1)*n//12; fc=400+2400*np.sin(np.pi*k/12)
    out[a:b]=sosfilt(butter(2,[fc*0.6,fc*1.4],btype='band',fs=SR,output='sos'),wn[a:b])
save('whoosh',out*np.sin(np.pi*tt/tt[-1]))
n=int(0.9*SR); tt=np.arange(n)/SR
hit=np.sin(2*np.pi*np.cumsum(55+60*np.exp(-tt/0.05))/SR)*np.exp(-tt/0.3)+bell(note(79),0.9,0.35)[:n]
save('hit',hit)
print('ok',TOTAL)

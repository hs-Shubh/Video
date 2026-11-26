import json, sys, numpy as np, soundfile as sf, sherpa_onnx, librosa
wav = sys.argv[1]
x, sr = sf.read(wav, dtype="float32")
x16 = librosa.resample(x, orig_sr=sr, target_sr=16000); sr=16000
# split at silence midpoints so chunks stay under ~14 s
sil=[(3.87,4.24),(5.63,6.00),(6.25,6.62),(10.87,11.25),(12.50,12.85),(18.92,19.25),(20.05,20.32),(20.93,21.24),(22.37,22.77),(23.59,23.97),(28.75,29.10),(29.80,30.15),(34.46,34.74),(36.71,37.09),(37.90,38.20),(43.61,43.97),(44.77,45.08),(45.86,46.13),(47.27,47.63),(48.25,48.50),(49.06,49.41),(50.12,50.45),(52.55,52.84),(56.86,57.13),(58.75,59.01),(63.56,63.84),(70.06,70.33),(75.29,75.55),(76.88,77.15),(79.36,79.71),(80.22,80.51),(81.13,81.38),(86.42,86.70),(91.25,91.53),(95.86,96.12),(99.86,100.14),(101.82,102.10)]
cuts=[0.0]+[ (a+b)/2 for a,b in sil ]+[len(x16)/sr]
D="/opt/asr/"
which=sys.argv[2]
if which=="dolphin":
    rec=sherpa_onnx.OfflineRecognizer.from_dolphin_ctc(model=D+"sherpa-onnx-dolphin-small-ctc-multi-lang-int8-2025-04-02/model.int8.onnx",tokens=D+"sherpa-onnx-dolphin-small-ctc-multi-lang-int8-2025-04-02/tokens.txt",num_threads=4)
else:
    p=D+"sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/"
    rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=p+"encoder.int8.onnx",decoder=p+"decoder.int8.onnx",joiner=p+"joiner.int8.onnx",tokens=p+"tokens.txt",model_type="nemo_transducer",num_threads=4)
segs=[]
for i in range(len(cuts)-1):
    a,b=cuts[i],cuts[i+1]
    s=rec.create_stream(); s.accept_waveform(sr, x16[int(a*sr):int(b*sr)]); rec.decode_stream(s)
    r=s.result
    toks=[{"t":t,"s":round(a+ts,3)} for t,ts in zip(r.tokens, r.timestamps)]
    segs.append({"a":round(a,3),"b":round(b,3),"text":r.text,"tokens":toks})
    print(f"{a:6.2f}-{b:6.2f} {r.text}")
json.dump(segs,open(f"asr_{which}.json","w"),ensure_ascii=False,indent=1)

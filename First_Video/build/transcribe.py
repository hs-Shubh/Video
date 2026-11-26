import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8")
segs, info = m.transcribe(sys.argv[1], language="hi", word_timestamps=True, vad_filter=False, beam_size=5)
out=[]
for s in segs:
    for w in s.words:
        out.append({"w":w.word.strip(),"s":round(w.start,3),"e":round(w.end,3),"p":round(w.probability,3)})
json.dump(out, open(sys.argv[3],"w"), ensure_ascii=False, indent=0)
print(len(out))

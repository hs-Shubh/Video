# Privacy scan: OCR every 2x frame of S06 and S07 (the Access Token scenes) and fail on any token-like string.
import json, os, re, subprocess, glob
from concurrent.futures import ProcessPoolExecutor

B = os.path.abspath(os.path.dirname(__file__))
P = json.load(open(B + "/plan.json"))
a, b = P["cuts"]["B05"], P["cuts"]["B08"]
D = B + "/ocr_frames"
os.makedirs(D, exist_ok=True)
os.environ["OMP_THREAD_LIMIT"] = "1"
need = int(round((b - a) * 30))
if len(glob.glob(D + "/*.png")) < need - 2:
    for f in glob.glob(D + "/*.png"):
        os.remove(f)
    subprocess.run(f'ffmpeg -y -loglevel error -ss {a} -to {b} -i "{B}/render/master_2x.mp4" -start_number 0 "{D}/f%05d.png"', shell=True, check=True)
frames = sorted(glob.glob(D + "/*.png"))
# token-like: long unbroken runs of letters and digits, or common key prefixes
TOK = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9_\-]*\d)(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9]{8,}|eyJ[A-Za-z0-9_\-]{10,}|[A-Fa-f0-9]{32,}|[A-Z]{3}-[A-Z]{3}-[A-Z]{3}")


def ocr(p):
    txt = subprocess.run(["tesseract", p, "-", "--psm", "11"], capture_output=True, text=True).stdout
    return p, txt


hits, seen_hidden = [], 0
with ProcessPoolExecutor(4) as ex:
    for p, txt in ex.map(ocr, frames):
        if "hidden" in txt:
            seen_hidden += 1
        for m in TOK.findall(txt):
            hits.append((os.path.basename(p), m))
res = {"scenes": "S05, S06 and S07 (all real Edits footage)", "range_s": [a, b], "frames_scanned": len(frames), "frames_showing_placeholder": seen_hidden,
       "token_like_hits": hits[:50], "pass": not hits}
json.dump(res, open(B + "/privacy_scan.json", "w"), indent=1)
print(json.dumps(res, indent=1))

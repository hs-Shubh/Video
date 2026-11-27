# Proves the masked footage holds no secret: OCR every frame, compare with the secrets read from the raw files (never printed).
import glob, os, re, subprocess, json
from concurrent.futures import ProcessPoolExecutor
os.environ["OMP_THREAD_LIMIT"] = "1"
U = "/root/.claude/uploads/715d3f00-c5ce-56c6-92d2-658ba45b7738"
O = os.path.abspath(os.path.dirname(__file__) + "/../reel/assets/footage")
T = "/tmp/claude-0/-home-user-Video/715d3f00-c5ce-56c6-92d2-658ba45b7738/scratchpad/maskcheck"
os.makedirs(T, exist_ok=True)
def ocr(p): return subprocess.run(["tesseract", p, "-", "--psm", "11"], capture_output=True, text=True).stdout
# secrets as read from the raw sources
raw = ocr(sorted(glob.glob(T + "/../rec/rec1_f.png"))[0])
tok = max(re.findall(r"[A-Za-z0-9]{30,}", raw), key=len)
login = re.findall(r"[A-Z]{3}-[A-Z]{3}-[A-Z]{3}", ocr("/tmp/claude-0/-home-user-Video/715d3f00-c5ce-56c6-92d2-658ba45b7738/images/4.png"))
secrets = [tok[:12], tok[-12:]] + [c[:7] for c in login]
for f in glob.glob(T + "/*.png"): os.remove(f)
for mp4 in glob.glob(O + "/*.mp4"):
    n = os.path.basename(mp4)[:-4]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp4, f"{T}/{n}_%04d.png"], check=True)
frames = sorted(glob.glob(T + "/*.png")) + sorted(glob.glob(O + "/*.png"))
TOK = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]{20,}")
hits = []
with ProcessPoolExecutor(4) as ex:
    for p, txt in zip(frames, ex.map(ocr, frames)):
        flat = txt.replace(" ", "")
        if any(s in flat for s in secrets) or TOK.search(txt):
            hits.append(os.path.basename(p))
res = {"frames_checked": len(frames), "hits": hits, "pass": not hits}
json.dump(res, open(os.path.dirname(os.path.abspath(__file__)) + "/footage_mask_check.json", "w"), indent=1)
print(res)

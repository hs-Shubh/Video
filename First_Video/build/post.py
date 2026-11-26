# Encodes the deliverables from the 2x render and runs the measurable quality gates.
import json, os, re, subprocess, glob, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.dirname(__file__) + "/..")
B = ROOT + "/build"
OUT = ROOT + "/renders"
os.makedirs(OUT, exist_ok=True)
T = json.load(open(ROOT + "/timeline.json"))
P = json.load(open(B + "/plan.json"))
TOTAL = T["total"]
FPS = 30
SRC = B + "/render/master_2x.mp4"
MIX = ROOT + "/reel/assets/audio/mix.wav"
NOM = ROOT + "/reel/assets/audio/mix_nomusic.wav"
gates = {}


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(cmd)
    return r.stdout + r.stderr


ENC = "-c:v libx264 -profile:v high -crf 17 -preset slow -tune animation -pix_fmt yuv420p -movflags +faststart"
AUD = "-c:a aac -b:a 320k -ar 48000"
SCALE = "scale=1080:1920:flags=lanczos"
step = sys.argv[1] if len(sys.argv) > 1 else "all"

if step in ("all", "encode"):
    # master: 2x frames, Lanczos downscale, final mix
    run(f'ffmpeg -y -loglevel error -i "{SRC}" -i "{MIX}" -map 0:v -map 1:a -vf {SCALE} {ENC} {AUD} -t {TOTAL} "{OUT}/EDITS_RESOLVE_9x16.mp4"')
    run(f'ffmpeg -y -loglevel error -i "{SRC}" -i "{NOM}" -map 0:v -map 1:a -vf {SCALE} {ENC} {AUD} -t {TOTAL} "{OUT}/EDITS_RESOLVE_nomusic.mp4"')
    # phone copy: two pass, sized for under 30 MB
    vb = int((27.5 * 8 * 1024 * 1024 / TOTAL - 160_000) / 1000)
    os.chdir(B)
    run(f'ffmpeg -y -loglevel error -i "{OUT}/EDITS_RESOLVE_9x16.mp4" -c:v libx264 -preset slow -b:v {vb}k -pass 1 -an -f null /dev/null')
    run(f'ffmpeg -y -loglevel error -i "{OUT}/EDITS_RESOLVE_9x16.mp4" -c:v libx264 -preset slow -b:v {vb}k -pass 2 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart "{OUT}/EDITS_RESOLVE_phone.mp4"')
    # teaser: B01, B02, B03, B12, B16 cut on the scene cuts
    cuts = P["cuts"]
    order = [s[1] for s in P["scenes"]]
    ends = {b: (cuts[order[i + 1]] if i + 1 < len(order) else TOTAL) for i, b in enumerate(order)}
    parts = ["B01", "B02", "B03", "B12", "B16"]
    segs = [(cuts[b], ends[b]) for b in parts]
    # B01 to B03 are contiguous: one segment
    segs = [(segs[0][0], segs[2][1]), segs[3], segs[4]]
    fc, n = [], 0
    for i, (a, b) in enumerate(segs):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b - a - 0.02:.3f}:d=0.02[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
    run(f'ffmpeg -y -loglevel error -i "{OUT}/EDITS_RESOLVE_9x16.mp4" -i "{MIX}" -filter_complex "{";".join(fc)}" -map "[v]" -map "[a]" {ENC} {AUD} "{OUT}/EDITS_RESOLVE_teaser.mp4"')
    print("teaser length", sum(b - a for a, b in segs))

if step in ("all", "srt"):
    def ts(t):
        ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []
    for i, (k, words, t0, t1) in enumerate(P["captions"]):
        txt = " ".join(words)
        lines.append(f"{i + 1}\n{ts(max(0.35 - 0.07, t0) if i == 0 else t0)} --> {ts(t1)}\n{txt}\n")
    open(OUT + "/captions.srt", "w").write("\n".join(lines))

if step in ("all", "gates"):
    M = OUT + "/EDITS_RESOLVE_9x16.mp4"
    dur = float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{M}"').strip())
    gates["G14_length_s"] = round(dur, 2)
    # loudness of the master
    r = run(f'ffmpeg -hide_banner -nostats -i "{M}" -af ebur128=peak=true -f null -')
    s = r[r.rfind("Summary"):]
    gates["G11_I_LUFS"] = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1))
    gates["G11_LRA"] = float(re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1))
    gates["G11_TP_dBFS"] = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))
    # 5 s windows
    r = run(f'ffmpeg -hide_banner -nostats -i "{M}" -af ebur128 -f null -')
    shorts = [float(x) for x in re.findall(r"S:\s*(-?[\d.]+)", r)]
    gates["G11_short_term_range"] = [min(x for x in shorts if x > -60), max(shorts)]
    # loop: last frame against frame 0
    run(f'ffmpeg -y -loglevel error -i "{M}" -vf "select=eq(n\\,0)" -vframes 1 {B}/f_first.png')
    nfr = int(run(f'ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "{M}"').strip())
    run(f'ffmpeg -y -loglevel error -i "{M}" -vf "select=eq(n\\,{nfr - 1})" -vframes 1 {B}/f_last.png')
    a = np.asarray(Image.open(B + "/f_first.png")).astype(float); b = np.asarray(Image.open(B + "/f_last.png")).astype(float)
    mse = ((a - b) ** 2).mean()
    gates["G12_loop_psnr_db"] = round(10 * np.log10(255 ** 2 / max(mse, 1e-9)), 2)
    gates["frames"] = nfr
    # blank or half drawn frames at every shot change (2 frames each side)
    bad = []
    os.makedirs(B + "/cutframes", exist_ok=True)
    for bid, t in P["cuts"].items():
        f0 = int(round(t * FPS))
        for f in range(max(0, f0 - 2), min(nfr, f0 + 3)):
            p = f"{B}/cutframes/{bid}_{f}.png"
            run(f'ffmpeg -y -loglevel error -i "{M}" -vf "select=eq(n\\,{f})" -vframes 1 {p}')
            im = np.asarray(Image.open(p).convert("L")).astype(float)
            lap = np.abs(np.diff(im, axis=1)).mean()
            if im.std() < 12 or lap < 1.0:
                bad.append((bid, f, round(im.std(), 1)))
    gates["G9_bad_cut_frames"] = bad
    json.dump(gates, open(B + "/gates.json", "w"), indent=1)
    print(json.dumps(gates, indent=1))

# Masks secrets in the creator's Edits captures and writes clean copies for the reel.
# Raw files are read from the session uploads and never copied into the project.
import glob, os, subprocess, json
from PIL import Image, ImageDraw, ImageFont
U = "/root/.claude/uploads/715d3f00-c5ce-56c6-92d2-658ba45b7738"
I = "/tmp/claude-0/-home-user-Video/715d3f00-c5ce-56c6-92d2-658ba45b7738/images"
O = os.path.abspath(os.path.dirname(__file__) + "/../reel/assets/footage")
os.makedirs(O, exist_ok=True)
def font(sz, w=600):
    for p in sorted(glob.glob(os.path.expanduser(f"~/.cache/hyperframes/fonts/inter/{w}-normal-*.woff2"))):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", sz)
def mask_box(draw, box, label, sz=22, r=10):
    draw.rounded_rectangle(box, r, fill=(5, 7, 11, 255), outline=(255, 255, 255, 46), width=2)
    if label:
        f = font(sz); x0, y0, x1, y1 = box
        tw = draw.textlength(label, font=f)
        draw.text((x0 + 18, (y0 + y1) / 2), label, font=f, fill=(138, 147, 166, 255), anchor="lm")
# 1) token mask for both Settings recordings (1600 x 1254), token row at y 579..603
TOKEN_BOX = (570, 564, 1398, 618)
m = Image.new("RGBA", (1600, 1254), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
mask_box(d, TOKEN_BOX, "token hidden", 24)
m.save(O + "/../../../build/token_mask.png")
for src, out in (("2e5168ea-*.mov", "edits_settings.mp4"), ("35a16d99-*.mov", "edits_copy.mp4")):
    f = glob.glob(f"{U}/{src}")[0]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-i", O + "/../../../build/token_mask.png",
                    "-filter_complex", "[0:v]fps=30,format=rgba[v];[v][1:v]overlay=0:0,format=yuv420p[o]", "-map", "[o]", "-an",
                    "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-g", "15", O + "/" + out], check=True)
# 2) screenshots
im = Image.open(I + "/4.png").convert("RGB"); d = ImageDraw.Draw(im)       # login: code and QR code
mask_box(d, (262, 910, 477, 958), None, r=8)
d.rounded_rectangle((1318, 500, 1712, 894), 24, fill=(14, 16, 22)); 
im.save(O + "/edits_login.png")
im = Image.open(I + "/3.png").convert("RGB"); d = ImageDraw.Draw(im)       # projects: profile photo
d.ellipse((1808, 78, 1890, 160), fill=(58, 62, 72)); d.ellipse((1836, 94, 1862, 120), fill=(150, 156, 170))
d.chord((1822, 118, 1876, 172), 180, 360, fill=(150, 156, 170)); d.ellipse((1808, 78, 1890, 160), outline=(28, 30, 36), width=6)
im.save(O + "/edits_projects.png")
Image.open(I + "/5.png").convert("RGB").save(O + "/edits_installer.png")
print("ok")

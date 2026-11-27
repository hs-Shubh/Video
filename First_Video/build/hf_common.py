# Shared styles, icons, JS helpers and recreated UI blocks for the reel.
# All UI here is a stylised, generic recreation. No official logos or artwork.
import json, math, random

W, H = 1080, 1920
NAVY = "#0E1422"
SAFF = "#FF9F1C"
GREEN = "#2FD27A"
RED = "#FF4D4D"
# laptop and screen rectangles (frame coordinates)
LID = (60, 150, 960, 616)
SCR = (74, 164, 932, 582)
SW, SH = SCR[2], SCR[3]
# layout zones
ZA = (60, 812, 960, 118)      # full width row under the laptop
ZR = (306, 950, 644, 400)     # right of the host
HOST = (36, 950, 250, 410)
CAP_BOTTOM = 1580

ICONS = {
    "download": '<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "toggle": '<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="17" cy="12" r="3"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
    "terminal": '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M7 9l3 3-3 3"/><path d="M12.5 15H17"/>',
    "power": '<path d="M12 3v8"/><path d="M6.3 7a8 8 0 1 0 11.4 0"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "alert": '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r=".6"/>',
    "bridge": '<path d="M2 18h20"/><path d="M4 18v-5a8 8 0 0 1 16 0v5"/><path d="M9 18v-4M15 18v-4"/>',
    "restart": '<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 4v5h-5"/>',
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    "text": '<path d="M4 7V5h16v2"/><path d="M12 5v14"/><path d="M9 19h6"/>',
    "music": '<path d="M9 18V6l11-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "send": '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/>',
    "folder": '<path d="M3 6.5h6l2 2.5h10v10H3z"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/>',
    "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    "phone": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
    "comment": '<path d="M21 12a8.5 8.5 0 0 1-12.6 7.4L3 21l1.6-5.2A8.5 8.5 0 1 1 21 12z"/>',
}

def icon(name, size=30, color="currentColor", sw=2.2, extra=""):
    return (f'<svg class="ic" {extra} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

CSS = r"""
#root{position:absolute;inset:0;overflow:hidden;font-family:Poppins, sans-serif;color:#fff}
.abs{position:absolute}
.laptop-lid{position:absolute;left:60px;top:150px;width:960px;height:616px;border-radius:28px;background:#0A0D14;
  box-shadow:0 2px 6px rgba(0,0,0,.35),0 24px 60px rgba(0,0,0,.45);}
.laptop-lid::after{content:"";position:absolute;inset:0;border-radius:28px;border-top:1px solid rgba(255,255,255,.16)}
.laptop-cam{position:absolute;left:536px;top:156px;width:8px;height:8px;border-radius:4px;background:#1b2130}
.laptop-base{position:absolute;left:30px;top:766px;width:1020px;height:24px;border-radius:2px 2px 18px 18px;
  background:linear-gradient(#3a4256,#202636);box-shadow:0 18px 40px rgba(0,0,0,.5)}
.laptop-notch{position:absolute;left:470px;top:766px;width:140px;height:9px;border-radius:0 0 9px 9px;background:#151a26}
.screen{position:absolute;left:74px;top:164px;width:932px;height:582px;border-radius:12px;overflow:hidden;background:#0b0f1a}
.push,.zoom{position:absolute;left:0;top:0;width:932px;height:582px}
.wall{position:absolute;inset:0;background:radial-gradient(120% 90% at 20% 10%,#2a3a63 0%,#16213b 45%,#0d1324 100%)}
.wall::after{content:"";position:absolute;left:-10%;top:55%;width:120%;height:70%;border-radius:50%;
  background:radial-gradient(closest-side,rgba(255,159,28,.10),rgba(255,159,28,0))}
.menubar{position:absolute;left:0;top:0;width:100%;height:24px;background:rgba(8,11,20,.55);display:flex;align-items:center;
  gap:16px;padding:0 14px;font:600 12px Inter, sans-serif;color:#e8ecf5}
.mb-dot{width:11px;height:11px;border-radius:6px;background:#e8ecf5;opacity:.9}
.mb-bar{height:7px;border-radius:4px;background:rgba(255,255,255,.28)}
.win{position:absolute;border-radius:12px;overflow:hidden;background:#1a1f2b;
  box-shadow:0 1px 3px rgba(0,0,0,.45),0 14px 34px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.08)}
.tbar{position:absolute;left:0;top:0;right:0;height:28px;display:flex;align-items:center;padding-left:12px;gap:7px;
  background:rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.06)}
.tl-dot{width:11px;height:11px;border-radius:6px;background:#565e70}
.ttitle{position:absolute;left:0;right:0;top:0;height:28px;line-height:28px;text-align:center;font:600 12px Inter, sans-serif;color:#aab2c4}
.wbody{position:absolute;left:0;right:0;top:28px;bottom:0}
.bar{border-radius:4px;background:rgba(255,255,255,.14);height:8px}
.dock{position:absolute;left:50%;bottom:8px;height:54px;padding:6px 10px;display:flex;gap:10px;border-radius:16px;
  background:rgba(20,26,40,.55);border:1px solid rgba(255,255,255,.12)}
.app{width:42px;height:42px;border-radius:11px;display:flex;align-items:center;justify-content:center;position:relative;
  box-shadow:0 2px 6px rgba(0,0,0,.4)}
.app .run{position:absolute;bottom:-6px;left:19px;width:4px;height:4px;border-radius:2px;background:#dfe5f1}
.cursor{position:absolute;left:0;top:0;width:22px;height:30px;z-index:50}
.ripple{position:absolute;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:22px;border:3px solid #fff;opacity:0;z-index:49}
.mono{font-family:"JetBrains Mono", monospace}
/* overlays */
.glass{position:absolute;border-radius:36px;overflow:hidden;
  background-image:url(assets/img/noise.png),linear-gradient(rgba(255,255,255,.08),rgba(255,255,255,.08)),url(assets/img/desk_blur.png);
  background-size:256px 256px,auto,1080px 1920px;
  box-shadow:0 2px 6px rgba(0,0,0,.35),0 24px 60px rgba(0,0,0,.45),inset 0 0 0 1px rgba(255,255,255,.22)}
.glass::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  border-top:1px solid rgba(255,255,255,.55);border-left:1px solid rgba(255,255,255,.3);
  -webkit-mask:linear-gradient(135deg,#000 0%,rgba(0,0,0,0) 45%);mask:linear-gradient(135deg,#000 0%,rgba(0,0,0,0) 45%)}
.sheen{position:absolute;top:-20%;left:0;width:38%;height:140%;pointer-events:none;
  background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.10),rgba(255,255,255,0));transform:skewX(-18deg) translateX(-160%)}
.chip{position:absolute;display:flex;align-items:center;gap:16px;height:68px;padding:0 28px 0 22px;border-radius:34px;
  font:500 35px/1 Poppins, sans-serif;color:#fff;white-space:nowrap}
.chip .ic{flex:none}
.chip2{height:auto;padding:16px 28px 16px 22px;white-space:normal;line-height:1.22}
.title{position:absolute;font:800 68px/1.08 Poppins, sans-serif;color:#fff;letter-spacing:-.5px}
.monobox{position:absolute;padding:20px 26px;border-radius:28px;font:500 33px/1.28 "JetBrains Mono", monospace;color:#eef2fa;
  white-space:pre-wrap;word-break:normal;overflow-wrap:anywhere}
.caret{display:inline-block;width:16px;height:34px;background:#FF9F1C;vertical-align:-5px;margin-left:3px}
.badge{position:absolute;height:56px;min-width:56px;padding:0 14px;border-radius:28px;background:#FF9F1C;color:#0E1422;
  font:800 28px/56px Poppins, sans-serif;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,.35),0 10px 24px rgba(0,0,0,.35);z-index:60}
.pill{position:absolute;display:flex;align-items:center;gap:12px;height:64px;padding:0 28px 0 20px;border-radius:32px;
  font:700 34px/1 Poppins, sans-serif;white-space:nowrap}
.pill.ok{background:#2FD27A;color:#07210f}
.pill.err{background:#FF4D4D;color:#2a0606}
.pop{position:absolute;font:800 120px/1 Poppins, sans-serif;color:#fff;letter-spacing:-1px}
.saff{color:#FF9F1C}
.dim{opacity:.45}
.selbox{position:absolute;border:3px solid #FF9F1C;border-radius:14px;opacity:0;z-index:40}
.vf{position:absolute;opacity:0;z-index:40}
.vf i{position:absolute;width:26px;height:26px;border-color:#fff;border-style:solid;border-width:0}
.vf .a{left:0;top:0;border-left-width:4px;border-top-width:4px}
.vf .b{right:0;top:0;border-right-width:4px;border-top-width:4px}
.vf .c{left:0;bottom:0;border-left-width:4px;border-bottom-width:4px}
.vf .d{right:0;bottom:0;border-right-width:4px;border-bottom-width:4px}
.ui{font-family:Inter, sans-serif}
.term{background:#0c0f16}
.tline{font:500 15px/1.5 "JetBrains Mono", monospace;color:#d7deea;white-space:pre}
.tdim{color:#7d889c}
.tok{color:#2FD27A}
.terr{color:#FF4D4D}
.mask{display:inline-block;background:#05070b;color:#8a93a6;border-radius:5px;padding:0 10px;font:600 13px/22px Inter, sans-serif;
  border:1px solid rgba(255,255,255,.18)}
.ck{display:flex;align-items:center;gap:18px;font:500 35px/1.2 Poppins, sans-serif;color:#fff}
.ckbox{flex:none;width:44px;height:44px;border-radius:12px;border:3px solid rgba(255,255,255,.5);position:relative}
.ckbox .tick{position:absolute;left:-3px;top:-3px;width:44px;height:44px;border-radius:12px;background:#2FD27A;opacity:0;
  display:flex;align-items:center;justify-content:center}
"""

JS_HELPERS = r"""
const F = 1/30;
const L = t => Math.max(0, +(t - S0).toFixed(4));
const tl = gsap.timeline({ paused: true });
function enter(sel, t, dy){
  tl.fromTo(sel,{opacity:0,y:(dy===undefined?24:dy),rotationX:12,transformPerspective:900,transformOrigin:"50% 100%"},{opacity:1,y:0,rotationX:0,duration:12*F,ease:"power3.out"},L(t));
  document.querySelectorAll(sel).forEach(el=>{ const sh=el.querySelector(":scope > .sheen"); if(sh) tl.fromTo(sh,{xPercent:-160},{xPercent:360,duration:0.8,ease:"power2.inOut",immediateRender:false},L(t)+0.18); });
}
function leave(sel, t){ tl.to(sel,{opacity:0,duration:6*F,ease:"none"},L(t)); }
function popIn(sel, t, s){ tl.fromTo(sel,{opacity:0,scale:(s||0.55)},{opacity:1,scale:1,duration:9*F,ease:"back.out(2.4)"},L(t)); }
function show(sel, t){ tl.set(sel,{opacity:1},L(t)); }
function hide(sel, t){ tl.set(sel,{opacity:0},L(t)); }
function typeText(sel, text, t, cps){ const d=Math.max(0.2,text.length/(cps||30)); tl.fromTo(sel,{text:""},{text:text,duration:d,ease:"none"},L(t)); return t+d; }
function cursorTo(id, t, x, y, d){ tl.to("#"+id,{x:x,y:y,duration:(d||0.5),ease:"power2.inOut"},L(t)); }
function clickAt(rid, t, x, y){ tl.fromTo("#"+rid,{x:x,y:y,scale:0.3,opacity:0.9},{scale:1.5,opacity:0,duration:0.38,ease:"power2.out",immediateRender:false},L(t)); }
const SW=932, SH=582;
function zoomTo(id, t, px, py, s, d){
  s=s||2; d=d||0.4;
  let x=SW/2 - s*px, y=SH/2 - s*py;
  x=Math.min(0,Math.max(SW - s*SW, x)); y=Math.min(0,Math.max(SH - s*SH, y));
  tl.to("#"+id,{scale:s,x:x,y:y,duration:d,ease:"power2.inOut",transformOrigin:"0 0"},L(t));
}
function zoomOut(id, t, d){ tl.to("#"+id,{scale:1,x:0,y:0,duration:(d||0.4),ease:"power2.inOut",transformOrigin:"0 0"},L(t)); }
function tick(sel, t){ tl.fromTo(sel,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:7*F,ease:"back.out(3)"},L(t)); }
function counter(sel, t0, t1, suffix){ const o={v:0}; const el=document.querySelector(sel);
  tl.fromTo(o,{v:0},{v:100,duration:t1-t0,ease:"power1.inOut",onUpdate:()=>{ el.textContent=Math.round(o.v)+(suffix||""); }},L(t0)); }
"""

def cursor_svg(cid):
    return (f'<svg id="{cid}" class="cursor" viewBox="0 0 22 30"><path d="M2 2 L2 24 L8 18.5 L12 28 L16 26.3 L12 17 L20 17 Z" '
            f'fill="#fff" stroke="#0a0d14" stroke-width="1.6" stroke-linejoin="round"/></svg>')

def laptop_frame():
    return ('<div class="laptop-base"></div><div class="laptop-notch"></div><div class="laptop-lid"></div>'
            '<div class="laptop-cam"></div>')

def menubar(app):
    bars = "".join(f'<div class="mb-bar" style="width:{w}px"></div>' for w in (34, 30, 40, 28))
    return (f'<div class="menubar"><div class="mb-dot"></div><span>{app}</span>{bars}'
            '<div style="flex:1"></div><div class="mb-bar" style="width:22px"></div><div class="mb-bar" style="width:46px"></div></div>')

APPS = {
    "finder": ("#4a78c9", "folder"),
    "browser": ("#3c5a8f", "spark"),
    "edits": ("#1b1f2a", "film"),
    "claude": ("#3a3631", "chat"),
    "terminal": ("#0b0d12", "terminal"),
    "resolve": ("#24272e", "chip"),
}

def dock(p, running=("finder", "edits", "claude", "terminal", "resolve")):
    items = []
    for k, (bg, ic) in APPS.items():
        run = f'<div class="run" id="{p}-run-{k}"></div>' if k in running else f'<div class="run" id="{p}-run-{k}" style="opacity:0"></div>'
        items.append(f'<div class="app" id="{p}-app-{k}" style="background:{bg}">{icon(ic, 24, "#e9edf6", 2)}{run}</div>')
    return f'<div class="dock" id="{p}-dock" style="transform:translateX(-50%)">{"".join(items)}</div>'

def win(wid, x, y, w, h, title, body, bg="#1a1f2b", extra_style=""):
    return (f'<div class="win" id="{wid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};{extra_style}">'
            f'<div class="tbar"><div class="tl-dot"></div><div class="tl-dot"></div><div class="tl-dot"></div></div>'
            f'<div class="ttitle">{title}</div><div class="wbody">{body}</div></div>')

def wave_path(w, h, seed, n=None, amp=0.9):
    rnd = random.Random(seed)
    n = n or max(8, int(w / 3))
    top, bot = [], []
    for i in range(n + 1):
        x = w * i / n
        a = (0.25 + 0.75 * abs(math.sin(i * 0.37 + seed)) * rnd.random()) * amp * h / 2
        top.append(f"{x:.1f},{h/2 - a:.1f}")
        bot.append(f"{x:.1f},{h/2 + a:.1f}")
    return "M" + " L".join(top) + " L" + " L".join(reversed(bot)) + " Z"

THUMBS = [
    "linear-gradient(160deg,#f2a65a 0%,#c25f3b 45%,#2b3a5a 100%)",
    "linear-gradient(170deg,#7fb4d9 0%,#3e6d94 50%,#1d2b45 100%)",
    "linear-gradient(150deg,#e8c27a 0%,#8c6a44 55%,#2a2a35 100%)",
    "linear-gradient(165deg,#9a8fd1 0%,#5a4f8f 50%,#1e1b33 100%)",
    "linear-gradient(155deg,#e58f7b 0%,#9a4a4a 50%,#2a1d28 100%)",
    "linear-gradient(175deg,#a9cfc0 0%,#4f7f78 55%,#1b2b30 100%)",
]

def thumb(i, w, h, extra=""):
    return (f'<div style="width:{w}px;height:{h}px;border-radius:5px;background:{THUMBS[i % len(THUMBS)]};position:relative;overflow:hidden;{extra}">'
            f'<div style="position:absolute;left:12%;bottom:18%;width:30%;height:35%;border-radius:50% 50% 8% 8%;background:rgba(10,12,20,.35)"></div></div>')

# ---------- Edits style editor ----------
TRACKS = [("Clips", "film"), ("Voiceover", "user"), ("Subtitles", "text"), ("Music", "music"), ("SFX", "spark")]

def edits_editor(p, w, h, show_labels=True):
    """Generic short form editor. Ids: {p}-clip{i}, {p}-vo, {p}-sub{i}, {p}-mus, {p}-sfx{i}, {p}-ph (playhead), {p}-prev."""
    tl_top = int(h * 0.50)
    lab_w = 92
    row_h = int((h - tl_top - 30) / 5)
    tw = w - lab_w - 14
    parts = []
    # top area: media strip, preview, inspector
    pv_h = tl_top - 24
    pv_w = int(pv_h * 9 / 16)
    pvx = int((w - pv_w) / 2)
    media = "".join(f'<div style="position:absolute;left:{12 + (i % 2) * 74}px;top:{12 + (i // 2) * 50}px">{thumb(i, 66, 42)}</div>' for i in range(6))
    parts.append(f'<div style="position:absolute;left:0;top:0;width:{pvx - 20}px;height:{tl_top - 8}px;border-right:1px solid rgba(255,255,255,.06)">{media}</div>')
    parts.append(f'<div id="{p}-prev" style="position:absolute;left:{pvx}px;top:10px;width:{pv_w}px;height:{pv_h}px;border-radius:8px;overflow:hidden;background:#05070c">'
                 f'<div id="{p}-previmg" style="position:absolute;inset:0;background:{THUMBS[0]};opacity:0"></div>'
                 f'<div id="{p}-prevsub" style="position:absolute;left:18%;right:18%;bottom:16%;height:9px;border-radius:5px;background:#fff;opacity:0"></div></div>')
    insp = "".join(f'<div class="bar" style="position:absolute;left:18px;top:{18 + i * 22}px;width:{60 + (i * 37) % 80}px"></div>' for i in range(7))
    parts.append(f'<div style="position:absolute;right:0;top:0;width:{w - pvx - pv_w - 20}px;height:{tl_top - 8}px;border-left:1px solid rgba(255,255,255,.06)">{insp}</div>')
    # timeline
    parts.append(f'<div style="position:absolute;left:0;right:0;top:{tl_top}px;bottom:0;background:#121620;border-top:1px solid rgba(255,255,255,.08)">')
    ticks = "".join(f'<div style="position:absolute;left:{lab_w + 8 + i * tw / 12:.0f}px;top:6px;width:1px;height:8px;background:rgba(255,255,255,.25)"></div>' for i in range(13))
    parts.append(ticks)
    for r, (name, ic) in enumerate(TRACKS):
        y = 22 + r * row_h
        lab = (f'<div style="position:absolute;left:8px;top:{y}px;width:{lab_w - 12}px;height:{row_h - 6}px;display:flex;align-items:center;gap:5px;'
               f'font:600 11px Inter, sans-serif;color:#aeb6c8">{icon(ic, 13, "#aeb6c8", 2)}{name if show_labels else ""}</div>')
        parts.append(lab)
        parts.append(f'<div style="position:absolute;left:{lab_w}px;right:8px;top:{y}px;height:{row_h - 6}px;border-radius:5px;background:rgba(255,255,255,.03)"></div>')
    x0 = lab_w + 4
    # clips
    y = 22
    widths = [0.15, 0.12, 0.18, 0.14, 0.16, 0.17]
    cx = x0
    for i, f in enumerate(widths):
        cw = tw * f - 3
        parts.append(f'<div id="{p}-clip{i}" style="position:absolute;left:{cx:.0f}px;top:{y}px;width:{cw:.0f}px;height:{row_h - 6}px;opacity:0;'
                     f'border-radius:5px;overflow:hidden;display:flex;gap:2px;border:1px solid rgba(255,255,255,.25)">'
                     + "".join(thumb(i + k, int(cw / 2), row_h - 6, "border-radius:0") for k in range(2)) + '</div>')
        cx += tw * f
    # voiceover
    y = 22 + row_h
    parts.append(f'<svg id="{p}-vo" style="position:absolute;left:{x0}px;top:{y}px;opacity:0" width="{tw * .97:.0f}" height="{row_h - 6}">'
                 f'<rect width="100%" height="100%" rx="5" fill="#2b4a6b"/><path d="{wave_path(tw * .97, row_h - 6, 3)}" fill="#8fc0ea"/></svg>')
    # subtitles
    y = 22 + 2 * row_h
    sx = x0
    for i in range(8):
        sw_ = tw * (0.09 + 0.03 * (i % 3))
        parts.append(f'<div id="{p}-sub{i}" style="position:absolute;left:{sx:.0f}px;top:{y + 4}px;width:{sw_:.0f}px;height:{row_h - 14}px;opacity:0;'
                     f'border-radius:4px;background:#d9dfeb;display:flex;align-items:center;padding:0 5px"><div style="height:4px;width:70%;border-radius:2px;background:#5b6478"></div></div>')
        sx += sw_ + tw * 0.012
    # music
    y = 22 + 3 * row_h
    parts.append(f'<svg id="{p}-mus" style="position:absolute;left:{x0}px;top:{y}px;opacity:0" width="{tw * .97:.0f}" height="{row_h - 6}">'
                 f'<rect width="100%" height="100%" rx="5" fill="#45396b"/><path d="{wave_path(tw * .97, row_h - 6, 11, amp=.7)}" fill="#b9acee"/></svg>')
    # sfx
    y = 22 + 4 * row_h
    for i, fx in enumerate((0.05, 0.33, 0.61, 0.86)):
        parts.append(f'<div id="{p}-sfx{i}" style="position:absolute;left:{x0 + tw * fx:.0f}px;top:{y}px;width:{tw * .07:.0f}px;height:{row_h - 6}px;opacity:0;'
                     f'border-radius:5px;background:#5b6b86"></div>')
    parts.append(f'<div id="{p}-ph" style="position:absolute;left:{x0}px;top:2px;width:2px;bottom:4px;background:#FF9F1C"></div>')
    parts.append('</div>')
    return "".join(parts)

def edits_fill_js(p, t0, speed=1.0, full=True):
    """JS to drop the editor content in, starting at absolute time t0."""
    s = speed
    js = [f'tl.fromTo("#{p}-clip0",{{opacity:0,y:-26}},{{opacity:1,y:0,duration:0.22,ease:"power3.out"}},L({t0}));']
    for i in range(1, 6):
        js.append(f'tl.fromTo("#{p}-clip{i}",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.16,ease:"power3.out"}},L({t0 + (0.35 + i * 0.13) * s:.3f}));')
    js.append(f'tl.fromTo("#{p}-vo",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,transformOrigin:"0 50%",duration:{0.5 * s:.2f},ease:"power2.out"}},L({t0 + 1.2 * s:.3f}));')
    for i in range(8):
        js.append(f'tl.fromTo("#{p}-sub{i}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.12}},L({t0 + (1.6 + i * 0.07) * s:.3f}));')
    js.append(f'tl.fromTo("#{p}-mus",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,transformOrigin:"0 50%",duration:{0.5 * s:.2f},ease:"power2.out"}},L({t0 + 2.4 * s:.3f}));')
    for i in range(4):
        js.append(f'tl.fromTo("#{p}-sfx{i}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:0.12}},L({t0 + (2.9 + i * 0.08) * s:.3f}));')
    js.append(f'tl.set("#{p}-previmg",{{opacity:1}},L({t0}));')
    js.append(f'tl.set("#{p}-prevsub",{{opacity:1}},L({t0 + 1.6 * s:.3f}));')
    return "\n".join(js)

def edits_filled_js(p):
    ids = [f"#{p}-clip{i}" for i in range(6)] + [f"#{p}-vo", f"#{p}-mus", f"#{p}-previmg", f"#{p}-prevsub"] + \
          [f"#{p}-sub{i}" for i in range(8)] + [f"#{p}-sfx{i}" for i in range(4)]
    return f'tl.set({json.dumps(",".join(ids))},{{opacity:1}},0);'

# ---------- Resolve style workspace ----------
def resolve_ui(p, w, h, menu=True):
    """Ids: {p}-ws (Workspace menu item), {p}-dd (dropdown), {p}-scripts, {p}-sub (submenu), {p}-bridge, {p}-pool{i}, {p}-tclip{i}, {p}-rq, {p}-rqbar, {p}-rqpct"""
    parts = []
    parts.append(f'<div style="position:absolute;left:0;right:0;top:0;height:24px;display:flex;align-items:center;gap:16px;padding:0 12px;'
                 f'background:#15171c;border-bottom:1px solid rgba(255,255,255,.06);font:600 12px Inter, sans-serif;color:#c9ced8">'
                 + "".join(f'<div class="bar" style="width:{bw}px;height:7px"></div>' for bw in (30, 26, 30))
                 + f'<span id="{p}-ws" style="padding:2px 7px;border-radius:4px">Workspace</span>'
                 + "".join(f'<div class="bar" style="width:{bw}px;height:7px"></div>' for bw in (34, 26)) + '</div>')
    top = 24
    pool_w = int(w * 0.36)
    # media pool
    pool = "".join(f'<div id="{p}-pool{i}" style="position:absolute;left:{10 + (i % 3) * (pool_w - 20) / 3:.0f}px;top:{38 + (i // 3) * 56}px">'
                   f'{thumb(i + 2, int((pool_w - 40) / 3), 44)}</div>' for i in range(6))
    parts.append(f'<div style="position:absolute;left:0;top:{top}px;width:{pool_w}px;height:{int(h * .48)}px;background:#1c1e24;border-right:1px solid rgba(255,255,255,.06)">'
                 f'<div class="bar" style="position:absolute;left:10px;top:12px;width:70px"></div>{pool}</div>')
    # viewer
    vw = w - pool_w
    parts.append(f'<div style="position:absolute;left:{pool_w}px;top:{top}px;width:{vw}px;height:{int(h * .48)}px;background:#17191e">'
                 f'<div id="{p}-view" style="position:absolute;left:{vw * .16:.0f}px;top:14px;width:{vw * .68:.0f}px;height:{h * .48 - 40:.0f}px;border-radius:4px;background:#0a0b0e;overflow:hidden">'
                 f'<div id="{p}-viewimg" style="position:absolute;inset:0;background:{THUMBS[2]};opacity:0"></div></div></div>')
    # timeline
    ty = top + int(h * .48)
    th = h - ty - 26
    parts.append(f'<div style="position:absolute;left:0;right:0;top:{ty}px;height:{th}px;background:#141519;border-top:1px solid rgba(255,255,255,.08)">')
    for r in range(3):
        parts.append(f'<div style="position:absolute;left:44px;right:8px;top:{16 + r * 30}px;height:24px;border-radius:3px;background:rgba(255,255,255,.03)"></div>'
                     f'<div class="bar" style="position:absolute;left:10px;top:{24 + r * 30}px;width:24px;height:7px"></div>')
    cx = 46
    for i, f in enumerate((0.2, 0.15, 0.22, 0.17)):
        cw = (w - 60) * f
        parts.append(f'<div id="{p}-tclip{i}" style="position:absolute;left:{cx:.0f}px;top:16px;width:{cw - 3:.0f}px;height:24px;border-radius:3px;opacity:0;'
                     f'background:#3d5f8a;border:1px solid rgba(255,255,255,.25)"></div>'
                     f'<div id="{p}-taud{i}" style="position:absolute;left:{cx:.0f}px;top:76px;width:{cw - 3:.0f}px;height:24px;border-radius:3px;opacity:0;'
                     f'background:#2f5d52;border:1px solid rgba(255,255,255,.2)"></div>')
        cx += cw
    # render queue panel
    parts.append(f'<div id="{p}-rq" style="position:absolute;right:10px;top:{th - 58}px;width:{w * .42:.0f}px;height:48px;border-radius:6px;background:#202329;opacity:0;'
                 f'border:1px solid rgba(255,255,255,.1)"><div style="position:absolute;left:10px;top:7px;font:600 12px Inter, sans-serif;color:#d7dbe3">Day 1</div>'
                 f'<div id="{p}-rqpct" style="position:absolute;right:10px;top:7px;font:600 12px Inter, sans-serif;color:#d7dbe3">0%</div>'
                 f'<div style="position:absolute;left:10px;right:10px;bottom:9px;height:6px;border-radius:3px;background:rgba(255,255,255,.1)">'
                 f'<div id="{p}-rqbar" style="width:100%;height:100%;border-radius:3px;background:#d7dbe3;transform:scaleX(0);transform-origin:0 50%"></div></div></div>')
    parts.append('</div>')
    # page tab icons row
    parts.append(f'<div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:#15171c;display:flex;justify-content:center;gap:22px;align-items:center">'
                 + "".join(f'<div style="width:12px;height:12px;border-radius:3px;border:2px solid #737a88"></div>' for _ in range(6)) + '</div>')
    if menu:
        dd_items = "".join(f'<div class="bar" style="width:{60 + (k * 23) % 50}px;margin:9px 12px"></div>' for k in range(3))
        parts.append(f'<div id="{p}-dd" style="position:absolute;left:146px;top:22px;width:150px;padding:4px 0;border-radius:7px;background:#2a2d34;'
                     f'box-shadow:0 8px 24px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.1);opacity:0;z-index:20;font:600 12px Inter, sans-serif;color:#e6e9ef">'
                     f'{dd_items}<div id="{p}-scripts" style="margin:2px 5px;padding:5px 8px;border-radius:5px">Scripts</div>'
                     f'<div class="bar" style="width:70px;margin:9px 12px"></div></div>')
        parts.append(f'<div id="{p}-sub" style="position:absolute;left:292px;top:110px;width:170px;padding:4px 0;border-radius:7px;background:#2a2d34;'
                     f'box-shadow:0 8px 24px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.1);opacity:0;z-index:21;font:600 12px Inter, sans-serif;color:#e6e9ef">'
                     f'<div id="{p}-bridge" style="margin:2px 5px;padding:5px 8px;border-radius:5px">Claude_MCP_Bridge</div></div>')
    return "".join(parts)

# ---------- Claude style chat ----------
def claude_chat(p, w, h):
    return (f'<div style="position:absolute;left:0;top:0;bottom:0;width:58px;background:#1f1e1c;border-right:1px solid rgba(255,255,255,.06)">'
            + "".join(f'<div style="width:22px;height:22px;border-radius:6px;margin:14px 18px;background:rgba(255,255,255,.12)"></div>' for _ in range(4))
            + '</div>'
            f'<div id="{p}-msgs" style="position:absolute;left:58px;right:0;top:0;bottom:70px;padding:18px 40px;font:500 15px/1.45 Inter, sans-serif;color:#ece9e2"></div>'
            f'<div style="position:absolute;left:{58 + 40}px;right:40px;bottom:16px;height:44px;border-radius:12px;background:#33312d;border:1px solid rgba(255,255,255,.1)">'
            f'<div id="{p}-input" style="position:absolute;left:14px;right:40px;top:12px;font:500 14px Inter, sans-serif;color:#ece9e2;white-space:nowrap;overflow:hidden"></div>'
            f'<div style="position:absolute;right:8px;top:8px;width:28px;height:28px;border-radius:8px;background:#5a564f;display:flex;align-items:center;justify-content:center">{icon("send", 15, "#ece9e2", 2.2)}</div></div>')

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

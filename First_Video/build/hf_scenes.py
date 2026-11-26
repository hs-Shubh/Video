# The 16 scenes. Every on screen overlay string comes from section 3b of the brief.
import json
from hf_common import *

F = 1 / 30


import re as _re


def fix_sets(js):
    """Initial states go through gsap.set (immediate), not a zero-time set inside the paused timeline."""
    return _re.sub(r'tl\.set\(("[^"]*"),(\{[^{}]*\}),0\)', r'gsap.set(\1,\2)', js)


class Sc:
    def __init__(self, sid, s0, dur, ctx):
        self.id, self.s0, self.dur, self.ctx = sid, s0, dur, ctx
        self.m, self.j = [], []
        self.p = sid  # id prefix

    # ---------- timing helpers ----------
    def w(self, beat, word, occ=1):
        return self.ctx.word(beat, word, occ)

    def we(self, beat, word, occ=1):
        return self.ctx.word_end(beat, word, occ)

    def trig(self, beat, word, occ=1):
        return max(self.s0, self.w(beat, word, occ) - 1.5 * F)

    def js(self, s):
        self.j.append(s)

    def add(self, s):
        self.m.append(s)

    # ---------- overlay builders ----------
    def glass_style(self, x, y):
        return f"background-position:0 0,0 0,-{int(x)}px -{int(y)}px;"

    def chip(self, cid, text, ic, x, y, t, out=None, center_row=False, wrap_w=None, cls="glass"):
        icon_html = icon(ic, 32, "#FF9F1C" if ic else "#fff", 2.4) if ic else ""
        style = self.glass_style(x, y)
        if wrap_w:
            inner = f'<div class="chip chip2 {cls}" id="{cid}" style="position:relative;{style};max-width:{wrap_w}px">{icon_html}<span>{text}</span></div>'
        else:
            inner = f'<div class="chip {cls}" id="{cid}" style="position:relative;{style}">{icon_html}<span>{text}</span></div>'
        if center_row:
            self.add(f'<div class="abs" style="left:60px;width:960px;top:{y}px;display:flex;justify-content:center">{inner}</div>')
        else:
            self.add(f'<div class="abs" style="left:{x}px;top:{y}px">{inner}</div>')
        self.js(f'tl.set("#{cid}",{{opacity:0}},0);')
        self.js(f'enter("#{cid}",{t:.3f});')
        if out:
            self.js(f'leave("#{cid}",{out:.3f});')

    def pill(self, cid, text, x, y, t, kind="ok", out=None, center_row=False):
        ic = icon("check", 34, "#07210f", 3) if kind == "ok" else icon("alert", 32, "#2a0606", 2.6)
        inner = f'<div class="pill {kind}" id="{cid}" style="position:relative">{ic}<span>{text}</span></div>'
        if center_row:
            self.add(f'<div class="abs" style="left:60px;width:960px;top:{y}px;display:flex;justify-content:center">{inner}</div>')
        else:
            self.add(f'<div class="abs" style="left:{x}px;top:{y}px">{inner}</div>')
        self.js(f'tl.set("#{cid}",{{opacity:0}},0);')
        self.js(f'popIn("#{cid}",{t:.3f},0.6);')
        if out:
            self.js(f'leave("#{cid}",{out:.3f});')

    def badge(self, cid, text, t, x=40, y=124):
        self.add(f'<div class="badge" id="{cid}" style="left:{x}px;top:{y}px">{text}</div>')
        self.js(f'tl.set("#{cid}",{{opacity:0}},0);')
        self.js(f'popIn("#{cid}",{t:.3f},0.4);')

    # ---------- base ----------
    def laptop(self, screen_html, push=True):
        p = self.p
        self.add(laptop_frame())
        self.add(f'<div class="screen" id="{p}-screen" data-layout-ignore><div class="push" id="{p}-push"><div class="zoom" id="{p}-zoom">{screen_html}'
                 f'<div class="ripple" id="{p}-rip"></div>{cursor_svg(p + "-cur")}</div></div></div>')
        if push:
            self.js(f'tl.fromTo("#{p}-push",{{scale:1}},{{scale:1.03,duration:{max(0.5, self.dur - 0.05):.3f},ease:"none",transformOrigin:"50% 50%"}},0);')

    def cursor(self, x, y, hidden=False):
        self.js(f'tl.set("#{self.p}-cur",{{x:{x},y:{y},opacity:{0 if hidden else 1}}},0);')

    def html(self):
        return ("<template>\n<style>" + CSS + "</style>\n"
                f'<div id="root" data-composition-id="{self.id}" data-width="1080" data-height="1920">\n'
                + "\n".join(self.m) + "\n</div>\n<script>\n(function(){\n"
                f"const S0 = {self.s0:.4f};\n" + JS_HELPERS + "\n" + fix_sets("\n".join(self.j))
                + f'\nwindow.__timelines["{self.id}"] = tl;\n}})();\n</script>\n</template>\n')


# ---------------------------------------------------------------- shared screens
def desktop_two_windows(p, menu_app="Edits"):
    ed = win(f"{p}-wE", 16, 36, 540, 318, "Edits", edits_editor(f"{p}e", 540, 290), "#161a23")
    rs = win(f"{p}-wR", 392, 196, 524, 318, "Resolve", resolve_ui(f"{p}r", 524, 290, menu=False), "#1a1c21")
    return f'<div class="wall"></div>{menubar(menu_app)}{ed}{rs}{dock(p)}'


def s01_state_js(p, t_snap=0.0):
    """Frame 0 state of the opening (also used by the loop ending)."""
    return (f'tl.fromTo("#{p}-wE",{{scale:0.94,opacity:1}},{{scale:1,duration:0.26,ease:"back.out(1.8)"}},L({t_snap:.3f}));\n'
            f'tl.fromTo("#{p}-wR",{{scale:0.94,opacity:1}},{{scale:1,duration:0.26,ease:"back.out(1.8)"}},L({t_snap + 0.08:.3f}));')


def prompt_bar(p, y=826):
    return (f'<div class="abs" style="left:60px;width:960px;top:{y}px;display:flex;justify-content:center">'
            f'<div class="monobox glass" id="{p}-pb" style="position:relative;width:760px;height:92px;display:flex;align-items:center;gap:18px;padding:0 30px;{"background-position:0 0,0 0,-160px -" + str(y) + "px"}">'
            f'{icon("terminal", 34, "#FF9F1C", 2.2)}<span id="{p}-pbt"></span><span class="caret"></span></div></div>')


# ---------------------------------------------------------------- S01 hook
def s01(c):
    p = c.p
    c.laptop(desktop_two_windows(p), push=False)
    c.js(edits_filled_js(f"{p}e"))
    c.js(f'tl.set("#{p}rr-x",{{opacity:1}},0);' if False else "")
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    c.cursor(700, 470, hidden=True)
    c.js(s01_state_js(p, 0.0))
    c.add(prompt_bar(p))
    c.js(f'typeText("#{p}-pbt","edit my reel",{c.ctx.beats["B01"]["start"]:.3f},20);')
    # title block in zone R
    x, y = ZR[0], 972
    c.add(f'<div class="title" id="{p}-tt" style="left:{x}px;top:{y}px;width:640px">'
          f'<div id="{p}-l1" style="opacity:0">CLAUDE</div>'
          f'<div><span id="{p}-p1" class="saff" style="opacity:0">+ </span><span id="{p}-l2" style="display:inline-block;opacity:0">EDITS</span></div>'
          f'<div><span id="{p}-p2" class="saff" style="opacity:0">+ </span><span id="{p}-l3" style="display:inline-block;opacity:0">RESOLVE</span></div></div>')
    te = c.trig("B01", "Edits")
    tr = c.trig("B01", "Resolve")
    tset = c.we("B01", "Resolve") + 0.25
    c.js(f'tl.fromTo("#{p}-l2",{{opacity:0,scale:1.7}},{{opacity:1,scale:1,duration:9*F,ease:"back.out(2.2)",transformOrigin:"0% 60%"}},L({te:.3f}));')
    c.js(f'tl.fromTo("#{p}-l3",{{opacity:0,scale:1.7}},{{opacity:1,scale:1,duration:9*F,ease:"back.out(2.2)",transformOrigin:"0% 60%"}},L({tr:.3f}));')
    c.js(f'enter("#{p}-l1",{tset:.3f},18); enter("#{p}-p1",{tset + 0.08:.3f},12); enter("#{p}-p2",{tset + 0.14:.3f},12);')
    c.js(f'tl.fromTo("#{p}-tt",{{scale:1}},{{scale:1.03,duration:{c.dur:.2f},ease:"none",transformOrigin:"0 0"}},0);')


# ---------------------------------------------------------------- S02 proof
def s02(c):
    p = c.p
    ed = win(f"{p}-wE", 8, 30, 916, 544, "Edits", edits_editor(f"{p}e", 916, 516), "#161a23")
    c.laptop(f'<div class="wall"></div>{menubar("Edits")}{ed}')
    c.cursor(520, 300)
    t_imp = c.ctx.sfx["impact"]
    c.js(edits_fill_js(f"{p}e", t_imp, 1.2))
    # cursor follow zoom on the first clip
    cx, cy = 8 + 96 + 60, 30 + 28 + 258 + 22 + 18
    c.js(f'cursorTo("{p}-cur",{c.s0:.3f},{cx + 10},{cy + 30},0.45);')
    c.js(f'zoomTo("{p}-zoom",{t_imp - 0.3:.3f},{cx},{cy},2.0,0.4);')
    c.js(f'clickAt("{p}-rip",{t_imp:.3f},{cx},{cy});')
    c.js(f'zoomOut("{p}-zoom",{t_imp + 1.65:.3f},0.4);')
    # speed ramp: the playhead sweeps fast, then 1x
    c.js(f'tl.fromTo("#{p}e-ph",{{x:0}},{{x:520,duration:1.1,ease:"power3.in"}},L({t_imp + 2.2:.3f}));')
    c.js(f'tl.to("#{p}e-ph",{{x:600,duration:1.2,ease:"none"}},L({t_imp + 3.3:.3f}));')
    c.chip(f"{p}-c1", "1 prompt", "terminal", 0, 826, c.trig("B02", "ek"), center_row=True)
    # one glass list card with three rows (counts as one overlay item)
    x, y = ZR[0], 968
    rows = [("Clips", "film", "clips"), ("Subtitles", "text", "subtitles"), ("Music", "music", "music")]
    inner = "".join(f'<div class="chip" id="{p}-r{i}" style="position:relative;height:72px;padding:0 8px;opacity:0">{icon(ic, 34, "#FF9F1C", 2.4)}<span>{t}</span></div>'
                    for i, (t, ic, wd) in enumerate(rows))
    c.add(f'<div class="glass abs" id="{p}-card" style="left:{x}px;top:{y}px;width:420px;padding:18px 26px;{c.glass_style(x, y)}">{inner}</div>')
    c.js(f'tl.set("#{p}-card",{{opacity:0}},0);')
    c.js(f'enter("#{p}-card",{c.trig("B02", "clips"):.3f});')
    for i, (t, ic, wd) in enumerate(rows):
        c.js(f'enter("#{p}-r{i}",{c.trig("B02", wd):.3f},14);')


# ---------------------------------------------------------------- S03 problem
def s03(c):
    p = c.p
    c.laptop(desktop_two_windows(p, "Finder"))
    c.js(edits_filled_js(f"{p}e"))
    c.cursor(0, 0, hidden=True)
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    # rack focus on the screen windows follows the cards
    t1, t2 = c.trig("B03", "Edits"), c.trig("B03", "free")
    tb = c.trig("B03", "band")
    c.js(f'tl.to("#{p}-wR",{{opacity:0.35,duration:0.3}},L({t1:.3f})); tl.to("#{p}-wE",{{opacity:1,duration:0.3}},L({t1:.3f}));')
    c.js(f'tl.to("#{p}-wE",{{opacity:0.35,duration:0.3}},L({t2:.3f})); tl.to("#{p}-wR",{{opacity:1,duration:0.3}},L({t2:.3f}));')
    x = ZR[0]
    y1, y2 = 958, 1166
    c.add(f'<div class="glass abs" id="{p}-k1" style="left:{x}px;top:{y1}px;width:644px;height:190px;{c.glass_style(x, y1)}">'
          f'<div class="title" style="left:30px;top:22px;font-size:64px">Edits for Mac</div>'
          f'<div class="chip" id="{p}-k1c" style="left:22px;top:108px;height:62px;font-size:33px;background:rgba(255,255,255,.08);padding:0 22px 0 16px">{icon("chip", 30, "#FF9F1C", 2.2)}<span>Apple silicon (M1 or later)</span></div></div>')
    c.add(f'<div class="glass abs" id="{p}-k2" style="left:{x}px;top:{y2}px;width:644px;height:190px;{c.glass_style(x, y2)}">'
          f'<div class="title" style="left:30px;top:22px;font-size:64px">Resolve free</div>'
          f'<div class="chip" id="{p}-k2c" style="left:22px;top:108px;height:62px;font-size:33px;background:rgba(255,255,255,.08);padding:0 22px 0 16px">{icon("lock", 30, "#FF9F1C", 2.2)}<span>Outside control locked</span></div>'
          f'<div class="selbox" id="{p}-sel" style="left:14px;top:100px;width:470px;height:78px"></div></div>')
    for s in (f"{p}-k1", f"{p}-k1c", f"{p}-k2", f"{p}-k2c"):
        c.js(f'tl.set("#{s}",{{opacity:0}},0);')
    c.js(f'enter("#{p}-k1",{t1:.3f}); enter("#{p}-k1c",{c.trig("B03", "Apple"):.3f},14);')
    c.js(f'enter("#{p}-k2",{t2:.3f}); enter("#{p}-k2c",{tb:.3f},14);')
    # rack focus between the cards
    c.js(f'tl.to("#{p}-k1",{{opacity:0.5,scale:0.97,duration:0.3,transformOrigin:"50% 50%"}},L({t2 + 0.1:.3f}));')
    c.js(f'tl.fromTo("#{p}-sel",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:7*F,ease:"power3.out"}},L({tb + 0.12:.3f}));')


# ---------------------------------------------------------------- S04 roadmap
def s04(c):
    p = c.p
    c.laptop(desktop_two_windows(p, "Finder"))
    c.js(edits_filled_js(f"{p}e"))
    c.cursor(0, 0, hidden=True)
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}-wE, #{p}-wR",{{opacity:0.35}},0);')
    x, y = ZR[0], 1010
    labels = [("Edits", "Edits"), ("Resolve", "Resolve"), ("Together", "ek")]
    dots = []
    for i, (lab, wd) in enumerate(labels):
        dx = 70 + i * 250
        dots.append(f'<div class="abs" style="left:{dx - 24}px;top:40px;width:48px;height:48px;border-radius:24px;border:4px solid rgba(255,255,255,.45)"></div>'
                    f'<div class="abs" id="{p}-d{i}" style="left:{dx - 24}px;top:40px;width:48px;height:48px;border-radius:24px;background:#FF9F1C;opacity:0"></div>'
                    f'<div class="abs" id="{p}-lb{i}" style="left:{dx - 110}px;width:220px;top:104px;text-align:center;font:600 35px Poppins, sans-serif;opacity:.4">{lab}</div>')
    line = (f'<div class="abs" style="left:94px;top:62px;width:452px;height:4px;background:rgba(255,255,255,.25)"></div>'
            f'<div class="abs" id="{p}-ln" style="left:94px;top:62px;width:452px;height:4px;background:#FF9F1C;transform:scaleX(0);transform-origin:0 50%"></div>')
    c.add(f'<div class="glass abs" id="{p}-trk" style="left:{x}px;top:{y}px;width:640px;height:180px;{c.glass_style(x, y)}">{line}{"".join(dots)}</div>')
    c.js(f'tl.set("#{p}-trk",{{opacity:0}},0); enter("#{p}-trk",{c.s0:.3f});')
    for i, (lab, wd) in enumerate(labels):
        t = c.trig("B04", wd)
        c.js(f'popIn("#{p}-d{i}",{t:.3f},0.3); tl.to("#{p}-lb{i}",{{opacity:1,duration:0.2}},L({t:.3f}));')
        if i:
            c.js(f'tl.to("#{p}-ln",{{scaleX:{i / 2},duration:0.3,ease:"power2.out"}},L({t - 0.1:.3f}));')
    c.js(f'tl.to("#{p}-wE",{{opacity:1,duration:0.25}},L({c.trig("B04", "Edits"):.3f}));')
    c.js(f'tl.to("#{p}-wE",{{opacity:0.35,duration:0.25}},L({c.trig("B04", "Resolve"):.3f})); tl.to("#{p}-wR",{{opacity:1,duration:0.25}},L({c.trig("B04", "Resolve"):.3f}));')
    c.js(f'tl.to("#{p}-wE",{{opacity:1,duration:0.25}},L({c.trig("B04", "ek"):.3f}));')


# ---------------------------------------------------------------- checklist card helper
def checklist(c, cid, items, x, y, w):
    """items: list of (text, appear_t, tick_t). One glass card = one overlay item."""
    rows = []
    for i, (txt, ta, tt) in enumerate(items):
        rows.append(f'<div class="ck" id="{cid}-i{i}" style="margin:14px 0;opacity:0"><div class="ckbox"><div class="tick" id="{cid}-t{i}">'
                    f'{icon("check", 34, "#07210f", 3.2)}</div></div><div>{txt}</div></div>')
    c.add(f'<div class="glass abs" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;padding:14px 28px;{c.glass_style(x, y)}">{"".join(rows)}</div>')
    c.js(f'tl.set("#{cid}",{{opacity:0}},0); enter("#{cid}",{items[0][1]:.3f});')
    for i, (txt, ta, tt) in enumerate(items):
        c.js(f'enter("#{cid}-i{i}",{ta:.3f},14);')
        if tt:
            c.js(f'tick("#{cid}-t{i}",{tt:.3f});')


# ---------------------------------------------------------------- S05 Edits 1
def s05(c):
    p = c.p
    page = (f'<div style="position:absolute;left:0;right:0;top:0;height:30px;background:#202533;display:flex;align-items:center;padding:0 14px;gap:8px">'
            f'<div style="flex:1;height:18px;border-radius:9px;background:#2c3242"></div></div>'
            f'<div style="position:absolute;left:0;right:0;top:30px;bottom:0;background:#f3f4f7">'
            f'<div style="position:absolute;left:60px;top:60px;width:64px;height:64px;border-radius:16px;background:#1b1f2a;display:flex;align-items:center;justify-content:center">{icon("film", 36, "#fff", 2)}</div>'
            f'<div style="position:absolute;left:60px;top:150px;width:330px;height:22px;border-radius:6px;background:#1b1f2a"></div>'
            f'<div style="position:absolute;left:60px;top:186px;width:260px;height:22px;border-radius:6px;background:#1b1f2a"></div>'
            f'<div class="bar" style="position:absolute;left:60px;top:230px;width:300px;background:#c9ced9"></div>'
            f'<div class="bar" style="position:absolute;left:60px;top:250px;width:240px;background:#c9ced9"></div>'
            f'<div id="{p}-dl" class="ui" style="position:absolute;left:60px;top:290px;height:46px;padding:0 22px;border-radius:23px;background:#1b1f2a;color:#fff;'
            f'display:flex;align-items:center;gap:10px;font:600 16px Inter, sans-serif">{icon("download", 18, "#fff", 2.4)}Download</div>'
            f'<div style="position:absolute;right:50px;top:50px;width:300px;height:330px;border-radius:18px;background:linear-gradient(160deg,#d9dde6,#b7bdcc)">'
            f'<div style="position:absolute;left:30px;top:30px;width:240px;height:160px;border-radius:10px;background:{THUMBS[0]}"></div>'
            f'<div class="bar" style="position:absolute;left:30px;top:214px;width:200px;background:#8f96a6"></div></div></div>')
    br = win(f"{p}-wB", 30, 40, 872, 500, "", page, "#f3f4f7")
    signin = (f'<div style="position:absolute;inset:0;background:#12151d;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px">'
              f'<div style="width:70px;height:70px;border-radius:18px;background:#1f2430;display:flex;align-items:center;justify-content:center">{icon("film", 40, "#fff", 2)}</div>'
              f'<div style="font:700 22px Inter, sans-serif;color:#fff">Edits</div>'
              f'<div id="{p}-si" style="height:46px;padding:0 24px;border-radius:12px;background:#fff;color:#12151d;display:flex;align-items:center;gap:10px;font:600 16px Inter, sans-serif">'
              f'{icon("user", 18, "#12151d", 2.4)}Sign in with Instagram</div></div>')
    ed = win(f"{p}-wS", 200, 70, 532, 420, "Edits", signin, "#12151d")
    c.laptop(f'<div class="wall"></div>{menubar("Edits")}{br}{ed}{dock(p)}')
    c.js(f'tl.set("#{p}-wS",{{opacity:0}},0);')
    tdl = c.trig("B05", "download")
    tsi = c.trig("B05", "sign")
    dlx, dly = 30 + 60 + 70, 40 + 28 + 30 + 313
    c.cursor(620, 470)
    c.js(f'cursorTo("{p}-cur",{tdl - 0.6:.3f},{dlx},{dly},0.55);')
    c.js(f'zoomTo("{p}-zoom",{tdl - 0.45:.3f},{dlx},{dly},2.0,0.4);')
    c.js(f'clickAt("{p}-rip",{tdl:.3f},{dlx},{dly});')
    c.js(f'tl.to("#{p}-dl",{{scale:0.94,duration:0.08,yoyo:true,repeat:1}},L({tdl:.3f}));')
    c.js(f'zoomOut("{p}-zoom",{tdl + 1.1:.3f},0.4);')
    c.js(f'tl.fromTo("#{p}-wS",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},L({tdl + 1.25:.3f}));')
    six, siy = 200 + 266, 70 + 28 + 210 + 60
    c.js(f'cursorTo("{p}-cur",{tsi - 0.55:.3f},{six},{siy},0.5);')
    c.js(f'zoomTo("{p}-zoom",{tsi - 0.4:.3f},{six},{siy},1.8,0.4);')
    c.js(f'clickAt("{p}-rip",{tsi + 0.25:.3f},{six},{siy});')
    c.badge(f"{p}-bd", "E1", c.trig("B05", "Edits"))
    checklist(c, f"{p}-ck", [("Download Edits for Mac", tdl, tdl + 0.35), ("Sign in with Instagram", tsi, tsi + 0.55)], ZR[0], 980, 644)


# ---------------------------------------------------------------- Edits settings screen
def edits_settings(p):
    side = "".join(f'<div class="bar" style="width:{70 + (k * 19) % 40}px;margin:15px 16px"></div>' for k in range(3))
    side += f'<div id="{p}-auto" style="margin:6px 8px;padding:7px 10px;border-radius:7px;font:600 14px Inter, sans-serif;color:#e8ecf5">Automation</div>'
    side += "".join(f'<div class="bar" style="width:{60 + (k * 23) % 40}px;margin:15px 16px"></div>' for k in range(2))
    row = 'style="position:absolute;left:24px;right:24px;height:54px;border-radius:10px;background:rgba(255,255,255,.04);display:flex;align-items:center;padding:0 16px;font:600 15px Inter, sans-serif;color:#e8ecf5"'
    panel = (f'<div id="{p}-panel" style="position:absolute;left:190px;right:0;top:0;bottom:0;opacity:0">'
             f'<div style="position:absolute;left:24px;top:20px;font:700 20px Inter, sans-serif;color:#fff">Automation</div>'
             f'<div {row.replace("left:24px", "left:24px;top:68px")}><span>Enable Automation Server</span><div style="flex:1"></div>'
             f'<div id="{p}-tg" style="position:relative;width:50px;height:28px;border-radius:14px;background:#3a4152">'
             f'<div id="{p}-tgon" style="position:absolute;inset:0;border-radius:14px;background:#2FD27A;opacity:0"></div>'
             f'<div id="{p}-knob" style="position:absolute;left:3px;top:3px;width:22px;height:22px;border-radius:11px;background:#fff"></div></div></div>'
             f'<div {row.replace("left:24px", "left:24px;top:134px")}><span>Access Token</span><div style="flex:1"></div>'
             f'<span class="mask" style="font-size:13px;padding:0 14px;line-height:26px">token hidden</span></div>'
             f'<div {row.replace("left:24px", "left:24px;top:200px")}><span>Claude Code</span><div style="flex:1"></div>'
             f'<div id="{p}-copy" style="height:30px;padding:0 14px;border-radius:8px;background:#e8ecf5;color:#141821;display:flex;align-items:center;gap:6px;font:600 13px Inter, sans-serif">{icon("copy", 15, "#141821", 2.4)}Copy</div></div>'
             f'<div {row.replace("left:24px", "left:24px;top:266px")}><div class="bar" style="width:120px"></div><div style="flex:1"></div>'
             f'<div style="height:30px;width:70px;border-radius:8px;background:rgba(255,255,255,.12)"></div></div></div>')
    body = (f'<div style="position:absolute;left:0;top:0;bottom:0;width:190px;background:#151923;border-right:1px solid rgba(255,255,255,.06);padding-top:10px">{side}</div>{panel}')
    return body


# ---------------------------------------------------------------- S06 Edits 2
def s06(c):
    p = c.p
    ed = win(f"{p}-wE", 8, 30, 916, 544, "Edits", edits_editor(f"{p}e", 916, 516), "#161a23")
    st = win(f"{p}-wS", 96, 60, 740, 420, "Settings", edits_settings(p), "#1b2030")
    c.laptop(f'<div class="wall"></div>{menubar("Edits")}{ed}{st}')
    c.js(edits_filled_js(f"{p}e"))
    c.js(f'tl.set("#{p}-wS",{{opacity:0}},0);')
    ts, ta, ten = c.trig("B06", "Settings"), c.trig("B06", "Automation"), c.trig("B06", "Enable")
    tcp = c.trig("B06", "Copy")
    ttog = c.ctx.sfx["toggle"]
    c.cursor(600, 300)
    c.js(f'cursorTo("{p}-cur",{ts - 0.5:.3f},860,44,0.45); clickAt("{p}-rip",{ts:.3f},860,44);')
    c.js(f'tl.fromTo("#{p}-wS",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(1.6)"}},L({ts + 0.12:.3f}));')
    ax, ay = 96 + 70, 60 + 28 + 10 + 3 * 38 + 22
    c.js(f'cursorTo("{p}-cur",{ta - 0.45:.3f},{ax},{ay},0.45); clickAt("{p}-rip",{ta:.3f},{ax},{ay});')
    c.js(f'tl.to("#{p}-auto",{{backgroundColor:"rgba(255,255,255,.12)",duration:0.1}},L({ta:.3f}));')
    c.js(f'tl.to("#{p}-panel",{{opacity:1,duration:0.2}},L({ta + 0.08:.3f}));')
    # digital zoom: viewfinder locks on the toggle
    tx, ty = 96 + 190 + 740 - 190 - 24 - 16 - 25, 60 + 28 + 68 + 27
    c.add(f'<div class="vf" id="{p}-vf" style="left:110px;top:{164 + 200}px;width:860px;height:170px"><i class="a"></i><i class="b"></i><i class="c"></i><i class="d"></i></div>')
    c.js(f'cursorTo("{p}-cur",{ten - 0.3:.3f},{tx},{ty},0.6);')
    c.js(f'zoomTo("{p}-zoom",{ten:.3f},{tx - 230},{ty},1.6,0.45);')
    c.js(f'tl.fromTo("#{p}-vf",{{opacity:0,scale:1.35}},{{opacity:1,scale:1,duration:8*F,ease:"power3.out"}},L({ten + 0.4:.3f}));')
    c.js(f'clickAt("{p}-rip",{ttog:.3f},{tx},{ty});')
    c.js(f'tl.to("#{p}-knob",{{x:22,duration:0.14,ease:"power2.out"}},L({ttog:.3f})); tl.to("#{p}-tgon",{{opacity:1,duration:0.14}},L({ttog:.3f}));')
    c.js(f'leave("#{p}-vf",{ttog + 0.55:.3f}); zoomOut("{p}-zoom",{ttog + 0.6:.3f},0.4);')
    cx, cy = 96 + 190 + 740 - 190 - 24 - 16 - 40, 60 + 28 + 200 + 27
    c.add(f'<div class="selbox" id="{p}-sel" style="left:{74 + cx - 50}px;top:{164 + cy - 22}px;width:100px;height:44px;border-radius:12px"></div>')
    c.js(f'cursorTo("{p}-cur",{tcp - 0.5:.3f},{cx + 10},{cy + 6},0.45);')
    c.js(f'tl.fromTo("#{p}-sel",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:7*F,ease:"power3.out"}},L({tcp:.3f}));')
    c.badge(f"{p}-bd", "E2", c.trig("B06", "Edits"))
    # breadcrumb: Settings > Automation > Enable Automation Server
    x, y = ZR[0], 972
    chev = icon("send", 0)  # unused placeholder
    def ch(i):
        return f'<svg id="{p}-ch{i}" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="opacity:.35;flex:none"><path d="M9 5l7 7-7 7"/></svg>'
    bc = (f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;font:700 38px/1.35 Poppins, sans-serif">'
          f'<span id="{p}-b0" style="opacity:.35">Settings</span>{ch(0)}<span id="{p}-b1" style="opacity:.35">Automation</span>{ch(1)}'
          f'<span id="{p}-b2" style="opacity:.35">Enable Automation Server</span></div>')
    c.add(f'<div class="glass abs" id="{p}-bc" style="left:{x}px;top:{y}px;width:644px;padding:22px 30px;{c.glass_style(x, y)}">{bc}</div>')
    c.js(f'tl.set("#{p}-bc",{{opacity:0}},0); enter("#{p}-bc",{ts:.3f});')
    for i, t in enumerate((ts, ta, ten)):
        c.js(f'tl.to("#{p}-b{i}",{{opacity:1,color:"#FF9F1C",duration:0.15}},L({t:.3f}));')
        if i:
            c.js(f'tl.to("#{p}-b{i - 1}",{{color:"#ffffff",duration:0.15}},L({t:.3f})); tl.to("#{p}-ch{i - 1}",{{opacity:1,duration:0.15}},L({t:.3f}));')
    c.chip(f"{p}-cc", "Copy for Claude Code", "copy", 0, 826, tcp, center_row=True)


# ---------------------------------------------------------------- S07 Edits 3
def s07(c):
    p = c.p
    st = win(f"{p}-wS", 40, 40, 620, 360, "Settings", edits_settings(p), "#1b2030")
    term = (f'<div class="term" style="position:absolute;inset:0;padding:12px 16px">'
            f'<div class="tline"><span class="tdim">%</span> <span id="{p}-paste" style="opacity:0"><span class="mask">token hidden</span></span></div>'
            f'<div class="tline" id="{p}-l2" style="opacity:0"><span class="tdim">%</span> </div></div>')
    tw_ = win(f"{p}-wT", 330, 150, 560, 230, "Terminal", term, "#0c0f16")
    cl = win(f"{p}-wC", 200, 64, 560, 380, "Claude", claude_chat(f"{p}c", 560, 352), "#262624")
    c.laptop(f'<div class="wall"></div>{menubar("Terminal")}{st}{tw_}{cl}{dock(p)}')
    c.js(f'tl.set("#{p}-panel",{{opacity:1}},0); tl.set("#{p}-knob",{{x:22}},0); tl.set("#{p}-tgon",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}-wT, #{p}-wC",{{opacity:0}},0);')
    tcp, tte, tpa, ten = c.trig("B07", "Copy"), c.trig("B07", "Terminal"), c.trig("B07", "paste"), c.trig("B07", "Enter")
    tq, tre = c.trig("B07", "poora"), c.trig("B07", "dobara")
    cx, cy = 40 + 190 + 620 - 190 - 24 - 16 - 40, 40 + 28 + 200 + 27
    c.cursor(cx + 60, cy + 80)
    c.js(f'cursorTo("{p}-cur",{tcp - 0.4:.3f},{cx},{cy},0.35); clickAt("{p}-rip",{tcp:.3f},{cx},{cy});')
    c.js(f'tl.to("#{p}-copy",{{scale:0.9,duration:0.08,yoyo:true,repeat:1}},L({tcp:.3f}));')
    # the copied command flies to the Terminal as a small chip (no text, never the token)
    c.add(f'<div class="abs" id="{p}-fly" style="left:0;top:0;width:44px;height:30px;border-radius:8px;background:#FF9F1C;display:flex;align-items:center;justify-content:center;opacity:0;z-index:45">{icon("copy", 18, "#0E1422", 2.4)}</div>')
    c.js(f'tl.fromTo("#{p}-fly",{{x:{74 + cx - 22},y:{164 + cy - 15},opacity:1,scale:1}},{{x:{74 + 360},y:{164 + 196},scale:0.8,duration:0.55,ease:"power2.inOut",immediateRender:false}},L({tcp + 0.15:.3f}));')
    c.js(f'tl.to("#{p}-fly",{{opacity:0,duration:0.1}},L({tcp + 0.7:.3f}));')
    c.js(f'tl.fromTo("#{p}-wT",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(1.6)"}},L({tte:.3f}));')
    c.js(f'tl.to("#{p}-wS",{{opacity:0.4,duration:0.2}},L({tte:.3f}));')
    c.js(f'zoomTo("{p}-zoom",{tte + 0.1:.3f},500,215,1.7,0.4);')
    c.js(f'show("#{p}-paste",{tpa + 0.1:.3f}); show("#{p}-l2",{ten + 0.15:.3f});')
    c.js(f'zoomOut("{p}-zoom",{ten + 0.6:.3f},0.4);')
    # Claude Desktop fully quit, then reopened (speed ramp: quick close, bounce)
    c.js(f'tl.set("#{p}-wC",{{opacity:1}},L({tte - 0.01:.3f})); tl.set("#{p}-wC",{{opacity:0}},L({tte:.3f}));')
    c.js(f'tl.fromTo("#{p}-wC",{{opacity:1,scale:1}},{{opacity:0,scale:0.9,duration:0.18,ease:"power2.in",immediateRender:false}},L({tq:.3f}));')
    c.js(f'tl.set("#{p}-wC",{{opacity:1,scale:1}},L({tq - 0.5:.3f}));')
    c.js(f'tl.to("#{p}-run-claude",{{opacity:0,duration:0.1}},L({tq + 0.1:.3f}));')
    c.js(f'tl.to("#{p}-app-claude",{{y:-16,duration:0.16,yoyo:true,repeat:3,ease:"power1.out"}},L({tre:.3f}));')
    c.js(f'tl.to("#{p}-run-claude",{{opacity:1,duration:0.1}},L({tre + 0.2:.3f}));')
    c.js(f'tl.fromTo("#{p}-wC",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(1.6)",immediateRender:false}},L({tre + 0.55:.3f}));')
    c.badge(f"{p}-bd", "E3", c.trig("B07", "Edits"))
    checklist(c, f"{p}-ck", [("Copy", tcp, tcp + 0.3), ("Terminal: paste, Enter", tte, ten + 0.2), ("Quit Claude Desktop fully, reopen", tq, tre + 0.6)], ZR[0], 962, 644)


# ---------------------------------------------------------------- S08 Edits 4
def s08(c):
    p = c.p
    cl = win(f"{p}-wC", 8, 30, 916, 544, "Claude", claude_chat(f"{p}c", 916, 516), "#262624")
    c.laptop(f'<div class="wall"></div>{menubar("Claude")}{cl}')
    q = "What tools does Edits have? Summarize them by category."
    tq, tl_, tc = c.trig("B08", "poochho"), c.trig("B08", "List"), c.trig("B08", "connected")
    # message area content
    cats = [("Clips", "film"), ("Voiceover", "user"), ("Subtitles", "text"), ("Music", "music"), ("Sound effects", "spark")]
    rows = "".join(f'<div id="{p}-cat{i}" style="display:flex;align-items:center;gap:10px;margin:7px 0;opacity:0">{icon(ic, 17, "#e9c79a", 2.2)}'
                   f'<b style="font-weight:700;width:120px">{n}</b><div class="bar" style="width:{150 + (i * 47) % 120}px;background:rgba(255,255,255,.16)"></div></div>'
                   for i, (n, ic) in enumerate(cats))
    msgs = (f'<div id="{p}-um" style="margin-left:auto;max-width:470px;padding:10px 14px;border-radius:12px;background:#3a3835;opacity:0">{q}</div>'
            f'<div id="{p}-rep" style="margin-top:16px;opacity:0">{rows}</div>')
    c.js(f'document.getElementById("{p}c-msgs").innerHTML = {json.dumps(msgs)};')
    c.cursor(0, 0, hidden=True)
    t_end = c.js_type_input = None
    c.js(f'typeText("#{p}c-input",{json.dumps(q)},{tq:.3f},44);')
    tsend = tq + len(q) / 44 + 0.1
    c.js(f'tl.set("#{p}c-input",{{text:""}},L({tsend:.3f})); enter("#{p}-um",{tsend:.3f},10);')
    c.js(f'tl.set("#{p}-rep",{{opacity:1}},L({tl_:.3f}));')
    for i in range(5):
        c.js(f'enter("#{p}-cat{i}",{tl_ + i * 0.09:.3f},8);')
    c.js(f'zoomTo("{p}-zoom",{tl_ - 0.2:.3f},466,220,1.18,0.45);')
    c.badge(f"{p}-bd", "E4", c.trig("B08", "Edits"))
    x, y = ZR[0], 968
    c.add(f'<div class="monobox glass" id="{p}-tb" style="left:{x}px;top:{y}px;width:644px;{c.glass_style(x, y)}"><span id="{p}-tbt"></span><span class="caret"></span></div>')
    c.js(f'tl.set("#{p}-tb",{{opacity:0}},0); enter("#{p}-tb",{tq:.3f}); typeText("#{p}-tbt",{json.dumps(q)},{tq + 0.1:.3f},44);')
    c.pill(f"{p}-ok", "Edits connected", 0, 830, tc, "ok", center_row=True)


# ---------------------------------------------------------------- Claude Code terminal
def claude_code_term(p, lines_html):
    return (f'<div class="term" style="position:absolute;inset:0;padding:12px 16px">'
            f'<div style="border:1px solid #6b5a46;border-radius:6px;padding:6px 10px;margin-bottom:8px" class="tline">'
            f'<span style="color:#e9a35a">*</span> Claude Code</div>{lines_html}</div>')


# ---------------------------------------------------------------- S09 Resolve 1
CMDS = ["/plugin marketplace add kingjamesch/davinci-resolve-mcp",
        "/plugin install davinci-resolve@davinci-resolve-mcp",
        "/davinci-resolve:setup"]
CMD_WRAP = ["/plugin marketplace add\nkingjamesch/davinci-resolve-mcp",
            "/plugin install\ndavinci-resolve@\ndavinci-resolve-mcp",
            "/davinci-resolve:setup"]
CMD_OUT = ["marketplace added", "installed", "setup done, restart Resolve"]


def s09(c):
    p = c.p
    # outgoing Edits desktop (Claude window) and the portal into the Resolve desktop
    old = f'<div class="wall"></div>{menubar("Claude")}' + win(f"{p}-wO", 8, 30, 916, 544, "Claude", claude_chat(f"{p}o", 916, 516), "#262624")
    lines = ""
    for i, cmd in enumerate(CMDS):
        lines += (f'<div class="tline" style="white-space:pre-wrap"><span style="color:#e9a35a">&gt;</span> <span id="{p}-cmd{i}"></span></div>'
                  f'<div class="tline tdim" id="{p}-out{i}" style="opacity:0"><span class="tok">&#10003;</span> {CMD_OUT[i]}</div>')
    rs = win(f"{p}-wR", 16, 36, 560, 360, "Resolve", resolve_ui(f"{p}r", 560, 332, menu=False), "#1a1c21")
    tm = win(f"{p}-wT", 300, 150, 616, 330, "Terminal", claude_code_term(p, lines), "#0c0f16")
    new = (f'<div class="abs" id="{p}-portal" style="inset:0;clip-path:circle(0px at 466px 291px)">'
           f'<div class="wall" style="filter:hue-rotate(-12deg)"></div>{menubar("Terminal")}{rs}{tm}{dock(p)}</div>'
           f'<div class="abs" id="{p}-ring" style="left:{466 - 40}px;top:{291 - 40}px;width:80px;height:80px;border-radius:40px;border:5px solid #FF9F1C;opacity:0"></div>')
    c.laptop(old + new)
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    c.cursor(0, 0, hidden=True)
    c.js(f'tl.fromTo("#{p}-portal",{{clipPath:"circle(0px at 466px 291px)"}},{{clipPath:"circle(560px at 466px 291px)",duration:0.5,ease:"power2.in"}},0.02);')
    c.js(f'tl.fromTo("#{p}-ring",{{opacity:1,scale:0.2}},{{scale:14,opacity:0,duration:0.52,ease:"power2.in"}},0.02);')
    tcm = c.trig("B09", "commands")
    tpaste = c.trig("B09", "paste")
    tres = c.trig("B09", "restart")
    t = tcm
    starts = [tcm, tcm + 0.62, tcm + 1.18]
    for i, cmd in enumerate(CMDS):
        c.js(f'typeText("#{p}-cmd{i}",{json.dumps(cmd)},{starts[i]:.3f},110);')
        c.js(f'show("#{p}-out{i}",{starts[i] + len(cmd) / 110 + 0.12:.3f});')
    c.js(f'zoomTo("{p}-zoom",{tcm - 0.3:.3f},610,300,1.5,0.4);')
    c.js(f'zoomOut("{p}-zoom",{tres - 0.4:.3f},0.35);')
    # restart: the Resolve window and dock dot blink off and on (speed ramp)
    c.js(f'tl.to("#{p}-wR",{{opacity:0,scale:0.92,duration:0.12}},L({tres:.3f})); tl.to("#{p}-run-resolve",{{opacity:0,duration:0.05}},L({tres:.3f}));')
    c.js(f'tl.to("#{p}-app-resolve",{{y:-16,duration:0.14,yoyo:true,repeat:3}},L({tres + 0.2:.3f})); tl.to("#{p}-run-resolve",{{opacity:1,duration:0.05}},L({tres + 0.5:.3f}));')
    c.js(f'tl.to("#{p}-wR",{{opacity:1,scale:1,duration:0.2,ease:"back.out(1.6)"}},L({tres + 0.6:.3f}));')
    c.badge(f"{p}-bd", "R1", c.trig("B09", "Resolve"))
    c.chip(f"{p}-br", "Bridge runs inside Resolve", "bridge", 0, 826, c.trig("B09", "bridge"), out=tres - 0.2, center_row=True)
    c.chip(f"{p}-rs", "Restart Resolve once", "restart", 0, 826, tres, center_row=True)
    x, y = ZR[0], 962
    blocks = "".join(f'<div id="{p}-k{i}" style="opacity:0;white-space:pre;border-left:3px solid #FF9F1C;padding-left:10px;margin:{0 if i == 0 else 16}px 0 0">{esc(CMD_WRAP[i])}</div>'
                     for i in range(3))
    c.add(f'<div class="monobox glass" id="{p}-cmds" style="left:{x}px;top:{y}px;width:644px;padding:18px 12px;font-size:32px;line-height:1.25;{c.glass_style(x, y)}">{blocks}</div>')
    c.js(f'tl.set("#{p}-cmds",{{opacity:0}},0); enter("#{p}-cmds",{starts[0]:.3f});')
    for i in range(3):
        c.js(f'enter("#{p}-k{i}",{starts[i]:.3f},12);')


# ---------------------------------------------------------------- S10 Resolve 2
def s10(c):
    p = c.p
    rs = win(f"{p}-wR", 8, 30, 916, 544, "Resolve", resolve_ui(f"{p}r", 916, 516, menu=True), "#1a1c21")
    lines = (f'<div class="tline"><span style="color:#e9a35a">&gt;</span> <span id="{p}-mcp"></span></div>'
             f'<div class="tline" id="{p}-mo" style="opacity:0">  davinci  <span class="tok">&#10003; connected</span></div>')
    tm = win(f"{p}-wT", 360, 250, 540, 250, "Terminal", claude_code_term(p, lines), "#0c0f16")
    c.laptop(f'<div class="wall"></div>{menubar("Resolve")}{rs}{tm}')
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0); tl.set("#{p}-wT",{{opacity:0}},0);')
    tws, tsc, tbr = c.trig("B10", "Workspace"), c.trig("B10", "Scripts"), c.trig("B10", "Claude")
    tclk = c.ctx.sfx["menu_click"]
    tm_, tco = c.trig("B10", "/mcp"), c.trig("B10", "connected")
    wsx, wsy = 8 + 182, 30 + 28 + 12
    scx, scy = 8 + 146 + 40, 30 + 28 + 22 + 4 + 3 * 26 + 14
    bx, by = 8 + 292 + 70, 30 + 28 + 110 + 16
    c.cursor(400, 300)
    c.js(f'cursorTo("{p}-cur",{tws - 0.45:.3f},{wsx},{wsy},0.45); clickAt("{p}-rip",{tws:.3f},{wsx},{wsy});')
    c.js(f'zoomTo("{p}-zoom",{tws - 0.3:.3f},300,130,1.9,0.4);')
    c.js(f'tl.to("#{p}r-ws",{{backgroundColor:"rgba(255,255,255,.16)",duration:0.08}},L({tws:.3f}));')
    c.js(f'tl.fromTo("#{p}r-dd",{{opacity:0,y:-6}},{{opacity:1,y:0,duration:0.15}},L({tws + 0.05:.3f}));')
    c.js(f'cursorTo("{p}-cur",{tsc - 0.35:.3f},{scx},{scy},0.35); tl.to("#{p}r-scripts",{{backgroundColor:"#3b6fd0",duration:0.08}},L({tsc:.3f}));')
    c.js(f'tl.fromTo("#{p}r-sub",{{opacity:0,x:-6}},{{opacity:1,x:0,duration:0.15}},L({tsc + 0.05:.3f}));')
    c.js(f'cursorTo("{p}-cur",{tbr - 0.35:.3f},{bx},{by},0.4); tl.to("#{p}r-bridge",{{backgroundColor:"#3b6fd0",duration:0.08}},L({tbr:.3f}));')
    # callout ring on each menu step
    c.add(f'<div class="abs" id="{p}-ring" style="left:0;top:0;width:150px;height:56px;border-radius:28px;border:4px solid #FF9F1C;opacity:0;z-index:44"></div>')
    def ring(t, x, y, w):
        return f'tl.to("#{p}-ring",{{x:{x},y:{y},width:{w},opacity:1,duration:0.2,ease:"power2.out"}},L({t:.3f}));'
    # ring positions are in frame coords; account for the zoom (1.9x around the menu)
    s = 1.9
    zx = min(0, max(SW - s * SW, SW / 2 - s * 300)); zy = min(0, max(SH - s * SH, SH / 2 - s * 130))
    def fx(x): return 74 + zx + s * x
    def fy(y): return 164 + zy + s * y
    c.js(ring(tws, fx(wsx) - 90, fy(wsy) - 28, 180))
    c.js(ring(tsc, fx(scx) - 80, fy(scy) - 28, 160))
    c.js(ring(tbr, fx(bx) - 150, fy(by) - 28, 300))
    c.js(f'clickAt("{p}-rip",{tclk:.3f},{bx},{by});')
    c.js(f'leave("#{p}-ring",{tclk + 0.3:.3f});')
    c.js(f'tl.to("#{p}r-dd, #{p}r-sub",{{opacity:0,duration:0.12}},L({tclk + 0.25:.3f}));')
    c.js(f'zoomOut("{p}-zoom",{tclk + 0.2:.3f},0.4);')
    c.js(f'tl.fromTo("#{p}-wT",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,ease:"power3.out"}},L({tm_ - 0.25:.3f}));')
    c.js(f'typeText("#{p}-mcp","/mcp",{tm_:.3f},14);')
    c.js(f'show("#{p}-mo",{tco:.3f});')
    c.js(f'zoomTo("{p}-zoom",{tco - 0.2:.3f},640,420,1.6,0.4);')
    c.badge(f"{p}-bd", "R2", tws)
    # breadcrumb Workspace > Scripts > Claude_MCP_Bridge
    x, y = ZR[0], 972
    def ch(i):
        return f'<svg id="{p}-ch{i}" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="opacity:.35;flex:none"><path d="M9 5l7 7-7 7"/></svg>'
    bc = (f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;font:700 38px/1.35 Poppins, sans-serif">'
          f'<span id="{p}-b0" style="opacity:.35">Workspace</span>{ch(0)}<span id="{p}-b1" style="opacity:.35">Scripts</span>{ch(1)}'
          f'<span id="{p}-b2" style="opacity:.35">Claude_MCP_Bridge</span></div>')
    c.add(f'<div class="glass abs" id="{p}-bc" style="left:{x}px;top:{y}px;width:644px;padding:22px 30px;{c.glass_style(x, y)}">{bc}</div>')
    c.js(f'tl.set("#{p}-bc",{{opacity:0}},0); enter("#{p}-bc",{tws:.3f}); leave("#{p}-bc",{tm_ - 0.25:.3f});')
    for i, t in enumerate((tws, tsc, tbr)):
        c.js(f'tl.to("#{p}-b{i}",{{opacity:1,color:"#FF9F1C",duration:0.15}},L({t:.3f}));')
        if i:
            c.js(f'tl.to("#{p}-b{i - 1}",{{color:"#ffffff",duration:0.15}},L({t:.3f})); tl.to("#{p}-ch{i - 1}",{{opacity:1,duration:0.15}},L({t:.3f}));')
    c.add(f'<div class="monobox glass" id="{p}-mb" style="left:{x}px;top:{y}px;width:300px;{c.glass_style(x, y)}"><span id="{p}-mbt"></span><span class="caret"></span></div>')
    c.js(f'tl.set("#{p}-mb",{{opacity:0}},0); enter("#{p}-mb",{tm_:.3f}); typeText("#{p}-mbt","/mcp",{tm_ + 0.05:.3f},14);')
    c.pill(f"{p}-ok", "davinci connected", 0, 830, tco, "ok", center_row=True)


# ---------------------------------------------------------------- S11 together
P1 = "In Resolve, import everything in ~/Footage/day1, make a timeline called Day 1 and render it to ~/Exports."
P2 = ("In Edits, create a 9:16 vertical video under 45 seconds from the render in ~/Exports. "
      "Add subtitles at the bottom center and choose an upbeat track from the library.")


def s11(c):
    p = c.p
    rs = win(f"{p}-wR", 6, 30, 456, 544, "Resolve", resolve_ui(f"{p}r", 456, 516, menu=False), "#1a1c21")
    ed = win(f"{p}-wE", 470, 30, 456, 544, "Edits", edits_editor(f"{p}e", 456, 516, show_labels=False), "#161a23")
    arrow = (f'<svg class="abs" id="{p}-arr" style="left:330px;top:440px;opacity:0;z-index:30" width="270" height="80" viewBox="0 0 270 80">'
             f'<path id="{p}-arrp" d="M10 60 C 90 0, 180 0, 255 40" fill="none" stroke="#FF9F1C" stroke-width="6" stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/>'
             f'<path d="M240 26 L258 42 L236 50" fill="none" stroke="#FF9F1C" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    c.laptop(f'<div class="wall"></div>{menubar("Resolve")}{rs}{ed}{arrow}')
    c.cursor(0, 0, hidden=True)
    tim, ttl, trn = c.trig("B11", "import"), c.trig("B11", "timeline"), c.trig("B11", "render")
    ted = c.trig("B11", "Edits")
    tp1 = c.trig("B11", "Resolve")
    for i in range(6):
        c.js(f'tl.set("#{p}r-pool{i}",{{opacity:0}},0); popIn("#{p}r-pool{i}",{tim + i * 0.06:.3f},0.5);')
    for i in range(4):
        c.js(f'tl.fromTo("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.15}},L({ttl + i * 0.1:.3f}));')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},L({ttl:.3f}));')
    rend_end = trn + 1.05
    c.js(f'tl.set("#{p}r-rq",{{opacity:1}},L({trn:.3f}));')
    c.js(f'tl.fromTo("#{p}r-rqbar",{{scaleX:0}},{{scaleX:1,duration:{rend_end - trn:.2f},ease:"power1.inOut"}},L({trn:.3f}));')
    c.js(f'counter("#{p}r-rqpct",{trn:.3f},{rend_end:.3f},"%");')
    c.js(f'tl.set("#{p}-arr",{{opacity:1}},L({ted:.3f})); tl.to("#{p}-arrp",{{strokeDashoffset:0,duration:0.4,ease:"power2.out"}},L({ted:.3f}));')
    c.js(f'leave("#{p}-arr",{ted + 1.3:.3f});')
    c.js(edits_fill_js(f"{p}e", ted + 0.5, 0.85))
    c.badge(f"{p}-bd", "E+R", c.trig("B11", "dono"))
    # left: prompt 1 with the render counter and DONE inside the same card
    xl, xr, y = 266, 610, 818
    c.add(f'<div class="monobox glass" id="{p}-m1" style="left:{xl}px;top:{y}px;width:334px;padding:18px 18px;font-size:32px;line-height:1.24;{c.glass_style(xl, y)}">'
          f'<span id="{p}-m1t"></span><span class="caret" id="{p}-m1c"></span>'
          f'<div style="display:flex;align-items:center;gap:14px;margin-top:14px;font-weight:700"><span id="{p}-pct" style="opacity:0">0%</span>'
          f'<div class="pill ok" id="{p}-done" style="position:relative;height:52px;font-size:32px;padding:0 20px 0 14px;opacity:0">{icon("check", 30, "#07210f", 3)}<span>DONE</span></div></div></div>')
    c.js(f'tl.set("#{p}-m1",{{opacity:0}},0); enter("#{p}-m1",{tp1:.3f});')
    t1end = typeText_end = tp1 + 0.1 + len(P1) / 52
    c.js(f'typeText("#{p}-m1t",{json.dumps(P1)},{tp1 + 0.1:.3f},52);')
    c.js(f'show("#{p}-pct",{trn:.3f}); counter("#{p}-pct",{trn:.3f},{rend_end:.3f},"%");')
    c.js(f'hide("#{p}-pct",{rend_end + 0.05:.3f}); popIn("#{p}-done",{rend_end + 0.05:.3f},0.5);')
    c.js(f'hide("#{p}-m1c",{ted:.3f});')
    c.add(f'<div class="monobox glass" id="{p}-m2" style="left:{xr}px;top:{y}px;width:340px;padding:18px 18px;font-size:32px;line-height:1.24;{c.glass_style(xr, y)}">'
          f'<span id="{p}-m2t"></span><span class="caret"></span></div>')
    c.js(f'tl.set("#{p}-m2",{{opacity:0}},0); enter("#{p}-m2",{ted:.3f}); typeText("#{p}-m2t",{json.dumps(P2)},{ted + 0.1:.3f},66);')
    return t1end


# ---------------------------------------------------------------- S12 result
def phone_reel(p):
    subs = "".join(f'<div id="{p}-ps{i}" style="position:absolute;left:18%;right:18%;bottom:20%;height:16px;border-radius:8px;background:#fff;opacity:0"></div>' for i in range(3))
    return (f'<div class="abs" id="{p}-ph" style="left:650px;top:118px;width:330px;height:690px;border-radius:52px;background:#05070b;'
            f'box-shadow:0 2px 6px rgba(0,0,0,.35),0 24px 60px rgba(0,0,0,.55),inset 0 0 0 2px #2c3344;z-index:30">'
            f'<div style="position:absolute;left:12px;top:12px;right:12px;bottom:12px;border-radius:42px;overflow:hidden;background:#000">'
            f'<div id="{p}-pv0" style="position:absolute;inset:-10%;background:{THUMBS[0]}"></div>'
            f'<div id="{p}-pv1" style="position:absolute;inset:-10%;background:{THUMBS[1]};opacity:0"></div>'
            f'<div id="{p}-pv2" style="position:absolute;inset:-10%;background:{THUMBS[2]};opacity:0"></div>'
            f'{subs}<div style="position:absolute;left:8%;right:8%;bottom:7%;height:4px;border-radius:2px;background:rgba(255,255,255,.3)">'
            f'<div id="{p}-pbar" style="width:100%;height:100%;background:#fff;transform:scaleX(0);transform-origin:0 50%"></div></div></div>'
            f'<div style="position:absolute;left:128px;top:22px;width:74px;height:20px;border-radius:10px;background:#05070b"></div></div>')


def s12(c):
    p = c.p
    ed = win(f"{p}-wE", 8, 30, 916, 544, "Edits", edits_editor(f"{p}e", 916, 516), "#161a23")
    c.laptop(f'<div class="wall"></div>{menubar("Edits")}{ed}'
             f'<div class="abs" id="{p}-out" style="left:12px;top:{30 + 28 + 258 - 4}px;width:600px;height:{516 - 258 + 2}px;border:4px solid #fff;border-radius:10px;opacity:0"></div>')
    c.js(edits_filled_js(f"{p}e"))
    c.cursor(0, 0, hidden=True)
    c.add(phone_reel(p))
    c.js(f'tl.fromTo("#{p}-ph",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},0);')
    d = c.dur
    for i in range(3):
        a = i * d / 3
        if i:
            c.js(f'tl.set("#{p}-pv{i}",{{opacity:1}},{a:.3f});')
        c.js(f'tl.fromTo("#{p}-pv{i}",{{scale:1}},{{scale:1.08,duration:{d / 3:.3f},ease:"none"}},{a:.3f});')
        c.js(f'tl.set("#{p}-ps{i}",{{opacity:1}},{a + 0.2:.3f}); tl.set("#{p}-ps{i}",{{opacity:0}},{a + d / 3:.3f});')
    c.js(f'tl.fromTo("#{p}-pbar",{{scaleX:0}},{{scaleX:1,duration:{d:.3f},ease:"none"}},0);')
    tfr = c.ctx.sfx["hit"]
    # playhead runs, then a 0.4 s freeze frame with an outline
    c.js(f'tl.fromTo("#{p}e-ph",{{x:0}},{{x:300,duration:{tfr - c.s0:.3f},ease:"none"}},0);')
    c.js(f'tl.set("#{p}-out",{{opacity:1}},L({tfr:.3f}));')
    c.js(f'tl.fromTo("#{p}-push",{{scale:1.03}},{{scale:1.03}},L({tfr:.3f}));')
    c.js(f'tl.to("#{p}e-ph",{{x:520,duration:{max(0.3, c.s0 + c.dur - tfr - 0.4):.3f},ease:"none"}},L({tfr + 0.4:.3f}));')
    c.pill(f"{p}-rr", "Reel ready", ZR[0], 980, c.trig("B12", "taiyaar"), "ok")
    lab = (f'<div class="abs" style="left:60px;width:960px;top:828px;display:flex;justify-content:flex-start;padding-left:20px">'
           f'<div id="{p}-lb" style="position:relative;padding:10px 26px;border:4px solid #fff;border-radius:18px;font:700 40px Poppins, sans-serif">Editable by hand</div></div>')
    c.add(lab)
    c.js(f'tl.set("#{p}-lb",{{opacity:0}},0); enter("#{p}-lb",{tfr:.3f},14);')
    c.chip(f"{p}-po", "Post from Edits", "send", ZR[0], 1090, c.trig("B12", "post"))


# ---------------------------------------------------------------- S13 to S15 fixes
def fix_card(c, n, front, back, t_front, t_flip):
    p = c.p
    x, y = ZR[0], 960
    ticks = "".join(f'<div style="position:relative;width:46px;height:46px;border-radius:23px;border:3px solid rgba(255,255,255,.45);'
                    f'font:800 24px/40px Poppins, sans-serif;text-align:center">{k}'
                    f'<div id="{p}-tk{k}" style="position:absolute;left:-3px;top:-3px;width:46px;height:46px;border-radius:23px;background:#2FD27A;color:#07210f;'
                    f'font:800 24px/46px Poppins, sans-serif;text-align:center;opacity:{1 if k < n else 0}">{k}</div></div>' for k in (1, 2, 3))
    face = 'position:absolute;inset:0;border-radius:36px;padding:96px 34px 30px;'
    c.add(f'<div class="abs" style="left:{x}px;top:{y}px;width:644px;height:330px">'
          f'<div class="glass" id="{p}-ff" style="{face}{c.glass_style(x, y)}">'
          f'<div class="abs" style="left:34px;top:30px">{icon("alert", 46, "#FF4D4D", 2.4)}</div>'
          f'<div style="font:800 56px/1.12 Poppins, sans-serif">{front}</div></div>'
          f'<div class="glass" id="{p}-fb" style="{face}{c.glass_style(x, y)};opacity:0">'
          f'<div class="abs" style="left:34px;top:30px">{icon("check", 46, "#2FD27A", 3)}</div>'
          f'<div style="font:800 50px/1.14 Poppins, sans-serif">{back}</div></div>'
          f'<div class="abs" id="{p}-tks" style="right:30px;top:26px;display:flex;gap:10px;opacity:0">{ticks}</div></div>')
    c.js(f'tl.set("#{p}-ff",{{opacity:0}},0);')
    c.js(f'enter("#{p}-ff",{t_front:.3f}); enter("#{p}-tks",{t_front:.3f});')
    c.js(f'tl.to("#{p}-ff",{{rotationY:90,transformPerspective:1200,duration:6*F,ease:"power1.in"}},L({t_flip:.3f}));')
    c.js(f'tl.set("#{p}-ff",{{opacity:0}},L({t_flip + 6 * F:.3f}));')
    c.js(f'tl.fromTo("#{p}-fb",{{opacity:1,rotationY:-90,transformPerspective:1200}},{{rotationY:0,duration:6*F,ease:"power1.out",immediateRender:false}},L({t_flip + 6 * F:.3f}));')
    c.js(f'tl.set("#{p}-fb",{{opacity:0}},0);')
    c.js(f'tick("#{p}-tk{n}",{t_flip + 0.35:.3f});')


def s13(c):
    p = c.p
    cl = win(f"{p}-wC", 60, 50, 812, 470, "Claude", claude_chat(f"{p}c", 812, 442), "#262624")
    c.laptop(f'<div class="wall"></div>{menubar("Claude")}{cl}{dock(p)}')
    c.cursor(0, 0, hidden=True)
    tf, tb = c.trig("B13", "Ek"), c.trig("B13", "Claude", 2)
    c.js(f'tl.to("#{p}-wC",{{opacity:0,scale:0.92,duration:0.18}},L({tb:.3f})); tl.to("#{p}-run-claude",{{opacity:0,duration:0.05}},L({tb:.3f}));')
    c.js(f'tl.to("#{p}-app-claude",{{y:-16,duration:0.14,yoyo:true,repeat:3}},L({tb + 0.9:.3f})); tl.to("#{p}-run-claude",{{opacity:1,duration:0.05}},L({tb + 1.2:.3f}));')
    c.js(f'tl.to("#{p}-wC",{{opacity:1,scale:1,duration:0.22,ease:"back.out(1.6)"}},L({tb + 1.4:.3f}));')
    fix_card(c, 1, "Edits tools not showing", "Quit Claude Desktop fully, reopen", tf, tb)


def s14(c):
    p = c.p
    lines = (f'<div class="tline"><span style="color:#e9a35a">&gt;</span> <span class="tdim">/mcp</span></div>'
             f'<div class="tline"><span class="terr">bridge is not running</span></div>')
    rs = win(f"{p}-wR", 16, 36, 560, 360, "Resolve", resolve_ui(f"{p}r", 560, 332, menu=False), "#1a1c21")
    tm = win(f"{p}-wT", 330, 190, 580, 220, "Terminal", claude_code_term(p, lines), "#0c0f16")
    c.laptop(f'<div class="wall"></div>{menubar("Terminal")}{rs}{tm}{dock(p)}')
    c.cursor(0, 0, hidden=True)
    tf, tb = c.trig("B14", "Do"), c.trig("B14", "project")
    c.js(f'zoomTo("{p}-zoom",{tf:.3f},560,280,1.4,0.5);')
    c.js(f'zoomOut("{p}-zoom",{tb:.3f},0.4);')
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:0}},0); tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},L({tb + 0.3:.3f}));')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},L({tb + 0.3:.3f}));')
    fix_card(c, 2, "bridge is not running", "Open a project, click Claude_MCP_Bridge again", tf, tb)
    c.chip(f"{p}-op", "Once per Resolve launch", "restart", 0, 826, tf, center_row=True)


def s15(c):
    p = c.p
    pop = (f'<div class="abs" id="{p}-pop" style="left:300px;top:170px;width:330px;height:190px;border-radius:12px;background:#2a2d34;'
           f'box-shadow:0 14px 40px rgba(0,0,0,.6);border:1px solid rgba(255,255,255,.14);z-index:25">'
           f'<div class="abs" style="left:22px;top:24px">{icon("alert", 34, "#e6c15a", 2.2)}</div>'
           f'<div class="bar" style="position:absolute;left:72px;top:30px;width:200px"></div>'
           f'<div class="bar" style="position:absolute;left:72px;top:52px;width:160px"></div>'
           f'<div class="bar" style="position:absolute;left:72px;top:74px;width:190px"></div>'
           f'<div id="{p}-okb" style="position:absolute;right:20px;bottom:20px;width:86px;height:32px;border-radius:8px;background:#3b6fd0"></div></div>')
    circ = (f'<svg class="abs" style="left:262px;top:136px;z-index:26" width="410" height="260" viewBox="0 0 410 260">'
            f'<path id="{p}-circ" d="M205 14 C 330 10, 400 60, 396 130 C 392 205, 300 248, 196 246 C 90 244, 14 200, 16 128 C 18 60, 100 18, 214 22" '
            f'fill="none" stroke="#FF4D4D" stroke-width="7" stroke-linecap="round" stroke-dasharray="1100" stroke-dashoffset="1100"/></svg>')
    rs = win(f"{p}-wR", 8, 30, 916, 544, "Resolve", resolve_ui(f"{p}r", 916, 516, menu=False), "#1a1c21")
    c.laptop(f'<div class="wall"></div>{menubar("Resolve")}{rs}{pop}{circ}')
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    tf, tp, tu = c.trig("B15", "Teen"), c.trig("B15", "popup"), c.trig("B15", "Use")
    c.cursor(700, 480)
    c.js(f'tl.to("#{p}-circ",{{strokeDashoffset:0,duration:0.45,ease:"power2.out"}},L({tp:.3f}));')
    okx, oky = 300 + 330 - 20 - 43, 170 + 190 - 20 - 16
    c.js(f'cursorTo("{p}-cur",{tu - 0.4:.3f},{okx},{oky},0.4); clickAt("{p}-rip",{tu + 0.1:.3f},{okx},{oky});')
    c.js(f'tl.to("#{p}-pop",{{opacity:0,scale:0.92,duration:0.15}},L({tu + 0.25:.3f})); tl.to("#{p}-circ",{{opacity:0,duration:0.15}},L({tu + 0.25:.3f}));')
    fix_card(c, 3, "Claude stuck", "Close the popup in Resolve", tf, tp)


# ---------------------------------------------------------------- S16 CTA and loop
def s16(c, total):
    p = c.p
    c.laptop(desktop_two_windows(p), push=False)
    c.js(edits_filled_js(f"{p}e"))
    for i in range(4):
        c.js(f'tl.set("#{p}r-tclip{i}, #{p}r-taud{i}",{{opacity:1}},0);')
    c.js(f'tl.set("#{p}r-viewimg",{{opacity:1}},0);')
    c.cursor(700, 470, hidden=True)
    tcm, tdm, tcl = c.trig("B16", "Comment"), c.trig("B16", "DM"), c.trig("B16", "Claude")
    tend = total - 0.62  # start of the loop return
    x, y = ZR[0], 1000
    c.add(f'<div class="glass abs" id="{p}-cb" style="left:{x}px;top:{y}px;width:644px;height:110px;border-radius:55px;{c.glass_style(x, y)}">'
          f'<div class="abs" style="left:22px;top:23px;width:64px;height:64px;border-radius:32px;background:rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center">{icon("user", 34, "#fff", 2.2)}</div>'
          f'<div class="abs" style="left:110px;top:24px;font:800 52px/62px Poppins, sans-serif"><span id="{p}-ct"></span><span class="caret" style="height:44px;vertical-align:-6px"></span></div>'
          f'<div class="abs" id="{p}-snd" style="right:22px;top:23px;width:64px;height:64px;border-radius:32px;background:#FF9F1C;display:flex;align-items:center;justify-content:center">{icon("send", 32, "#0E1422", 2.4)}</div></div>')
    c.js(f'tl.set("#{p}-cb",{{opacity:0}},0); enter("#{p}-cb",{tcm:.3f}); typeText("#{p}-ct","EDIT",{tcm + 0.15:.3f},9);')
    c.js(f'tl.to("#{p}-snd",{{scale:0.85,duration:0.08,yoyo:true,repeat:1}},L({tdm - 0.4:.3f}));')
    # DM paper plane flies out of the comment box
    c.add(f'<div class="abs" id="{p}-plane" style="left:0;top:0;opacity:0;z-index:50">{icon("send", 56, "#FF9F1C", 2.4)}</div>')
    c.js(f'tl.fromTo("#{p}-plane",{{x:{x + 560},y:{y + 26},opacity:1,rotation:0}},{{x:{x + 520},y:880,opacity:0,rotation:-20,duration:0.6,ease:"power2.in",immediateRender:false}},L({tdm - 0.35:.3f}));')
    c.chip(f"{p}-dm", "Guide in your DM", "send", 0, 826, tdm, out=tend, center_row=True)
    c.chip(f"{p}-mw", "Made with Claude", "spark", 430, 1150, tcl, out=tend)
    c.js(f'leave("#{p}-cb",{tend:.3f});')
    # loop return: rebuild the exact frame 0 state of S01
    c.js(f'tl.to("#{p}-wE, #{p}-wR",{{scale:0.94,duration:0.2,ease:"power2.inOut"}},L({tend:.3f}));')
    c.add(prompt_bar(p))
    c.js(f'tl.set("#{p}-pb",{{opacity:0}},0); enter("#{p}-pb",{tend + 0.1:.3f},0);')
    c.js(f'tl.set("#{p}-pb",{{opacity:1,y:0}},L({tend + 0.45:.3f}));')

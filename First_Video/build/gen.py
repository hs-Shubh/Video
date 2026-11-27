# Builds the HyperFrames project from timeline.json (voice timing), mouth cues and the beat grid.
import json, os, re, random, math
from hf_common import *
import hf_scenes as S

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
REEL = ROOT + "/reel"
FPS = 30
F = 1 / FPS
T = json.load(open(ROOT + "/timeline.json"))
TOTAL = T["total"]
LEAD = T["lead_in"]
WORDS = T["words"]
BEATS = {b["id"]: b for b in T["beats"]}
ORDER = [b["id"] for b in T["beats"]]
SIL = [(3.87, 4.24), (5.63, 6.00), (6.25, 6.62), (10.87, 11.25), (12.50, 12.85), (18.92, 19.25), (20.05, 20.32), (20.93, 21.24), (22.37, 22.77), (23.59, 23.97), (28.75, 29.10), (29.80, 30.15), (34.46, 34.74), (36.71, 37.09), (37.90, 38.20), (43.61, 43.97), (44.77, 45.08), (45.86, 46.13), (47.27, 47.63), (48.25, 48.50), (49.06, 49.41), (50.12, 50.45), (52.55, 52.84), (56.86, 57.13), (58.75, 59.01), (63.56, 63.84), (70.06, 70.33), (75.29, 75.55), (76.88, 77.15), (79.36, 79.71), (80.22, 80.51), (81.13, 81.38), (86.42, 86.70), (91.25, 91.53), (95.86, 96.12), (99.86, 100.14), (101.82, 102.10)]
SIL_R = [(a + LEAD, b + LEAD) for a, b in SIL]


def norm(s):
    return re.sub(r"[^a-z0-9/]", "", s.lower())


class Ctx:
    def __init__(self):
        self.beats = BEATS
        self.sfx = {}

    def _find(self, beat, word, occ):
        k = 0
        for w in WORDS:
            if w["beat"] == beat and norm(w["text"]) == norm(word):
                k += 1
                if k == occ:
                    return w
        raise KeyError(f"{beat} {word} {occ}")

    def word(self, beat, word, occ=1):
        return self._find(beat, word, occ)["t0"]

    def word_end(self, beat, word, occ=1):
        return self._find(beat, word, occ)["t1"]


ctx = Ctx()


def gap_after(t):
    for a, b in SIL_R:
        if a >= t + 0.02:
            return a
    return t


# ---------- sound moments (each sits in a gap or one frame after a word) ----------
ctx.sfx = {
    "sting1": 0.0,
    "impact": round(gap_after(ctx.word("B02", "Dekho")) + 0.02, 3),
    "toggle": round(gap_after(ctx.word("B06", "karo", 1)) + 0.02, 3),
    "chime1": round(gap_after(ctx.word("B08", "connected")) + 0.02, 3),
    "menu_click": round(ctx.word_end("B10", "click") + F, 3),
    "chime2": round(gap_after(ctx.word("B10", "connected")) + 0.02, 3),
    "hit": round(gap_after(ctx.word("B12", "taiyaar")) + 0.02, 3),
    "sting2": round(gap_after(ctx.word("B16", "jayenge")) + 0.02, 3),
}
ctx.sfx["riser"] = round(ctx.sfx["impact"] - 1.1, 3)
ctx.sfx["whoosh"] = round(ctx.sfx["chime1"] + 0.2, 3)

# ---------- cuts: on the voice, J-cut for steps, snapped to the music beat grid ----------
bj = json.load(open(ROOT + "/build/beats.json"))
grid = sorted(set([round(x, 3) for x in bj["beats"]]))
per = 60 / bj["tempo"]
g0 = grid[0]
while g0 - per > 0:
    g0 -= per
    grid.insert(0, round(g0, 3))
STEPS = {"B05", "B06", "B07", "B08", "B10"}


def snap(t, lo, hi):
    best = None
    for g in grid:
        if lo <= g <= hi and (best is None or abs(g - t) < abs(best - t)):
            best = g
    return round(best, 3) if best is not None else round(t, 3)


cuts = {}
for bid in ORDER:
    s = BEATS[bid]["start"]
    if bid == "B01":
        cuts[bid] = 0.0
    elif bid == "B09":
        cuts[bid] = round(ctx.sfx["whoosh"], 3)  # the zoom portal is the transition, in the gap
    elif bid in STEPS:
        cuts[bid] = snap(s + 8 * F, s + 6 * F, s + 10 * F)
    else:
        cuts[bid] = snap(s - 2 * F, s - 6 * F, s + 2 * F)
    cuts[bid] = round(round(cuts[bid] * FPS) / FPS, 4)  # frame aligned
ends = {}
for i, bid in enumerate(ORDER):
    ends[bid] = cuts[ORDER[i + 1]] if i + 1 < len(ORDER) else TOTAL

# ---------- scenes ----------
os.makedirs(REEL + "/compositions", exist_ok=True)
builders = [S.s01, S.s02, S.s03, S.s04, S.s05, S.s06, S.s07, S.s08, S.s09, S.s10, S.s11, S.s12, S.s13, S.s14, S.s15, S.s16]
scene_ids = []
for i, bid in enumerate(ORDER):
    sid = f"s{i + 1:02d}"
    c = S.Sc(sid, cuts[bid], round(ends[bid] - cuts[bid], 4), ctx)
    if bid == "B16":
        S.s16(c, TOTAL)
    else:
        builders[i](c)
    open(f"{REEL}/compositions/{sid}.html", "w").write(c.html())
    scene_ids.append((sid, bid, cuts[bid], round(ends[bid] - cuts[bid], 4)))

# ---------- mouth cues: Rhubarb, silenced in pauses, merged ----------
mc = json.load(open(ROOT + "/build/mouth_cues.json"))["mouthCues"]
cues = []
for q in mc:
    a, b, v = q["start"] + LEAD, q["end"] + LEAD, q["value"]
    mid = (a + b) / 2
    if any(sa + 0.03 <= mid <= sb - 0.03 for sa, sb in SIL_R):
        v = "X"
    if cues and cues[-1][2] == v:
        cues[-1][1] = b
        continue
    if cues and (b - a) < F * 0.9:  # shorter than a frame: fold into the previous shape
        cues[-1][1] = b
        continue
    cues.append([a, b, v])
# end of the voice and the silences: mouth at rest
cues = [c_ for c_ in cues if c_[0] < TOTAL]

# ---------- host avatar ----------
SKIN, HAIR, SAF, SAF2 = "#BE8159", "#1C1B24", "#FF9F1C", "#E5870C"
MOUTHS = {
    "X": '<path d="M-12 -1 Q0 6 12 -1" stroke="#5a2a22" stroke-width="4" fill="none" stroke-linecap="round"/>',
    "A": '<path d="M-11 0 L11 0" stroke="#5a2a22" stroke-width="5" fill="none" stroke-linecap="round"/>',
    "B": '<path d="M-13 -2 Q0 -4 13 -2 Q0 9 -13 -2 Z" fill="#4a1a1a"/><rect x="-9" y="-3" width="18" height="4" rx="2" fill="#fff"/>',
    "C": '<ellipse cx="0" cy="1" rx="12" ry="7" fill="#4a1a1a"/><rect x="-9" y="-6" width="18" height="4" rx="2" fill="#fff"/>',
    "D": '<ellipse cx="0" cy="3" rx="15" ry="11" fill="#4a1a1a"/><ellipse cx="0" cy="9" rx="8" ry="4" fill="#d7737a"/><rect x="-11" y="-8" width="22" height="5" rx="2.5" fill="#fff"/>',
    "E": '<ellipse cx="0" cy="2" rx="9" ry="9" fill="#4a1a1a"/>',
    "F": '<ellipse cx="0" cy="2" rx="6" ry="6" fill="#4a1a1a" stroke="#7a3a30" stroke-width="3"/>',
    "G": '<path d="M-12 2 Q0 8 12 2" stroke="#7a3a30" stroke-width="4" fill="none" stroke-linecap="round"/><rect x="-10" y="-4" width="20" height="6" rx="2" fill="#fff"/>',
    "H": '<ellipse cx="0" cy="2" rx="12" ry="9" fill="#4a1a1a"/><ellipse cx="0" cy="-3" rx="6" ry="4" fill="#d7737a"/>',
}
mouth_svg = "".join(f'<g id="h-m{k}" style="opacity:{1 if k == "X" else 0}">{v}</g>' for k, v in MOUTHS.items())
head_svg = (f'<svg width="250" height="190" viewBox="0 0 250 190" style="position:absolute;left:0;top:0;overflow:visible">'
            f'<circle cx="74" cy="104" r="11" fill="{SKIN}"/><circle cx="176" cy="104" r="11" fill="{SKIN}"/>'
            f'<ellipse cx="125" cy="100" rx="51" ry="57" fill="{SKIN}"/>'
            f'<path d="M74 96 Q68 38 125 36 Q182 36 177 92 Q166 62 140 60 Q120 70 98 62 Q82 70 74 96 Z" fill="{HAIR}"/>'
            f'<path d="M96 80 Q106 75 116 79" stroke="{HAIR}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="M134 79 Q144 75 154 80" stroke="{HAIR}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<g id="h-eyes"><ellipse cx="106" cy="99" rx="5.5" ry="7.5" fill="#15151c"/><ellipse cx="144" cy="99" rx="5.5" ry="7.5" fill="#15151c"/>'
            f'<circle cx="108" cy="96" r="1.8" fill="#fff"/><circle cx="146" cy="96" r="1.8" fill="#fff"/></g>'
            f'<path d="M125 104 Q120 117 128 119" stroke="#9c6342" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<g transform="translate(125,134)">{mouth_svg}</g></svg>')
body_svg = (f'<svg width="250" height="410" viewBox="0 0 250 410" style="position:absolute;left:0;top:0">'
            f'<ellipse cx="125" cy="402" rx="84" ry="8" fill="rgba(0,0,0,.35)"/>'
            f'<rect x="92" y="296" width="30" height="98" rx="12" fill="#1d2335"/><rect x="128" y="296" width="30" height="98" rx="12" fill="#1d2335"/>'
            f'<rect x="80" y="384" width="46" height="17" rx="8.5" fill="#e9edf5"/><rect x="124" y="384" width="46" height="17" rx="8.5" fill="#e9edf5"/>'
            f'<rect x="112" y="140" width="26" height="30" fill="#A86B49"/>'
            f'<path d="M70 192 Q70 166 96 163 L154 163 Q180 166 180 192 L186 304 Q186 316 174 316 L76 316 Q64 316 64 304 Z" fill="{SAF}"/>'
            f'<path d="M150 165 Q178 168 180 192 L186 304 Q186 316 174 316 L160 316 Z" fill="{SAF2}" opacity=".55"/>'
            f'<path d="M92 262 L158 262 L164 300 L86 300 Z" fill="none" stroke="{SAF2}" stroke-width="4" stroke-linejoin="round"/>'
            f'<ellipse cx="125" cy="166" rx="42" ry="13" fill="{SAF2}"/>'
            f'<path d="M114 172 L112 206 M136 172 L138 206" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/></svg>')


def hand_html(side):
    s = side
    fing = lambda dx, h=24, w=8: f'<div style="position:absolute;left:{14 - w / 2 + dx}px;top:16px;width:{w}px;height:{h}px;border-radius:{w / 2}px;background:{SKIN}"></div>'
    return (f'<div class="abs" style="left:-2px;top:58px;width:28px;height:44px">'
            f'<div id="h-{s}-open" class="abs" style="left:0;top:0;width:28px;height:32px;border-radius:13px;background:{SKIN}"></div>'
            f'<div id="h-{s}-fist" class="abs" style="left:1px;top:0;width:26px;height:26px;border-radius:13px;background:{SKIN};opacity:0"></div>'
            f'<div id="h-{s}-point" class="abs" style="left:0;top:0;width:28px;height:44px;opacity:0"><div class="abs" style="left:1px;top:0;width:26px;height:24px;border-radius:12px;background:{SKIN}"></div>{fing(0, 26)}</div>'
            f'<div id="h-{s}-two" class="abs" style="left:0;top:0;width:28px;height:44px;opacity:0"><div class="abs" style="left:1px;top:0;width:26px;height:24px;border-radius:12px;background:{SKIN}"></div>{fing(-5, 24, 7)}{fing(5, 24, 7)}</div>'
            f'<div id="h-{s}-three" class="abs" style="left:0;top:0;width:28px;height:44px;opacity:0"><div class="abs" style="left:1px;top:0;width:26px;height:24px;border-radius:12px;background:{SKIN}"></div>{fing(-8, 22, 6)}{fing(0, 25, 6)}{fing(8, 22, 6)}</div>'
            f'<div id="h-{s}-thumb" class="abs" style="left:0;top:0;width:28px;height:44px;opacity:0"><div class="abs" style="left:1px;top:0;width:26px;height:24px;border-radius:12px;background:{SKIN}"></div>{fing(-4, 22, 10)}</div>'
            f'</div>')


def arm_html(side, x):
    return (f'<div class="abs" id="h-{side}-up" style="left:{x - 14}px;top:170px;width:28px;height:78px;border-radius:14px;background:{SAF if side == "L" else SAF2}">'
            f'<div class="abs" id="h-{side}-fore" style="left:2px;top:64px;width:24px;height:64px;border-radius:12px;background:{SAF if side == "L" else SAF2}">'
            f'<div class="abs" style="left:0;top:50px;width:24px;height:10px;border-radius:5px;background:{SAF2 if side == "L" else "#c9740a"}"></div>'
            f'{hand_html(side)}</div></div>')


POSES = {  # shoulder L, elbow L, hand L, shoulder R, elbow R, hand R
    "rest": (12, -8, "open", -12, 8, "open"),
    "wave": (12, -8, "open", -145, -25, "open"),
    "pointUp": (12, -8, "open", -158, -12, "point"),
    "pointRight": (12, -8, "open", -92, 2, "point"),
    "pointDown": (12, -8, "open", -50, -12, "point"),
    "handsUp": (150, 22, "open", -150, -22, "open"),
    "shrug": (38, 96, "open", -38, -96, "open"),
    "one": (12, -8, "open", -22, -150, "point"),
    "two": (12, -8, "open", -22, -150, "two"),
    "three": (12, -8, "open", -22, -150, "three"),
    "fist": (12, -8, "open", -165, -6, "fist"),
    "thumbs": (24, 142, "thumb", -24, -142, "thumb"),
    "crossed": (16, -104, "fist", -16, 104, "fist"),
}


def W_(b, w, o=1):
    return ctx.word(b, w, o)


acts = [  # (time, pose)
    (0.0, "rest"), (0.45, "wave"), (W_("B01", "DaVinci") - 0.2, "pointUp"), (W_("B01", "edit") + 0.3, "rest"),
    (W_("B02", "ek") - 0.1, "handsUp"), (W_("B02", "sab"), "rest"),
    (W_("B03", "atakte") - 0.1, "shrug"), (W_("B03", "Edits") + 0.4, "rest"), (W_("B03", "band") - 0.15, "pointUp"),
    (W_("B04", "Pehle") - 0.1, "one"), (BEATS["B04"]["end"] + 0.1, "rest"),
    (W_("B05", "Instagram") - 0.2, "pointUp"), (W_("B05", "sign") + 0.6, "rest"),
    (W_("B06", "Enable") - 0.2, "pointUp"), (W_("B06", "Wahin"), "rest"), (W_("B06", "Copy") - 0.15, "pointUp"),
    (W_("B07", "Copy") - 0.15, "one"), (W_("B07", "Terminal") - 0.15, "two"), (W_("B07", "poora") - 0.15, "three"), (BEATS["B07"]["end"], "rest"),
    (W_("B08", "connected") - 0.1, "fist"), (BEATS["B08"]["end"] + 0.3, "rest"),
    (W_("B09", "Resolve") - 0.1, "pointUp"), (W_("B09", "commands") - 0.15, "pointUp"), (W_("B09", "restart"), "rest"),
    (W_("B10", "Workspace") - 0.2, "pointUp"), (W_("B10", "connected") - 0.1, "thumbs"), (BEATS["B10"]["end"] + 0.1, "rest"),
    (W_("B11", "dono") - 0.1, "crossed"), (BEATS["B11"]["end"], "rest"),
    (W_("B12", "taiyaar") - 0.15, "thumbs"), (BEATS["B12"]["end"], "rest"),
    (W_("B13", "Ek") - 0.15, "one"), (BEATS["B13"]["end"], "rest"),
    (W_("B14", "Do") - 0.15, "two"), (BEATS["B14"]["end"], "rest"),
    (W_("B15", "Teen") - 0.15, "three"), (W_("B15", "popup") - 0.15, "pointUp"), (BEATS["B15"]["end"], "rest"),
    (W_("B16", "Poora"), "wave"), (W_("B16", "Comment") - 0.15, "pointDown"), (TOTAL - 0.75, "rest"),
]
hj = ["const F=1/30; const tl=gsap.timeline({paused:true});",
      'tl.set("#h-L-up,#h-R-up",{transformOrigin:"14px 8px"},0); tl.set("#h-L-fore,#h-R-fore",{transformOrigin:"12px 6px"},0);']
cur_hand = {"L": "open", "R": "open"}
first = True
for t, pose in acts:
    sL, eL, hL, sR, eR, hR = POSES[pose]
    d = 0 if first else 0.4
    ease = "steps(6)"  # body on twos
    if first:
        hj.append(f'tl.set("#h-L-up",{{rotation:{sL}}},0); tl.set("#h-L-fore",{{rotation:{eL}}},0); tl.set("#h-R-up",{{rotation:{sR}}},0); tl.set("#h-R-fore",{{rotation:{eR}}},0);')
    else:
        hj.append(f'tl.to("#h-L-up",{{rotation:{sL},duration:{d},ease:"{ease}"}},{t:.3f}); tl.to("#h-L-fore",{{rotation:{eL},duration:{d},ease:"{ease}"}},{t:.3f});')
        hj.append(f'tl.to("#h-R-up",{{rotation:{sR},duration:{d},ease:"{ease}"}},{t:.3f}); tl.to("#h-R-fore",{{rotation:{eR},duration:{d},ease:"{ease}"}},{t:.3f});')
    for side, hh in (("L", hL), ("R", hR)):
        if hh != cur_hand[side]:
            hj.append(f'tl.set("#h-{side}-{cur_hand[side]}",{{opacity:0}},{t + 0.2:.3f}); tl.set("#h-{side}-{hh}",{{opacity:1}},{t + 0.2:.3f});')
            cur_hand[side] = hh
    if pose == "wave":
        for k in range(3):
            hj.append(f'tl.to("#h-R-fore",{{rotation:{-25 + (30 if k % 2 == 0 else 0)},duration:0.2,ease:"steps(3)"}},{t + 0.4 + k * 0.2:.3f});')
    if pose == "fist":
        hj.append(f'tl.to("#h-R-up",{{rotation:-140,duration:0.14,yoyo:true,repeat:3,ease:"steps(2)"}},{t + 0.4:.3f});')
    if pose == "shrug":
        hj.append(f'tl.fromTo("#h-head",{{rotation:0}},{{rotation:-6,duration:0.2,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')
    first = False
# nods during B11
for tn in (ctx.word("B11", "render", 1), ctx.word("B11", "music")):
    hj.append(f'tl.fromTo("#h-head",{{rotation:0,y:0}},{{rotation:5,y:4,duration:0.14,yoyo:true,repeat:1,immediateRender:false}},{tn:.3f});')
# steps back in B11 (scale 0.93, stays over 380 px tall)
hj.append(f'tl.to("#h-wrap",{{scale:0.93,x:-16,duration:0.4,ease:"power2.inOut"}},{BEATS["B11"]["start"]:.3f});')
hj.append(f'tl.to("#h-wrap",{{scale:1,x:0,duration:0.4,ease:"power2.inOut"}},{cuts["B12"]:.3f});')
# head bob on saffron words
for w in WORDS:
    if w["hl"] and w["t0"] > 0.5:
        hj.append(f'tl.fromTo("#h-head",{{y:0}},{{y:-5,duration:0.09,yoyo:true,repeat:1,ease:"power1.out",immediateRender:false}},{w["t0"]:.3f});')
# seeded blinks every 3 to 5 s, none near the loop frames
rnd = random.Random(42)
t = 1.6
while t < TOTAL - 1.0:
    hj.append(f'tl.to("#h-eyes",{{scaleY:0.1,duration:2*F,yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{t:.3f});')
    t += 3 + 2 * rnd.random()
# mouth shapes
prev = "X"
for a, b, v in cues:
    if v != prev:
        hj.append(f'tl.set("#h-m{prev}",{{opacity:0}},{a:.3f}); tl.set("#h-m{v}",{{opacity:1}},{a:.3f});')
        prev = v
if prev != "X":
    hj.append(f'tl.set("#h-m{prev}",{{opacity:0}},{TOTAL - 0.9:.3f}); tl.set("#h-mX",{{opacity:1}},{TOTAL - 0.9:.3f});')
# version 3: the host appears only in the hook, proof, roadmap, together, payoff and CTA beats
VIS = {"B01", "B02", "B04", "B11", "B12", "B16"}
hj.append('tl.set("#h-wrap",{opacity:0},0);')
hj.append('tl.fromTo("#h-wrap",{opacity:0,y:70},{opacity:1,y:0,duration:0.32,ease:"back.out(1.6)",immediateRender:false},2.8);')
shown = True
for bid in ORDER[1:]:
    t = cuts[bid]
    v = bid in VIS
    if v and not shown:
        hj.append(f'tl.fromTo("#h-wrap",{{opacity:0,y:70}},{{opacity:1,y:0,duration:0.32,ease:"back.out(1.6)",immediateRender:false}},{t + 0.1:.3f});')
    elif shown and not v:
        hj.append(f'tl.to("#h-wrap",{{opacity:0,y:50,duration:0.2,ease:"power2.in"}},{t - 0.05:.3f});')
    shown = v
hj.append(f'tl.to("#h-wrap",{{opacity:0,y:50,duration:0.2,ease:"power2.in"}},{TOTAL - 0.62:.3f});')
# the loop: back to the exact frame 0 pose
hj.append(f'tl.set("#h-head",{{x:0,y:0,rotation:0}},{TOTAL - 0.62:.3f}); tl.set("#h-eyes",{{scaleY:1}},{TOTAL - 0.62:.3f}); tl.set("#h-wrap",{{x:0,scale:1}},{TOTAL - 0.62:.3f});')
hj.append(f'tl.set({{}},{{}},{TOTAL - 0.01:.3f});')
hj.append('window.__timelines["host"] = tl;')
host_html = ("<template>\n<style>#root{position:absolute;inset:0;overflow:hidden}.abs{position:absolute}</style>\n"
             '<div id="root" data-composition-id="host" data-width="1080" data-height="1920">'
             f'<div class="abs" id="h-wrap" style="left:{HOST[0]}px;top:{HOST[1]}px;width:250px;height:410px;transform-origin:0 100%">'
             f'{body_svg}{arm_html("L", 78)}<div class="abs" id="h-head" style="left:0;top:0;width:250px;height:190px;transform-origin:125px 160px">{head_svg}</div>'
             f'{arm_html("R", 172)}</div></div>\n<script>\n(function(){{\n' + "\n".join(hj) + "\n})();\n</script>\n</template>\n")
host_html = S.fix_sets(host_html)
open(REEL + "/compositions/host.html", "w").write(host_html)

# ---------- captions ----------
KEEP = [("apple", "silicon"), ("enable", "automation", "server"), ("claude", "mcp", "bridge"), ("claude", "code"), ("claude", "desktop"),
        ("davinci", "connected"), ("sign", "in"), ("vertical", "reel"), ("instagram", "edits"), ("davinci", "resolve"), ("teen", "fix"),
        ("is", "not", "running"), ("ek", "prompt"), ("teen", "commands"), ("dono", "ek", "saath"), ("claude", "ne", "banayi")]
STEPNUM = {"1", "2", "3", "4"}
chunks = []
i = 0
ws = WORDS
while i < len(ws):
    w = ws[i]
    if w["beat"] == "B01":
        chunks.append([i]); i += 1; continue
    # step numeral chunk: "Edits 1"
    if i + 1 < len(ws) and ws[i + 1]["text"] in STEPNUM and ws[i + 1]["beat"] == w["beat"]:
        chunks.append([i, i + 1]); i += 2; continue
    # keep-together phrases
    matched = None
    for ph in KEEP:
        n = len(ph)
        if i + n <= len(ws) and tuple(norm(x["text"]) for x in ws[i:i + n]) == ph and all(x["beat"] == w["beat"] for x in ws[i:i + n]):
            matched = n
            break
    if matched:
        ch = list(range(i, i + matched)); i += matched
    else:
        ch = [i]; i += 1
    # grow to 2 or 3 words unless a punctuation break or a beat change
    while len(ch) < 3 and i < len(ws) and ws[i]["beat"] == w["beat"] and not ws[ch[-1]]["punct"]:
        nxt = ws[i]
        if nxt["text"] in STEPNUM:
            break
        is_phrase = any(tuple(norm(x["text"]) for x in ws[i:i + len(ph)]) == ph for ph in KEEP)
        if is_phrase:
            break
        if len(ch) == 2 and ws[ch[-1]]["t1"] - ws[ch[0]]["t0"] > 0.75:
            break
        ch.append(i); i += 1
    chunks.append(ch)
cap_items = []
for k, ch in enumerate(chunks):
    t0 = ws[ch[0]]["t0"] - 2 * F
    nxt = ws[chunks[k + 1][0]]["t0"] - 2 * F if k + 1 < len(chunks) else TOTAL - 0.65
    endw = ws[ch[-1]]["t1"]
    t1 = nxt if nxt - endw < 0.7 else endw + 0.35
    t1 = max(t1, t0 + 0.6)
    if k + 1 < len(chunks):
        t1 = min(t1, nxt)
    if k == 0:
        t0 = 0.0
    cap_items.append((k, ch, round(t0, 3), round(t1, 3)))
cap_html, cj = [], ["const F=1/30; const tl=gsap.timeline({paused:true});"]
for k, ch, t0, t1 in cap_items:
    spans = []
    for j in ch:
        w = ws[j]
        txt = w["text"] + (w["punct"] if w["punct"] == "?" else "")
        spans.append(f'<span id="cw{j}">{esc(txt)}</span>')
    pop = ws[ch[0]]["beat"] == "B01" or (len(ch) == 2 and ws[ch[1]]["text"] in STEPNUM)
    cap_html.append(f'<div class="cap clip" id="cc{k}" data-start="{t0}" data-duration="{round(t1 - t0, 3)}" data-track-index="0"><div class="ci" id="ci{k}">{" ".join(spans)}</div></div>')
    if pop and k > 0:
        cj.append(f'tl.fromTo("#ci{k}",{{scale:0.7,opacity:0.4}},{{scale:1,opacity:1,duration:6*F,ease:"back.out(2.6)"}},{t0:.3f});')
    for j in ch:
        w = ws[j]
        if w["hl"]:
            cj.append(f'tl.set("#cw{j}",{{color:"#FF9F1C"}},{w["t0"] - F:.3f}); tl.set("#cw{j}",{{color:"#ffffff"}},{max(w["t1"], w["t0"] + 0.25):.3f});')
# the loop: the first chunk returns, inactive, for the last frames
k0 = cap_items[0]
cap_html.append(f'<div class="cap clip" id="ccL" data-start="{TOTAL - 0.62:.3f}" data-duration="0.62" data-track-index="0"><div class="ci">{esc(ws[0]["text"])}</div></div>')
cj.append(f'tl.set({{}},{{}},{TOTAL - 0.01:.3f});')
cj.append('window.__timelines["captions"] = tl;')
cap_css = ("#root{position:absolute;inset:0;overflow:hidden}"
           ".cap{position:absolute;left:100px;width:860px;bottom:340px;text-align:center}"
           ".ci{display:inline-block;font:800 88px/1.08 Poppins, sans-serif;color:#fff;letter-spacing:-.5px;"
           "-webkit-text-stroke:12px #0E1422;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.45);transform-origin:50% 100%}")
open(REEL + "/compositions/captions.html", "w").write(
    f"<template>\n<style>{cap_css}</style>\n<div id=\"root\" data-composition-id=\"captions\" data-width=\"1080\" data-height=\"1920\">\n"
    + "\n".join(cap_html) + "\n</div>\n<script>\n(function(){\n" + "\n".join(cj) + "\n})();\n</script>\n</template>\n")

# ---------- index ----------
hosts = []
for n, (sid, bid, s0, d) in enumerate(scene_ids):
    hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s0}" data-duration="{d}" '
                 f'data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:10"></div>')
index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/vendor/TextPlugin.min.js"></script>
    <script>gsap.registerPlugin(TextPlugin);</script>
    <style>
      :root {{ --ground: #0E1422; --accent: #FF9F1C; --ink: #ffffff; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; background: var(--ground); font-family: Poppins, sans-serif; }}
      #bg {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background: url(assets/img/desk.png); }}
      #grain {{ position: absolute; inset: 0; background: url(assets/img/noise.png); background-size: 256px 256px; opacity: .03; mix-blend-mode: overlay; z-index: 90; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="bg"></div>
{chr(10).join(hosts)}
      <div id="host" data-composition-id="host" data-composition-src="compositions/host.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:30"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:40"></div>
      <div id="grain"></div>
      <audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // slow camera drift on the grid, returning to the start for the loop
      tl.fromTo("#bg", {{ x: 0, y: 0 }}, {{ x: -40, y: -30, duration: {TOTAL / 2:.3f}, ease: "sine.inOut" }}, 0);
      tl.to("#bg", {{ x: 0, y: 0, duration: {TOTAL / 2:.3f}, ease: "sine.inOut" }}, {TOTAL / 2:.3f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(REEL + "/index.html", "w").write(index)

# ---------- docs and timing record ----------
json.dump({"cuts": cuts, "sfx": ctx.sfx, "scenes": scene_ids, "captions": [(k, [ws[j]["text"] for j in ch], t0, t1) for k, ch, t0, t1 in cap_items],
           "mouth_cues": len(cues), "grid_tempo": bj["tempo"]}, open(ROOT + "/build/plan.json", "w"), indent=1)
os.makedirs(ROOT + "/docs", exist_ok=True)
md = ["# Beat table", "", "Measured from `voice/voiceover.wav` (sherpa-onnx Parakeet word timestamps, English anchors, silence gaps). Reel time includes the 0.35 s lead in.", "",
      "| Beat | Role | Voice start | Voice end | Reel start | Reel end | Picture cut | Length |", "|---|---|---|---|---|---|---|---|"]
for b in T["beats"]:
    md.append(f'| {b["id"]} | {b["role"]} | {b["vs"]:.2f} | {b["ve"]:.2f} | {b["start"]:.2f} | {b["end"]:.2f} | {cuts[b["id"]]:.2f} | {b["end"] - b["start"]:.2f} |')
md += ["", f"Total reel length: {TOTAL:.2f} s (voice {T['voice_duration']:.2f} s + 0.35 s lead in + 0.6 s tail).", "",
       "## Sound moments (reel time)", ""] + [f"- {k}: {v:.2f} s" for k, v in sorted(ctx.sfx.items(), key=lambda x: x[1])]
open(ROOT + "/docs/beats.md", "w").write("\n".join(md) + "\n")
print("ok total", TOTAL, "chunks", len(chunks), "cues", len(cues))
print(json.dumps(cuts))
print(json.dumps(ctx.sfx))

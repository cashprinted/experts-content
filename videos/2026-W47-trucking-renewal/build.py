"""Build index.html for the Experts Agency 'Don't sign that renewal' reel from timing.json."""
import json

T = json.load(open("timing.json"))
L = T["lines"]
MAP = json.load(open("map12.json"))
W = lambda li, wi: L[li]["words"][wi][1]          # word start
WE = lambda li, wi: L[li]["words"][wi][2]         # word end
ONYX, BRASS, DEEP, BONE, PAPER = "#0F0F0F", "#C2A24C", "#8A6F2B", "#F7F5F0", "#F2EFE8"

# scene boundaries
from scenes import S2, S3, S4, S5, S5B, S6, S7, DUR

js = []          # timeline statements
def at(t): return f"{t:.3f}"
def add(s): js.append(s)

# ---------------- captions: kinetic words, chunks of up to 3 words ----------------
cap_html = []
for li, line in enumerate(L):
    if li == 7: continue  # end card shows its own type
    words = line["words"]
    chunks, cur = [], []
    for wi, w in enumerate(words):
        if cur and sum(len(words[k][0]) + 1 for k in cur) + len(w[0]) > 19:
            chunks.append(cur); cur = []
        cur.append(wi)
        if len(cur) == 3 or w[0].endswith((",", ".", "?")) or wi == len(words) - 1:
            chunks.append(cur); cur = []
    for ci, ch in enumerate(chunks):
        cid = f"c{li}_{ci}"
        spans = "".join(f'<span class="w" id="{cid}_{k}">{words[wi][0].rstrip(",.").upper()}</span>' for k, wi in enumerate(ch))
        cap_html.append(f'<div class="cap" id="{cid}">{spans}</div>')
        t0 = words[ch[0]][1] - 0.04
        nxt = chunks[ci + 1] if ci + 1 < len(chunks) else None
        t1 = (words[nxt[0]][1] - 0.06) if nxt else min(line["speech"][1] + 0.22, (L[li + 1]["speech"][0] - 0.06) if li + 1 < len(L) else 99)
        add(f'tl.set("#{cid}", {{autoAlpha: 1}}, {at(t0)});')
        for k, wi in enumerate(ch):
            ws = words[wi][1]
            add(f'tl.fromTo("#{cid}_{k}", {{opacity: 0, y: 26, scale: 0.92}}, {{opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "expo.out"}}, {at(ws - 0.03)});')
            add(f'tl.set("#{cid}_{k}", {{color: "{BRASS}"}}, {at(ws - 0.03)});')
            nxt_w = words[ch[k + 1]][1] if k + 1 < len(ch) else t1
            add(f'tl.set("#{cid}_{k}", {{color: "{BONE}"}}, {at(nxt_w - 0.03)});')
        add(f'tl.to("#{cid}", {{autoAlpha: 0, y: -14, duration: 0.12, ease: "power2.in"}}, {at(t1 - 0.1)});')

# ---------------- desk: renewal notice, compare, send (0 - S4) ----------------
def doc(id_, title, rows, sign=True, muted=False):
    bars = "".join(
        f'<div class="row"><div class="lab">{r}</div><div class="bar" style="width:{w}%"></div></div>'
        for r, w in rows)
    sig = ('<div class="sig"><div class="lab">Insured signature</div><div class="line"></div></div>' if sign else "")
    cls = "doc muted" if muted else "doc"
    return (f'<div class="{cls}" id="{id_}"><div class="dt">{title}</div><div class="rule"></div>{bars}'
            f'<div class="prem"><div class="lab">Renewal premium</div><div class="pv">$<span class="bar" style="width:150px"></span></div></div>{sig}</div>')

rows = [("Auto liability", 78), ("Motor truck cargo", 64), ("Physical damage", 70)]
desk = (doc("docA", "Renewal notice", rows) + doc("docB", "Other options", rows, sign=False, muted=True)
        + '<div class="stamp" id="stamp"><span>NOT</span><span>YET</span></div>'
        + '<div class="vs" id="vs">VS</div>'
        + '<div class="badge" id="badge"><img src="assets/img/logo.svg" alt=""></div>')

# hook: the notice is already flying at frame 0
add('tl.fromTo("#docA", {x: 0, y: -40, scale: 1.42, rotation: -9}, {x: 0, y: 0, scale: 1, rotation: -3, duration: 0.5, ease: "expo.out"}, 0);')
add(f'tl.to("#docA", {{y: -10, rotation: -2.2, duration: {S2 - 0.5:.2f}, ease: "sine.inOut"}}, 0.5);')
st = W(0, 5)  # "yet"
add(f'tl.fromTo("#stamp", {{autoAlpha: 0, scale: 2.4, rotation: -4}}, {{autoAlpha: 1, scale: 1, rotation: -13, duration: 0.13, ease: "power4.in"}}, {at(st - 0.11)});')
add(f'tl.fromTo("#desk", {{x: 0, y: 0}}, {{keyframes: [{{x: -9, y: 6, duration: 0.04}}, {{x: 7, y: -5, duration: 0.04}}, {{x: -4, y: 3, duration: 0.05}}, {{x: 0, y: 0, duration: 0.07}}]}}, {at(st + 0.02)});')
# compare
add(f'tl.to(["#docA", "#stamp"], {{x: -232, scale: 0.74, rotation: -6, duration: 0.55, ease: "power3.inOut"}}, {at(S2)});')
add(f'tl.fromTo("#docB", {{x: 900, scale: 0.74, rotation: 14, autoAlpha: 0}}, {{x: 232, rotation: 5, autoAlpha: 1, duration: 0.6, ease: "expo.out"}}, {at(S2 + 0.12)});')
cmp_t = W(1, 3)
add(f'tl.fromTo("#vs", {{autoAlpha: 0, scale: 0.3}}, {{autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)"}}, {at(cmp_t - 0.04)});')
# send
add(f'tl.to("#vs", {{autoAlpha: 0, scale: 0.6, duration: 0.18, ease: "power2.in"}}, {at(S3 - 0.05)});')
add(f'tl.to("#docB", {{x: 1100, rotation: 12, autoAlpha: 0, duration: 0.45, ease: "power3.in"}}, {at(S3)});')
add(f'tl.to("#stamp", {{autoAlpha: 0, duration: 0.2}}, {at(S3)});')
add(f'tl.to("#docA", {{x: 0, y: 200, scale: 0.7, rotation: 0, duration: 0.55, ease: "power3.inOut"}}, {at(S3 + 0.05)});')
add(f'tl.fromTo("#badge", {{autoAlpha: 0, scale: 0.6, y: 30}}, {{autoAlpha: 1, scale: 1, y: 0, duration: 0.45, ease: "expo.out"}}, {at(W(2, 0))});')
pol = W(2, 4)
add(f'tl.to("#docA", {{y: -400, scale: 0.12, rotation: 8, autoAlpha: 0.0, duration: 0.42, ease: "power3.in"}}, {at(pol - 0.12)});')
add(f'tl.to("#badge", {{keyframes: [{{scale: 1.12, duration: 0.09, ease: "power2.out"}}, {{scale: 1, duration: 0.35, ease: "expo.out"}}]}}, {at(pol + 0.3)});')
add(f'tl.fromTo("#ring", {{autoAlpha: 0.9, scale: 0.6}}, {{autoAlpha: 0, scale: 1.9, duration: 0.7, ease: "expo.out", immediateRender: false}}, {at(pol + 0.3)});')

# ---------------- S4: side by side ----------------
def card(id_, head, brass=False):
    rws = "".join(f'<div class="crow" id="{id_}r{k}"><svg class="ck" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"></path></svg><span>{r}</span></div>'
                  for k, (r, _) in enumerate(rows))
    return (f'<div class="card{" gold" if brass else ""}" id="{id_}"><div class="ch">{head}</div>{rws}'
            f'<div class="cprem" id="{id_}p"><div class="lab">Premium</div><div class="fill" id="{id_}f"></div></div></div>')
cmp_html = card("cardL", "Your policy") + '<div class="midline" id="midline"></div>' + card("cardR", "Our quote", True)
add(f'tl.fromTo("#cardL", {{x: -140, autoAlpha: 0}}, {{x: 0, autoAlpha: 1, duration: 0.55, ease: "expo.out"}}, {at(S4)});')
add(f'tl.fromTo("#cardR", {{x: 140, autoAlpha: 0}}, {{x: 0, autoAlpha: 1, duration: 0.55, ease: "expo.out"}}, {at(S4 + 0.06)});')
for k, t in enumerate([W(3, 1), W(3, 3), W(3, 3) + 0.3]):
    for c in ("cardL", "cardR"):
        add(f'tl.fromTo("#{c}r{k}", {{autoAlpha: 0, x: -18}}, {{autoAlpha: 1, x: 0, duration: 0.3, ease: "expo.out"}}, {at(t)});')
        add(f'tl.fromTo("#{c}r{k} .ck path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.25, ease: "power2.out"}}, {at(t + 0.06)});')
num = W(3, 8)
for c in ("cardL", "cardR"):
    add(f'tl.fromTo("#{c}p", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.2}}, {at(num - 0.05)});')
    add(f'tl.fromTo("#{c}f", {{scaleX: 0}}, {{scaleX: 1, duration: 0.5, ease: "expo.out"}}, {at(num)});')
sbs = W(3, 9)
add(f'tl.to("#cardL", {{x: 26, duration: 0.5, ease: "power3.inOut"}}, {at(sbs)});')
add(f'tl.to("#cardR", {{x: -26, duration: 0.5, ease: "power3.inOut"}}, {at(sbs)});')
add(f'tl.fromTo("#midline", {{scaleY: 0}}, {{scaleY: 1, duration: 0.5, ease: "expo.out"}}, {at(sbs + 0.1)});')

# ---------------- S5: beat it / already set ----------------
bars = ('<div class="chart" id="chart"><div class="bcol"><div class="bar2 cur" id="barCur"></div><div class="bl">Current rate</div></div>'
        '<div class="bcol"><div class="bar2 ours" id="barOurs"></div><div class="bl gold">Our quote</div></div>'
        '<div class="gap" id="gapMark"><div class="gl"></div><div class="gt">YOU SAVE</div></div></div>')
lock = (doc("docC", "Renewal notice", rows)
        + '<svg class="lock" id="lock" viewBox="0 -60 200 310"><g id="shackle"><path class="so" d="M52 118V78a48 48 0 0 1 96 0v40"></path><path class="si" d="M52 118V78a48 48 0 0 1 96 0v40"></path></g>'
          '<rect class="lb" x="18" y="112" width="164" height="128" rx="20"></rect><circle class="kh" cx="100" cy="164" r="15"></circle><rect class="kh" x="93" y="170" width="14" height="34" rx="5"></rect></svg>'
        + '<div class="locklab" id="locklab">LOCKED IN FOR 12 MONTHS</div>')
add(f'tl.fromTo("#barCur", {{scaleY: 0}}, {{scaleY: 1, duration: 0.55, ease: "expo.out"}}, {at(S5 + 0.05)});')
add(f'tl.fromTo("#barOurs", {{scaleY: 0}}, {{scaleY: 1, duration: 0.6, ease: "expo.out"}}, {at(W(4, 3) - 0.04)});')
sv = W(4, 7)
add(f'tl.fromTo("#gapMark", {{autoAlpha: 0, x: -20}}, {{autoAlpha: 1, x: 0, duration: 0.3, ease: "expo.out"}}, {at(sv - 0.05)});')
add(f'tl.to("#chart", {{keyframes: [{{scale: 1.04, duration: 0.07}}, {{scale: 1, duration: 0.4, ease: "expo.out"}}]}}, {at(sv)});')
add(f'tl.to("#chart", {{autoAlpha: 0, y: -40, duration: 0.22, ease: "power2.in"}}, {at(S5B - 0.26)});')
add(f'tl.fromTo("#docC", {{autoAlpha: 0, y: 80, scale: 0.62, rotation: 4}}, {{autoAlpha: 1, y: 0, scale: 0.72, rotation: -2, duration: 0.55, ease: "expo.out"}}, {at(S5B + 0.02)});')
add(f'tl.fromTo("#lock", {{autoAlpha: 0, scale: 1.5, y: -60}}, {{autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: "expo.out"}}, {at(S5B + 0.3)});')
add(f'tl.fromTo("#shackle", {{y: -46}}, {{y: -46, duration: 0.01}}, {at(S5B)});')
lk = W(5, 6)  # "overpay"
add(f'tl.to("#shackle", {{y: 0, duration: 0.12, ease: "power4.in"}}, {at(lk - 0.12)});')
add(f'tl.to("#lock", {{keyframes: [{{scale: 1.08, duration: 0.06}}, {{scale: 1, duration: 0.4, ease: "expo.out"}}]}}, {at(lk)});')
add(f'tl.to("#docC", {{opacity: 0.42, duration: 0.5, ease: "power2.out"}}, {at(lk)});')
add(f'tl.fromTo("#sSave .cam", {{y: 0}}, {{keyframes: [{{y: 10, duration: 0.04}}, {{y: -7, duration: 0.04}}, {{y: 4, duration: 0.05}}, {{y: 0, duration: 0.07}}]}}, {at(lk + 0.01)});')
add(f'tl.fromTo("#locklab", {{autoAlpha: 0, y: 24, letterSpacing: "0.3em"}}, {{autoAlpha: 1, y: 0, letterSpacing: "0.14em", duration: 0.5, ease: "expo.out"}}, {at(W(5, 7) - 0.04)});')

# ---------------- S6: twelve states ----------------
state_paths = "".join(f'<path class="lit" id="st{k}" d="{s["d"]}"></path>' for k, s in enumerate(MAP["states"]))
mapsvg = (f'<svg class="map" id="map" viewBox="0 0 {MAP["W"]} {MAP["H"]}"><path class="dim" d="{MAP["dim"]}"></path>{state_paths}</svg>')
counter = '<div class="count" id="count"><div class="cn"><span id="cnum">0</span></div><div class="cl">States licensed</div></div>'
abbr = '<div class="abbr" id="abbr">' + "".join(f'<span id="ab{k}">{s["ab"]}</span>' for k, s in enumerate(sorted(MAP["states"], key=lambda s: s["ab"]))) + "</div>"
add(f'tl.fromTo("#map", {{scale: 1.18, autoAlpha: 0}}, {{scale: 1, autoAlpha: 1, duration: 0.7, ease: "expo.out"}}, {at(S6)});')
add(f'tl.fromTo("#count", {{autoAlpha: 0, y: 30}}, {{autoAlpha: 1, y: 0, duration: 0.45, ease: "expo.out"}}, {at(S6 + 0.08)});')
tw = W(6, 4)  # "twelve"
t0 = S6 + 0.25
lit_times = [t0 + k * (tw - t0) / 11 for k in range(12)]
for k, t in enumerate(lit_times):
    add(f'tl.fromTo("#st{k}", {{opacity: 0}}, {{opacity: 1, duration: 0.18, ease: "power2.out"}}, {at(t)});')
    add(f'tl.set("#cnum", {{textContent: "{k + 1}"}}, {at(t)});')
abs_sorted = sorted(range(12), key=lambda k: MAP["states"][k]["ab"])
for j, k in enumerate(abs_sorted):
    add(f'tl.fromTo("#ab{j}", {{autoAlpha: 0, y: 10}}, {{autoAlpha: 1, y: 0, duration: 0.25, ease: "expo.out"}}, {at(lit_times[k])});')
add(f'tl.to("#count .cn", {{keyframes: [{{scale: 1.18, duration: 0.08}}, {{scale: 1, duration: 0.45, ease: "expo.out"}}]}}, {at(tw + 0.02)});')

# ---------------- S7: end card ----------------
add(f'tl.fromTo("#kick", {{autoAlpha: 0, y: -30, scale: 1.1}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: "expo.out"}}, {at(W(7, 0) - 0.05)});')
add(f'tl.set("#kick", {{color: "{BRASS}"}}, {at(W(7, 3) - 0.03)});')
add(f'tl.fromTo("#endLogo", {{autoAlpha: 0, scale: 0.86}}, {{autoAlpha: 1, scale: 1, duration: 0.7, ease: "expo.out"}}, {at(S7 - 0.02)});')
add(f'tl.fromTo("#endRule", {{scaleX: 0}}, {{scaleX: 1, duration: 0.6, ease: "expo.out"}}, {at(S7 + 0.25)});')
gq = W(7, 5)
add(f'tl.fromTo("#cta", {{autoAlpha: 0, y: 40, scale: 0.9}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.42, ease: "back.out(1.8)"}}, {at(gq - 0.05)});')
add(f'tl.fromTo("#free", {{autoAlpha: 0, y: 20}}, {{autoAlpha: 1, y: 0, duration: 0.35, ease: "expo.out"}}, {at(W(7, 8) - 0.03)});')
add(f'tl.fromTo("#phone", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.4}}, {at(W(7, 8) + 0.25)});')
add(f'tl.fromTo("#fine", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.4}}, {at(W(7, 8) + 0.45)});')
add(f'tl.to("#cta", {{keyframes: [{{scale: 1.05, duration: 0.25, ease: "sine.out"}}, {{scale: 1, duration: 0.35, ease: "sine.in"}}]}}, {at(W(7, 8) + 0.9)});')

# ---------------- scene camera and whip transitions ----------------
scenes = [("sDesk", 0, S4), ("sCmp", S4, S5), ("sSave", S5, S6), ("sMap", S6, S7), ("sEnd", S7, DUR)]
for i, (sid, a, b) in enumerate(scenes):
    add(f'tl.fromTo("#{sid} .cam", {{scale: 1}}, {{scale: 1.035, duration: {b - a:.3f}, ease: "none"}}, {at(a)});')
    if i > 0:
        add(f'tl.fromTo("#{sid} .cam", {{x: 420}}, {{x: 0, duration: 0.42, ease: "expo.out"}}, {at(a)});')
    if i < len(scenes) - 1:
        add(f'tl.to("#{sid} .cam", {{x: -420, duration: 0.2, ease: "power3.in"}}, {at(b - 0.2)});')

# grain flicker (deterministic)
add(f'tl.fromTo("#grain", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "-{int(DUR * 30) * 37 % 512 + 512}px -{int(DUR * 30) * 53 % 512 + 512}px", duration: {DUR}, ease: "steps({int(DUR * 30)})"}}, 0);')
add(f'tl.fromTo("#glow", {{x: -160, y: 0}}, {{x: 160, y: 120, duration: {DUR}, ease: "sine.inOut"}}, 0);')

def scene(sid, a, b, inner):
    return f'<div class="clip scene" id="{sid}" data-start="{a:.3f}" data-duration="{b - a:.3f}"><div class="cam">{inner}</div></div>'

end_html = ('<div id="kick">YOUR RENEWAL WON&#39;T WAIT</div><img id="endLogo" src="assets/img/logo.svg" alt="The Experts Agency">'
            '<div id="endRule"></div>'
            '<div id="cta">GET A FREE QUOTE</div><div id="free">IT&#39;S FREE</div>'
            '<div id="phone">(929) 675-2948</div>'
            '<div id="fine">Coverage and pricing subject to underwriting and state availability.</div>')

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {ONYX}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {ONYX}; color: {BONE}; font-family: "Archivo", sans-serif; -webkit-font-smoothing: antialiased; }}
#glow {{ position: absolute; left: 90px; top: 380px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(closest-side, rgba(194,162,76,0.16), rgba(194,162,76,0)); }}
#grain {{ position: absolute; inset: 0; background-image: url("assets/img/grain.png"); background-size: 512px 512px; opacity: 0.05; mix-blend-mode: screen; pointer-events: none; z-index: 40; }}
#vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 42%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%); z-index: 39; pointer-events: none; }}
.scene {{ position: absolute; left: 0; top: 110px; width: 1080px; height: 1920px; }}
.cam {{ position: absolute; inset: 0; transform-origin: 540px 700px; }}
#desk {{ position: absolute; inset: 0; }}
.doc {{ position: absolute; left: 260px; top: 300px; width: 560px; height: 760px; padding: 50px 46px; background: {PAPER}; color: {ONYX}; box-shadow: 0 40px 90px rgba(0,0,0,0.65); display: flex; flex-direction: column; gap: 26px; }}
.doc.muted {{ background: #D9D4C8; opacity: 0.92; }}
.dt {{ font-size: 28px; font-weight: 750; letter-spacing: 0.12em; font-stretch: 125%; text-transform: uppercase; }}
.rule {{ height: 3px; background: {ONYX}; }}
.row, .sig {{ display: flex; flex-direction: column; gap: 11px; }}
.lab {{ font-size: 17px; font-weight: 650; letter-spacing: 0.12em; text-transform: uppercase; color: #6B665C; font-stretch: 112%; }}
.doc .bar {{ height: 14px; border-radius: 7px; background: #D6D0C3; }}
.doc.muted .bar {{ background: #C2BCAE; }}
.prem {{ display: flex; justify-content: space-between; align-items: center; border-top: 2px solid #D6D0C3; padding-top: 22px; }}
.pv {{ display: flex; align-items: center; gap: 10px; font-size: 30px; font-weight: 750; }}
.line {{ height: 2px; background: {ONYX}; margin-top: 26px; }}
.stamp {{ position: absolute; left: 545px; top: 820px; width: 240px; height: 240px; border-radius: 50%; border: 8px solid {DEEP}; outline: 2px solid {DEEP}; outline-offset: -20px; color: {DEEP}; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 800; font-size: 46px; line-height: 46px; letter-spacing: 0.06em; font-stretch: 125%; transform-origin: 120px 120px; }}
.vs {{ position: absolute; left: 470px; top: 610px; width: 140px; height: 140px; border-radius: 50%; background: {BRASS}; color: {ONYX}; display: flex; align-items: center; justify-content: center; font-size: 52px; font-weight: 800; font-stretch: 125%; box-shadow: 0 0 0 10px rgba(15,15,15,0.9); }}
.badge {{ position: absolute; left: 340px; top: 250px; width: 400px; height: 190px; display: flex; align-items: center; justify-content: center; }}
.badge img {{ width: 400px; }}
#ring {{ position: absolute; left: 390px; top: 195px; width: 300px; height: 300px; border-radius: 50%; border: 3px solid {BRASS}; opacity: 0; }}
.card {{ position: absolute; top: 380px; width: 440px; height: 590px; padding: 40px 34px; background: #161616; border: 2px solid rgba(247,245,240,0.16); display: flex; flex-direction: column; gap: 30px; }}
#cardL {{ left: 70px; }} #cardR {{ left: 570px; border-color: rgba(194,162,76,0.75); }}
.ch {{ font-size: 30px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; font-stretch: 125%; padding-bottom: 22px; border-bottom: 2px solid rgba(247,245,240,0.2); }}
.card.gold .ch {{ color: {BRASS}; border-color: rgba(194,162,76,0.6); }}
.crow {{ display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 580; }}
.ck {{ width: 38px; height: 38px; flex: none; fill: none; stroke: {BRASS}; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
.ck path {{ stroke-dasharray: 30; }}
.cprem {{ margin-top: auto; display: flex; flex-direction: column; gap: 14px; border-top: 2px solid rgba(247,245,240,0.2); padding-top: 24px; }}
.cprem .lab {{ color: rgba(247,245,240,0.7); }}
.fill {{ height: 54px; border-radius: 6px; background: linear-gradient(90deg, rgba(247,245,240,0.22), rgba(247,245,240,0.08)); transform-origin: 0 50%; }}
.card.gold .fill {{ background: linear-gradient(90deg, rgba(194,162,76,0.85), rgba(194,162,76,0.35)); }}
#midline {{ position: absolute; left: 539px; top: 400px; width: 2px; height: 550px; background: {BRASS}; transform-origin: 50% 50%; }}
.chart {{ position: absolute; left: 190px; top: 340px; width: 700px; height: 720px; display: flex; align-items: flex-end; gap: 90px; padding-left: 40px; }}
.bcol {{ display: flex; flex-direction: column; align-items: center; gap: 22px; width: 200px; }}
.bar2 {{ width: 200px; transform-origin: 50% 100%; }}
.bar2.cur {{ height: 560px; background: linear-gradient(180deg, rgba(247,245,240,0.38), rgba(247,245,240,0.12)); }}
.bar2.ours {{ height: 380px; background: linear-gradient(180deg, {BRASS}, rgba(194,162,76,0.45)); }}
.bl {{ font-size: 26px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; font-stretch: 112%; white-space: nowrap; }}
.bl.gold {{ color: {BRASS}; }}
.gap {{ position: absolute; left: 552px; top: 108px; height: 180px; width: 300px; }}
.gl {{ position: absolute; left: 0; top: 0; width: 26px; height: 180px; border: 3px solid {BRASS}; border-left: none; }}
.gt {{ position: absolute; left: 46px; top: 66px; font-size: 34px; font-weight: 800; color: {BRASS}; letter-spacing: 0.06em; font-stretch: 125%; white-space: nowrap; }}
#docC {{ top: 250px; }}
.lock {{ position: absolute; left: 400px; top: 556px; width: 280px; height: 434px; filter: drop-shadow(0 30px 50px rgba(0,0,0,0.7)); }}
.lock path {{ fill: none; stroke-linecap: round; }}
.lock .so {{ stroke: {ONYX}; stroke-width: 28; }}
.lock .si {{ stroke: #B9B4A8; stroke-width: 18; }}
.lock .lb {{ fill: {BRASS}; }}
.lock .kh {{ fill: {ONYX}; }}
.locklab {{ position: absolute; left: 0; right: 0; top: 1020px; text-align: center; font-size: 40px; font-weight: 800; color: {BRASS}; letter-spacing: 0.14em; font-stretch: 125%; white-space: nowrap; }}
.map {{ position: absolute; left: 40px; top: 430px; width: 1000px; height: 625px; }}
.map .dim {{ fill: #26231D; stroke: {ONYX}; stroke-width: 1.4; stroke-linejoin: round; }}
.map .lit {{ fill: {BRASS}; stroke: {ONYX}; stroke-width: 1.4; stroke-linejoin: round; }}
.count {{ position: absolute; left: 0; right: 0; top: 270px; display: flex; align-items: baseline; justify-content: center; gap: 22px; }}
.cn {{ font-size: 132px; line-height: 132px; font-weight: 650; color: {BRASS}; font-stretch: 112%; min-width: 170px; text-align: right; }}
.cl {{ font-size: 32px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; font-stretch: 125%; }}
.abbr {{ position: absolute; left: 60px; right: 60px; top: 1068px; display: flex; justify-content: center; gap: 18px; font-size: 26px; font-weight: 700; letter-spacing: 0.06em; color: rgba(247,245,240,0.86); }}
#kick {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: 0.08em; font-stretch: 125%; white-space: nowrap; }}
#endLogo {{ position: absolute; left: 230px; top: 470px; width: 620px; }}
#endRule {{ position: absolute; left: 340px; top: 720px; width: 400px; height: 2px; background: rgba(194,162,76,0.6); }}
#cta {{ position: absolute; left: 190px; width: 700px; top: 780px; height: 120px; display: flex; align-items: center; justify-content: center; background: {BRASS}; color: {ONYX}; font-size: 50px; font-weight: 800; letter-spacing: 0.03em; font-stretch: 125%; }}
#free {{ position: absolute; left: 0; right: 0; top: 928px; text-align: center; font-size: 38px; font-weight: 700; letter-spacing: 0.14em; font-stretch: 125%; color: {BRASS}; }}
#phone {{ position: absolute; left: 0; right: 0; top: 1010px; text-align: center; font-size: 40px; font-weight: 650; }}
#fine {{ position: absolute; left: 60px; right: 60px; top: 1130px; text-align: center; font-size: 22px; line-height: 28px; color: rgba(247,245,240,0.66); }}
#caps {{ position: absolute; left: 0; right: 0; top: 1236px; height: 110px; z-index: 30; }}
.cap {{ position: absolute; left: 30px; right: 30px; top: 0; display: flex; justify-content: center; gap: 22px; visibility: hidden; font-size: 66px; line-height: 90px; font-weight: 760; font-stretch: 112%; letter-spacing: 0.01em; text-shadow: 0 6px 24px rgba(0,0,0,0.7); white-space: nowrap; }}
.w {{ display: inline-block; opacity: 0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-motion-blur="on" data-motion-blur-shutter="200">
<div id="glow"></div>
{scene("sDesk", 0, S4, '<div id="desk">' + desk + '<div id="ring"></div></div>')}
{scene("sCmp", S4, S5, cmp_html)}
{scene("sSave", S5, S6, bars + lock)}
{scene("sMap", S6, S7, counter + mapsvg + abbr)}
{scene("sEnd", S7, DUR, end_html)}
<div id="caps">{"".join(cap_html)}</div>
<div id="vig"></div>
<div id="grain"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''
open("index.html", "w").write(html)
print("ok", len(js), "tweens")

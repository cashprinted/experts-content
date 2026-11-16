"""Build index.html for the Experts Agency 'Already have insurance? Perfect.' reel from timing.json."""
import json

L = json.load(open("timing.json"))["lines"]
W = lambda li, wi: L[li]["words"][wi][1]
ONYX, BRASS, DEEP, BONE, PAPER = "#0F0F0F", "#C2A24C", "#8A6F2B", "#F7F5F0", "#F2EFE8"
st = lambda i, pad=0.12: round(L[i]["speech"][0] - pad, 3)
S1, S2, S3, S4, S5, S6, S7 = st(1), st(2), st(3), st(4, 0.1), st(5), st(6, 0.14), st(7, 0.13)
DUR = round(L[7]["speech"][1] + 2.35, 1)
json.dump({"S": [0, S1, S2, S3, S4, S5, S6, S7], "DUR": DUR}, open("scenes.json", "w"))

js = []
def at(t): return f"{t:.3f}"
def add(s): js.append(s)

# ---------------- captions (lines 5 and 7 carry their own type on screen) ----------------
cap_html = []
for li, line in enumerate(L):
    if li in (5, 7): continue
    words = line["words"]; chunks, cur = [], []
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
        t1 = (words[nxt[0]][1] - 0.06) if nxt else min(line["speech"][1] + 0.22, L[li + 1]["speech"][0] - 0.06)
        add(f'tl.set("#{cid}", {{autoAlpha: 1}}, {at(t0)});')
        for k, wi in enumerate(ch):
            ws = words[wi][1]
            add(f'tl.fromTo("#{cid}_{k}", {{opacity: 0, y: 26, scale: 0.92}}, {{opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "expo.out"}}, {at(ws - 0.03)});')
            add(f'tl.set("#{cid}_{k}", {{color: "{BRASS}"}}, {at(ws - 0.03)});')
            nxt_w = words[ch[k + 1]][1] if k + 1 < len(ch) else t1
            add(f'tl.set("#{cid}_{k}", {{color: "{BONE}"}}, {at(nxt_w - 0.03)});')
        add(f'tl.to("#{cid}", {{autoAlpha: 0, y: -14, duration: 0.12, ease: "power2.in"}}, {at(t1 - 0.1)});')

ICON = {
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"></path><path d="M15 18H9"></path><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"></path><circle cx="17" cy="18" r="2"></circle><circle cx="7" cy="18" r="2"></circle>',
    "bld": '<path d="M10 12h4"></path><path d="M10 8h4"></path><path d="M14 21v-3a2 2 0 0 0-4 0v3"></path><path d="M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2"></path><path d="M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"></path>',
    "umb": '<path d="M12 13v7a2 2 0 0 0 4 0"></path><path d="M12 2v2"></path><path d="M20.992 13a1 1 0 0 0 .97-1.274 10.284 10.284 0 0 0-19.923 0A1 1 0 0 0 3 13z"></path>',
    "brf": '<path d="M12 12h.01"></path><path d="M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"></path><path d="M22 13a18.15 18.15 0 0 1-20 0"></path><rect width="20" height="14" x="2" y="6" rx="2"></rect>',
}
def icon(k, cls="ic"): return f'<svg class="{cls}" viewBox="0 0 24 24">{ICON[k]}</svg>'
CHECK = '<svg class="chk" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"></path></svg>'

# ---------------- S0: hook, the policy card ----------------
pc = ('<div id="pcard"><div class="pc-top"><div><div class="pc-k">Commercial policy</div><div class="pc-t">STATUS: ACTIVE</div></div>'
      + icon("car", "pc-ic") + '</div>'
      + "".join(f'<div class="pc-row"><span>{a}</span><i style="width:{w}px"></i></div>' for a, w in [("Policy no.", 220), ("Effective", 180), ("Premium", 150)])
      + f'<div id="okBadge">{CHECK}</div></div>')
add('tl.fromTo("#pcard", {x: 40, y: -60, scale: 1.5, rotation: -11}, {x: 0, y: 0, scale: 1, rotation: -3, duration: 0.55, ease: "expo.out"}, 0);')
add(f'tl.to("#pcard", {{rotation: -1.5, y: -12, duration: {S1 - 0.55:.2f}, ease: "sine.inOut"}}, 0.55);')
pf = W(0, 3)
add(f'tl.fromTo("#okBadge", {{autoAlpha: 0, scale: 2.2, rotation: -30}}, {{autoAlpha: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2)"}}, {at(pf - 0.08)});')
add(f'tl.fromTo("#okBadge .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.25, ease: "power2.out"}}, {at(pf + 0.05)});')

# ---------------- S1: years roll back ----------------
years = "".join(f'<div class="yr">{y}</div>' for y in range(2026, 2019, -1))
yrs = f'<div id="yLab">LAST TIME IT WAS SHOPPED</div><div id="yWin"><div id="yStrip">{years}</div></div><div id="yQ">?</div>'
y0, y1 = W(1, 2), W(1, 7)
add(f'tl.fromTo("#yLab", {{autoAlpha: 0, y: 20}}, {{autoAlpha: 1, y: 0, duration: 0.4, ease: "expo.out"}}, {at(S1 + 0.1)});')
add(f'tl.fromTo("#yWin", {{autoAlpha: 0, scale: 0.85}}, {{autoAlpha: 1, scale: 1, duration: 0.45, ease: "expo.out"}}, {at(S1 + 0.05)});')
year_steps = [y0 + k * (y1 - y0) / 6 for k in range(1, 7)]
for k, t in enumerate(year_steps):
    add(f'tl.to("#yStrip", {{y: {-(k + 1) * 280}, duration: 0.24, ease: "power3.out"}}, {at(t - 0.12)});')
q = W(1, 9)
add(f'tl.to("#yWin", {{opacity: 0.3, x: -110, scale: 0.9, duration: 0.35, ease: "expo.out"}}, {at(q - 0.05)});')
add(f'tl.fromTo("#yQ", {{autoAlpha: 0, scale: 2.4}}, {{autoAlpha: 1, scale: 1, duration: 0.28, ease: "power4.out"}}, {at(q - 0.06)});')

# ---------------- S2: auto-renew and the bills ----------------
renew = ('<div id="rPanel"><div class="rp-h">YOUR POLICY</div>'
         '<div class="rp-row"><span>Auto-renew</span><div id="tg"><div id="tgK"></div></div></div>'
         '<div id="rBadge">RATE UPDATED</div></div>'
         + "".join(f'<div class="bill" id="bill{k}"><div><div class="b-k">Renewal premium</div><div class="b-m">{m}</div></div><i></i><div class="paid" id="paid{k}">PAID</div></div>'
                   for k, m in enumerate(["YEAR 1", "YEAR 2", "YEAR 3"])))
add(f'tl.fromTo("#rPanel", {{autoAlpha: 0, y: 60}}, {{autoAlpha: 1, y: 0, duration: 0.5, ease: "expo.out"}}, {at(S2 + 0.02)});')
add(f'tl.fromTo("#rBadge", {{autoAlpha: 0, scale: 0.5}}, {{autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)"}}, {at(W(2, 1) - 0.05)});')
tgt = W(2, 3)
add(f'tl.to("#tgK", {{x: 72, duration: 0.18, ease: "power3.out"}}, {at(tgt - 0.02)});')
add(f'tl.to("#tg", {{backgroundColor: "{BRASS}", duration: 0.18}}, {at(tgt - 0.02)});')
kp = W(2, 5)
add(f'tl.to("#rPanel", {{y: -250, scale: 0.8, autoAlpha: 0.0, duration: 0.4, ease: "power3.in"}}, {at(kp - 0.25)});')
pay_t = [W(2, 7) - 0.04, W(2, 8) - 0.02, W(2, 8) + 0.24]
for k in range(3):
    add(f'tl.fromTo("#bill{k}", {{autoAlpha: 0, y: 140, rotation: {(-1) ** k * 4}}}, {{autoAlpha: 1, y: 0, rotation: {(-1) ** k * 1.5}, duration: 0.4, ease: "expo.out"}}, {at(kp - 0.05 + k * 0.12)});')
    add(f'tl.fromTo("#paid{k}", {{autoAlpha: 0, scale: 2.2}}, {{autoAlpha: 1, scale: 1, duration: 0.12, ease: "power4.in"}}, {at(pay_t[k] - 0.1)});')

# ---------------- S3: send the declarations page ----------------
def doc(id_, title, rows):
    bars = "".join(f'<div class="row" id="{id_}r{k}"><div class="lab">{r}</div><div class="bar" style="width:{w}%"></div></div>' for k, (r, w) in enumerate(rows))
    return (f'<div class="doc" id="{id_}"><div class="dt">{title}</div><div class="rule"></div>{bars}'
            f'<div class="prem"><div class="lab">Total premium</div><div class="pv">$<span class="bar" style="width:150px"></span></div></div></div>')
rows = [("Named insured", 74), ("Policy period", 56), ("Coverages and limits", 86)]
send = doc("docA", "Declarations page", rows) + '<div class="badge" id="badge"><img src="assets/img/logo.svg" alt=""></div><div id="ring"></div>'
add(f'tl.fromTo("#docA", {{autoAlpha: 0, y: 260, rotation: 6, scale: 0.8}}, {{autoAlpha: 1, y: 150, rotation: -2, scale: 0.8, duration: 0.55, ease: "expo.out"}}, {at(S3 + 0.02)});')
add(f'tl.fromTo("#badge", {{autoAlpha: 0, scale: 0.6, y: 30}}, {{autoAlpha: 1, scale: 1, y: 0, duration: 0.45, ease: "expo.out"}}, {at(S3 + 0.1)});')
pg = W(3, 4)
add(f'tl.to("#docA", {{y: -330, scale: 0.12, rotation: 8, autoAlpha: 0, duration: 0.42, ease: "power3.in"}}, {at(pg - 0.12)});')
add(f'tl.to("#badge", {{keyframes: [{{scale: 1.12, duration: 0.09, ease: "power2.out"}}, {{scale: 1, duration: 0.35, ease: "expo.out"}}]}}, {at(pg + 0.3)});')
add(f'tl.fromTo("#ring", {{autoAlpha: 0.9, scale: 0.6}}, {{autoAlpha: 0, scale: 1.9, duration: 0.7, ease: "expo.out", immediateRender: false}}, {at(pg + 0.3)});')

# ---------------- S4: shop it, what you could save ----------------
shop = (doc("docB", "Declarations page", rows) + '<div id="scan"></div>'
        + "".join(f'<div class="rck" id="rck{k}">{CHECK}</div>' for k in range(3))
        + '<div id="saveTag"><div class="st-k">WHAT YOU COULD SAVE</div><div class="st-v">$<i></i></div></div>')
add(f'tl.fromTo("#docB", {{autoAlpha: 0, x: -200, rotation: -6}}, {{autoAlpha: 1, x: -110, rotation: -2, duration: 0.55, ease: "expo.out"}}, {at(S4)});')
sh = W(4, 1)
add(f'tl.fromTo("#scan", {{autoAlpha: 0, y: 0}}, {{autoAlpha: 1, y: 0, duration: 0.1}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{y: 560, duration: 1.1, ease: "power1.inOut"}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{autoAlpha: 0, duration: 0.15}}, {at(sh + 1.05)});')
for k in range(3):
    add(f'tl.fromTo("#rck{k}", {{autoAlpha: 0, scale: 0.4}}, {{autoAlpha: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)"}}, {at(sh + 0.25 + k * 0.28)});')
    add(f'tl.fromTo("#rck{k} .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.22, ease: "power2.out"}}, {at(sh + 0.3 + k * 0.28)});')
sv = W(4, 10)
add(f'tl.fromTo("#saveTag", {{autoAlpha: 0, x: -120, rotation: 0}}, {{autoAlpha: 1, x: 0, rotation: 4, duration: 0.45, ease: "expo.out"}}, {at(sv - 0.08)});')
add(f'tl.fromTo("#saveTag i", {{backgroundPosition: "-300px 0px"}}, {{backgroundPosition: "300px 0px", duration: 1.2, ease: "none"}}, {at(sv)});')

# ---------------- S5: lines we write ----------------
cov = [("car", "Auto", W(5, 0)), ("truck", "Trucking", W(5, 1)), ("bld", "General liability", W(5, 2)), ("umb", "Umbrella", W(5, 4)), ("brf", "Business", W(5, 5))]
lines_html = "".join(f'<div class="cv" id="cv{k}">{icon(ic)}<span>{t}</span></div>' for k, (ic, t, _) in enumerate(cov))
for k, (_, _, t) in enumerate(cov):
    add(f'tl.fromTo("#cv{k}", {{autoAlpha: 0, x: 40}}, {{autoAlpha: 0.16, x: 0, duration: 0.12, ease: "power2.out"}}, {at(S5 + k * 0.02)});')
    lt = max(t - 0.06, S5 + 0.14 + k * 0.02)
    add(f'tl.to("#cv{k}", {{opacity: 1, duration: 0.18, ease: "power2.out"}}, {at(lt)});')
    add(f'tl.fromTo("#cv{k} .ic", {{scale: 1}}, {{keyframes: [{{scale: 1.3, duration: 0.08}}, {{scale: 1, duration: 0.35, ease: "expo.out"}}]}}, {at(lt)});')
    add(f'tl.set("#cv{k}", {{color: "{BRASS}"}}, {at(t - 0.06)});')
    if k: add(f'tl.set("#cv{k - 1}", {{color: "{BONE}"}}, {at(t - 0.06)});')
add(f'tl.set("#cv4", {{color: "{BONE}"}}, {at(L[5]["speech"][1] + 0.1)});')

# ---------------- S6: every month you wait ----------------
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
grid = '<div id="mGrid">' + "".join(f'<div class="mt" id="mt{k}">{m}</div>' for k, m in enumerate(months)) + '</div><div id="mLab">STILL AT YOUR OLD RATE</div>'
m0, m1 = S6 + 0.45, W(6, 9) - 0.15
mt_times = [m0 + k * (m1 - m0) / 11 for k in range(12)]
for k, t in enumerate(mt_times):
    add(f'tl.fromTo("#mt{k}", {{autoAlpha: 0, y: 30}}, {{autoAlpha: 0.22, y: 0, duration: 0.25, ease: "expo.out"}}, {at(S6 + 0.02 + k * 0.012)});')
    add(f'tl.to("#mt{k}", {{keyframes: [{{opacity: 1, scaleY: 0.15, duration: 0.07, ease: "power2.in"}}, {{scaleY: 1, duration: 0.2, ease: "expo.out"}}]}}, {at(t)});')
old = W(6, 9)
add(f'tl.to(".mt", {{backgroundColor: "rgba(194,162,76,0.9)", color: "{ONYX}", duration: 0.2, stagger: 0.015}}, {at(old - 0.06)});')
add(f'tl.fromTo("#mLab", {{autoAlpha: 0, y: 30}}, {{autoAlpha: 1, y: 0, duration: 0.4, ease: "expo.out"}}, {at(old - 0.04)});')
add(f'tl.to("#mGrid", {{keyframes: [{{scale: 1.04, duration: 0.07}}, {{scale: 1, duration: 0.4, ease: "expo.out"}}]}}, {at(old)});')

# ---------------- S7: end card ----------------
end_html = ('<div id="kick">STILL ON YOUR OLD RATE?</div><img id="endLogo" src="assets/img/logo.svg" alt="The Experts Agency">'
            '<div id="endRule"></div><div id="cta">GET A FREE QUOTE</div><div id="free">IT&#39;S FREE</div>'
            '<div id="phone">(929) 675-2948</div><div id="fine">Coverage and pricing subject to underwriting and state availability.</div>')
add(f'tl.fromTo("#kick", {{autoAlpha: 0, y: -30, scale: 1.1}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: "expo.out"}}, {at(S7)});')
add(f'tl.fromTo("#endLogo", {{autoAlpha: 0, scale: 0.86}}, {{autoAlpha: 1, scale: 1, duration: 0.7, ease: "expo.out"}}, {at(S7 + 0.05)});')
add(f'tl.fromTo("#endRule", {{scaleX: 0}}, {{scaleX: 1, duration: 0.6, ease: "expo.out"}}, {at(S7 + 0.3)});')
gq = W(7, 1)
add(f'tl.fromTo("#cta", {{autoAlpha: 0, y: 40, scale: 0.9}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.42, ease: "back.out(1.8)"}}, {at(gq - 0.05)});')
fr = W(7, 4)
add(f'tl.fromTo("#free", {{autoAlpha: 0, y: 20}}, {{autoAlpha: 1, y: 0, duration: 0.35, ease: "expo.out"}}, {at(fr - 0.03)});')
add(f'tl.set("#kick", {{color: "{BRASS}"}}, {at(fr - 0.03)});')
add(f'tl.fromTo("#phone", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.4}}, {at(fr + 0.3)});')
add(f'tl.fromTo("#fine", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.4}}, {at(fr + 0.5)});')
add(f'tl.to("#cta", {{keyframes: [{{scale: 1.05, duration: 0.25, ease: "sine.out"}}, {{scale: 1, duration: 0.35, ease: "sine.in"}}]}}, {at(fr + 1.0)});')

# ---------------- camera, whips, texture ----------------
bounds = [0, S1, S2, S3, S4, S5, S6, S7, DUR]
ids = ["sHook", "sYears", "sRenew", "sSend", "sShop", "sCov", "sMonths", "sEnd"]
for i, sid in enumerate(ids):
    a, b = bounds[i], bounds[i + 1]
    add(f'tl.fromTo("#{sid} .cam", {{scale: 1}}, {{scale: 1.035, duration: {b - a:.3f}, ease: "none"}}, {at(a)});')
    if i > 0: add(f'tl.fromTo("#{sid} .cam", {{x: 420}}, {{x: 0, duration: 0.42, ease: "expo.out"}}, {at(a)});')
    if i < len(ids) - 1: add(f'tl.to("#{sid} .cam", {{x: -420, duration: 0.2, ease: "power3.in"}}, {at(b - 0.2)});')
add(f'tl.fromTo("#grain", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "-{int(DUR * 30) * 37 % 512 + 512}px -{int(DUR * 30) * 53 % 512 + 512}px", duration: {DUR}, ease: "steps({int(DUR * 30)})"}}, 0);')
add(f'tl.fromTo("#glow", {{x: -160, y: 0}}, {{x: 160, y: 120, duration: {DUR}, ease: "sine.inOut"}}, 0);')

def scene(i, inner):
    a, b = bounds[i], bounds[i + 1]
    return f'<div class="clip scene" id="{ids[i]}" data-start="{a:.3f}" data-duration="{b - a:.3f}"><div class="cam">{inner}</div></div>'

css = f'''
@font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {ONYX}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {ONYX}; color: {BONE}; font-family: "Archivo", sans-serif; -webkit-font-smoothing: antialiased; }}
#glow {{ position: absolute; left: 90px; top: 380px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(closest-side, rgba(194,162,76,0.16), rgba(194,162,76,0)); }}
#grain {{ position: absolute; inset: 0; background-image: url("assets/img/grain.png"); background-size: 512px 512px; opacity: 0.05; mix-blend-mode: screen; pointer-events: none; z-index: 40; }}
#vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 42%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%); z-index: 39; pointer-events: none; }}
.scene {{ position: absolute; left: 0; top: 110px; width: 1080px; height: 1920px; }}
.cam {{ position: absolute; inset: 0; transform-origin: 540px 700px; }}
.chk {{ fill: none; stroke: {ONYX}; stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }}
.chk path {{ stroke-dasharray: 30; }}
#pcard {{ position: absolute; left: 150px; top: 380px; width: 780px; height: 480px; padding: 48px 52px; border-radius: 26px; background: linear-gradient(145deg, #1F1E1B, #121212); border: 2px solid rgba(194,162,76,0.7); box-shadow: 0 50px 100px rgba(0,0,0,0.7); display: flex; flex-direction: column; gap: 30px; }}
.pc-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
.pc-k {{ font-size: 22px; font-weight: 650; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(247,245,240,0.6); font-stretch: 112%; }}
.pc-t {{ margin-top: 10px; font-size: 44px; font-weight: 780; letter-spacing: 0.04em; font-stretch: 125%; color: {BRASS}; }}
.pc-ic {{ width: 76px; height: 76px; fill: none; stroke: {BRASS}; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }}
.pc-row {{ display: flex; align-items: center; justify-content: space-between; font-size: 24px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(247,245,240,0.75); border-top: 1px solid rgba(247,245,240,0.14); padding-top: 22px; }}
.pc-row i {{ display: block; height: 14px; border-radius: 7px; background: rgba(247,245,240,0.2); }}
#okBadge {{ position: absolute; right: -44px; top: -44px; width: 132px; height: 132px; border-radius: 50%; background: {BRASS}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 10px {ONYX}; }}
#okBadge .chk {{ width: 74px; height: 74px; }}
#yLab {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 34px; font-weight: 700; letter-spacing: 0.14em; font-stretch: 125%; color: {BRASS}; }}
#yWin {{ position: absolute; left: 140px; width: 800px; top: 430px; height: 280px; overflow: hidden; }}
.yr {{ height: 280px; line-height: 280px; text-align: center; font-size: 250px; font-weight: 650; font-stretch: 112%; letter-spacing: -0.01em; }}
#yQ {{ position: absolute; left: 770px; width: 220px; top: 410px; text-align: center; font-size: 320px; line-height: 320px; font-weight: 700; color: {BRASS}; }}
#rPanel {{ position: absolute; left: 170px; top: 400px; width: 740px; padding: 44px 48px; border-radius: 26px; background: #171717; border: 2px solid rgba(247,245,240,0.16); display: flex; flex-direction: column; gap: 34px; }}
.rp-h {{ font-size: 26px; font-weight: 700; letter-spacing: 0.14em; color: rgba(247,245,240,0.6); font-stretch: 125%; }}
.rp-row {{ display: flex; align-items: center; justify-content: space-between; font-size: 46px; font-weight: 650; }}
#tg {{ width: 148px; height: 76px; border-radius: 38px; background: #3A3833; padding: 6px; }}
#tgK {{ width: 64px; height: 64px; border-radius: 50%; background: {BONE}; }}
#rBadge {{ align-self: flex-start; padding: 12px 22px; border-radius: 10px; background: rgba(194,162,76,0.16); border: 2px solid {BRASS}; color: {BRASS}; font-size: 26px; font-weight: 800; letter-spacing: 0.1em; font-stretch: 125%; }}
.bill {{ position: absolute; left: 190px; width: 700px; height: 170px; padding: 0 44px; border-radius: 18px; background: {PAPER}; color: {ONYX}; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 30px 60px rgba(0,0,0,0.6); }}
#bill0 {{ top: 330px; }} #bill1 {{ top: 530px; }} #bill2 {{ top: 730px; }}
.b-k {{ font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #6B665C; }}
.b-m {{ margin-top: 8px; font-size: 40px; font-weight: 800; font-stretch: 125%; }}
.bill i {{ display: block; width: 150px; height: 16px; border-radius: 8px; background: #D6D0C3; margin-right: 140px; }}
.paid {{ position: absolute; right: 30px; top: 34px; padding: 10px 18px; border: 5px solid {DEEP}; border-radius: 10px; color: {DEEP}; font-size: 40px; font-weight: 800; letter-spacing: 0.1em; font-stretch: 125%; transform: rotate(-10deg); }}
.doc {{ position: absolute; left: 260px; top: 260px; width: 560px; height: 700px; padding: 50px 46px; background: {PAPER}; color: {ONYX}; box-shadow: 0 40px 90px rgba(0,0,0,0.65); display: flex; flex-direction: column; gap: 30px; }}
.dt {{ font-size: 28px; font-weight: 750; letter-spacing: 0.1em; font-stretch: 125%; text-transform: uppercase; }}
.rule {{ height: 3px; background: {ONYX}; }}
.row {{ display: flex; flex-direction: column; gap: 11px; }}
.lab {{ font-size: 17px; font-weight: 650; letter-spacing: 0.12em; text-transform: uppercase; color: #6B665C; font-stretch: 112%; }}
.doc .bar {{ height: 14px; border-radius: 7px; background: #D6D0C3; }}
.prem {{ display: flex; justify-content: space-between; align-items: center; border-top: 2px solid #D6D0C3; padding-top: 22px; margin-top: auto; }}
.pv {{ display: flex; align-items: center; gap: 10px; font-size: 30px; font-weight: 750; }}
.badge {{ position: absolute; left: 340px; top: 250px; width: 400px; height: 190px; display: flex; align-items: center; justify-content: center; }}
.badge img {{ width: 400px; }}
#ring {{ position: absolute; left: 390px; top: 195px; width: 300px; height: 300px; border-radius: 50%; border: 3px solid {BRASS}; opacity: 0; }}
#scan {{ position: absolute; left: 130px; top: 300px; width: 600px; height: 6px; background: {BRASS}; box-shadow: 0 0 30px 8px rgba(194,162,76,0.55); }}
.rck {{ position: absolute; left: 676px; width: 56px; height: 56px; border-radius: 50%; background: {BRASS}; display: flex; align-items: center; justify-content: center; }}
.rck .chk {{ width: 32px; height: 32px; }}
#rck0 {{ top: 392px; }} #rck1 {{ top: 482px; }} #rck2 {{ top: 572px; }}
#saveTag {{ position: absolute; left: 520px; top: 760px; width: 500px; padding: 30px 34px; border-radius: 18px; background: {BRASS}; color: {ONYX}; box-shadow: 0 30px 70px rgba(0,0,0,0.6); }}
.st-k {{ font-size: 24px; font-weight: 800; letter-spacing: 0.08em; font-stretch: 125%; }}
.st-v {{ margin-top: 14px; display: flex; align-items: center; gap: 12px; font-size: 54px; font-weight: 800; }}
.st-v i {{ display: block; width: 250px; height: 30px; border-radius: 15px; background: linear-gradient(90deg, rgba(15,15,15,0.25) 0%, rgba(15,15,15,0.55) 50%, rgba(15,15,15,0.25) 100%); background-size: 300px 30px; }}
.cv {{ position: absolute; left: 116px; display: flex; align-items: center; gap: 30px; font-size: 58px; font-weight: 760; font-stretch: 118%; letter-spacing: 0.01em; text-transform: uppercase; white-space: nowrap; }}
.cv .ic {{ width: 78px; height: 78px; flex: none; fill: none; stroke: {BRASS}; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
#cv0 {{ top: 360px; }} #cv1 {{ top: 490px; }} #cv2 {{ top: 620px; }} #cv3 {{ top: 750px; }} #cv4 {{ top: 880px; }}
#mGrid {{ position: absolute; left: 110px; top: 360px; width: 860px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }}
.mt {{ height: 130px; border-radius: 14px; border: 2px solid rgba(194,162,76,0.55); background: rgba(247,245,240,0.05); display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: 750; letter-spacing: 0.08em; font-stretch: 125%; }}
#mLab {{ position: absolute; left: 0; right: 0; top: 860px; text-align: center; font-size: 46px; font-weight: 800; letter-spacing: 0.06em; font-stretch: 125%; color: {BRASS}; white-space: nowrap; }}
#kick {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 46px; font-weight: 800; letter-spacing: 0.06em; font-stretch: 125%; white-space: nowrap; }}
#endLogo {{ position: absolute; left: 230px; top: 470px; width: 620px; }}
#endRule {{ position: absolute; left: 340px; top: 720px; width: 400px; height: 2px; background: rgba(194,162,76,0.6); }}
#cta {{ position: absolute; left: 190px; width: 700px; top: 780px; height: 120px; display: flex; align-items: center; justify-content: center; background: {BRASS}; color: {ONYX}; font-size: 50px; font-weight: 800; letter-spacing: 0.03em; font-stretch: 125%; }}
#free {{ position: absolute; left: 0; right: 0; top: 928px; text-align: center; font-size: 38px; font-weight: 700; letter-spacing: 0.14em; font-stretch: 125%; color: {BRASS}; }}
#phone {{ position: absolute; left: 0; right: 0; top: 1010px; text-align: center; font-size: 40px; font-weight: 650; }}
#fine {{ position: absolute; left: 60px; right: 60px; top: 1130px; text-align: center; font-size: 22px; line-height: 28px; color: rgba(247,245,240,0.66); }}
#caps {{ position: absolute; left: 0; right: 0; top: 1236px; height: 110px; z-index: 30; }}
.cap {{ position: absolute; left: 30px; right: 30px; top: 0; display: flex; justify-content: center; gap: 22px; visibility: hidden; font-size: 66px; line-height: 90px; font-weight: 760; font-stretch: 112%; letter-spacing: 0.01em; text-shadow: 0 6px 24px rgba(0,0,0,0.7); white-space: nowrap; }}
.w {{ display: inline-block; opacity: 0; }}
'''

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-motion-blur="on" data-motion-blur-shutter="200">
<div id="glow"></div>
{scene(0, pc)}
{scene(1, yrs)}
{scene(2, renew)}
{scene(3, send)}
{scene(4, shop)}
{scene(5, lines_html)}
{scene(6, grid)}
{scene(7, end_html)}
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
print("ok", len(js), "tweens", "DUR", DUR, "scenes", bounds)

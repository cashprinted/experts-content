"""Build index.html for 'Already insured' v3 (the 16 s cut) from timing_<V>.json.

    python3 build.py A|B

v3 changes, from the motion-reel studio rules and the hook-writer / reels-script skills:
  * the hook fires on three channels in frame 0: a moving card, the spoken line, and a full on-screen headline
    that works muted (it is on screen before the voice says it, and lights word by word as it is spoken);
  * every cut is on the measured beat grid, and its first frame shows the new image (no fade from black):
    the main object of each scene is visible on the cut and arrives with a punch-in (scale 1.10 -> 1);
  * secondary objects enter with direction and weight, not a plain fade;
  * camera shake on three hits only (the price, the last PAID, the old-rate lock);
  * every accent is registered in HITS, which drives both the sound effects and the sync check.
Writes index.html and hits_<V>.json.
"""
import json, sys

V = sys.argv[1]
T = json.load(open(f"timing_{V}.json"))
L = {l["i"]: l for l in T["lines"]}
HOOK = 0 if V == "A" else 1
W = lambda li, wi: L[li]["words"][wi][1]
ONYX, BRASS, DEEP, BONE, PAPER = "#0F0F0F", "#C2A24C", "#8A6F2B", "#F7F5F0", "#F2EFE8"
CUTS, DUR = T["cuts"], T["dur"]
S0, S1, S2, S3, S4, S5 = CUTS
js, HITS = [], []
at = lambda t: f"{t:.3f}"
add = js.append


def hit(t, label, lib=None, synth=None):
    """lib: (name, dB, bus) from the ElevenLabs library; synth: (motion-reel sfx name, opts)."""
    HITS.append({"t": round(t, 3), "label": label, "lib": lib, "synth": synth})


def shake(sel, t, amp=14, n=6):
    ks = ", ".join(f'{{x: {amp * (1 - k / n) * (1 if k % 2 else -1):.1f}, y: {amp * 0.5 * (1 - k / n) * (-1 if k % 3 else 1):.1f}, duration: 0.035}}' for k in range(n))
    add(f'tl.to("{sel}", {{keyframes: [{ks}, {{x: 0, y: 0, duration: 0.05}}]}}, {at(t)});')


# ---------------- captions for the body lines (hook and end card carry their own type) ----------------
cap_html = []
for li in (2, 3, 4, 5):
    line, nxt_line = L[li], L[li + 1]
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
        nx = chunks[ci + 1] if ci + 1 < len(chunks) else None
        t1 = (words[nx[0]][1] - 0.06) if nx else min(line["speech"][1] + 0.2, nxt_line["speech"][0] - 0.12)
        add(f'tl.set("#{cid}", {{autoAlpha: 1}}, {at(t0)});')
        for k, wi in enumerate(ch):
            ws = words[wi][1]
            add(f'tl.fromTo("#{cid}_{k}", {{opacity: 0, y: 26, scale: 0.92}}, {{opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "expo.out"}}, {at(ws - 0.03)});')
            add(f'tl.set("#{cid}_{k}", {{color: "{BRASS}"}}, {at(ws - 0.03)});')
            nw = words[ch[k + 1]][1] if k + 1 < len(ch) else t1
            add(f'tl.set("#{cid}_{k}", {{color: "{BONE}"}}, {at(nw - 0.03)});')
        add(f'tl.to("#{cid}", {{autoAlpha: 0, y: -14, duration: 0.1, ease: "power2.in"}}, {at(t1 - 0.08)});')

ICON = {
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle>',
}
CHECK = '<svg class="chk" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"></path></svg>'

# ---------------- S0: hook (headline on screen in frame 0 + the policy card) ----------------
HL = {"A": [("YOUR INSURANCE", "RENEWED ITSELF.", [0, 1], [2, 3]), ("DID ANYONE", "CHECK THE PRICE?", [4, 5], [6, 7, 8])],
      "B": [("ALREADY", "INSURED?", [0], [1]), ("YOU COULD STILL", "BE OVERPAYING.", [2, 3, 4], [5, 6])]}[V]
hl_html = ""
for h, (a, b, wa, wb) in enumerate(HL):
    spans = []
    for row, (txt, idx) in enumerate(((a, wa), (b, wb))):
        ws = txt.split(" ")
        spans.append('<div class="hlr">' + "".join(f'<span id="h{h}_{row}_{k}">{w}</span>' for k, w in enumerate(ws)) + "</div>")
    hl_html += f'<div class="hl" id="hl{h}">{"".join(spans)}</div>'
# headline 0 is on screen at frame 0 (muted viewers read it before the voice), rises slightly; words light as spoken
add('tl.fromTo("#hl0", {y: 36, scale: 1.06}, {y: 0, scale: 1, duration: 0.5, ease: "expo.out"}, 0);')
add('tl.set("#hl1", {autoAlpha: 0}, 0);')
for h, (a, b, wa, wb) in enumerate(HL):
    for row, (txt, idx) in enumerate(((a, wa), (b, wb))):
        for k, wi in enumerate(idx):
            add(f'tl.set("#h{h}_{row}_{k}", {{color: "{BRASS}"}}, {at(W(HOOK, wi) - 0.03)});')
swap = W(HOOK, HL[1][2][0]) - 0.12
add(f'tl.to("#hl0", {{y: -70, autoAlpha: 0, duration: 0.16, ease: "power3.in"}}, {at(swap - 0.06)});')
add(f'tl.fromTo("#hl1", {{autoAlpha: 1, y: 80, scale: 1.08}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: "expo.out", immediateRender: false}}, {at(swap + 0.08)});')
hit(swap + 0.08, "headline 2", ("whoosh", -16, "fx"), ("click", {"gain": 0.2}))

pc = ('<div id="pcard"><div class="pc-top"><div><div class="pc-k">Commercial policy</div><div class="pc-t">STATUS: ACTIVE</div></div>'
      f'<svg class="pc-ic" viewBox="0 0 24 24">{ICON["car"]}</svg></div>'
      '<div class="pc-row"><span>Policy no.</span><i style="width:220px"></i></div>'
      '<div class="pc-row"><span>Auto-renew</span><div id="tg"><div id="tgK"></div></div></div>'
      '<div class="pc-row" id="premRow"><span>Premium</span><i id="premBar" style="width:150px"></i></div>'
      f'<div id="okBadge">{CHECK}</div><div id="stampR">RENEWED</div><div id="qBadge">?</div></div>')
add('tl.fromTo("#pcard", {x: 60, y: 170, scale: 1.4, rotation: -12}, {x: 0, y: 0, scale: 1, rotation: -3, duration: 0.5, ease: "expo.out"}, 0);')
add(f'tl.to("#pcard", {{rotation: -1.5, y: -10, duration: {S1 - 0.5:.2f}, ease: "sine.inOut"}}, 0.5);')
hit(0.0, "card lands", ("impact", -8, "hero"), ("whoosh", {"gain": 0.25, "from": 3000, "to": 300}))
if V == "A":
    tg = W(0, 2)
    add(f'tl.to("#tgK", {{x: 72, duration: 0.14, ease: "power3.out"}}, {at(tg - 0.02)});')
    add(f'tl.to("#tg", {{backgroundColor: "{BRASS}", duration: 0.14}}, {at(tg - 0.02)});')
    hit(tg - 0.02, "auto-renew on", ("tick", -6, "fx"), ("click", {}))
    st = W(0, 3)
    add(f'tl.fromTo("#stampR", {{autoAlpha: 0, scale: 2.4, rotation: -4}}, {{autoAlpha: 1, scale: 1, rotation: -12, duration: 0.13, ease: "power4.in"}}, {at(st - 0.1)});')
    hit(st + 0.03, "RENEWED stamp", ("stamp", -5, "hero"), ("thud", {"gain": 0.35}))
    q = W(0, 8)
else:
    ok = W(1, 1)
    add(f'tl.fromTo("#okBadge", {{autoAlpha: 0, scale: 2.2, rotation: -30}}, {{autoAlpha: 1, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(2)"}}, {at(ok - 0.1)});')
    add(f'tl.fromTo("#okBadge .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.22, ease: "power2.out"}}, {at(ok)});')
    hit(ok - 0.02, "insured check", ("pop", -6, "fx"), ("pop", {"gain": 0.25}))
    q = W(1, 6)
# the price: premium bar inflates and turns brass, "?" badge slams, camera pushes toward it, shake
add(f'tl.to("#premBar", {{width: 430, backgroundColor: "{BRASS}", duration: 0.32, ease: "expo.out"}}, {at(q - 0.06)});')
add(f'tl.fromTo("#qBadge", {{autoAlpha: 0, scale: 2.6}}, {{autoAlpha: 1, scale: 1, duration: 0.16, ease: "power4.in"}}, {at(q - 0.06)});')
add(f'tl.to("#sHook .cam", {{scale: 1.08, y: 40, duration: {S1 - q + 0.06:.3f}, ease: "power2.out"}}, {at(q - 0.06)});')
shake("#sHook .shk", q + 0.1, 16)
hit(q + 0.1, "price ?", ("impact", -12, "hero"), ("sub", {"gain": 0.45, "len": 0.5}))

# ---------------- S1 (the drop): rate updated, bills roll in, PAID x3 ----------------
renew = ('<div id="rPanel"><div class="rp-h">RENEWAL NOTICE</div><div class="rp-row"><span>Your rate</span><i></i></div>'
         '<div id="rBadge">RATE UPDATED</div></div>'
         + "".join(f'<div class="bill" id="bill{k}"><div><div class="b-k">Renewal premium</div><div class="b-m">{m}</div></div><i></i><div class="paid" id="paid{k}">PAID</div></div>'
                   for k, m in enumerate(["YEAR 1", "YEAR 2", "YEAR 3"])))
add(f'tl.set(".bill", {{autoAlpha: 0}}, 0);')
add(f'tl.fromTo("#rBadge", {{autoAlpha: 0, scale: 0.4, rotation: -8}}, {{autoAlpha: 1, scale: 1, rotation: 0, duration: 0.26, ease: "back.out(2.6)"}}, {at(W(2, 1) - 0.06)});')
hit(W(2, 1) - 0.02, "rate updated", ("pop", -10, "fx"), ("blip", {"gain": 0.18, "pitch": "A5"}))
ro = W(2, 2)
add(f'tl.to("#rPanel", {{y: -300, scale: 0.78, rotation: -4, autoAlpha: 0, duration: 0.34, ease: "power3.in"}}, {at(ro - 0.2)});')
hit(ro - 0.05, "panel out", ("swipe", -12, "fx"), None)
for k in range(3):
    add(f'tl.fromTo("#bill{k}", {{autoAlpha: 1, y: 900, rotation: {(-1) ** k * 7}}}, {{autoAlpha: 1, y: 0, rotation: {(-1) ** k * 1.5}, duration: 0.42, ease: "expo.out", immediateRender: false}}, {at(ro - 0.06 + k * 0.13)});')
pay = [W(2, 6) - 0.05, W(2, 7) - 0.03, W(2, 7) + 0.22]
for k, t in enumerate(pay):
    add(f'tl.fromTo("#paid{k}", {{autoAlpha: 0, scale: 2.3}}, {{autoAlpha: 1, scale: 1, duration: 0.11, ease: "power4.in"}}, {at(t - 0.1)});')
    hit(t + 0.01, f"PAID {k + 1}", ("stamp", -5, "hero"), ("thud", {"gain": 0.3}) if k == 2 else None)
shake("#sRenew .shk", pay[2] + 0.02, 12)

# ---------------- S2: send the declarations page into the agency ----------------
def doc(id_, title, rows):
    bars = "".join(f'<div class="row"><div class="lab">{r}</div><div class="bar" style="width:{w}%"></div></div>' for r, w in rows)
    return (f'<div class="doc" id="{id_}"><div class="dt">{title}</div><div class="rule"></div>{bars}'
            f'<div class="prem"><div class="lab">Total premium</div><div class="pv">$<span class="bar" style="width:150px"></span></div></div></div>')
rows = [("Named insured", 74), ("Policy period", 56), ("Coverages and limits", 86)]
send = doc("docA", "Declarations page", rows) + '<div class="badge" id="badge"><img src="assets/img/logo.svg" alt=""></div><div id="ring"></div>'
add(f'tl.fromTo("#docA", {{x: 380, y: 40, rotation: 9, scale: 0.84}}, {{x: 0, y: 40, rotation: -2, scale: 0.8, duration: 0.5, ease: "expo.out"}}, {at(S2)});')
add(f'tl.fromTo("#badge", {{autoAlpha: 0, scale: 0.5, y: -40}}, {{autoAlpha: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.7)"}}, {at(W(3, 1) - 0.08)});')
hit(W(3, 1) - 0.05, "logo in", ("pop", -14, "fx"), None)
pg = W(3, 4)
add(f'tl.to("#docA", {{y: -330, scale: 0.12, rotation: 9, autoAlpha: 0, duration: 0.4, ease: "power3.in"}}, {at(pg - 0.14)});')
hit(pg - 0.1, "doc sent", ("swoosh_up", -8, "fx"), None)
add(f'tl.to("#badge", {{keyframes: [{{scale: 1.14, duration: 0.08, ease: "power2.out"}}, {{scale: 1, duration: 0.34, ease: "expo.out"}}]}}, {at(pg + 0.26)});')
add(f'tl.fromTo("#ring", {{autoAlpha: 0.9, scale: 0.6}}, {{autoAlpha: 0, scale: 1.9, duration: 0.6, ease: "expo.out", immediateRender: false}}, {at(pg + 0.26)});')
hit(pg + 0.26, "received", ("chime", -15, "fx"), ("bell", {"gain": 0.16, "pitch": "E6"}))

# ---------------- S3: we shop it, what you could save ----------------
shop = (doc("docB", "Declarations page", rows) + '<div id="scan"></div>'
        + "".join(f'<div class="rck" id="rck{k}">{CHECK}</div>' for k in range(3))
        + '<div id="saveTag"><div class="st-k">WHAT YOU COULD SAVE</div><div class="st-v">$<i></i></div></div>')
add(f'tl.set(".rck", {{autoAlpha: 0}}, 0);')
add(f'tl.fromTo("#docB", {{x: -330, rotation: -8}}, {{x: -110, rotation: -2, duration: 0.5, ease: "expo.out"}}, {at(S3)});')
sh = W(4, 1)
add(f'tl.fromTo("#scan", {{autoAlpha: 0, y: 0}}, {{autoAlpha: 1, y: 0, duration: 0.08}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{y: 560, duration: 0.95, ease: "power1.inOut"}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{autoAlpha: 0, duration: 0.12}}, {at(sh + 0.9)});')
hit(sh - 0.05, "scan", ("swipe", -14, "fx"), None)
for k in range(3):
    t = sh + 0.22 + k * 0.24
    add(f'tl.fromTo("#rck{k}", {{autoAlpha: 0, scale: 0.4}}, {{autoAlpha: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", immediateRender: false}}, {at(t)});')
    add(f'tl.fromTo("#rck{k} .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.2, ease: "power2.out"}}, {at(t + 0.05)});')
    hit(t + 0.03, f"check {k + 1}", ("tick", -13, "fx"), None)
sv = W(4, 6)
add(f'tl.fromTo("#saveTag", {{autoAlpha: 0, x: 260, rotation: 10}}, {{autoAlpha: 1, x: 0, rotation: 4, duration: 0.42, ease: "expo.out"}}, {at(sv - 0.08)});')
add(f'tl.fromTo("#saveTag i", {{backgroundPosition: "-300px 0px"}}, {{backgroundPosition: "300px 0px", duration: 1.1, ease: "none"}}, {at(sv)});')
add(f'tl.to("#sShop .cam", {{scale: 1.08, x: -40, duration: 0.6, ease: "power2.out"}}, {at(sv)});')
hit(sv - 0.04, "save tag", ("impact", -11, "hero"), ("bell", {"gain": 0.22, "pitch": "A6"}))

# ---------------- S4: every month you wait ----------------
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
grid = '<div id="mGrid">' + "".join(f'<div class="mt" id="mt{k}">{m}</div>' for k, m in enumerate(months)) + '</div><div id="mLab">STILL AT YOUR OLD RATE</div>'
add('tl.set(".mt", {opacity: 0.4}, 0);')
add('tl.set("#mLab", {autoAlpha: 0}, 0);')
old = W(5, 9)
m0, m1 = S4 + 0.3, old - 0.14
for k in range(12):
    t = m0 + k * (m1 - m0) / 11
    add(f'tl.to("#mt{k}", {{keyframes: [{{opacity: 1, scaleY: 0.15, duration: 0.06, ease: "power2.in"}}, {{scaleY: 1, duration: 0.18, ease: "expo.out"}}]}}, {at(t)});')
    hit(t + 0.06, f"month {k + 1}", ("tick", -19, "fx"), None)
add(f'tl.to(".mt", {{backgroundColor: "rgba(194,162,76,0.92)", color: "{ONYX}", duration: 0.18, stagger: 0.012}}, {at(old - 0.06)});')
add(f'tl.fromTo("#mLab", {{autoAlpha: 0, y: 40}}, {{autoAlpha: 1, y: 0, duration: 0.36, ease: "expo.out", immediateRender: false}}, {at(old - 0.04)});')
shake("#sMonths .shk", old, 12)
hit(old, "old rate lock", ("impact", -9, "hero"), ("sub", {"gain": 0.4, "len": 0.45}))

# ---------------- S5: end card ----------------
end_html = ('<div id="kick">STILL ON YOUR OLD RATE?</div><img id="endLogo" src="assets/img/logo.svg" alt="The Experts Agency">'
            '<div id="endRule"></div><div id="cta">GET A FREE QUOTE</div><div id="free">IT&#39;S FREE</div>'
            '<div id="phone">(929) 675-2948</div><div id="fine">Coverage and pricing subject to underwriting and state availability.</div>')
add(f'tl.set(["#cta", "#free", "#phone", "#fine"], {{autoAlpha: 0}}, 0);')
add(f'tl.fromTo("#kick", {{y: -40, scale: 1.12}}, {{y: 0, scale: 1, duration: 0.42, ease: "expo.out"}}, {at(S5)});')
add(f'tl.fromTo("#endLogo", {{scale: 0.84}}, {{scale: 1, duration: 0.6, ease: "expo.out"}}, {at(S5)});')
add(f'tl.fromTo("#endRule", {{scaleX: 0}}, {{scaleX: 1, duration: 0.5, ease: "expo.out"}}, {at(S5 + 0.2)});')
gq = W(6, 1)
add(f'tl.fromTo("#cta", {{autoAlpha: 0, y: 60, scale: 0.86}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.38, ease: "back.out(1.8)", immediateRender: false}}, {at(gq - 0.06)});')
hit(gq - 0.02, "GET A FREE QUOTE", ("pop", -8, "fx"), ("bell", {"gain": 0.2, "pitch": "D6"}))
fr = W(6, 4)
add(f'tl.fromTo("#free", {{autoAlpha: 0, y: 24}}, {{autoAlpha: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: false}}, {at(fr - 0.03)});')
add(f'tl.set("#kick", {{color: "{BRASS}"}}, {at(fr - 0.03)});')
hit(fr, "free", ("pop", -15, "fx"), None)
add(f'tl.fromTo("#phone", {{autoAlpha: 0, y: 16}}, {{autoAlpha: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: false}}, {at(gq + 0.2)});')
add(f'tl.fromTo("#fine", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.3, immediateRender: false}}, {at(gq + 0.3)});')
add(f'tl.to("#cta", {{keyframes: [{{scale: 1.05, duration: 0.22, ease: "sine.out"}}, {{scale: 1, duration: 0.3, ease: "sine.in"}}]}}, {at(fr + 0.7)});')

# ---------------- camera: punch-in on every cut, slow push between ----------------
bounds = CUTS + [DUR]
ids = ["sHook", "sRenew", "sSend", "sShop", "sMonths", "sEnd"]
dirs = [(0, 0), (90, 0), (0, 70), (-90, 0), (0, -70), (0, 0)]
for i, sid in enumerate(ids):
    a, b = bounds[i], bounds[i + 1]
    if i == 0:
        continue  # the hook camera is driven by the price push above
    dx, dy = dirs[i]
    add(f'tl.fromTo("#{sid} .cam", {{scale: 1.1, x: {dx}, y: {dy}}}, {{scale: 1, x: 0, y: 0, duration: 0.38, ease: "expo.out"}}, {at(a)});')
    if sid != "sShop":
        add(f'tl.to("#{sid} .cam", {{scale: 1.03, duration: {max(b - a - 0.38, 0.1):.3f}, ease: "none"}}, {at(a + 0.38)});')
    hit(a, f"cut {i}", ("whoosh_hard", -10 if i > 1 else -7, "fx"), ("sub", {"gain": 0.5 if i == 1 else 0.3, "len": 0.5 if i == 1 else 0.3}))
hit(S1, "drop", ("impact", -6, "hero"), ("riser", {"gain": 0.22, "len": 1.2}))
add(f'tl.fromTo("#grain", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "-{int(DUR * 30) * 37 % 512 + 512}px -{int(DUR * 30) * 53 % 512 + 512}px", duration: {DUR}, ease: "steps({int(DUR * 30)})"}}, 0);')
add(f'tl.fromTo("#glow", {{x: -160, y: 0}}, {{x: 160, y: 120, duration: {DUR}, ease: "sine.inOut"}}, 0);')


def scene(i, inner):
    a, b = bounds[i], bounds[i + 1]
    return f'<div class="clip scene" id="{ids[i]}" data-start="{a:.3f}" data-duration="{b - a:.3f}"><div class="shk"><div class="cam">{inner}</div></div></div>'


css = open("style.css").read().replace("BRASS", BRASS).replace("ONYX", ONYX).replace("BONE", BONE).replace("PAPER", PAPER).replace("DEEPB", DEEP)
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
<div class="clip" id="hlWrap" data-start="0" data-duration="{S1:.3f}">{hl_html}</div>
{scene(1, renew)}
{scene(2, send)}
{scene(3, shop)}
{scene(4, grid)}
{scene(5, end_html)}
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
HITS.sort(key=lambda h: h["t"])
json.dump({"variant": V, "dur": DUR, "cuts": CUTS, "drop": T["drop"], "music_trim": T["music_trim"], "hits": HITS},
          open(f"hits_{V}.json", "w"), indent=1)
print("ok", V, len(js), "tweens", len(HITS), "hits", "DUR", DUR, "cuts", CUTS)

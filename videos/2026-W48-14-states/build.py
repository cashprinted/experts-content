"""Build index.html for W48 V2 '14 States' (hooks A/B on one body) from timing_<V>.json.

    python3 build.py A|B

Same system as Already Insured v3 (motion-reel studio rules):
  * frame 0: the licensed-states map is already moving and the full hook headline is on screen, lighting
    word by word as it is spoken (works muted);
    A: twelve states lit, Maine and Michigan light on their words; B: the states light west to east;
  * every cut sits on the measured beat grid and opens on the new image, punching in from scale 1.10;
  * camera shake on three hits only (the last new state / the map lands, the 14 counter, the old-rate lock);
  * every accent is registered with hit(), which drives the sound effects and the sync check.
Map shapes: map14.json (copy of brand/us-map-licensed.json). Writes index.html and hits_<V>.json.
"""
import json, sys

V = sys.argv[1]
T = json.load(open(f"timing_{V}.json"))
L = {l["i"]: l for l in T["lines"]}
HOOK = 0 if V == "A" else 1
W = lambda li, wi: L[li]["words"][wi][1]
ONYX, BRASS, DEEP, BONE, PAPER = "#0F0F0F", "#C2A24C", "#8A6F2B", "#F7F5F0", "#F2EFE8"
DIMF = "#26231D"
CUTS, DUR = T["cuts"], T["dur"]
S0, S1, S2, S3, S4, S5, S6 = CUTS
js, HITS = [], []
at = lambda t: f"{t:.3f}"
add = js.append

MAP = json.load(open("map14.json"))
C = {"ME": [912, 92], "MI": [665, 172]}  # visual centres (lower peninsula for Michigan)
for s in MAP["states"]:
    s.setdefault("c", C.get(s["ab"]))
NEW = ("ME", "MI")


def hit(t, label, lib=None, synth=None):
    """lib: (name, dB, bus) from the ElevenLabs library; synth: (motion-reel sfx name, opts)."""
    HITS.append({"t": round(t, 3), "label": label, "lib": lib, "synth": synth})


def shake(sel, t, amp=14, n=6):
    ks = ", ".join(f'{{x: {amp * (1 - k / n) * (1 if k % 2 else -1):.1f}, y: {amp * 0.5 * (1 - k / n) * (-1 if k % 3 else 1):.1f}, duration: 0.035}}' for k in range(n))
    add(f'tl.to("{sel}", {{keyframes: [{ks}, {{x: 0, y: 0, duration: 0.05}}]}}, {at(t)});')


# ---------------- captions for the body lines (hook and end card carry their own type) ----------------
BODY = (2, 3, 4, 5, 6)
cap_html = []
for li in BODY:
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
    "truck": '<path d="M2 5h12v11H2z"></path><path d="M14 9h4l4 4v3h-8z"></path><circle cx="6" cy="18" r="2"></circle><circle cx="18" cy="18" r="2"></circle>',
    "home": '<path d="M3 10.5 12 3l9 7.5"></path><path d="M5 9v12h14V9"></path><path d="M10 21v-6h4v6"></path>',
    "biz": '<rect x="3" y="7" width="18" height="13" rx="2"></rect><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><path d="M3 13h18"></path>',
    "umb": '<path d="M22 12a10 10 0 0 0-20 0Z"></path><path d="M12 12v8a2 2 0 0 0 4 0"></path><path d="M12 2v1"></path>',
}
svg = lambda k, cls: f'<svg class="{cls}" viewBox="0 0 24 24">{ICON[k]}</svg>'
CHECK = '<svg class="chk" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"></path></svg>'
order = sorted(range(len(MAP["states"])), key=lambda k: MAP["states"][k]["c"][0])  # west to east


def mapsvg(id_, lit_all):
    paths = "".join(f'<path class="st{" on" if lit_all or (V == "A" and s["ab"] not in NEW) else ""}" id="{id_}s{s["ab"]}" d="{s["d"]}"></path>'
                    for s in MAP["states"])
    return f'<svg class="map" id="{id_}" viewBox="0 0 {MAP["W"]} {MAP["H"]}"><path class="dim" d="{MAP["dim"]}"></path>{paths}</svg>'


# ---------------- S0: hook (headline on screen in frame 0 + the map) ----------------
HL = {"A": [("NOW QUOTING", "IN MAINE", [0, 1], [2, 3]), ("AND", "MICHIGAN.", [4], [5])],
      "B": [("IS YOUR", "STATE", [0, 1], [2]), ("ON OUR", "MAP?", [3, 4], [5])]}[V]
hl_html = ""
for h, (a, b, wa, wb) in enumerate(HL):
    spans = []
    for row, (txt, idx) in enumerate(((a, wa), (b, wb))):
        ws = txt.split(" ")
        spans.append('<div class="hlr">' + "".join(f'<span id="h{h}_{row}_{k}">{w}</span>' for k, w in enumerate(ws)) + "</div>")
    hl_html += f'<div class="hl" id="hl{h}">{"".join(spans)}</div>'
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

K = 1000 / MAP["W"]  # map px per map unit in the hook (map 1000 wide at left 40, top 470)
chips = "".join(f'<div class="chip" id="chip{ab}" style="left:{40 + C[ab][0] * K - 70:.0f}px; top:{470 + C[ab][1] * K - 118:.0f}px">{ab}</div>' for ab in NEW)
hook = mapsvg("m0", False) + (chips if V == "A" else "")
add('tl.fromTo("#m0", {scale: 1.15, y: 120, rotation: -3}, {scale: 1, y: 0, rotation: 0, duration: 0.6, ease: "expo.out"}, 0);')
add(f'tl.to("#m0", {{scale: 1.04, duration: {S1 - 0.6:.2f}, ease: "sine.inOut"}}, 0.6);')
hit(0.0, "map lands", ("impact", -8, "hero"), ("whoosh", {"gain": 0.25, "from": 3000, "to": 300}))


def light(sel, t, big=True):
    add(f'tl.to("{sel}", {{fill: "{BRASS}", duration: 0.08}}, {at(t)});')
    if big:
        add(f'tl.fromTo("{sel}", {{scale: 1.5, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false}}, {at(t)});')


if V == "A":
    add('tl.set(".chip", {autoAlpha: 0}, 0);')
    for k, (ab, wi) in enumerate((("ME", 3), ("MI", 5))):
        t = W(0, wi) - 0.03
        light(f"#m0s{ab}", t)
        add(f'tl.fromTo("#chip{ab}", {{autoAlpha: 0, y: 30, scale: 0.6}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.2)", immediateRender: false}}, {at(t + 0.02)});')
        hit(t + 0.01, f"{ab} lights", ("chime", -12, "fx"), ("bell", {"gain": 0.22, "pitch": ["A5", "E6"][k]}))
    last = W(0, 5)
else:
    t0, t1 = 0.12, W(1, 4) - 0.05  # all 14 light west to east by "our"
    for n, k in enumerate(order):
        t = t0 + n * (t1 - t0) / (len(order) - 1)
        light(f'#m0s{MAP["states"][k]["ab"]}', t, big=False)
        hit(t + 0.01, f'{MAP["states"][k]["ab"]} lights', ("tick", -18, "fx"), None)
    last = W(1, 5)
# the payoff: the map pulses, camera pushes, one shake
pulse = "#m0 .st" if V == "B" else "#m0 .st:not(#m0sMI)"
add(f'tl.fromTo("{pulse}", {{scale: 1.12, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.015, immediateRender: false}}, {at(last - 0.02)});')
add(f'tl.to("#sHook .cam", {{scale: 1.07, y: 20, duration: {S1 - last + 0.02:.3f}, ease: "power2.out"}}, {at(last - 0.02)});')
shake("#sHook .shk", last + 0.06, 15)
hit(last + 0.06, "map payoff", ("impact", -10, "hero"), ("thud", {"gain": 0.4}))

# ---------------- S1 (the drop): fourteen states, one team ----------------
K1 = 900 / MAP["W"]
ny = next(s["c"] for s in MAP["states"] if s["ab"] == "NY")
lines = "".join(f'<line class="ln" id="ln{s["ab"]}" x1="{ny[0]}" y1="{ny[1]}" x2="{s["c"][0]}" y2="{s["c"][1]}"></line>'
                for s in MAP["states"] if s["ab"] != "NY")
team = ('<div id="count"><span id="num">14</span><span id="numL">STATES</span></div>'
        + mapsvg("m1", True).replace("</svg>", f'<g id="net">{lines}</g><circle id="hub" cx="{ny[0]}" cy="{ny[1]}" r="11"></circle>'
                                     f'<circle id="hubR" cx="{ny[0]}" cy="{ny[1]}" r="11"></circle></svg>')
        )
add('tl.set(["#hub", "#hubR"], {autoAlpha: 0}, 0);')
add('tl.set(".ln", {strokeDashoffset: 1000}, 0);')
add(f'tl.fromTo("#count", {{y: 0, scale: 1.3}}, {{y: 0, scale: 1, duration: 0.24, ease: "power4.in"}}, {at(S1)});')
fo = W(2, 0)
for n in range(1, 15):  # count 1 -> 14 on "Fourteen", easing out
    add(f'tl.set("#num", {{textContent: "{n}"}}, {at(S1 if n == 1 else fo - 0.04 + 0.42 * (1 - (1 - (n - 1) / 13) ** 2))});')
shake("#sTeam .shk", fo + 0.4, 12)
hit(fo + 0.4, "14 lands", ("impact", -8, "hero"), None)
for n in range(3):
    hit(fo - 0.02 + n * 0.1, f"count {n}", ("tick", -18, "fx"), None)
ot = W(2, 2)
add(f'tl.to(".ln", {{strokeDashoffset: 0, duration: 0.45, ease: "power2.out", stagger: 0.02}}, {at(ot - 0.06)});')
add(f'tl.fromTo("#hub", {{autoAlpha: 0, scale: 0.2, transformOrigin: "50% 50%"}}, {{autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: false}}, {at(ot - 0.06)});')
hit(ot - 0.04, "network", ("swipe", -14, "fx"), None)
tm = W(2, 3)
add(f'tl.fromTo("#hubR", {{autoAlpha: 0.9, scale: 1, transformOrigin: "50% 50%"}}, {{autoAlpha: 0, scale: 5, duration: 0.6, ease: "expo.out", immediateRender: false}}, {at(tm - 0.03)});')
hit(tm - 0.01, "one team", ("pop", -10, "fx"), ("bell", {"gain": 0.2, "pitch": "D6"}))

# ---------------- S2: auto, trucking, business, home and umbrella ----------------
tiles = [("car", "AUTO", 0), ("truck", "TRUCKING", 1), ("biz", "BUSINESS", 2), ("home", "HOME", 3), ("umb", "UMBRELLA", 5)]
lines_html = "".join(f'<div class="tile" id="tile{k}">{svg(ic, "t-ic")}<div class="t-l">{lab}</div></div>' for k, (ic, lab, _) in enumerate(tiles))
add('tl.set(".tile", {opacity: 0.5}, 0);')
for k in range(5):
    add(f'tl.fromTo("#tile{k}", {{y: {110 + 30 * k}, rotation: {(-1) ** k * 4}}}, {{y: 0, rotation: 0, duration: 0.42, ease: "expo.out"}}, {at(S2 + 0.02 * k)});')
for k, (_, lab, wi) in enumerate(tiles):
    t = W(3, wi)
    add(f'tl.to("#tile{k}", {{keyframes: [{{opacity: 1, scale: 1.12, borderColor: "{BRASS}", duration: 0.1, ease: "power2.out"}}, {{scale: 1, duration: 0.3, ease: "expo.out"}}]}}, {at(t - 0.04)});')
    add(f'tl.to("#tile{k} .t-ic", {{stroke: "{BRASS}", duration: 0.1}}, {at(t - 0.04)});')
    add(f'tl.to("#tile{k} .t-l", {{color: "{BRASS}", duration: 0.1}}, {at(t - 0.04)});')
    hit(t - 0.02, f"tile {lab}", ("pop", -11, "fx"), ("blip", {"gain": 0.16, "pitch": ["C6", "D6", "E6", "G6", "A6"][k]}))


# ---------------- S3: send your current policy into the agency ----------------
def doc(id_, title, rows):
    bars = "".join(f'<div class="row"><div class="lab">{r}</div><div class="bar" style="width:{w}%"></div></div>' for r, w in rows)
    return (f'<div class="doc" id="{id_}"><div class="dt">{title}</div><div class="rule"></div>{bars}'
            f'<div class="prem"><div class="lab">Total premium</div><div class="pv">$<span class="bar" style="width:150px"></span></div></div></div>')


rows = [("Named insured", 74), ("Policy period", 56), ("Coverages and limits", 86)]
send = doc("docA", "Current policy", rows) + '<div class="badge" id="badge"><img src="assets/img/logo.svg" alt=""></div><div id="ring"></div>' + f'<div id="rcv"><span class="rc">{CHECK}</span><span>POLICY RECEIVED</span></div>'
add(f'tl.fromTo("#docA", {{x: 380, y: 40, rotation: 9, scale: 0.84}}, {{x: 0, y: 40, rotation: -2, scale: 0.8, duration: 0.5, ease: "expo.out"}}, {at(S3)});')
add(f'tl.fromTo("#badge", {{autoAlpha: 0, scale: 0.5, y: -40}}, {{autoAlpha: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.7)"}}, {at(W(4, 1) - 0.08)});')
hit(W(4, 1) - 0.05, "logo in", ("pop", -14, "fx"), None)
pg = W(4, 4)
add(f'tl.to("#docA", {{y: -330, scale: 0.12, rotation: 9, autoAlpha: 0, duration: 0.4, ease: "power3.in"}}, {at(pg - 0.14)});')
hit(pg - 0.1, "doc sent", ("swoosh_up", -8, "fx"), None)
add(f'tl.to("#badge", {{keyframes: [{{scale: 1.14, duration: 0.08, ease: "power2.out"}}, {{scale: 1, duration: 0.34, ease: "expo.out"}}]}}, {at(pg + 0.26)});')
add(f'tl.fromTo("#ring", {{autoAlpha: 0.9, scale: 0.6}}, {{autoAlpha: 0, scale: 1.9, duration: 0.6, ease: "expo.out", immediateRender: false}}, {at(pg + 0.26)});')
add('tl.set("#rcv", {autoAlpha: 0}, 0);')
add(f'tl.fromTo("#rcv", {{autoAlpha: 0, y: 60, scale: 0.7}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.34, ease: "back.out(2)", immediateRender: false}}, {at(pg + 0.26)});')
add(f'tl.fromTo("#rcv .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.22, ease: "power2.out", immediateRender: false}}, {at(pg + 0.34)});')
hit(pg + 0.26, "received", ("chime", -15, "fx"), ("bell", {"gain": 0.16, "pitch": "E6"}))

# ---------------- S4: we shop it, what you could save ----------------
shop = (doc("docB", "Current policy", rows) + '<div id="scan"></div>'
        + "".join(f'<div class="rck" id="rck{k}">{CHECK}</div>' for k in range(3))
        + '<div id="saveTag"><div class="st-k">WHAT YOU COULD SAVE</div><div class="st-v">$<i></i></div></div>')
add('tl.set(".rck", {autoAlpha: 0}, 0);')
add(f'tl.fromTo("#docB", {{x: -330, rotation: -8}}, {{x: -110, rotation: -2, duration: 0.5, ease: "expo.out"}}, {at(S4)});')
sh = W(5, 1)
add(f'tl.fromTo("#scan", {{autoAlpha: 0, y: 0}}, {{autoAlpha: 1, y: 0, duration: 0.08}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{y: 560, duration: 0.95, ease: "power1.inOut"}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{autoAlpha: 0, duration: 0.12}}, {at(sh + 0.9)});')
hit(sh - 0.05, "scan", ("swipe", -14, "fx"), None)
for k in range(3):
    t = sh + 0.22 + k * 0.24
    add(f'tl.fromTo("#rck{k}", {{autoAlpha: 0, scale: 0.4}}, {{autoAlpha: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", immediateRender: false}}, {at(t)});')
    add(f'tl.fromTo("#rck{k} .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.2, ease: "power2.out", immediateRender: false}}, {at(t + 0.05)});')
    hit(t + 0.03, f"check {k + 1}", ("tick", -13, "fx"), None)
sv = W(5, 9)
add(f'tl.fromTo("#saveTag", {{autoAlpha: 0, x: 260, rotation: 10}}, {{autoAlpha: 1, x: 0, rotation: 4, duration: 0.42, ease: "expo.out"}}, {at(sv - 0.08)});')
add(f'tl.fromTo("#saveTag i", {{backgroundPosition: "-300px 0px"}}, {{backgroundPosition: "300px 0px", duration: 1.1, ease: "none"}}, {at(sv)});')
add(f'tl.to("#sShop .cam", {{scale: 1.08, x: -40, duration: 0.6, ease: "power2.out"}}, {at(sv)});')
hit(sv - 0.04, "save tag", ("impact", -11, "hero"), ("bell", {"gain": 0.22, "pitch": "A6"}))

# ---------------- S5: every month you wait ----------------
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
grid = '<div id="mGrid">' + "".join(f'<div class="mt" id="mt{k}">{m}</div>' for k, m in enumerate(months)) + '</div><div id="mLab">STILL AT YOUR OLD RATE</div>'
add('tl.set(".mt", {opacity: 0.4}, 0);')
add('tl.set("#mLab", {autoAlpha: 0}, 0);')
old = W(6, 9)
m0, m1 = S5 + 0.3, old - 0.14
for k in range(12):
    t = m0 + k * (m1 - m0) / 11
    add(f'tl.to("#mt{k}", {{keyframes: [{{opacity: 1, scaleY: 0.15, duration: 0.06, ease: "power2.in"}}, {{scaleY: 1, duration: 0.18, ease: "expo.out"}}]}}, {at(t)});')
    hit(t + 0.06, f"month {k + 1}", ("tick", -19, "fx"), None)
add(f'tl.to(".mt", {{backgroundColor: "rgba(194,162,76,0.92)", color: "{ONYX}", duration: 0.18, stagger: 0.012}}, {at(old - 0.06)});')
add(f'tl.fromTo("#mLab", {{autoAlpha: 0, y: 40}}, {{autoAlpha: 1, y: 0, duration: 0.36, ease: "expo.out", immediateRender: false}}, {at(old - 0.04)});')
shake("#sMonths .shk", old, 12)
hit(old, "old rate lock", ("impact", -9, "hero"), ("sub", {"gain": 0.4, "len": 0.45}))

# ---------------- S6: end card ----------------
end_html = ('<div id="kick">NOW IN 14 STATES</div><img id="endLogo" src="assets/img/logo.svg" alt="The Experts Agency">'
            '<div id="endRule"></div><div id="cta">GET A FREE QUOTE</div><div id="free">IT&#39;S FREE</div>'
            '<div id="phone">(929) 675-2948</div><div id="fine">Coverage and pricing subject to underwriting and state availability.</div>')
add('tl.set(["#cta", "#free", "#phone", "#fine"], {autoAlpha: 0}, 0);')
add(f'tl.fromTo("#kick", {{y: -40, scale: 1.12}}, {{y: 0, scale: 1, duration: 0.42, ease: "expo.out"}}, {at(S6)});')
add(f'tl.fromTo("#endLogo", {{scale: 0.84}}, {{scale: 1, duration: 0.6, ease: "expo.out"}}, {at(S6)});')
add(f'tl.fromTo("#endRule", {{scaleX: 0}}, {{scaleX: 1, duration: 0.5, ease: "expo.out"}}, {at(S6 + 0.2)});')
gq = W(7, 1)
add(f'tl.fromTo("#cta", {{autoAlpha: 0, y: 60, scale: 0.86}}, {{autoAlpha: 1, y: 0, scale: 1, duration: 0.38, ease: "back.out(1.8)", immediateRender: false}}, {at(gq - 0.06)});')
hit(gq - 0.02, "GET A FREE QUOTE", ("pop", -8, "fx"), ("bell", {"gain": 0.2, "pitch": "D6"}))
fr = W(7, 4)
add(f'tl.fromTo("#free", {{autoAlpha: 0, y: 24}}, {{autoAlpha: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: false}}, {at(fr - 0.03)});')
add(f'tl.set("#kick", {{color: "{BRASS}"}}, {at(fr - 0.03)});')
hit(fr, "free", ("pop", -15, "fx"), None)
add(f'tl.fromTo("#phone", {{autoAlpha: 0, y: 16}}, {{autoAlpha: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: false}}, {at(gq + 0.2)});')
add(f'tl.fromTo("#fine", {{autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.3, immediateRender: false}}, {at(gq + 0.3)});')
add(f'tl.to("#cta", {{keyframes: [{{scale: 1.05, duration: 0.22, ease: "sine.out"}}, {{scale: 1, duration: 0.3, ease: "sine.in"}}]}}, {at(fr + 0.7)});')

# ---------------- camera: punch-in on every cut, slow push between ----------------
bounds = CUTS + [DUR]
ids = ["sHook", "sTeam", "sLines", "sSend", "sShop", "sMonths", "sEnd"]
dirs = [(0, 0), (0, 90), (90, 0), (0, 70), (-90, 0), (0, -70), (0, 0)]
for i, sid in enumerate(ids):
    a, b = bounds[i], bounds[i + 1]
    if i == 0:
        continue  # the hook camera is driven by the payoff push above
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


css = open("style.css").read()
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
{scene(0, hook)}
<div class="clip" id="hlWrap" data-start="0" data-duration="{S1:.3f}">{hl_html}</div>
{scene(1, team)}
{scene(2, lines_html)}
{scene(3, send)}
{scene(4, shop)}
{scene(5, grid)}
{scene(6, end_html)}
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

"""Build index.html for W48 V1 'Umbrella' (hooks A/B on one body) from timing_<V>.json.

    python3 build.py A|B

Same system as Already Insured v3 (motion-reel studio rules):
  * frame 0: the liability gauge card is already moving and the full hook headline is on screen, lighting
    word by word as it is spoken (works muted);
  * every cut sits on the measured beat grid and opens on the new image, punching in from scale 1.10;
  * secondary objects enter with direction and weight; camera shake on three hits only
    (claim over the limit, the umbrella layer landing, the umbrella band over auto/home/business);
  * every accent is registered with hit(), which drives the sound effects and the sync check.
Story: a claim rises past the policy limit; an umbrella adds a layer above it; it sits above auto, home and
business; send the current policy; we show where your limits stand. No numbers anywhere (bars stand in).
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
BODY = (2, 3, 4, 5)
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
    "home": '<path d="M3 10.5 12 3l9 7.5"></path><path d="M5 9v12h14V9"></path><path d="M10 21v-6h4v6"></path>',
    "biz": '<rect x="3" y="7" width="18" height="13" rx="2"></rect><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><path d="M3 13h18"></path>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>',
    "umb": '<path d="M22 12a10 10 0 0 0-20 0Z"></path><path d="M12 12v8a2 2 0 0 0 4 0"></path><path d="M12 2v1"></path>',
}
svg = lambda k, cls: f'<svg class="{cls}" viewBox="0 0 24 24">{ICON[k]}</svg>'
CHECK = '<svg class="chk" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"></path></svg>'


def gauge(id_, extra=""):
    return (f'<div class="gcard" id="{id_}"><div class="g-top"><div><div class="g-k">Your policy</div><div class="g-t">LIABILITY LIMIT</div></div>'
            f'{svg("shield", "g-ic")}</div>'
            f'<div class="gz"><div class="claim"><span>CLAIM</span></div><div class="over"></div><div class="cov"></div>'
            f'<div class="lim"></div><div class="limLab">YOUR LIMIT</div><div class="overLab">OVER THE<br>LIMIT</div>{extra}</div></div>')


# ---------------- S0: hook (headline on screen in frame 0 + the gauge card) ----------------
HL = {"A": [("YOUR INSURANCE", "HAS A LIMIT.", [0, 1], [2, 3, 4]), ("A LAWSUIT", "DOESN&#39;T.", [5, 6], [7])],
      "B": [("WHAT HAPPENS", "WHEN A CLAIM", [0, 1], [2, 3, 4]), ("IS BIGGER THAN", "YOUR COVERAGE?", [5, 6, 7], [8, 9])]}[V]
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

g0 = '<div id="g0w">' + gauge("g0") + "</div>"
add('tl.set(["#g0 .over", "#g0 .overLab", "#g0 .cov"], {autoAlpha: 0}, 0);')
add('tl.set("#g0 .claim", {height: 44}, 0);')
add('tl.fromTo("#g0", {x: -60, y: 190, scale: 1.4, rotation: 10}, {x: 0, y: 0, scale: 1, rotation: 2, duration: 0.5, ease: "expo.out"}, 0);')
add(f'tl.to("#g0", {{rotation: 0.5, y: -10, duration: {S1 - 0.5:.2f}, ease: "sine.inOut"}}, 0.5);')
hit(0.0, "card lands", ("impact", -8, "hero"), ("whoosh", {"gain": 0.25, "from": 3000, "to": 300}))
if V == "A":
    add('tl.to("#g0 .claim", {height: 130, duration: 0.8, ease: "power2.out"}, 0.0);')
    lim, surge, over = W(0, 4), W(0, 6), W(0, 7)
else:
    lim, surge, over = 0.34, W(1, 6), W(1, 9)
    add(f'tl.to("#g0 .claim", {{height: 80, duration: 0.5, ease: "power2.out"}}, 0.0);')
    add(f'tl.to("#g0 .claim", {{height: 140, duration: 0.4, ease: "expo.out"}}, {at(W(1, 4) - 0.06)});')
    hit(W(1, 4) - 0.04, "claim rises", ("tick", -10, "fx"), ("blip", {"gain": 0.16, "pitch": "E5"}))
add(f'tl.fromTo("#g0 .lim", {{scaleX: 0}}, {{scaleX: 1, duration: 0.32, ease: "expo.out"}}, {at(lim - 0.06)});')
add(f'tl.fromTo("#g0 .limLab", {{autoAlpha: 0, x: 40}}, {{autoAlpha: 1, x: 0, duration: 0.3, ease: "expo.out"}}, {at(lim - 0.02)});')
hit(lim - 0.04, "limit line", ("swipe", -14, "fx"), ("click", {"gain": 0.22}))
# the claim surges past the limit (riser builds into it), then the overflow turns hatched brass and the camera shakes
add(f'tl.to("#g0 .claim", {{height: 330, duration: 0.34, ease: "expo.out"}}, {at(surge - 0.06)});')
hit(surge - 0.02, "claim surges", ("whoosh_hard", -12, "fx"), ("sub", {"gain": 0.35, "len": 0.35}))
add(f'tl.fromTo("#g0 .over", {{autoAlpha: 0, scaleY: 0.2}}, {{autoAlpha: 1, scaleY: 1, duration: 0.16, ease: "power4.out"}}, {at(over - 0.08)});')
add(f'tl.fromTo("#g0 .overLab", {{autoAlpha: 0, x: 60, scale: 1.3}}, {{autoAlpha: 1, x: 0, scale: 1, duration: 0.2, ease: "power4.out"}}, {at(over - 0.08)});')
add(f'tl.to("#sHook .cam", {{scale: 1.07, y: 30, duration: {S1 - over + 0.08:.3f}, ease: "power2.out"}}, {at(over - 0.08)});')
shake("#sHook .shk", over + 0.06, 16)
hit(over + 0.06, "over the limit", ("impact", -10, "hero"), ("thud", {"gain": 0.4}))

# ---------------- S1 (the drop): the umbrella adds a layer above the limit ----------------
umb_html = (f'<div id="umb">{svg("umb", "umb-ic")}</div>'
            + gauge("g1", '<div class="layer"><span>UMBRELLA LAYER</span></div>')
            + f'<div id="okU">{CHECK}</div>')
add('tl.set(["#g1 .cov", "#g1 .layer", "#okU"], {autoAlpha: 0}, 0);')
add('tl.set("#g1 .claim", {height: 330}, 0);')
um = W(2, 1)
add(f'tl.fromTo("#umb", {{autoAlpha: 1, y: -560, rotation: -14}}, {{autoAlpha: 1, y: 0, rotation: 0, duration: 0.36, ease: "back.out(1.5)", immediateRender: true}}, {at(um - 0.2)});')
hit(um + 0.1, "umbrella lands", ("stamp", -9, "hero"), ("thud", {"gain": 0.3}))
ly = W(2, 4)
add(f'tl.fromTo("#g1 .layer", {{autoAlpha: 1, y: -260, scaleY: 0.6}}, {{autoAlpha: 1, y: 0, scaleY: 1, duration: 0.2, ease: "power4.in", immediateRender: false}}, {at(ly - 0.14)});')
add(f'tl.to(["#g1 .overLab", "#g1 .limLab"], {{autoAlpha: 0, duration: 0.1}}, {at(ly - 0.02)});')
add(f'tl.to("#g1 .cov", {{autoAlpha: 1, duration: 0.18}}, {at(ly + 0.04)});')
shake("#sUmb .shk", ly + 0.06, 13)
hit(ly + 0.06, "layer lands", ("impact", -9, "hero"), ("thud", {"gain": 0.4}))
cv = W(2, 7)
add(f'tl.fromTo("#okU", {{autoAlpha: 0, scale: 2.2, rotation: -30}}, {{autoAlpha: 1, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(2)", immediateRender: false}}, {at(cv - 0.1)});')
add(f'tl.fromTo("#okU .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.22, ease: "power2.out", immediateRender: false}}, {at(cv)});')
hit(cv - 0.02, "covered", ("chime", -15, "fx"), ("bell", {"gain": 0.18, "pitch": "E6"}))

# ---------------- S2: above your auto, home or business policy ----------------
tiles = [("car", "AUTO", 2), ("home", "HOME", 3), ("biz", "BUSINESS", 5)]
above = ('<div id="band">' + svg("umb", "band-ic") + '<span>UMBRELLA LIABILITY</span></div><div id="arrows">'
         + "".join(f'<i id="ar{k}"></i>' for k in range(3)) + '</div>'
         + "".join(f'<div class="tile" id="tile{k}">{svg(ic, "t-ic")}<div class="t-l">{lab}</div></div>' for k, (ic, lab, _) in enumerate(tiles)))
add('tl.set(".tile", {opacity: 0.45}, 0);')
add('tl.set("#arrows i", {scaleY: 0}, 0);')
ab = W(3, 0)
add(f'tl.fromTo("#band", {{y: -170, scaleX: 0.8}}, {{y: 0, scaleX: 1, duration: 0.2, ease: "power4.in"}}, {at(S2)});')
shake("#sAbove .shk", S2 + 0.2, 11)
hit(S2 + 0.2, "band slams", ("stamp", -7, "hero"), ("thud", {"gain": 0.35}))
for k, (_, lab, wi) in enumerate(tiles):
    t = W(3, wi)
    add(f'tl.to("#tile{k}", {{keyframes: [{{opacity: 1, scale: 1.12, borderColor: "{BRASS}", duration: 0.1, ease: "power2.out"}}, {{scale: 1, duration: 0.3, ease: "expo.out"}}]}}, {at(t - 0.04)});')
    add(f'tl.to("#tile{k} .t-ic", {{stroke: "{BRASS}", duration: 0.1}}, {at(t - 0.04)});')
    add(f'tl.to("#tile{k} .t-l", {{color: "{BRASS}", duration: 0.1}}, {at(t - 0.04)});')
    add(f'tl.to("#ar{k}", {{scaleY: 1, duration: 0.2, ease: "expo.out"}}, {at(t - 0.04)});')
    hit(t - 0.02, f"tile {lab}", ("pop", -11, "fx"), ("blip", {"gain": 0.16, "pitch": ["C6", "E6", "G6"][k]}))


# ---------------- S3: send your current policy into the agency ----------------
def doc(id_, title, rows):
    bars = "".join(f'<div class="row"><div class="lab">{r}</div><div class="bar" style="width:{w}%"></div></div>' for r, w in rows)
    return (f'<div class="doc" id="{id_}"><div class="dt">{title}</div><div class="rule"></div>{bars}'
            f'<div class="prem"><div class="lab">Liability limit</div><div class="pv"><span class="bar" style="width:170px"></span></div></div></div>')


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

# ---------------- S4: where your limits stand ----------------
shop = (doc("docB", "Current policy", rows) + '<div id="scan"></div>'
        + "".join(f'<div class="rck" id="rck{k}">{CHECK}</div>' for k in range(3))
        + '<div id="limTag"><div class="st-k">WHERE YOUR<br>LIMITS STAND</div><div class="lt-g"><b id="ltF"></b><i id="ltM"></i></div></div>')
add('tl.set(".rck", {autoAlpha: 0}, 0);')
add(f'tl.fromTo("#docB", {{x: -330, rotation: -8}}, {{x: -110, rotation: -2, duration: 0.5, ease: "expo.out"}}, {at(S4)});')
sh = W(5, 1)
add(f'tl.fromTo("#scan", {{autoAlpha: 0, y: 0}}, {{autoAlpha: 1, y: 0, duration: 0.08}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{y: 560, duration: 0.9, ease: "power1.inOut"}}, {at(sh - 0.05)});')
add(f'tl.to("#scan", {{autoAlpha: 0, duration: 0.12}}, {at(sh + 0.85)});')
hit(sh - 0.05, "scan", ("swipe", -14, "fx"), None)
for k in range(3):
    t = sh + 0.2 + k * 0.22
    add(f'tl.fromTo("#rck{k}", {{autoAlpha: 0, scale: 0.4}}, {{autoAlpha: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", immediateRender: false}}, {at(t)});')
    add(f'tl.fromTo("#rck{k} .chk path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: 0.2, ease: "power2.out", immediateRender: false}}, {at(t + 0.05)});')
    hit(t + 0.03, f"check {k + 1}", ("tick", -13, "fx"), None)
lm, sd = W(5, 5), W(5, 6)
add(f'tl.fromTo("#limTag", {{autoAlpha: 0, x: 260, rotation: 10}}, {{autoAlpha: 1, x: 0, rotation: 4, duration: 0.42, ease: "expo.out"}}, {at(lm - 0.1)});')
hit(lm - 0.06, "limits tag", ("stamp", -9, "hero"), ("bell", {"gain": 0.2, "pitch": "A6"}))
add(f'tl.fromTo("#ltM", {{x: 0}}, {{x: 300, duration: 0.5, ease: "back.out(1.4)"}}, {at(sd - 0.04)});')
add(f'tl.fromTo("#ltF", {{scaleX: 0}}, {{scaleX: 1, duration: 0.5, ease: "back.out(1.4)"}}, {at(sd - 0.04)});')
add(f'tl.to("#sLimits .cam", {{scale: 1.08, x: -40, duration: 0.6, ease: "power2.out"}}, {at(lm)});')
hit(sd + 0.3, "marker set", ("tick", -10, "fx"), ("click", {"gain": 0.2}))

# ---------------- S5: end card ----------------
end_html = ('<div id="kick">IS YOUR LIMIT ENOUGH?</div><img id="endLogo" src="assets/img/logo.svg" alt="The Experts Agency">'
            '<div id="endRule"></div><div id="cta">GET A FREE QUOTE</div><div id="free">IT&#39;S FREE</div>'
            '<div id="phone">(929) 675-2948</div><div id="fine">Coverage varies by policy and is subject to underwriting.</div>')
add('tl.set(["#cta", "#free", "#phone", "#fine"], {autoAlpha: 0}, 0);')
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
ids = ["sHook", "sUmb", "sAbove", "sSend", "sLimits", "sEnd"]
dirs = [(0, 0), (0, 90), (90, 0), (0, 70), (-90, 0), (0, 0)]
for i, sid in enumerate(ids):
    a, b = bounds[i], bounds[i + 1]
    if i == 0:
        continue  # the hook camera is driven by the overflow push above
    dx, dy = dirs[i]
    add(f'tl.fromTo("#{sid} .cam", {{scale: 1.1, x: {dx}, y: {dy}}}, {{scale: 1, x: 0, y: 0, duration: 0.38, ease: "expo.out"}}, {at(a)});')
    if sid != "sLimits":
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
{scene(0, g0)}
<div class="clip" id="hlWrap" data-start="0" data-duration="{S1:.3f}">{hl_html}</div>
{scene(1, umb_html)}
{scene(2, above)}
{scene(3, send)}
{scene(4, shop)}
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

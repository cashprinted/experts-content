"""Week 1 static graphics for The Experts Agency: 4 concepts x (4:5 feed, 9:16 stories/reels)."""
import json, os, sys

# Output folder for the canvas files (project/canvas.json + project/*.dc.html)
ROOT = sys.argv[1] if len(sys.argv) > 1 else "renders/canvas"
os.makedirs(f"{ROOT}/project", exist_ok=True)

ONYX, BRASS, BRASS_DEEP, BONE = "#0F0F0F", "#C2A24C", "#8A6F2B", "#F7F5F0"
LOGO = "/_blob/d91c389046288165979f5493ce1850a3"
TRUCK = "/_blob/774f3a7e5b26639268ac9df34cc5f07a"
FINE = "Coverage and pricing subject to underwriting and state availability."


def icon(paths, size=46, color=BRASS, sw=1.6):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


ICONS = {
    "bandage": '<path d="M10 10.01h.01"></path><path d="M10 14.01h.01"></path><path d="M14 10.01h.01"></path><path d="M14 14.01h.01"></path><path d="M18 6v12"></path><path d="M6 6v12"></path><rect x="2" y="6" width="20" height="12" rx="2"></rect>',
    "house": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>',
    "megaphone": '<path d="M11 6a13 13 0 0 0 8.4-2.8A1 1 0 0 1 21 4v12a1 1 0 0 1-1.6.8A13 13 0 0 0 11 14H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z"></path><path d="M6 14a12 12 0 0 0 2.4 7.2 2 2 0 0 0 3.2-2.4A8 8 0 0 1 10 14"></path><path d="M8 6v8"></path>',
    "scale": '<path d="M12 3v18"></path><path d="m19 8 3 8a5 5 0 0 1-6 0zV7"></path><path d="M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1"></path><path d="m5 8 3 8a5 5 0 0 1-6 0zV7"></path><path d="M7 21h10"></path>',
}

A = "position: absolute;"
CAPS = "font-stretch: 125%; text-transform: uppercase; white-space: nowrap;"


def logo(top, w):
    return f'<img src="{LOGO}" alt="The Experts Agency" style="{A} left: {540 - w / 2:.0f}px; top: {top}px; width: {w}px; display: block">'


def eyebrow(top, text, size=26):
    return f'<div style="{A} left: 40px; right: 40px; top: {top}px; font-size: {size}px; line-height: {size + 8}px; font-weight: 600; letter-spacing: 0.16em; color: {BRASS}; {CAPS}">{text}</div>'


def headline(top, lines, size, lh):
    spans = "".join(f'<span style="display: block; color: {c}">{t}</span>' for t, c in lines)
    return f'<h1 style="{A} left: 30px; right: 30px; top: {top}px; margin: 0; font-size: {size}px; line-height: {lh}px; font-weight: 580; letter-spacing: 0.01em; {CAPS}">{spans}</h1>'


def body(top, text, size=28, lh=36, weight=450, color=BONE, width=860):
    return f'<p style="{A} left: {540 - width / 2:.0f}px; width: {width}px; top: {top}px; margin: 0; font-size: {size}px; line-height: {lh}px; font-weight: {weight}; color: {color}">{text}</p>'


def fine(top, text=FINE):
    return f'<div style="{A} left: 40px; right: 40px; top: {top}px; font-size: 16px; line-height: 20px; font-weight: 500; color: rgba(247,245,240,0.66)">{text}</div>'


BAR = (f'<div style="{A} left: 0; right: 0; bottom: 0; height: 96px; display: flex; align-items: center; justify-content: center; gap: 26px; '
       f'background: {BRASS}; color: {ONYX}; font-size: 34px; font-weight: 700; white-space: nowrap">'
       f'<span style="font-stretch: 112%; letter-spacing: 0.02em">GET A FREE QUOTE</span>'
       f'<span style="width: 2px; height: 32px; background: {ONYX}"></span><span>(929) 675-2948</span></div>')


# ---------- concept content (1080 x 1350 coordinate space; bar occupies 1254-1350) ----------

def trucking():
    top = 384
    return "\n".join([
        eyebrow(108, "Trucking companies", 30),
        headline(152, [("Renewal coming up?", BONE)], 62, 74),
        f'<div style="{A} left: 40px; right: 40px; top: 238px; font-size: 40px; line-height: 48px; font-weight: 600; letter-spacing: 0.02em; color: {BRASS}; {CAPS}">Compare before you renew</div>',
        body(316, "We shop your coverage and show you the numbers side by side.", 28, 37, 450, BONE, 960),
        f'<img src="{TRUCK}" alt="Black commercial truck" style="{A} left: 0; top: {top}px; width: 1080px; height: 694px; display: block">',
        f'<img src="{LOGO}" alt="" style="{A} left: 152px; top: {top + 200}px; width: 350px; display: block">',
        f'<div style="{A} left: 20px; width: 614px; top: {top + 330}px; font-size: 18px; line-height: 22px; font-weight: 600; letter-spacing: 0.18em; color: {BRASS}; {CAPS}">Commercial trucking insurance</div>',
    ])


def already():
    lines = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 10px"><div style="font-size: 14px; line-height: 16px; font-weight: 650; letter-spacing: 0.12em; color: #6B665C; {CAPS}">{label}</div>'
        + "".join(f'<div style="height: 12px; width: {w}%; border-radius: 6px; background: #DAD5C9"></div>' for w in widths)
        + "</div>"
        for label, widths in [("Named insured", [72]), ("Policy period", [54]), ("Coverages", [88, 76, 64])])
    card = (f'<div style="{A} left: 286px; top: 540px; width: 508px; height: 610px; box-sizing: border-box; padding: 44px 44px 0; '
            f'background: #F2EFE8; transform: rotate(-3deg); box-shadow: 0 30px 70px rgba(0,0,0,0.6); display: flex; flex-direction: column; gap: 26px; text-align: left">'
            f'<div style="font-size: 21px; line-height: 24px; font-weight: 700; letter-spacing: 0.12em; color: {ONYX}; {CAPS}">Policy declarations</div>'
            f'<div style="height: 2px; background: {ONYX}"></div>{lines}'
            f'<div style="display: flex; align-items: center; justify-content: space-between; border-top: 2px solid #DAD5C9; padding-top: 22px">'
            f'<div style="font-size: 14px; font-weight: 650; letter-spacing: 0.12em; color: #6B665C; {CAPS}">Total premium</div>'
            f'<div style="display: flex; align-items: center; gap: 8px; font-size: 26px; font-weight: 700; color: {ONYX}">$<span style="display: block; width: 130px; height: 14px; border-radius: 7px; background: #DAD5C9"></span></div></div></div>')
    back = (f'<div style="{A} left: 300px; top: 556px; width: 508px; height: 610px; background: #24221D; transform: rotate(5deg)"></div>')
    stamp = (f'<div style="{A} left: 650px; top: 930px; width: 210px; height: 210px; box-sizing: border-box; border-radius: 50%; border: 6px solid {BRASS_DEEP}; '
             f'transform: rotate(-14deg); display: flex; align-items: center; justify-content: center">'
             f'<div style="width: 176px; height: 176px; box-sizing: border-box; border-radius: 50%; border: 2px solid {BRASS_DEEP}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; color: {BRASS_DEEP}; font-weight: 750; {CAPS}">'
             f'<span style="font-size: 20px; line-height: 24px; letter-spacing: 0.12em; font-stretch: 100%">We&#39;ll</span><span style="font-size: 25px; line-height: 28px; letter-spacing: 0.02em; font-stretch: 100%">compare</span></div></div>')
    return "\n".join([
        logo(44, 280),
        headline(168, [("Already have", BONE), ("insurance?", BRASS)], 84, 92),
        body(382, "Send us your declarations page.", 34, 42, 620),
        body(428, "We&#39;ll see if we can beat your current rate.", 28, 36, 450, "rgba(247,245,240,0.82)"),
        back, card, stamp,
    ])


def gl():
    tiles = [("bandage", "Customer injuries", "Someone gets hurt at your business."),
             ("house", "Property damage", "You damage someone else&#39;s property."),
             ("megaphone", "Reputation claims", "Libel, slander and advertising injury."),
             ("scale", "Legal defense", "Defense costs if you&#39;re sued over a covered claim.")]
    cells = "".join(
        f'<div style="box-sizing: border-box; height: 232px; padding: 34px 30px 0; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 12px">'
        f'{icon(ICONS[i], 54)}<div style="font-size: 32px; line-height: 38px; font-weight: 650">{t}</div>'
        f'<div style="font-size: 22px; line-height: 28px; font-weight: 450; color: rgba(247,245,240,0.8)">{d}</div></div>' for i, t, d in tiles)
    arrow = ('<span style="display: inline-flex; vertical-align: -5px; padding: 0 14px">'
             + icon('<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>', 28, BRASS, 2) + '</span>')
    return "\n".join([
        logo(44, 280),
        eyebrow(168, "General liability"),
        headline(210, [("What your GL", BONE), ("actually covers", BRASS)], 70, 80),
        f'<div style="{A} left: 70px; right: 70px; top: 404px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0">{cells}</div>',
        f'<div style="{A} left: 539px; width: 2px; top: 428px; height: 416px; background: rgba(194,162,76,0.55)"></div>',
        f'<div style="{A} left: 110px; width: 860px; top: 635px; height: 2px; background: rgba(194,162,76,0.55)"></div>',
        eyebrow(904, "Not covered by GL", 22),
        f'<div style="{A} left: 40px; right: 40px; top: 946px; font-size: 28px; line-height: 42px; font-weight: 500; white-space: nowrap">'
        f'<div>Injured employees{arrow}Workers comp</div><div>Company vehicles{arrow}Commercial auto</div></div>',
        body(1060, "Not sure what yours covers? We&#39;ll review it free.", 29, 36, 600, BONE, 960),
    ])


def proof():
    col = lambda x, n, label: (f'<div style="{A} left: {x - 220}px; width: 440px; top: 790px; display: flex; flex-direction: column; align-items: center; gap: 10px">'
                               f'<div style="font-size: 140px; line-height: 140px; font-weight: 600; font-stretch: 112%">{n}</div>'
                               f'<div style="font-size: 22px; line-height: 26px; font-weight: 600; letter-spacing: 0.14em; color: {BRASS}; {CAPS}">{label}</div></div>')
    return "\n".join([
        logo(52, 340),
        eyebrow(196, "The track record"),
        headline(240, [("Experts in name.", BONE), ("Experts in numbers.", BRASS)], 58, 68),
        f'<div style="{A} left: 40px; right: 40px; top: 430px; font-size: 210px; line-height: 210px; font-weight: 600; font-stretch: 112%; letter-spacing: -0.01em">$20M+</div>',
        f'<div style="{A} left: 40px; right: 40px; top: 654px; font-size: 28px; line-height: 32px; font-weight: 600; letter-spacing: 0.14em; color: {BRASS}; {CAPS}">In policies bound</div>',
        f'<div style="{A} left: 240px; width: 600px; top: 732px; height: 2px; background: rgba(194,162,76,0.6)"></div>',
        col(300, "5+", "Years of experience"), col(780, "12", "States licensed"),
        f'<div style="{A} left: 539px; width: 2px; top: 800px; height: 180px; background: rgba(194,162,76,0.6)"></div>',
        body(1044, "Combined record of our team. Licensed in 12 states and growing.", 22, 28, 500, "rgba(247,245,240,0.72)"),
    ])


CONCEPTS = [
    ("Trucking", "Trucking renewal", trucking, FINE),
    ("AlreadyInsured", "Already insured", already, FINE),
    ("GLCoverage", "GL coverage explainer", gl, "Coverage varies by policy and is subject to underwriting."),
    ("TrackRecord", "Track record", proof, FINE),
]


def page(title, inner, w, h):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:{BRASS}}}a:hover{{color:{BONE}}}
</style>
</helmet>
<div style="position: relative; width: {w}px; height: {h}px; overflow: hidden; background: {ONYX}; color: {BONE}; font-family: 'Archivo', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; text-align: center">
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''


def feed(fn, fine_text):
    return fn() + "\n" + fine(1208, fine_text) + "\n" + BAR


def story(fn, fine_text):
    # Stories/Reels: 4:5 content (without bar) scaled 0.8 inside the safe area; Reels UI covers the bottom 35%.
    inner = (f'<div style="{A} left: 0; top: 236px; width: 1080px; height: 1220px">{fn()}</div>'
             f'<div style="{A} left: 0; right: 0; top: 1492px; display: flex; align-items: center; justify-content: center; gap: 22px; font-size: 34px; line-height: 40px; font-weight: 700; color: {BRASS}; white-space: nowrap">'
             f'<span style="font-stretch: 112%; letter-spacing: 0.02em">GET A FREE QUOTE</span><span style="width: 2px; height: 30px; background: {BRASS}"></span><span>(929) 675-2948</span></div>'
             f'<div style="{A} left: 40px; right: 40px; top: 1552px; font-size: 16px; line-height: 20px; font-weight: 500; color: rgba(247,245,240,0.66)">{fine_text}</div>')
    return inner


boards, order, files = {}, [], []
for i, (key, title, fn, fine_text) in enumerate(CONCEPTS):
    y = i * 2160
    for kind, w, h, x, build in [("4x5", 1080, 1350, 0, feed), ("9x16", 1080, 1920, 1160, story)]:
        name = "Main.dc.html" if (i == 0 and kind == "4x5") else f"W1-{key}-{kind}.dc.html"
        open(f"{ROOT}/project/{name}", "w").write(page(f"{title} {kind.replace('x', ':')}", build(fn, fine_text), w, h))
        boards[name] = {"x": x, "y": y, "w": w, "h": h, "title": f"W1 {title} {kind.replace('x', ':')}"}
        order.append(name); files.append(name)

canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-13T20:05:00Z"}, "title": "Experts Agency Content",
          "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order,
          "notes": {"week1": {"x": 0, "y": -320, "text": "Week 1 graphics: 4:5 feed and 9:16 Stories/Reels", "kind": "title1", "maxW": 2240}},
          "designSystems": []}
json.dump(canvas, open(f"{ROOT}/project/canvas.json", "w"), indent=1)
print("\n".join(files))

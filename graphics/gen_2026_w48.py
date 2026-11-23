"""Week 48 (2026) static graphics for The Experts Agency: 4 concepts x (4:5 feed, 9:16 stories/reels).
Copied from gen_2026_w47.py; same helpers, page shell and Stories layout. Writes .dc.html artboards plus
boards.json (the page to add to the Design canvas; merge it into the live canvas.json, never overwrite)."""
import json, os, sys

# Output folder for the canvas files (project/canvas.json + project/*.dc.html)
ROOT = sys.argv[1] if len(sys.argv) > 1 else "renders/canvas-w48"
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
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(open(os.path.join(ROOT_DIR, "brand/us-map-licensed.json")))
FINE_EXPLAIN = "Coverage varies by policy and is subject to underwriting."
PAPER, RULE, LABEL = "#F2EFE8", "#DAD5C9", "#6B665C"

ICONS.update({
    "umbrella": '<path d="M22 12a10.06 10.06 1 0 0-20 0Z"></path><path d="M12 12v8a2 2 0 0 0 4 0"></path><path d="M12 2v1"></path>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"></path><path d="M15 18H9"></path><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"></path><circle cx="17" cy="18" r="2"></circle><circle cx="7" cy="18" r="2"></circle>',
})


def skel(label, widths, hi=False):
    bars = "".join(f'<div style="height: 12px; width: {w}%; border-radius: 6px; background: {RULE}"></div>' for w in widths)
    lab = f'<div style="font-size: 14px; line-height: 16px; font-weight: 650; letter-spacing: 0.12em; color: {BRASS_DEEP if hi else LABEL}; {CAPS}">{label}</div>'
    box = f"border: 3px solid {BRASS_DEEP}; border-radius: 8px; padding: 12px 14px; margin: -15px -17px;" if hi else ""
    return f'<div style="display: flex; flex-direction: column; gap: 10px; {box}">{lab}{bars}</div>'


def paper(left, top, w, h, title, rows, rot=-3):
    back = f'<div style="{A} left: {left + 14}px; top: {top + 16}px; width: {w}px; height: {h}px; background: #24221D; transform: rotate({rot + 8}deg)"></div>'
    card = (f'<div style="{A} left: {left}px; top: {top}px; width: {w}px; height: {h}px; box-sizing: border-box; padding: 40px 44px 0; overflow: hidden; '
            f'background: {PAPER}; transform: rotate({rot}deg); box-shadow: 0 30px 70px rgba(0,0,0,0.6); display: flex; flex-direction: column; gap: 24px; text-align: left">'
            f'<div style="font-size: 21px; line-height: 24px; font-weight: 700; letter-spacing: 0.12em; color: {ONYX}; {CAPS}">{title}</div>'
            f'<div style="height: 2px; background: {ONYX}; flex: none"></div>{"".join(rows)}</div>')
    return back + card


def stamp(left, top, small, big, rot=-14):
    return (f'<div style="{A} left: {left}px; top: {top}px; width: 210px; height: 210px; box-sizing: border-box; border-radius: 50%; border: 6px solid {BRASS_DEEP}; '
            f'transform: rotate({rot}deg); display: flex; align-items: center; justify-content: center">'
            f'<div style="width: 176px; height: 176px; box-sizing: border-box; border-radius: 50%; border: 2px solid {BRASS_DEEP}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; color: {BRASS_DEEP}; font-weight: 750; {CAPS}">'
            f'<span style="font-size: 20px; line-height: 24px; letter-spacing: 0.12em; font-stretch: 100%">{small}</span><span style="font-size: 25px; line-height: 28px; letter-spacing: 0.02em; font-stretch: 100%">{big}</span></div></div>')


def states_map():
    lit = "".join(f'<path d="{s["d"]}"></path>' for s in MAP["states"])
    svg = (f'<svg aria-label="US map with the 14 licensed states lit" viewBox="0 0 {MAP["W"]} {MAP["H"]}" width="1000" height="625" style="{A} left: 40px; top: 444px; display: block">'
           f'<path d="{MAP["dim"]}" fill="#26231D" stroke="{ONYX}" stroke-width="1"></path>'
           f'<g fill="{BRASS}" stroke="{ONYX}" stroke-width="1">{lit}</g></svg>')
    return "\n".join([
        logo(44, 280),
        eyebrow(168, "Now including Maine and Michigan"),
        headline(214, [("Now in 14 states.", BONE), ("Is yours lit up?", BRASS)], 66, 78),
        body(380, "Auto, home, trucking and business insurance.", 28, 36, 500, "rgba(247,245,240,0.82)"),
        svg,
        body(1086, "Send us your current policy.", 30, 38, 650, BONE, 960),
        body(1126, "We&#39;ll shop it and show you what you could be saving.", 28, 36, 450, "rgba(247,245,240,0.82)", 960),
    ])


def umbrella():
    rows = [skel("Named insured", [70]), skel("Liability limit", [46], hi=True), skel("Coverages", [86, 64])]
    return "\n".join([
        logo(44, 280),
        eyebrow(168, "Personal and commercial umbrella"),
        headline(214, [("Your policy", BONE), ("has a limit.", BONE), ("A lawsuit doesn&#39;t.", BRASS)], 64, 76),
        body(462, "An umbrella adds liability coverage above your auto, home or business policy.", 28, 36, 450, "rgba(247,245,240,0.82)", 840),
        f'<div style="{A} left: 415px; top: 548px; width: 250px; height: 250px">{icon(ICONS["umbrella"], 250, BRASS, 1.2)}</div>',
        paper(306, 812, 468, 318, "Your policy", rows, -2),
    ])


def work_vehicle():
    rows = [skel("Named insured", [72]), skel("Vehicles", [60]), skel("Business use", [40], hi=True), skel("Coverages", [84, 66])]
    return "\n".join([
        logo(44, 280),
        eyebrow(168, "Commercial auto"),
        headline(214, [("Driving for work", BONE), ("on a personal", BONE), ("auto policy?", BRASS)], 64, 76),
        body(462, "Personal auto policies can exclude business use. A vehicle that works may need commercial auto.", 28, 36, 450, "rgba(247,245,240,0.82)", 880),
        f'<div style="{A} left: 84px; top: 566px; transform: rotate(-6deg)">{icon(ICONS["truck"], 180, BRASS, 1.2)}</div>',
        paper(316, 618, 468, 500, "Personal auto policy", rows, -3),
        stamp(556, 904, "Covered", "for work?"),
    ])


def renewal_lock():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    tiles = "".join(
        f'<div style="height: 96px; box-sizing: border-box; border: 2px solid rgba(194,162,76,0.55); border-radius: 10px; background: #1A1813; display: flex; align-items: center; justify-content: center; '
        f'font-size: 24px; font-weight: 650; letter-spacing: 0.08em; color: rgba(247,245,240,0.85); {CAPS}; font-stretch: 100%">{m}</div>' for m in months)
    return "\n".join([
        logo(44, 280),
        eyebrow(168, "Home, auto and business"),
        headline(214, [("Renewing soon?", BONE), ("Compare before", BRASS), ("you&#39;re locked in.", BRASS)], 64, 76),
        f'<div style="{A} left: 450px; top: 476px; width: 200px; height: 200px">{icon(ICONS["lock"], 200, BRASS, 1.2)}</div>',
        f'<div style="{A} left: 100px; width: 880px; top: 724px; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 18px">{tiles}</div>',
        body(982, "Once it renews, every month runs at that rate.", 30, 38, 600, BONE, 900),
        body(1038, "Send us your policy before it renews. We&#39;ll shop it and show you what you could be saving.", 28, 36, 450, "rgba(247,245,240,0.82)", 860),
    ])


CONCEPTS = [
    ("StatesMap", "14 states map", states_map, FINE),
    ("Umbrella", "Umbrella limit", umbrella, FINE_EXPLAIN),
    ("WorkVehicle", "Work vehicle", work_vehicle, FINE_EXPLAIN),
    ("RenewalLock", "Renewal lock", renewal_lock, FINE),
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



# Page for the Design canvas: boards placed in a 2-column grid; names carry the week so they never clash.
boards, order, files = {}, [], []
for i, (key, title, fn, fine_text) in enumerate(CONCEPTS):
    y = i * 2160
    for kind, w, h, x, build in [("4x5", 1080, 1350, 0, feed), ("9x16", 1080, 1920, 1160, story)]:
        name = f"W48-{key}-{kind}.dc.html"
        open(f"{ROOT}/project/{name}", "w").write(page(f"{title} {kind.replace('x', ':')}", build(fn, fine_text), w, h))
        boards[name] = {"x": x, "y": y, "w": w, "h": h, "title": f"W48 {title} {kind.replace('x', ':')}"}
        order.append(name); files.append(name)
json.dump({"boards": boards, "order": order,
           "notes": {"week48": {"x": 0, "y": -320, "text": "Week 48 graphics: 4:5 feed and 9:16 Stories/Reels", "kind": "title1", "maxW": 2240}}},
          open(f"{ROOT}/project/boards.json", "w"), indent=1)
print("\n".join(files))

"""Place the voiceover on the music's measured beat grid.

    python3 timing.py A|B

Variant A opens on hook line 0, variant B on hook line 1; the body (lines 2..) is shared.
Rules (motion-reel studio rules, applied to a voiceover reel):
  * the drop is the first cut: it lands HOOK_GAP after the hook's last word, and the music is trimmed so a
    measured downbeat sits exactly there (the bed is low-passed under the hook and opens on that cut);
  * every later cut is snapped up to the next half-beat after the previous line ends (+MIN_GAP), so picture,
    music and voice share one clock; speech starts LEAD after its cut;
  * the end card holds END_HOLD after the last word, rounded up to a beat.
Writes timing_<V>.json.
"""
import json, math, sys

V = sys.argv[1]
HOOK = {"A": 0, "B": 1}[V]
A = json.load(open("assets/vo/align.json"))
G = json.load(open("grid/beats.json"))
PERIOD = G["period"]
HOOK_GAP, MIN_GAP, LEAD, END_HOLD, T0 = 0.14, 0.1, 0.07, 1.4, 0.08


def words_of(i):
    a = A[str(i)]["align"]; ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    s0 = next(st[k] for k, c in enumerate(ch) if c.strip()); s1 = max(en[k] for k, c in enumerate(ch) if c.strip())
    words, cur, ws, we = [], "", None, None
    for c, a0, a1 in zip(ch, st, en):
        if c == " ":
            if cur: words.append([cur, ws, we]); cur = ""
            continue
        if not cur: ws = a0
        cur += c; we = a1
    if cur: words.append([cur, ws, we])
    return s0, s1, words


def place(i, onset):
    s0, s1, words = words_of(i)
    at = onset - s0
    return {"i": i, "text": A[str(i)]["text"], "file": A[str(i)]["file"], "at": round(at, 3),
            "speech": [round(onset, 3), round(at + s1, 3)],
            "words": [[w, round(at + a, 3), round(at + b, 3)] for w, a, b in words]}


lines, cuts = [place(HOOK, T0)], [0.0]
drop = round(lines[0]["speech"][1] + HOOK_GAP, 3)
cuts.append(drop)
lines.append(place(2, drop + LEAD))
half = PERIOD / 2
for i in range(3, len(A)):
    want = lines[-1]["speech"][1] + MIN_GAP
    cut = drop + math.ceil((want - drop) / half - 1e-6) * half
    cuts.append(round(cut, 3))
    lines.append(place(i, cut + LEAD))
end = drop + math.ceil((lines[-1]["speech"][1] + END_HOLD - drop) / PERIOD) * PERIOD

# music trim: the first measured downbeat at or after `drop` in the track lands on the video's drop
db = next(d for d in G["downbeats"] if d >= drop)
music_trim = round(db - drop, 4)
json.dump({"variant": V, "lines": lines, "cuts": cuts, "drop": drop, "dur": round(end, 3), "period": PERIOD,
           "music_trim": music_trim}, open(f"timing_{V}.json", "w"), indent=1)
for l, c in zip(lines, cuts):
    print(f"cut {c:6.3f}  line {l['i']}  speech {l['speech']}  {l['text']}")
print(f"drop {drop}  end {end:.3f}  music trim {music_trim}  (track downbeat {db})")

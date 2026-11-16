import json, re
A = json.load(open("assets/vo/align.json"))
GAPS = [0.0, 0.16, 0.22, 0.18, 0.24, 0.10, 0.34, 0.30]  # pause before each line
t = 0.12; lines = []
for i in range(len(A)):
    a = A[str(i)]["align"]; ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    s0 = next(st[k] for k, c in enumerate(ch) if c.strip()); s1 = max(en[k] for k, c in enumerate(ch) if c.strip())
    words, cur, ws = [], "", None
    for c, a0, a1 in zip(ch, st, en):
        if c == " ":
            if cur: words.append([cur, ws, we]); cur = ""
            continue
        if not cur: ws = a0
        cur += c; we = a1
    if cur: words.append([cur, ws, we])
    t += GAPS[i]
    start = t - s0 + 0.0  # place speech onset at t
    lines.append({"i": i, "text": A[str(i)]["text"], "file": A[str(i)]["file"], "at": round(start, 3),
                  "speech": [round(start + s0, 3), round(start + s1, 3)],
                  "words": [[w, round(start + a, 3), round(start + b, 3)] for w, a, b in words]})
    t = start + s1
json.dump({"lines": lines, "end": round(t, 3)}, open("timing.json", "w"), indent=1)
for l in lines: print(l["i"], l["speech"], " ".join(f"{w}@{a}" for w, a, b in l["words"]))
print("speech ends", round(t, 2))

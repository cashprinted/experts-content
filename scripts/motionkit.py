"""Glue between an Experts video project and the motion-reel plugin's tools (no account or key needed).

The plugin ships with the owner's claude.ai account and is found under ~/.claude/plugins (or MOTION_REEL_SKILL).
Every function degrades gracefully: without the plugin, uv or node, it returns None and says why, and the
project falls back to last week's pipeline (library sound effects only, manual timing).

    from motionkit import skill, beat_grid, synth_sfx, sync_check, sheets

beat_grid(track, work)            measure a music bed's beats -> dict (bpm, period, beats, downbeats, ...)
synth_sfx(hits, dur, out_wav)     synthesized accent layer (sub drops, bells, clicks...) on exact hit times
sync_check(mix_wav, hits, dur)    nearest audio onset for every visual hit (ms); writes sync.png
sheets(video, out_dir, fps=2)     contact sheet + half-size "phone" sheet of a rendered video
"""
import glob, json, os, pathlib, shutil, subprocess, tempfile


def skill():
    env = os.environ.get("MOTION_REEL_SKILL")
    cands = [env] if env else sorted(glob.glob(str(pathlib.Path.home() / ".claude/plugins/**/skills/motion-reel"), recursive=True))
    for c in cands:
        if c and (pathlib.Path(c) / "scripts" / "mix.mjs").is_file():
            return pathlib.Path(c)
    return None


def available():
    ok = bool(skill() and shutil.which("uv") and shutil.which("node"))
    if not ok:
        print("motionkit: motion-reel plugin, uv or node missing; using the fallback pipeline")
    return ok


def _film(work, dur):
    work = pathlib.Path(work); (work / "film" / "audio").mkdir(parents=True, exist_ok=True)
    (work / "film" / "film.json").write_text(json.dumps({"title": "experts", "duration": dur, "formats": ["9x16"]}))
    return work


def beat_grid(track, work="grid_work"):
    """Measured grid of a supplied bed (beats.py --full). Never assume a tempo; ElevenLabs drifts from the prompt."""
    if not available():
        return None
    work = _film(work, 30)
    r = subprocess.run(["uv", "run", "-q", str(skill() / "scripts/beats.py"), "film", "--track", str(pathlib.Path(track).resolve()), "--full"],
                       cwd=work, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-800:]); return None
    return json.loads((work / "film" / "beats.json").read_text())


def synth_sfx(hits, dur, out_wav, period=0.5):
    """hits: [{"t": s, "label": str, "synth": [name, opts]}]. Runs the plugin's sfx.mjs on our own hit list
    (its call into the plugin renderer is replaced by our hits.json). `node sfx.mjs --list` shows the palette."""
    if not available():
        return None
    work = _film(tempfile.mkdtemp(prefix="sfx_"), dur)
    rows = [{"beat": round(h["t"] / period, 3), "t": h["t"], "label": h["label"], "sfx": h["synth"][0], "opts": h["synth"][1] or {}}
            for h in hits if h.get("synth")]
    (work / "out" / "film").mkdir(parents=True, exist_ok=True)
    (work / "out" / "film" / "hits.json").write_text(json.dumps(rows))
    src = (skill() / "scripts" / "sfx.mjs").read_text()
    a = src.index("const RENDER ="); b = src.index("const hits = JSON.parse")
    (work / "_sfx.mjs").write_text(src[:a] + src[b:])
    for dep in ("pw.mjs",):  # keep relative imports resolvable if the script grows any
        if (skill() / "scripts" / dep).exists():
            shutil.copy(skill() / "scripts" / dep, work / dep)
    r = subprocess.run(["node", "_sfx.mjs", "film"], cwd=work, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-800:]); return None
    print(r.stdout.strip())
    shutil.copy(work / "film" / "audio" / "sfx.wav", out_wav)
    return out_wav


def sync_check(mix_wav, hits, dur, out_png=None):
    """Picture hits vs audio onsets with the plugin's sync.py. Returns [(label, offset_ms)]."""
    if not available():
        return None
    work = _film(tempfile.mkdtemp(prefix="sync_"), dur)
    shutil.copy(mix_wav, work / "film" / "audio" / "mix.wav")
    (work / "out" / "film").mkdir(parents=True, exist_ok=True)
    (work / "out" / "film" / "hits.json").write_text(json.dumps([{"beat": h["t"], "t": h["t"], "label": h["label"]} for h in hits]))
    r = subprocess.run(["uv", "run", "-q", str(skill() / "scripts/sync.py"), "film"], cwd=work, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-800:]); return None
    if out_png:
        shutil.copy(work / "out" / "film" / "sync.png", out_png)
    rows = []
    for line in r.stdout.splitlines():
        if "nearest onset" in line:
            lab = line.split("nearest onset")[0].split(None, 1)[1].strip()
            rows.append((lab, float(line.rsplit("onset", 1)[1].split("ms")[0])))
    return rows


def sheets(video, out_dir, fps=2, cols=8, tag=""):
    """Contact sheet (full) and phone sheet (half size, a phone at arm's length) of a rendered video."""
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    full, phone = out / f"contact{tag}.png", out / f"phone{tag}.png"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout)
    rows = max(1, -(-int(dur * fps + 1) // cols))
    for w, f in ((270, full), (135, phone)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf",
                        f"fps={fps},scale={w}:-2,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize={max(10, w // 18)}:fontcolor=white:box=1:boxcolor=black@0.6,tile={cols}x{rows}:padding=4",
                        "-frames:v", "1", str(f)], check=True)
    return full, phone

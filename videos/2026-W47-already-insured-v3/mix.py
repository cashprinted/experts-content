"""Mix for the v3 cut: voice, ElevenLabs sound library, motion-reel synthesized accents, and the music bed
with a real drop. Writes renders/mix_<V>.wav at -14 LUFS / -1.5 dBTP and prints the sync report.

    python3 mix.py A|B

* Music: trimmed so a measured downbeat lands on the first cut. Under the hook it is low-passed (500 Hz) and
  pulled down 7 dB; on the cut the filter opens (that is the drop). It ducks under the voice and fades out
  under the end card.
* Effects: every hit in hits_<V>.json. `lib` cues come from the ElevenLabs library (aligned to each file's
  measured hit time); `synth` cues are rendered by the motion-reel plugin's sfx.mjs on the same times.
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(HERE, "..", "..", "scripts"), "/home/claude/experts-repo/scripts"):
    if os.path.isfile(os.path.join(_p, "motionkit.py")):
        sys.path.insert(0, _p); break
import motionkit

V = sys.argv[1]
SR = 48000
T = json.load(open(f"timing_{V}.json")); H = json.load(open(f"hits_{V}.json"))
DUR, DROP, TRIM = T["dur"], T["drop"], T["music_trim"]
LIB = {k: v for k, v in json.load(open("assets/sfx/sfx.json")).items() if not k.startswith("_")}
N = int(DUR * SR)
os.makedirs("renders", exist_ok=True)


def load(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def place(buf, x, t, db):
    i = int(round(t * SR)); x = x * 10 ** (db / 20)
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x))
    if j > i: buf[i:j] += x[: j - i]


vo, fx, hero = (np.zeros((N, 2), np.float32) for _ in range(3))
for l in T["lines"]:
    x = load(l["file"]); f = int(0.004 * SR)
    x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    place(vo, x, l["at"], 0)

cache = {}
for h in H["hits"]:
    if h["lib"]:
        name, db, bus = h["lib"]
        if name not in cache: cache[name] = load(f"assets/sfx/{name}.wav")
        place(hero if bus == "hero" else fx, cache[name], h["t"] - LIB[name]["hit"], db)

synth = np.zeros((N, 2), np.float32)
if motionkit.synth_sfx(H["hits"], DUR, f"renders/synth_{V}.wav", T["period"]):
    s, sr = sf.read(f"renders/synth_{V}.wav", dtype="float32")
    if sr != SR: s = load(f"renders/synth_{V}.wav")
    if s.ndim == 1: s = np.stack([s, s], 1)
    synth[: min(N, len(s))] = s[:N]

# music: trim, filtered hook, drop on the first cut
full = load("assets/music_bed.mp3", f"atrim=start={TRIM},asetpts=PTS-STARTPTS")
low = load("assets/music_bed.mp3", f"atrim=start={TRIM},asetpts=PTS-STARTPTS,lowpass=f=500,lowpass=f=500")
m = min(len(full), len(low), N)
mus = np.zeros((N, 2), np.float32)
d = int(DROP * SR); x = int(0.03 * SR)
mus[:d] = low[:d] * 10 ** (-7 / 20)
mus[d:m] = full[d:m]
xf = np.linspace(0, 1, x)[:, None]
mus[d:d + x] = low[d:d + x] * 10 ** (-7 / 20) * (1 - xf) + full[d:d + x] * xf

env = np.convolve(np.abs(vo).mean(1), np.ones(int(0.03 * SR)) / int(0.03 * SR), "same")
active = np.convolve((env > 0.01).astype(np.float32), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same").clip(0, 1)
fx *= (1 - 0.45 * active)[:, None]
synth *= (1 - 0.35 * active)[:, None]
endcut = T["cuts"][-1]
fade = np.ones(N, np.float32); a, b = int((endcut + 0.9) * SR), int((DUR - 0.05) * SR)
fade[a:b] = np.linspace(1, 0, b - a) ** 1.5; fade[b:] = 0
mus *= (fade * (1 - 0.35 * active) * 10 ** (-17 / 20))[:, None]

mix = vo + fx + hero + synth * 10 ** (-4 / 20) + mus
pk = np.abs(mix).max()
if pk > 0.89: mix *= 0.89 / pk
sf.write(f"renders/premaster_{V}.wav", mix, SR, subtype="FLOAT")
meas = subprocess.run(["ffmpeg", "-v", "info", "-i", f"renders/premaster_{V}.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"renders/premaster_{V}.wav", "-af", af, "-ar", "48000", f"renders/mix_{V}.wav"], check=True)
print("premaster", j["input_i"], "LUFS", j["input_tp"], "dBTP")

sf.write(f"renders/fxstem_{V}.wav", fx + hero + synth * 10 ** (-4 / 20), SR, subtype="FLOAT")
# effects stem only: the voice's own onsets would otherwise be matched to the nearest hit
rows = motionkit.sync_check(f"renders/fxstem_{V}.wav", [h for h in H["hits"] if h["lib"] or h["synth"]], DUR, f"renders/sync_{V}.png")
if rows:
    off = [abs(o) for _, o in rows if o == o]
    bad = [(l, o) for l, o in rows if o == o and abs(o) > 20]
    print(f"sync: {len(rows)} hits, median {np.median(off):.1f} ms, {len(bad)} over 20 ms: {bad[:8]}")

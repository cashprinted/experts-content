"""Voiceover, sound design and music mix for the 'Already have insurance?' reel. Writes renders/mix.wav at -14 LUFS."""
import json, os, subprocess, numpy as np, soundfile as sf

SR = 48000
L = json.load(open("timing.json"))["lines"]
SC = json.load(open("scenes.json")); S = SC["S"]; DUR = SC["DUR"]
S1, S2, S3, S4, S5, S6, S7 = S[1:]
SFX = json.load(open("assets/sfx/sfx.json"))
W = lambda li, wi: L[li]["words"][wi][1]
os.makedirs("renders", exist_ok=True)

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

N = int(DUR * SR)
vo, fx, hero = (np.zeros((N, 2), np.float32) for _ in range(3))
def place(buf, x, t, db):
    i = int(round(t * SR)); x = x * 10 ** (db / 20)
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x)); buf[i:j] += x[: j - i]
for l in L:
    x = load(l["file"]); f = int(0.004 * SR)
    x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    place(vo, x, l["at"], 0)
cache = {}
def cue(name, t, db, bus="fx"):
    if name not in cache: cache[name] = load(f"assets/sfx/{name}.wav")
    place(hero if bus == "hero" else fx, cache[name], t - SFX[name]["hit"], db)

# hook
cue("impact", 0.12, -5, "hero"); cue("whoosh_long", 0.30, -16)
cue("pop", W(0, 3) - 0.02, -6); cue("impact", W(0, 3), -14, "hero")
# years roll back
cue("whoosh_hard", S1, -9)
y0, y1 = W(1, 2), W(1, 7)
for k in range(1, 7): cue("tick", y0 + k * (y1 - y0) / 6 - 0.06, -14)
cue("impact", W(1, 9), -9, "hero"); cue("pop", W(1, 9), -12)
# auto-renew and bills
cue("whoosh_hard", S2, -9); cue("pop", W(2, 1), -13); cue("tick", W(2, 3), -6)
kp = W(2, 5); cue("swipe", kp - 0.05, -12)
for t in (W(2, 7) - 0.04, W(2, 8) - 0.02, W(2, 8) + 0.24): cue("stamp", t, -5, "hero")
# send dec page
cue("whoosh_hard", S3, -9); cue("paper", S3 + 0.1, -12); cue("pop", S3 + 0.2, -17)
cue("swoosh_up", W(3, 4) + 0.1, -8); cue("chime", W(3, 4) + 0.3, -16)
# shop it
cue("whoosh_hard", S4, -9); sh = W(4, 1); cue("swipe", sh, -14)
for k in range(3): cue("tick", sh + 0.3 + k * 0.28, -13)
cue("impact", W(4, 10), -9, "hero"); cue("swipe", W(4, 10) - 0.05, -12)
# coverage lines
cue("whoosh_hard", S5, -9)
for wi in (0, 1, 2, 4, 5): cue("tick", W(5, wi), -10)
# months
cue("whoosh_hard", S6, -9)
m0, m1 = S6 + 0.45, W(6, 9) - 0.15
for k in range(12): cue("tick", m0 + k * (m1 - m0) / 11 + 0.03, -20)
cue("impact", W(6, 9), -9, "hero"); cue("riser", W(6, 9), -17)
# end card
cue("whoosh_hard", S7, -9); cue("chime", S7 + 0.05, -11); cue("pop", W(7, 1), -9); cue("pop", W(7, 4), -15)

env = np.convolve(np.abs(vo).mean(1), np.ones(int(0.03 * SR)) / int(0.03 * SR), "same")
active = np.convolve((env > 0.01).astype(np.float32), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same").clip(0, 1)
fx *= (1 - 0.45 * active)[:, None]
mus = load("assets/music_bed.mp3")[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
fade = np.ones(N, np.float32); a, b = int((S7 + 1.0) * SR), int((DUR - 0.2) * SR)
fade[a:b] = np.linspace(1, 0, b - a); fade[b:] = 0
mus *= (fade * (1 - 0.35 * active) * 10 ** (-18 / 20))[:, None]
mix = vo + fx + hero + mus
# keep the summed peak in range before loudness normalisation
pk = np.abs(mix).max()
if pk > 0.89: mix *= 0.89 / pk
sf.write("renders/premaster.wav", mix, SR, subtype="FLOAT")
m = subprocess.run(["ffmpeg", "-v", "info", "-i", "renders/premaster.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "renders/premaster.wav", "-af", af, "-ar", "48000", "renders/mix.wav"], check=True)
print("input", j["input_i"], "LUFS", j["input_tp"], "dBTP")

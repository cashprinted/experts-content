"""Voiceover + sound design mix for the trucking renewal reel. Writes renders/v2-mix.wav at -14 LUFS."""
import json, subprocess, numpy as np, soundfile as sf

SR = 48000
from scenes import S2, S3, S4, S5, S5B, S6, S7, DUR
T = json.load(open("timing.json")); L = T["lines"]
SFX = json.load(open("assets/sfx/sfx.json"))
W = lambda li, wi: L[li]["words"][wi][1]

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

N = int(DUR * SR)
vo = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32); hero = np.zeros((N, 2), np.float32)

def place(buf, x, t, db):
    i = int(round(t * SR)); x = x * 10 ** (db / 20)
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x)); buf[i:j] += x[: j - i]

for l in L:
    x = load(l["file"]); f = int(0.004 * SR)
    x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    place(vo, x, l["at"], 0)

cache = {}
def cue(name, hit_time, db, bus="fx"):
    if name not in cache: cache[name] = load(f"assets/sfx/{name}.wav")
    place(hero if bus == "hero" else fx, cache[name], hit_time - SFX[name]["hit"], db)

st, pol, num, sbs, tw = W(0, 5), W(2, 4), W(3, 8), W(3, 9), W(6, 4)
cue("impact", 0.12, -5, "hero")
cue("whoosh_long", 0.30, -16)
cue("stamp", st + 0.02, -3, "hero"); cue("impact", st + 0.02, -15, "hero")
cue("swipe", S2 + 0.15, -12); cue("whoosh", S2 + 0.30, -10)
cue("pop", W(1, 3), -9)
cue("whoosh", S3 + 0.2, -13); cue("pop", W(2, 0) + 0.05, -17)
cue("swoosh_up", pol + 0.10, -8); cue("chime", pol + 0.30, -16)
cue("whoosh_hard", S4, -9)
for t in (W(3, 1), W(3, 3), W(3, 3) + 0.3): cue("tick", t + 0.06, -13)
cue("swipe", num, -13); cue("whoosh_long", sbs + 0.1, -15)
cue("whoosh_hard", S5, -9); cue("swipe", W(4, 3), -12)
cue("impact", W(4, 7), -8, "hero")
cue("whoosh", S5B, -11); cue("whoosh_long", S5B + 0.45, -14)
lk = W(5, 6)
cue("stamp", lk, -3, "hero"); cue("impact", lk, -9, "hero"); cue("tick", W(5, 7), -14)
cue("whoosh_hard", S6, -9); cue("riser", tw, -15)
t0 = S6 + 0.25
for k in range(12): cue("tick", t0 + k * (tw - t0) / 11, -21)
cue("impact", tw + 0.02, -12, "hero")
cue("whoosh_hard", S7, -9); cue("chime", S7 + 0.03, -11); cue("tick", W(7, 3), -12); cue("pop", W(7, 5), -9); cue("pop", W(7, 8), -15)

# duck the sound design under the voice (hero hits stay on top)
env = np.abs(vo).mean(1)
k = int(0.03 * SR); env = np.convolve(env, np.ones(k) / k, "same")
active = (env > 0.01).astype(np.float32)
k2 = int(0.12 * SR); active = np.convolve(active, np.ones(k2) / k2, "same").clip(0, 1)
fx *= (1 - 0.45 * active)[:, None]
# licensed ElevenLabs music bed, kept well under the voice, fading out on the end card
mus = load("assets/music_bed.mp3")[:N]
mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
fade = np.ones(N, np.float32); a, b = int((S7 + 0.6) * SR), int((S7 + 2.2) * SR)
fade[a:b] = np.linspace(1, 0, b - a); fade[b:] = 0
mus *= (fade * (1 - 0.35 * active) * 10 ** (-17 / 20))[:, None]
mix = vo + fx + hero + mus

sf.write("renders/v2-premaster.wav", mix, SR, subtype="FLOAT")
# two-pass loudness normalisation to Instagram's -14 LUFS, -1 dBTP
m = subprocess.run(["ffmpeg", "-v", "info", "-i", "renders/v2-premaster.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "renders/v2-premaster.wav", "-af", af, "-ar", "48000", "renders/v2-mix.wav"], check=True)
print("input", j["input_i"], "LUFS", j["input_tp"], "dBTP")

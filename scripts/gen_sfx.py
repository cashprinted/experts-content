import json, subprocess, sys
import os
KEY = os.environ.get('ELEVENLABS_API_KEY') or open(os.path.expanduser('~/.eleven_experts_key')).read().strip()
SFX = {
 "impact_deep": ("Deep cinematic impact hit with sub bass boom, short clean tail, no music", 1.6),
 "whoosh_fast": ("Fast clean air whoosh swipe transition for motion graphics, no music", 0.8),
 "whoosh_soft": ("Soft smooth airy whoosh, subtle motion graphics transition, no music", 1.0),
 "stamp": ("Heavy rubber stamp slamming onto paper on a wooden desk, one single hit", 0.6),
 "paper": ("Single sheet of paper sliding quickly across a desk", 0.8),
 "tick": ("Crisp short modern user interface click tick, single", 0.5),
 "riser": ("Short clean cinematic tension riser building up, no music", 1.5),
 "pop": ("Soft subtle digital pop, user interface confirmation, single", 0.5),
 "swoosh_up": ("Quick upward swoosh of an object flying away fast", 0.7),
 "chime": ("Elegant soft premium logo reveal shimmer chime, short, no melody", 1.6),
}
for name, (text, dur) in SFX.items():
    r = subprocess.run(["curl", "-sS", "--max-time", "120", "-o", f"{name}.mp3", "-w", "%{http_code}", "-X", "POST",
        "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json",
        "-d", json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.6})], capture_output=True, text=True)
    print(name, r.stdout, r.stderr[:200])

import json, base64, sys, subprocess
import os
KEY = os.environ.get('ELEVENLABS_API_KEY') or open(os.path.expanduser('~/.eleven_experts_key')).read().strip()
VOICE = 'cjVigY5qzO86Huf0OWal'  # Eric
def post(url, body):
    r = subprocess.run(["curl", "-sS", "--max-time", "120", "-X", "POST", url, "-H", f"xi-api-key: {KEY}",
                        "-H", "Content-Type: application/json", "-d", json.dumps(body)], capture_output=True, check=True)
    return r.stdout
if __name__ == "__main__":
    LINES = json.load(open(sys.argv[1]))
    only = [int(a) for a in sys.argv[2:]]
    try: out = {int(k): v for k, v in json.load(open("assets/vo/align.json")).items()}
    except FileNotFoundError: out = {}
    for i, (text, style) in enumerate(LINES):
        if only and i not in only: continue
        body = {"text": text, "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.42, "similarity_boost": 0.8, "style": style, "use_speaker_boost": True, "speed": 1.1}}
        d = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", body))
        fn = f"assets/vo/l{i:02d}.mp3"; open(fn, "wb").write(base64.b64decode(d["audio_base64"]))
        out[i] = {"text": text, "file": fn, "align": d["alignment"]}; print(i, text)
    json.dump(out, open("assets/vo/align.json", "w"))

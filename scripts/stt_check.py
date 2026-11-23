"""stt_check.py <project dir> A B : ElevenLabs speech-to-text of renders/mix_<V>.wav vs the script, word for word."""
import json, os, re, subprocess, sys
d = sys.argv[1]
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("’", "'")).split()
for V in sys.argv[2:]:
    T = json.load(open(f"{d}/timing_{V}.json"))
    script = " ".join(l["text"] for l in T["lines"])
    r = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", f"xi-api-key: {os.environ['ELEVENLABS_API_KEY']}",
                        "-F", "model_id=scribe_v1", "-F", "tag_audio_events=false", "-F", f"file=@{d}/renders/mix_{V}.wav"], capture_output=True, text=True)
    got = json.loads(r.stdout)["text"]
    a, b = norm(script), norm(got.replace("fourteen", "fourteen").replace("14", "fourteen"))
    print(V, "MATCH" if a == b else "DIFF", "|", got)
    if a != b:
        import difflib; print("  ", [x for x in difflib.ndiff(a, b) if x[0] in "+-"])

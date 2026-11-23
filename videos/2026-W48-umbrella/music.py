"""Music bed from ElevenLabs Music (commercial use on the paid plan): full energy from the first beat.

    python3 music.py <main_ms> <outro_ms> [out.mp3]

ElevenLabs does not hold section timings exactly (a planned 3 s intro came back 8 s long), so the bed is
generated at full energy and the hook's "before the drop" sound is made in the mix instead: the music
under the hook is low-passed and pulled down, and opens on the first cut (mix.py). That puts the drop
exactly on the cut. The beat grid is then measured with the motion-reel plugin (beats.py), never assumed.
"""
import json, os, subprocess, sys

KEY = os.environ.get("ELEVENLABS_API_KEY") or open(os.path.expanduser("~/.eleven_experts_key")).read().strip()
main, outro = (int(x) for x in sys.argv[1:3])
out = sys.argv[3] if len(sys.argv) > 3 else "assets/music_bed.mp3"
plan = {
    "positive_global_styles": ["instrumental", "modern premium commercial", "dark minimal trap-house", "120 BPM",
                               "tight punchy drums", "deep sub bass", "confident", "clean mix"],
    "negative_global_styles": ["vocals", "singing", "choir", "spoken word", "lo-fi", "acoustic guitar", "cheesy", "8-bit"],
    "sections": [
        {"section_name": "main", "positive_local_styles": ["full drums from the very first beat", "punchy kick on every beat",
                                                           "driving sub bass", "crisp claps", "forward momentum"],
         "negative_local_styles": ["intro", "slow build", "breakdown", "ambient opening"], "duration_ms": main, "lines": []},
        {"section_name": "end", "positive_local_styles": ["drums stop", "warm sustained chord", "resolving", "clean tail"],
         "negative_local_styles": ["new melody"], "duration_ms": outro, "lines": []},
    ],
}
body = {"composition_plan": plan, "model_id": "music_v1"}
r = subprocess.run(["curl", "-sS", "--max-time", "300", "-X", "POST",
                    "https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                    "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json",
                    "-d", json.dumps(body), "-o", out, "-w", "%{http_code}"], capture_output=True, text=True)
if r.stdout != "200":
    sys.exit(f"music failed ({r.stdout}): {open(out, errors='replace').read()[:400]}")
print("wrote", out)

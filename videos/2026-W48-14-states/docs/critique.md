# Critique log: W48 14 States (motion-reel critique-pass rubric)

## Round 0 (layout stills from the timeline, before the first render)
Removed a "ONE TEAM" tag on the map that repeated the caption directly under it; hook map entrance scale 1.25 -> 1.15 so less
of it starts off frame.

## Round 1 (variant A, full 60 fps render with the mix, 4 fps contact + phone sheets)
| hook | read | motion | variety | brand | sync | min |
|  8   |  8   |   7    |    8    |   9   |  8   |  7  |

Worst three:
1. [2.03] The drop frame shows the "14 STATES" counter flying in from above the Stories safe zone with a lone "1".
   Fix: counter enters from y -90 at scale 1.35, inside the safe zone on the cut.
2. [3.78-4.0] The five product tiles fly in from 320 to 440 px below and cross the caption block; the cut frame is a blur.
   Fix: entrance offsets 110 to 230 px, rotation 4 degrees.
3. [3.0-3.7] The "one team" network lines from New York are 2.4 px in map units and vanish at phone size.
   Fix: 4.5 px, opacity 0.95, hub dot r 14.
Also: same 0.8 s near-empty frame after the policy reaches the logo as Umbrella; same fix ("POLICY RECEIVED" chip).
Sync: "14 lands" stamp -24 ms against a synthesized thud on the same hit; thud removed and the count ticks cut from 4 to 3.
Checks failed: dead frame (1). Verdict: ANOTHER ROUND

## Round 2 (both variants re-rendered at 60 fps with the fixes, 4 fps contact + phone sheets, plus the 4:5 crop)
| variant | hook | read | motion | variety | brand | sync | min |
| A       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |
| B       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |

Round 1 fixes hold: tiles land without crossing the caption, the network lines read at phone size, "POLICY RECEIVED" fills
the gap after the logo. New problem found in the 4:5 crop: on the drop the "14 STATES" counter entered from above and was
clipped by the 4:5 top edge (y 165) for about 0.25 s. Fix: the counter punches in place (scale 1.3 -> 1, no y travel);
both variants re-rendered. Sync: "14 lands" moved from a stamp (-24 ms) to the impact (+24 / +27 ms, audio slightly after
the picture, the forgiving direction); left there.
Verdict: re-render, then technical checks.

## Round 3 (final deliverables after the counter re-render)
- Phone and 4:5 sheets: counter fully inside both frames; no clipped text, no caption on paper, every cut opens on the new image.
- Loudness: A -14.1 LUFS / -1.9 dBTP, B -14.1 / -1.7, all four files (finalize.sh master stage).
- ffprobe: 1080x1920 and 1080x1350, 60/1 fps, yuv420p, AAC 48 kHz on all four. Lengths 16.53 s (A), 16.07 s (B).
- Speech-to-text matches both scripts word for word (B transcribes "Fourteen" as "14").
- Effects sync: median 5.0 ms (A) / 5.8 ms (B). Over 20 ms: whooshes, swipes and the drop riser (by design), the t=0 map
  impact (+21 ms, detector at file start), "14 lands" (+24 / +27 ms, see round 2) and in B "NJ lights" (+33 ms, one tick in
  a run of 14 ticks about 85 ms apart where the detector can't separate neighbours).
- Music bed: "[outro jingle]", no vocals. Copy: no prices, carriers or guarantees; fine print "Coverage and pricing subject
  to underwriting and state availability."
Verdict: READY

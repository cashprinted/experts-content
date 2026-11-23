# Critique log: W48 Umbrella (motion-reel critique-pass rubric)

## Round 0 (layout stills from the timeline, before the first render)
Fixed before rendering: the "WHERE YOUR LIMITS STAND" tag ran off the right edge (moved left, two lines); frame 0 could show
hidden elements before the timeline's first set (initial states now also in CSS); the hook B card opened empty (the claim
bar now starts low and rises from frame 0).

## Round 1 (variant A, full 60 fps render with the mix, 4 fps contact + phone sheets)
| hook | read | motion | variety | brand | sync | min |
|  7   |  8   |   8    |    8    |   9   |  8   |  7  |

Worst three:
1. [0.0-2.5] The gauge card sits in the top half; the lower 45% of the frame is empty during the hook and the claim bar is
   small at phone size. Fix: hook card scaled 1.17 from its top edge (`#g0w`), so it fills to y 1166 (no captions in the hook).
2. [8.4-9.2] After the policy flies into the logo the frame is nearly empty for about 0.8 s. Fix: a "POLICY RECEIVED" chip
   with a drawn check pops under the logo on the received chime.
3. [5.29] Cut 2 opens with the umbrella band mostly above the frame. Fix: band starts at y -170 (scaleX 0.8), visible on the cut.

Sync (effects stem): two impacts were early ("layer lands" -70 ms, "limits tag" -27 ms). Fix: layer lands pairs the impact
with a synthesized thud instead of a sub; the limits tag uses the stamp. Re-check: every percussive cue within 20 ms except
the t=0 card impact (+21 ms, onset detector at file start); whooshes, swipes and the riser build into their hits by design.
Speech-to-text: both variants match the script word for word.
Checks failed: dead frame (2). Verdict: ANOTHER ROUND

## Round 2 (both variants re-rendered at 60 fps with the fixes, final mixes, 4 fps contact + phone sheets, plus the 4:5 crop)
| variant | hook | read | motion | variety | brand | sync | min |
| A       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |
| B       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |

All three round 1 fixes hold: the hook card fills the frame to y 1166 and the claim bar reads at phone size; "POLICY RECEIVED"
fills the gap after the logo; the umbrella band is on screen on the 5.29 / 5.34 s cut. 4:5 crop: nothing clipped, the umbrella
icon clears the top edge once landed. Remaining, minor: the "UMBRELLA LAYER" label is small at phone size (the brass slab and
the check carry the beat, and the caption says it).
Verdict: technical checks next.

## Round 3 (final deliverables, technical)
- Loudness: the linear loudnorm in mix.py stopped at -14.7 LUFS (true-peak ceiling). finalize.sh now adds the missing gain
  and a true-peak limiter: A -14.0 LUFS / -2.0 dBTP, B -14.1 / -1.9, all four files.
- ffprobe: 1080x1920 and 1080x1350, 60/1 fps, yuv420p, AAC 48 kHz on all four.
- Speech-to-text (ElevenLabs scribe_v1) matches both scripts word for word.
- Effects sync: median 10.3 ms (A) / 12.2 ms (B). Every percussive cue within 20 ms except the t=0 card impact (+21 ms,
  onset detector at file start). Over 20 ms and by design: whooshes, swipes and the drop riser, which build into their hits.
- Music bed: transcribes as "[outro jingle]", no vocals.
- Copy: no prices, percentages, carriers or guarantees; fine print "Coverage varies by policy and is subject to underwriting."
Verdict: READY

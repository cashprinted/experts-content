# Critique log: Already Insured v3 (motion-reel critique-pass rubric)

## Round 1 (variant A, full 60 fps render, 4 fps contact + phone sheets)
| hook | read | motion | variety | brand | sync | min |
|  7   |  6   |   8    |    8    |   9   |  8   |  6  |

Worst three:
1. [6.25-7.40] The declarations page covers the caption block; white caption words sit on white paper and vanish ("DECLARATIONS"). Fix: page enters from the right at y 40 (bottom now about 1040, above the captions at 1112).
2. [2.25-2.90] The hook's push toward the price (scale 1.12, y -60) lifts the card into the second headline ("CHECK THE PRICE?" overlaps the card top). Fix: push scale 1.08, y +40, so the card moves away from the headline.
3. [2.96-3.75] The drop opens on a small renewal panel in a mostly empty frame; the "RATE UPDATED" badge is tiny at phone size. Fix: panel 860 px wide, row type 60 px, badge type 40 px.

Also fixed from the sync check: the library's tick, chime, pop and stamp were timed to their loudest sample, which is up to 46 ms after you hear them. Hit times now use the attack (sfx.json `_note`). Median sync error went from 17.7 ms to 7.3 ms.
Checks failed: caption readability (1). Verdict: ANOTHER ROUND

## Round 2 (snapshots of every fixed moment, both variants)
| hook | read | motion | variety | brand | sync | min |
|  8   |  8   |   8    |    8    |   9   |  8   |  8  |

All three round 1 fixes hold: the page sits above the captions (6.5 to 7.3), the hook push no longer touches the headline (2.3, 2.7), the drop panel fills the frame width.
Variant B checked: headline readable at frame 0, card slams in under it, check badge on "insured", the premium bar and "?" on "overpaying".
Remaining, minor: the drop frame (2.96 to 3.75) still leaves the lower half of the frame dark for under a second; the caption carries it.
Verdict: render both variants for round 3.

## Round 3 (both variants, final 60 fps renders with the final mix, 4 fps contact + phone sheets)
| variant | hook | read | motion | variety | brand | sync | min |
| A       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |
| B       |  8   |  8   |   8    |    8    |   9   |  8   |  8  |

Checks: no clipped text, no caption on paper, every cut opens on the new image, longest gap without a new event 1.4 s,
end card holds 3 s. Speech-to-text matches both scripts word for word. -14.1 / -14.2 LUFS, peaks -1.1 / -1.4 dBTP.
60 fps, yuv420p, audio present on all four files. Effects sync: median 7.3 ms (whooshes and the riser build into
their hits by design). Music transcribes as an audio event only, no vocals.
Still open: for about 0.15 s as the drop scene changes (3.7 s in A), the rising bills pass over the fading "RATES CHANGE" caption.
Verdict: READY

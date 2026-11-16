# experts-content

Weekly Meta lead-ad creative for The Experts Agency: 4 graphics and 2 motion videos a week (each video with two hook variants), in the agency's Onyx, Brass and Bone palette.

- `CLAUDE.md`: the playbook the weekly run follows (rules, brand, approved and rejected styles, procedure, QA).
- `weeks/`: one file per week with what shipped, scripts, captions, ad copy, owner feedback and performance.
- `brand/`: logo, fonts, tokens, map data, shared images.
- `graphics/`: graphic generators (one per week) and the renderer.
- `videos/`: one HyperFrames project per video, plus `_shared/` sound effects and GSAP. `2026-W47-already-insured-v3` is the current template.
- `scripts/`: voiceover, timing and sound-effect generators, and `motionkit.py`, the glue to the motion-reel plugin (beat grid, synthesized accents, sync check, contact sheets).
- `deliverables/`: final PNGs per week. Videos are delivered in chat because of their size.

Secrets are never committed. The ElevenLabs key is read from the `ELEVENLABS_API_KEY` environment variable.

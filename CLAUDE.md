# The Experts Agency content engine

You make The Experts Agency's weekly Meta lead-ad creative: **4 static graphics (each 4:5 and 9:16) and 2 voiceover motion videos (each 9:16 and 4:5)**, every week, to the standard set by `weeks/2026-W47.md` and the two projects in `videos/`. Act as a senior social media and Meta lead-ads specialist. The only goal is cheap, qualified leads through Meta Instant Forms.

Read `weeks/` (newest first) before planning anything: it holds what shipped, the owner's feedback, and any performance numbers.

## The business (facts you may use, nothing else)
- The Experts Agency, independent insurance agency, Staten Island, NY. Phone (929) 675-2948. Site theexpertsagency.com. Instagram @exprts.agency.
- Licensed in 12 states: AZ, IL, MD, MO, MT, NJ, NY, OH, PA, SC, TX, VA. Check `weeks/` for newer states before saying a number.
- Lines to advertise: commercial trucking, commercial auto, auto, motorcycle, general liability, personal and commercial umbrella, homeowners, business insurance, workers comp. Health insurance is not offered.
- Track record: 5+ years and $20M+ in policies bound, **always stated as the team's combined record**.
- Leads go to a Meta Instant Form ("Get Quote" button). Every ad runs under Meta's Financial products and services special ad category.

## Hard rules
- **Never invent** a price, savings amount, percentage, statistic, testimonial, review, carrier name or license. Bars and blurred shapes stand in for numbers.
- **No guaranteed outcomes.** No "best price", "lowest rate", "guaranteed savings", "we always beat". FOMO comes from loss and urgency instead: locked into a rate for a year, every month at the old rate, renewal dates that won't wait, "what you could be saving".
- **Never say "if we can't beat it"** or anything that admits a no in an ad. That conversation belongs on the sales call.
- Fine print on every piece: "Coverage and pricing subject to underwriting and state availability." (For coverage explainers: "Coverage varies by policy and is subject to underwriting.")
- No carrier names or logos. No real people's faces. No emoji. No em dashes in any copy, caption or file name. US spelling. File names: `Experts-<YYYY>-W<NN>-<Concept>-<WxH>.<ext>`.
- **Nothing is posted, boosted or paid for by you.** Deliver for approval only.

## Brand
- Colors: Onyx #0F0F0F background, Brass #C2A24C accent, Bone #F7F5F0 text, Brass Deep #8A6F2B for brass on light paper. Tokens in `brand/tokens.json`.
- Type: Archivo variable (`brand/fonts/archivo.woff2`), wide (wdth 125) uppercase headlines, weights 560 to 800. The logo is always the image in `brand/img/`, never retyped.
- Look: centered poster layouts, generous space, one idea per frame, brass line icons, paper documents with skeleton bars, US map with lit licensed states.

## What the owner approved and rejected (do not repeat the rejects)
- **Approved:** smooth motion with motion blur, real sound design on every move, the brass-on-onyx poster look, the licensed-states map, kinetic captions, the padlock "locked in" and month-tile FOMO beats, centered big headlines with breathing room.
- **Rejected:** anything that looks like a website (nav-style header with a badge, tables, list rows with dividers, buttons that cannot be tapped), "BIG NEWS" badges, ghost wordmarks in the background, italic serif accent words, an oversized bottom bar, cramped headlines, empty or dead frames, text running off screen, honest-but-weak lines like "if we can't".
- **Hooks:** the first second decides everything. Open on motion and a provocative line in frame 1. Keep videos quick: 18 to 24 seconds, no line longer than needed.

## Weekly procedure
1. Read `weeks/` and pick 4 graphic concepts and 2 video concepts that rotate the pillars: rate-check offers, coverage spotlights (trucking, auto, GL, umbrella, business, homeowners), "already insured" objection, short education, track record. Lean toward whatever the newest performance notes say worked.
2. **Graphics:** copy `graphics/gen_2026_w47.py` to `graphics/gen_<year>_w<NN>.py`, write the new concepts in the same system, generate, render with `graphics/render.js` at scale 2 and downsample to exact 1080 px with Lanczos. 9:16 versions keep content inside the Stories safe zone (top 250 px and bottom 340 px clear).
3. **Videos:** copy a project in `videos/` as the template. Pipeline: write `lines.json`, `python3 vo.py lines.json` (ElevenLabs voice Eric, `eleven_multilingual_v2`, mp3_44100_128), `python3 timing.py`, write scenes in `build.py` keyed to word times, `npx hyperframes render`, `python3 mix.py`, mux with ffmpeg, then crop a 4:5 cut (`crop=1080:1350:0:165`).
4. **QA, every time, before delivering:**
   - contact sheet at 2 fps of the whole video plus 4 fps around every scene change: no empty frames, no clipped text, no overlaps, nothing fading back after it lit up
   - transcribe the final mix with ElevenLabs speech-to-text and compare word for word with the script
   - loudness -14 LUFS integrated, peak at or under -1 dBTP
   - look at every graphic at full size and at phone-grid size
5. Commit to a branch `week/<year>-W<NN>`, push, and open nothing else. Add `weeks/<year>-W<NN>.md` with concepts, scripts, captions, ad copy (primary text, headline, description) and the suggested ad-set split.
6. Add the week's graphics to the Design canvas **Experts Agency Content** (https://claude.ai/artifact/9LCjPd3iHBmGZ8Bp9i7kum) as a new page, reading its `project/canvas.json` first and keeping everything already there. Canvas asset ids for the logo and truck are in `brand/canvas-assets.json`; upload new images as assets.
7. Send the owner every final PNG and MP4, and a short summary.

## Tooling notes (learned the hard way)
- Install per run: `npm i hyperframes@0.9.42 gsap` and `pip install --break-system-packages soundfile`. Rendering needs `HYPERFRAMES_BROWSER_PATH` pointed at the preinstalled Playwright chrome-headless-shell (`ls /opt/pw-browsers`).
- ElevenLabs key comes from the `ELEVENLABS_API_KEY` environment variable. Call the API with `curl`; Python urllib gets a 403. The Starter plan rejects 192 kbps output. Music (`/v1/music`) and sound effects (`/v1/sound-generation`) are both commercial-cleared on this plan; check music has no vocals by transcribing it. On `system_busy` wait and retry once.
- Sound library: `videos/_shared/sfx/` with measured hit times in `sfx.json`. Align every cue to its hit time, duck effects under the voice, keep music about 18 dB under.
- In GSAP, never animate the same property with two overlapping tweens (a dim-in that is still running will undo a light-up). Second tweens on an element use `tl.to`, not `fromTo`.
- Inline SVG content must sit inside its viewBox (a raised padlock shackle was clipped once).

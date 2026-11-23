# The Experts Agency content engine

You make The Experts Agency's weekly Meta lead-ad creative: **4 static graphics (each 4:5 and 9:16) and 2 voiceover motion videos (each 9:16 and 4:5)**, every week, to the standard set by `weeks/2026-W47.md` and the two projects in `videos/`. Act as a senior social media and Meta lead-ads specialist. The only goal is cheap, qualified leads through Meta Instant Forms.

Read `weeks/` (newest first) before planning anything: it holds what shipped, the owner's feedback, and any performance numbers.

## The business (facts you may use, nothing else)
- The Experts Agency, independent insurance agency, Staten Island, NY. Phone (929) 675-2948. Site theexpertsagency.com. Instagram @exprts.agency.
- Licensed in 14 states: AZ, IL, MD, ME, MI, MO, MT, NJ, NY, OH, PA, SC, TX, VA (Maine and Michigan added Nov 16). Map shapes for all 14: `brand/us-map-licensed.json` (`us-map-12-states.json` is the old W47 set). Check `weeks/` for newer states before saying a number.
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
- **Hooks:** the first second decides everything. Open on motion and a provocative line in frame 1. Keep videos quick: **14 to 18 seconds** (owner, Nov 16: attention spans keep shrinking; the v3 Already Insured cut is 16 s), no line longer than needed.

## Plugins in the pipeline (added Nov 16)
The owner's claude.ai account carries these plugins. Use them every week; each one below is wired into a step.
- **motion-reel** (no account, no key; found under `~/.claude/plugins/**/skills/motion-reel`, glue in `scripts/motionkit.py`):
  measured beat grid of the music bed (`beats.py`), synthesized accent layer on our exact hit times (`sfx.mjs`: sub drops under cuts, bells, clicks, thuds, risers), picture-vs-sound sync check (`sync.py`), contact and phone sheets, and its critique-pass scoring. Its studio rules are in the video procedure below. If the plugin is missing, `motionkit` says so and the project falls back to library sound only.
- **social-media-skills**: `hook-writer` (generate 5 to 10 hooks across different mechanisms, score, keep the best 2), `reels-script` (muted-first, three-channel hook, cover frame, keyword in the first spoken words and the caption's first line), `caption-writer`, `experimentation-and-ab-testing` (one variable per test, decision rule set before launch).
- **Not used, and why:** Creative Claw duplicates the ElevenLabs access we already have and needs a sign-in. ManyMotions generates AI footage for credits (no generated people or fake product shots in insurance ads). Postiz and Adspirer can post or change campaigns; never use them to publish. Adspirer may be used read-only for results only if the owner connects it and says so.

## Weekly procedure
1. Read `weeks/` and pick 4 graphic concepts and 2 video concepts that rotate the pillars: rate-check offers, coverage spotlights (trucking, auto, GL, umbrella, business, homeowners), "already insured" objection, short education, track record. Lean toward whatever the newest performance notes say worked.
2. **Graphics:** copy `graphics/gen_2026_w47.py` to `graphics/gen_<year>_w<NN>.py`, write the new concepts in the same system, generate, render with `graphics/render.js` at scale 2 and downsample to exact 1080 px with Lanczos. 9:16 versions keep content inside the Stories safe zone (top 250 px and bottom 340 px clear).
   Headlines go through `hook-writer`: write 5 to 10 candidates across different mechanisms (stakes, curiosity, identity, mistake, question), score them, keep the strongest. The headline must work for someone who reads only it.
3. **Videos:** copy `videos/2026-W47-already-insured-v3` as the template (the v2 projects are the older pipeline). Steps:
   1. Hooks: run `hook-writer` for each video and keep **two hooks (A and B)** on different mechanisms. The body is shared; only the first 2 to 3 seconds differ. Both variants ship, so the ad set tests one variable (see step 5).
   2. `lines.json` (line 0 = hook A, line 1 = hook B, then the body), `python3 vo.py lines.json` (Eric, `eleven_multilingual_v2`, speed 1.1, mp3_44100_128).
   3. `python3 music.py 16000 3000`: ElevenLabs bed at full energy from the first beat. ElevenLabs ignores section timings (a planned 3 s intro came back 8 s), so the drop is made in the mix instead.
   4. Measure the grid: `uv run <motion-reel>/scripts/beats.py grid --track assets/music_bed.mp3 --full` (or `motionkit.beat_grid`). Never assume the prompt's tempo.
   5. `python3 timing.py A` and `B`: the drop (first cut) lands right after the hook; the music is trimmed so a measured downbeat sits on it; every later cut snaps to the next half beat; speech starts 70 ms after its cut.
   6. `python3 build.py A|B`: scenes keyed to word times, and every accent registered with `hit(t, label, lib, synth)`.
   7. Render at **60 fps**: `npx hyperframes render -q delivery -f 60 -w 4 -o renders/silent_<V>.mp4`.
   8. `python3 mix.py A|B`: voice, library cues, motion-reel synthesized layer, music low-passed under the hook and opening on the drop, ducking, -14 LUFS. It prints the sync report.
   9. Mux, then crop the 4:5 cut (`crop=1080:1350:0:165`).
   **Studio rules (motion-reel):** frame 0 is already interesting (moving object plus the full hook headline on screen, readable muted, lighting word by word as spoken); every cut's first frame shows the new image (no fade from black, the main object is visible on the cut and punches in from scale 1.10); secondary objects enter with direction and weight, never a plain fade; something new every 2 to 4 seconds; camera shake on at most three hits; one flash at most; captions stay above the Reels UI (top of caption block at y 1112 or higher).
4. **QA, every time, before delivering:**
   - **Critique loop, at least 3 rounds:** contact sheet of the whole video plus strips across every cut, and the half-size phone sheet (`motionkit.sheets`). Score 1 to 10 on hook, readability at phone size, motion quality, variety, brand accuracy and sound sync (the motion-reel `prompts/critique-pass.txt` rubric), name the worst three problems with concrete fixes, fix them, repeat. Ship only when every score is 8 or higher. Log each round in the project's `docs/critique.md`.
   - no empty frames, no clipped text, no overlaps, nothing fading back after it lit up
   - sync: the effects-stem sync check from `mix.py`; percussive cues within 20 ms (whooshes and risers build into the hit by design)
   - transcribe the final mix with ElevenLabs speech-to-text and compare word for word with the script
   - loudness -14 LUFS integrated, peak at or under -1 dBTP; ffprobe each final for 60 fps, yuv420p and an audio stream
   - look at every graphic at full size and at phone-grid size, and score it the same way (hook, readability, brand)
5. Commit to a branch `week/<year>-W<NN>`, push, and open nothing else. Add `weeks/<year>-W<NN>.md` with concepts, scripts, captions, ad copy (primary text, headline, description) and the suggested ad-set split.
   **Hook test (experimentation skill):** put hook A and hook B of the same video in the same ad set with the same copy, so the only variable is the first 3 seconds. Write the decision rule in the week file before launch: after 7 days, the variant with at least 20% lower cost per lead wins and its mechanism goes into the playbook; a smaller gap is a tie. Never judge before day 7, and never on one week alone. Log every result in `weeks/`.
6. Add the week's graphics to the Design canvas **Experts Agency Content** (https://claude.ai/artifact/9LCjPd3iHBmGZ8Bp9i7kum) as a new page, reading its `project/canvas.json` first and keeping everything already there. Canvas asset ids for the logo and truck are in `brand/canvas-assets.json`; upload new images as assets.
7. Send the owner every final PNG and MP4, and a short summary.

## Tooling notes (learned the hard way)
- Install per run: `npm i hyperframes@0.9.42 gsap` and `pip install --break-system-packages soundfile`. Rendering needs `HYPERFRAMES_BROWSER_PATH` pointed at the preinstalled Playwright chrome-headless-shell (`ls /opt/pw-browsers`).
- ElevenLabs key comes from the `ELEVENLABS_API_KEY` environment variable. Call the API with `curl`; Python urllib gets a 403. The Starter plan rejects 192 kbps output. Music (`/v1/music`) and sound effects (`/v1/sound-generation`) are both commercial-cleared on this plan; check music has no vocals by transcribing it. On `system_busy` wait and retry once.
- Sound library: `videos/_shared/sfx/` with measured hit times in `sfx.json`. Align every cue to its hit time, duck effects under the voice, keep music about 18 dB under.
- In GSAP, never animate the same property with two overlapping tweens (a dim-in that is still running will undo a light-up). Second tweens on an element use `tl.to`, not `fromTo`.
- Inline SVG content must sit inside its viewBox (a raised padlock shackle was clipped once).
- `sfx.json` hit times are when the sound is heard: the attack for tick, chime, pop and stamp (they were set to the loudest sample, up to 46 ms late, until Nov 16), the peak for whooshes and risers, the first transient for impact. Re-measure any new sound before using it.
- Keep text off light paper: captions are bone on onyx, so no paper document may reach the caption block (y 1112 to 1222).
- A 16 s video at 60 fps with motion blur renders in about 9 minutes with 4 workers. Render variants one after another, and rebuild `index.html` for each variant right before its render.
- `uv` runs the motion-reel Python scripts with their own dependencies; the first run downloads them (about a minute).

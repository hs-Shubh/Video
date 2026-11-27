# REPORT: Claude + Edits + Resolve reel

## Plan (written at the start)

1. Read the brief and the script. Build one vertical reel, 1080 x 1920, 30 fps, from the ElevenLabs voice, in HyperFrames.
2. Set up Node, ffmpeg, HyperFrames, Python, an ASR for word timings, Rhubarb and librosa.
3. Convert the MP3 to a 48 kHz WAV, time the 16 beats from the voice, save `timeline.json` and `docs/beats.md`.
4. Build captions (Roman Hinglish) and the overlay text from section 3b only.
5. Build the host avatar with lip sync, glass cards, the Playbook effects per beat, code-made music and sparse sound, the mix.
6. Compose the 16 beats on the voice timing, look test with 4 stills, render, run gates G1 to G14, fix and repeat.
7. Deliver the master, phone copy, no music version, teaser, srt, cover and this report into `renders/`.

Change from the brief, by your instruction: no screen recordings were supplied. Every screen is a stylised, generic recreation in HTML and CSS (MacBook frame, macOS style desktop, Terminal, Claude Desktop and Claude Code, an Edits style editor, a Resolve style workspace). No official logos or trademarked artwork. The Access Token only ever appears as the placeholder `token hidden` on a solid mask.

## Version 2 (27 Nov): real Edits footage, redrawn Resolve, more animation

- **Real Edits captures from the creator** replace the recreated Edits screens:
  - B05: the Edits installer (the drag to Applications is animated with the real app icon), the real login screen, the real Projects page.
  - B06: the real Settings > Automation recording. It is timed so the real toggle flip lands on the click sound, with a viewfinder lock on the toggle and a select box on the real Claude Code Copy button.
  - B07: the real Copy click on Claude Code.
  - B01, B03, B04, B16: the real Projects window on the opening and closing desktop.
- **Masked before use:** the Access Token (solid "token hidden" box on every frame), the login code, the login QR code and the profile photo. Raw files stay in the session uploads and are never copied into the project or git. Every masked frame was OCR checked against the real secrets (`build/footage_mask_check.json`: 293 frames, 0 hits). A positive control on a raw frame was flagged, so the check works.
- **Not used:**
  - The three Claude recordings. They show the `claude mcp add` command pasted into the Claude chat instead of Terminal, and Claude replying that it cannot operate Edits. So they are not proof of the Edits demo, and they also show the token.
  - The downloaded YouTube tutorial by another creator. No written permission was provided.
- **Resolve redrawn in the real app layout:** the Edit page with Media Pool, bins and clip names, dual viewers with timecode, V2/V1/A1 tracks with named clips and waveforms, the page bar, a Render Queue for the render step, and the Workspace > Scripts > Claude_MCP_Bridge path in the macOS menu bar. It is a generic drawing with no logos.
- **More animation** (requested by the creator):
  - In the hook, an orbit of three glass icons (Claude, Edits, Resolve) around the title. It passes behind the title and fades at its left edge, so it never covers a letter. The brief's Playbook lesson warned against orbit, so it is used once only.
  - A light sheen sweep and a flip-up tilt on every glass card entrance.
- **Action for the creator:** regenerate the Edits Access Token (Settings > Automation > Regenerate). It was visible in the shared screenshots and recordings.

## Deliverables

| File | What |
|---|---|
| `renders/EDITS_RESOLVE_9x16.mp4` | Master, 1080 x 1920, 30 fps, H.264 High, crf 17, preset slow, tune animation, AAC 320 kbps 48 kHz, from 2x frames with a Lanczos downscale |
| `renders/EDITS_RESOLVE_phone.mp4` | Phone copy, two pass, 23.0 MB (under 30 MB) |
| `renders/EDITS_RESOLVE_nomusic.mp4` | Same picture, voice and sound moments only |
| `renders/EDITS_RESOLVE_teaser.mp4` | 30.4 s teaser: B01, B02, B03, B12, B16 |
| `renders/captions.srt` | Roman Hinglish captions, 135 cues |
| `renders/cover.png` | S10 frame with the green `davinci connected` pill, host on the left, title CLAUDE + EDITS + RESOLVE with saffron plus signs, captions off |
| `timeline.json`, `docs/beats.md`, `assets/CREDITS.md` | Timing, beat table, credits |

Source: `reel/` (HyperFrames project, generated) and `build/` (generators and checks). `build/pipeline.sh` re-renders and re-delivers everything.

## Choices I made (where the brief was unclear or could not apply)

1. **ASR.** faster-whisper could not download its models: Hugging Face is blocked from this container. I used the brief's fallback, sherpa-onnx, with NVIDIA Parakeet TDT 0.6b v3 (from the sherpa-onnx GitHub releases). It is not a Hindi model, but it spelled the English anchors (Edits, Resolve, Claude, Terminal, Settings, Automation, bridge, MCP, popup, edit) correctly with word timestamps, which is all the timing needs. I also tried the Dolphin multilingual CTC model; its output was too poor to use.
2. **Paste file.** `voice/edits_resolve_elevenlabs_paste.txt` was not supplied. I used the Roman lines of section 3 as the beat text and caption source.
3. **Beat matching.** Needleman Wunsch alignment of the 277 caption words against the ASR words (phonetic similarity), with English anchors snapped, silence gaps for beat edges, and length-weighted spreading between anchors. 144 of 277 words are anchored to a measured ASR word.
4. **Length.** Voice 102.11 s plus 0.35 s lead in plus 0.6 s tail = 103.06 s. Inside 95 to 140 s, so no stop.
5. **Avatar.** No Day 1 rig was supplied. I drew a flat host in SVG and CSS: saffron hoodie, dark hair, 9 Rhubarb mouth shapes, seeded blinks every 3 to 5 s, head bob on saffron words, stepped arm motion (on twos). Poses: wave, point, hands up, shrug, 1/2/3 fingers, fist pump, thumbs up, arms crossed, nods.
6. **Rhubarb** ran in phonetic mode (language independent, suits Hinglish). Mouth cues inside measured silences are forced to rest.
7. **Layout for 9:16.** MacBook at the top (y 150 to 790), the host lower left (x 36 to 286, y 950 to 1360), overlays in a row under the laptop and in a zone to the right of the host, captions bottom-anchored at y 1580. Nothing important in the top 110 px, the bottom 330 px or the right 130 px below y 1000.
8. **Phone in B12** is about 36 percent of the frame height, not 70 percent. At 70 percent it would cover the host, the captions and the three B12 overlays.
9. **Two glass cards side by side (B03)** are stacked vertically to fit the zone right of the host.
10. **Max 3 overlay items.** Where the sheet would put 4 on screen, I grouped items into one glass list card: B02 Clips/Subtitles/Music, B07 the three checklist lines, B09 the three commands. In B09 the `Bridge runs inside Resolve` chip hands its row to `Restart Resolve once`. In B10 the breadcrumb leaves when `/mcp` types, after holding the clean menu path for 1.28 s.
11. **Long commands** wrap at `/` and `@` boundaries in a 32 px mono card, never cut off. The characters are exact.
12. **Source chips** in B03 ("Edits for Mac, Apple silicon", "Resolve free edition") are not in section 3b, so section 3b wins and they are left out.
13. **Captions** do not move up 120 px on fix cards: the layout already keeps them clear of the cards.
14. **Terminal and Claude output lines** are short illustrations: `marketplace added`, `installed`, `setup done, restart Resolve`, `davinci ✓ connected`, the Edits tool categories (Clips, Voiceover, Subtitles, Music, Sound effects, from section 2), `bridge is not running` in red. The pasted Edits command in B07 is shown only as the solid `token hidden` mask, never as text.
15. **J-cut** for B05 to B08 and B10: the picture cuts 6 to 10 frames after the voice, snapped to the music beat grid. B09 cuts in the gap before its voice, because the zoom portal is the transition.
16. **The host does not walk** between windows. It would cover the overlays in the 9:16 layout. It points instead, and steps back (scale 0.93) for the split screen.
17. **Music and sound** are code made (numpy), 96 BPM. The beat grid comes from librosa. 9 sound moments: sting, riser into impact, toggle click, chime on Edits connected, whoosh on the portal, menu click, chime on davinci connected, hit on the finished reel, closing sting. Each sits in a gap or one frame after a word. The exception is the whoosh, whose tail runs under the first word of B09.
18. **Loudness range.** The ElevenLabs voice is very even, and the mix measures LRA 3.0 LU, under the 4 to 7 LU target. Getting more range would need uneven voice levels, which would hurt clarity on phones. I left it.
19. **Cover** text is the title only. The pill is the S10 overlay.

## What I could not do

- faster-whisper and Whisper models (Hugging Face blocked). sherpa-onnx Parakeet was used instead.
- Listen. Audio is measured, not heard. Please do the listen test (headphones, phone speaker, muted with captions).
- The real Day 1 template, rig, fonts choice and sting: not supplied. Poppins ExtraBold, JetBrains Mono and a new code-made sting are used.

## Process notes

- Look test at 4 stills (S01, S03, S06) and a 15 still check of every scene before the first full render. Fixed: glass grain too strong, the S06 zoom cutting the toggle label, badge over the window title, mid-word wraps in mono boxes, the S08 zoom cropping the tool list, the host's hand touching chips.
- First 2x render: G9 found a tick row showing before its fix card (B13 to B15) and a stray paper plane at the start of B16. Both fixed, re-rendered.
- Second render: G12 found a 3 px head offset at the loop frame (overlapping head tweens). Fixed with absolute tweens and a reset to the frame 0 pose, re-rendered.
- Render time: about 11 minutes per full 2x render (3092 frames at 2160 x 3840, 4 workers, software GL), about 3.5 minutes of encodes.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 hook | Pass | Frame 0 shows the Edits and Resolve windows, the host and the first caption (`Maine`); the prompt bar types `edit my reel` from 0.35 s |
| G2 timing | Pass on measured words, 2 outliers | Final mix re-transcribed: 51 of 53 English anchor words start within 3 frames of their caption word (mean 0.54 frames, max 7.2 frames on 2 words). The other caption words are spread by length between anchors, so they cannot be measured one by one |
| G3 lip sync | Pass | 672 Rhubarb mouth cues; every cue inside a measured silence forced to rest (X) |
| G4 real proof | Partial | Real Edits footage for B05 to B07 and the desktop. The Edits demo (B02, B11, B12), Resolve, Terminal and Claude are recreations, because no working Edits demo or Resolve recording was supplied. Every command and menu name matches the brief exactly |
| G5 facts | Pass | All 35 overlay strings checked against the section 3b text by script; claims are only those in section 2 |
| G6 clarity | Pass | Every overlay holds to the end of its beat (at least 1 s after its trigger word); commands wrap, never cut off |
| G7 glass | Pass | At most two glass cards at once (B03, B11); no backdrop-filter anywhere; no glow or neon |
| G8 privacy | Pass | OCR of all 636 2x frames of S05 to S07 (every scene with real Edits footage): 0 token-like strings and 0 login codes; `token hidden` seen in 361 frames. Masked source footage: 293 frames, 0 hits |
| G9 frames | Pass | 2 frames each side of all 16 cuts: no blank frames (lowest contrast 22.3, blank is under 12), no single-frame flashes. Earlier render failed (stray tick row, stray icon), fixed |
| G10 brand | Pass | Navy #0E1422, one saffron accent #FF9F1C, green only for connected and done, red only for errors, Poppins ExtraBold and JetBrains Mono, code-made sting at the start and at the end |
| G11 audio | Pass, with one note | -14.0 LUFS integrated, true peak -1.9 dBTP, 48 kHz, short-term (3 s) between -17.5 and -11.9 LUFS, 9 sound moments only. Note: loudness range 3.0 LU, under the 4 to 7 LU target (see choice 18) |
| G12 loop | Pass | Last frame against frame 0: PSNR 48.8 dB, only 18 of 2,073,600 pixels differ by more than 20 levels (sub-pixel grid drift and compression). The sting fades in over 4 ms and the mix fades out, so there is no click at the loop. Earlier render failed (3 px head offset), fixed |
| G13 text | Pass | No em or en dashes in any caption, overlay, code file, srt or report (scripted scan) |
| G14 length | Pass | 103.07 s (95 to 140 s). Teaser 30.4 s |

## Privacy scan

Passed on the final render. 636 frames of S05, S06 and S07 at 2160 x 3840 were OCR scanned with tesseract. No token, key or long secret-like string was found. The Access Token row only ever shows the solid `token hidden` mask, and the pasted command in B07 is only the mask. No real names, emails or paths: the demo paths are `~/Footage/day1` and `~/Exports`. Result file: `build/privacy_scan.json`.

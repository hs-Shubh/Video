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

## Deliverables

| File | What |
|---|---|
| `renders/EDITS_RESOLVE_9x16.mp4` | Master, 1080 x 1920, 30 fps, H.264 High, crf 17, preset slow, tune animation, AAC 320 kbps 48 kHz, from 2x frames with a Lanczos downscale |
| `renders/EDITS_RESOLVE_phone.mp4` | Phone copy, two pass, about 23 MB (under 30 MB) |
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

GATES_TABLE

## Privacy scan

PRIVACY_LINE

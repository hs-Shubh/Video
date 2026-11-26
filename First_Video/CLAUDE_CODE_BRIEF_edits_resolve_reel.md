# CLAUDE + EDITS + DAVINCI RESOLVE: Faceless reel production brief

Faceless AI Creator profile, pillar Build, comment keyword **EDIT**. One vertical reel, 1080 x 1920, 30 fps, about 105 to 130 seconds, Hinglish, hosted by the **main host avatar** inside **Desktop World**.
Written 27 Nov 2026. Built on the **Video Playbook 2.2** (formats, effects and lessons). The story and the exact words are in `edits_resolve_reel_script.md`. This replaces the Resolve-only brief.

**To Claude Code:** read this whole file first, then the Day 1 Desktop World template and the avatar rig notes. Build with **HyperFrames**. Effect names in section 7 are the Playbook's names; use its "pro" settings for each. Where it says **STOP**, stop, show me, and wait. Keep one session per stage (timing, look test, scenes, sound, mix) so token use stays low. Every fact, command and menu name on screen must come from this file or from my recordings. If something is missing, **never invent it**: stop and ask. You cannot hear audio, so you measure it and I listen.

---

## How this works, in plain words

1. **I record the real setup** on my Mac: Edits, Terminal, Claude, Resolve. These recordings are the proof and the realism. Motion graphics make them clear and fast; they never replace them.
2. **The voice comes from ElevenLabs.** I hand you one WAV. You measure it and every timing comes from it.
3. **The main host avatar** lives in the desktop, reacts to each beat and points at the screen. Mouth shapes come from the voice with Rhubarb.
4. **Every scene** is a Desktop World scene: real recordings inside device frames, restrained frosted glass cards, word by word captions, cuts on the beat.
5. **Finish:** loudness mix, loop frame, cover, captions file. I add a licensed trending sound inside Edits afterwards.

---

## 0. Decisions (locked)

| Decision | Choice |
|---|---|
| Playbook format | **Faceless explainer** beats, with the **Screen-share tutorial** step pattern (hook, what we build, steps, gotchas, result, CTA) |
| Playbook look | **Dark tech (graph paper and glass)**, retuned to our brand kit: navy and saffron instead of violet and cyan, **flat icons instead of 3D emoji** |
| Format | 1080 x 1920, 30 fps, master from 2x frames |
| Length | Expected 105 to 130 s. Hard limits 95 to 140 s |
| Engine | HyperFrames (HTML to MP4) |
| Host | Main host avatar rig from Day 1 (`assets/avatar/host_rig/`), 9 mouth shapes, Rhubarb. No realistic twin in this reel |
| Voice | ElevenLabs, one WAV: `voice/voiceover.wav`. Text in `voice/edits_resolve_elevenlabs_paste.txt`, 16 paragraphs = 16 beats |
| Proof | Screen recordings (section 4). Real clicks, real output |
| CTA | One, in the last beat only: comment **EDIT**. Loop frame equals the first frame |
| Music | No trending song in the master. I add one from Edits' licensed library afterwards. Never upload a ripped copy, never type song lyrics |
| Captions | Roman Hinglish from section 3, word by word. Timing from Whisper, wording from this file |

### Brand kit (fixed)

| Element | Choice |
|---|---|
| Desktop | Deep navy `#0E1422` with a faint graph-paper grid and a slow camera drift |
| Accent | Electric saffron `#FF9F1C`. **One accent only** |
| Text | White. Success green `#2FD27A` only for "connected" and checks. Warning red `#FF4D4D` only for errors |
| Display font | The Day 1 choice, else **Poppins ExtraBold** |
| Mono font | The Day 1 choice, else **JetBrains Mono** |
| Sound logo | The Day 1 three note sting on the first window snap and on the last beat |
| Avatar | Same hoodie in the brand saffron, same hair, always |

---

## 1. What the Playbook taught us, and what we do about it

| Playbook lesson | In this reel |
|---|---|
| **Clean beats busy.** Real footage, flat cards and one accent colour won; glow, neon, 3D text, orbiting icons and studio replace lost (Dots reel) | Glass cards are allowed, but restrained: frosted and flat, one saffron accent, **no glow, no neon, no orbit, no 3D text** |
| Liquid glass is slow: pre-render the blur as a PNG, animate only transform and opacity, no live backdrop-filter on large areas | Every glass card uses a pre-rendered blurred crop of the desktop (section 6.3) |
| **Fewer sounds land harder.** 9 moments with real recordings beat 40 synthetic clicks | Sparse sound, 9 planned moments (section 9). No sound on every click |
| 3D emoji read as AI-made for news and business reels; flat line icons looked cleaner | Flat line icons only |
| Two stops before the full render: a 4 still look test, then a full length listen test | Pipeline gates 5 and 8 |
| Scrub every shot change for blank frames | Gate G9 |
| Render fast: heavy canvas filters once per frame, 2x frames as JPEG q 0.97, Lanczos downscale | Render step |
| Phones receive files only under 30 MB: send a two-pass 1080p copy | Deliverables |
| Add popular songs inside Instagram or Edits from the licensed library | Section 9 |
| Claude cannot hear: rank by measurement, a person picks by ear | Gates 8 and 11 |
| Fit the timeline to the real voice lengths, never to estimates | Section 5 |

---

## 2. Facts allowed on screen

Only these claims may appear as text, labels or diagrams. Anything else needs my yes.

| Fact | Beat |
|---|---|
| Edits for Mac runs only on Apple silicon (M1 or later) | B03 |
| Free Resolve blocks external scripting, so outside servers cannot connect | B03 |
| Edits: download Edits for Mac, sign in with Instagram | B05 |
| Edits: Settings, Automation, Enable Automation Server. The same screen has Copy buttons for Claude Code | B06 |
| Edits: paste the copied command in Terminal, press Enter, then fully quit and reopen Claude Desktop | B07 |
| Edits tool check prompt: "What tools does Edits have? Summarize them by category." If the tools are listed, it is connected | B08 |
| Resolve: three commands `/plugin marketplace add kingjamesch/davinci-resolve-mcp`, `/plugin install davinci-resolve@davinci-resolve-mcp`, `/davinci-resolve:setup`; restart Resolve once | B09 |
| Resolve menu: Workspace > Scripts > Claude_MCP_Bridge. `/mcp` lists `davinci` as connected | B10 |
| Edits can arrange clips, voiceover, subtitles, music and sound effects on its timeline, and everything stays editable by hand | B02, B11, B12 |
| Edits can post directly (Playbook 2.2 notes direct posting) | B12 |
| Fixes: Claude Desktop fully quit and reopened; bridge restarted with a project open; a blocking Resolve popup closed | B13 to B15 |
| "Edits for Mac, Apple silicon" and "Resolve 21.1, macOS" badges, **only if my recordings show them** | B05, B09 |

Not allowed: colour grading, Fairlight or Fusion on free Resolve, "replaces your editor", any number of minutes for setup, any claim about views or income.

---

## 3. The beats

The voice text is in `voice/edits_resolve_elevenlabs_paste.txt`, one paragraph per beat in this order. The Roman lines are the **caption source**. Bold words are the saffron highlight words.

| Beat | Caption lines (Roman, word by word) | Role |
|---|---|---|
| **B01** | Maine Claude ko **Instagram Edits** aur **DaVinci Resolve** se jod diya. Ab edit **bolkar** hota hai. | Hook |
| **B02** | Dekho: **ek prompt**, aur **clips, subtitles, music**, sab timeline pe lag gaye. | Proof |
| **B03** | Par log yahin **atakte** hain. Edits sirf **Apple silicon** Mac pe chalta hai, aur **free Resolve** mein Blackmagic bahar se control **band** rakhta hai. | Problem |
| **B04** | Pehle **Edits.** Phir **Resolve.** Phir dono **ek saath.** | Roadmap |
| **B05** | **Edits 1.** Instagram ki site se Mac ke liye Edits **download** karo, aur apne Instagram se **sign in** karo. | Step |
| **B06** | **Edits 2.** **Settings** kholo, **Automation** pe jao, aur **Enable Automation Server** on karo. Wahin Claude Code ke liye **Copy** dikhega. | Step |
| **B07** | **Edits 3.** Copy dabao, **Terminal** mein paste karke Enter. Phir Claude Desktop **poora band** karke dobara kholo. | Step |
| **B08** | **Edits 4.** Claude se poochho: Edits ke **tools** kya hain? List aa gayi, toh **connected.** | Step |
| **B09** | Ab **Resolve.** Free edition mein **bridge andar se** chalta hai. Claude Code mein **teen commands** paste karo, phir Resolve ek baar **restart** karo. | Step |
| **B10** | Phir **Workspace, Scripts, Claude MCP Bridge** pe ek click. **/mcp** mein **davinci connected** dikhega. | Step |
| **B11** | Ab **dono ek saath.** Bolo: Resolve mein is folder ke clips **import** karo, **timeline** banao, **render** karo. Phir bolo: Edits mein is render se **vertical reel** banao, **subtitles** aur **music** ke saath. | Payoff |
| **B12** | Reel timeline pe **taiyaar.** Haath se **tweak** karo, aur seedha **post** karo. | Result |
| **B13** | Atak gaye? **Teen fix.** **Ek:** Claude ko Edits ke tools nahi dikh rahe? Claude Desktop **poora band** karke dobara kholo. | Fix 1 |
| **B14** | **Do:** bridge is not running? Resolve mein **project kholo** aur bridge **dobara click** karo. | Fix 2 |
| **B15** | **Teen:** Claude atak gaya? Resolve mein koi **popup** khula hoga. Use **band** karo. | Fix 3 |
| **B16** | Poora **guide** chahiye? Comment karo **EDIT.** Commands **DM** mein aa jayenge. Aur yeh reel **Claude ne banayi** hai. | CTA |

Spoken numbers are words; on screen they are digits ("Edits 1"). No dashes anywhere.

---

## 3b. Overlay text sheet (every on-screen word besides the captions)

This is the complete list. **Nothing else may appear as text.** Each item appears on its **trigger word** (the first frame of that spoken word from the timeline, minus 1 to 2 frames), stays until the end of its beat, and never less than 0.6 s. Strings are exact, in the exact case shown.

| Style | Spec |
|---|---|
| Title | Display font ExtraBold, 64 to 72 px, white, saffron on the key part |
| Chip | Display font Medium, 34 to 36 px, glass pill, flat icon on the left |
| Mono | Mono font, 32 to 34 px, command and typed text, saffron cursor |
| Badge | Saffron circle or pill with the id, 56 px, top left of its window |
| Pill | Green (connected, done) or red (error), 34 px, rounded |
| Position | Above the caption line: between y 760 and y 1380. Never inside the Instagram zones |

| Beat | Trigger word | Overlay text (exact) | Kind |
|---|---|---|---|
| B01 | start | `edit my reel` (typed in the prompt bar) | Mono |
| B01 | "Edits" | **EDITS** | One-word pop |
| B01 | "Resolve" | **RESOLVE**, then the full title **CLAUDE + EDITS + RESOLVE** settles | One-word pop, Title |
| B02 | "ek prompt" | `1 prompt` | Chip |
| B02 | "clips" | `Clips` | Chip |
| B02 | "subtitles" | `Subtitles` | Chip |
| B02 | "music" | `Music` | Chip |
| B03 | "Edits" | **Edits for Mac** | Title on card 1 |
| B03 | "Apple silicon" | `Apple silicon (M1 or later)` | Chip, card 1 |
| B03 | "free Resolve" | **Resolve free** | Title on card 2 |
| B03 | "band" | `Outside control locked` | Chip, card 2 |
| B04 | "Edits" / "Resolve" / "ek saath" | Tracker labels `Edits`, `Resolve`, `Together`, one lights per spoken word | Chip x3 |
| B05 | "Edits ek" | `E1` | Badge |
| B05 | "download" | `Download Edits for Mac` | Checklist line 1 |
| B05 | "sign in" | `Sign in with Instagram` | Checklist line 2 |
| B06 | "Edits do" | `E2` | Badge |
| B06 | "Settings" | `Settings` > `Automation` > `Enable Automation Server` (each segment lights on its own spoken word) | Breadcrumb |
| B06 | "Copy" | `Copy for Claude Code` | Chip on the Copy button |
| B07 | "Edits teen" | `E3` | Badge |
| B07 | "Copy" | `Copy` | Chip |
| B07 | "Terminal" | `Terminal: paste, Enter` | Chip |
| B07 | "poora band" | `Quit Claude Desktop fully, reopen` | Chip |
| B08 | "Edits chaar" | `E4` | Badge |
| B08 | "poochho" | `What tools does Edits have? Summarize them by category.` (typed) | Mono |
| B08 | "connected" | `Edits connected` | Green pill |
| B09 | "Resolve" | `R1` | Badge |
| B09 | "bridge" | `Bridge runs inside Resolve` | Chip |
| B09 | "teen commands" | `/plugin marketplace add kingjamesch/davinci-resolve-mcp`, `/plugin install davinci-resolve@davinci-resolve-mcp`, `/davinci-resolve:setup` (three chips, one at a time, in order) | Mono |
| B09 | "restart" | `Restart Resolve once` | Chip |
| B10 | "Workspace" | `R2` | Badge |
| B10 | "Workspace, Scripts, Claude MCP Bridge" | `Workspace` > `Scripts` > `Claude_MCP_Bridge` (each segment lights on its word) | Breadcrumb |
| B10 | "/mcp" | `/mcp` (typed) | Mono |
| B10 | "connected" | `davinci connected` | Green pill |
| B11 | "dono ek saath" | `E+R` | Badge |
| B11 | "Resolve" | Prompt 1 as typed in recording R05: `In Resolve, import everything in ~/Footage/day1, make a timeline called Day 1 and render it to ~/Exports.` | Mono, left |
| B11 | "render" | render percent counter `0%` to `100%`, then `DONE` | Counter, green pill |
| B11 | "Edits" (second) | Prompt 2 as typed in recording E05: `In Edits, create a 9:16 vertical video under 45 seconds from the render in ~/Exports. Add subtitles at the bottom center and choose an upbeat track from the library.` | Mono, right |
| B12 | "taiyaar" | `Reel ready` | Pill (green) |
| B12 | freeze frame | `Editable by hand` | Label with outline |
| B12 | "post" | `Post from Edits` | Chip |
| B13 | "Ek" | Front `Edits tools not showing`, back `Quit Claude Desktop fully, reopen`, tick `1` | Card, checklist |
| B14 | "Do" | Front `bridge is not running`, back `Open a project, click Claude_MCP_Bridge again`, chip `Once per Resolve launch`, tick `2` | Card, chip |
| B15 | "Teen" | Front `Claude stuck`, back `Close the popup in Resolve`, tick `3` | Card |
| B16 | "Comment" | `EDIT` (typed into a comment box) | Typing box |
| B16 | "DM" | `Guide in your DM` | Chip |
| B16 | "Claude ne banayi" | `Made with Claude` | Chip |

Rules for this sheet:
- The **prompts in B11 are the target text**. Use the words that are actually visible in recordings R05 and E05; if they differ, the recording wins and you report the difference in `REPORT.md`.
- Folder names `~/Footage/day1` and `~/Exports` are demo names. Never show a real user name or path.
- Max 3 overlay items on screen at once, plus the caption. Fix cards and badges count as one item.
- On a fix card, move the captions up 120 px so nothing overlaps.
- The shot list in section 8 describes labels loosely (for example "editable by hand" in lower case). **If a label in section 8 differs from section 3b, section 3b wins.**

---

## 4. Inputs, and the recordings I make

Check all of this at the start of stage 1.

| File | What it is |
|---|---|
| `voice/voiceover.wav` | The ElevenLabs take I picked, 16 beats in order |
| `voice/edits_resolve_elevenlabs_paste.txt` | The exact text spoken, 16 paragraphs |
| `assets/avatar/host_rig/` | The main host rig from Day 1 |
| `recordings/` | The screen recordings below |
| `assets/music/` | A CC0 or code-made music bed. The beat grid is read from it |

How I record: macOS screen recording (Cmd+Shift+5), native resolution, cursor visible, **Do Not Disturb on**, Claude and Terminal at a large font, dark theme, a clean demo folder `~/Footage/day1`. One take per file with a little extra time at the start and end.

| ID | File | What it shows | Beat |
|---|---|---|---|
| E01 | `E01_edits_download.mov` | Edits for Mac open and signed in (the download page if I have it) | B05 |
| E02 | `E02_edits_settings.mov` | Settings, Automation, Enable Automation Server on, the Copy buttons. **The Access Token is on this screen** | B06 |
| E03 | `E03_edits_terminal.mov` | Copy pressed, Terminal, paste, Enter, then Claude Desktop quit and reopened. **The pasted command can contain the token** | B07 |
| E04 | `E04_edits_toolcheck.mov` | The tool check prompt and Claude listing Edits' tools by category | B08 |
| E05 | `E05_edits_timeline.mov` | The big prompt in Claude and the Edits timeline filling with clips, subtitles, music. Raw 45 to 90 s | B02, B11, B12 |
| E06 | `E06_final_reel.mov` | The finished reel playing, and the export or post screen | B12 |
| R01 | `R01_resolve_commands.mov` | The three commands run in Claude Code, with output | B09 |
| R02 | `R02_resolve_restart.mov` | Quit Resolve, reopen, project open | B09 |
| R03 | `R03_bridge_menu.mov` | Workspace, Scripts, Claude_MCP_Bridge, one click | B10 |
| R04 | `R04_mcp_connected.mov` | `/mcp` showing `davinci` connected | B10 |
| R05 | `R05_resolve_demo.mov` | The Resolve prompt: import, Day 1 timeline, render. Raw 45 to 90 s | B11 |
| X01 | `X01_bridge_not_running.mov` | Optional. The real "bridge is not running" message | B14 |
| X02 | `X02_popup.mov` | Optional. A real Resolve popup that blocks the bridge | B15 |

### Privacy: the Access Token

The Edits Settings screen shows an **Access Token**, and the copied command may contain it. It is a secret. Rules:

1. Mask every region that can show it (E02, and the command line in E03) with a solid mask, not a light blur, from the **first frame to the last**. I give you the mask boxes in `recordings/masks.json`; if they are missing, STOP and ask me.
2. After rendering, OCR every 2x frame of those scenes and fail the build if anything that looks like a token appears.
3. If a token is ever visible in a frame, STOP, tell me, and do not export.

**If an optional recording is missing:** build a clean card clearly marked as an illustration (a rounded card with the error words, no fake terminal or screenshot) and list it in `REPORT.md`. **If a required one is missing, STOP.** Never fake a success screen.

---

## 5. Timing: everything comes from the voice

1. Transcribe `voice/voiceover.wav` with faster-whisper, `language="hi"`, word timestamps. Whisper writes Hindi words in Devanagari and may mangle some. That is fine: it is used only for timing. If its models will not download, use sherpa-onnx with Parakeet for word timings.
2. Split the audio into 16 beats using the 16 paragraphs of the paste file. Match each beat's start and end with the English anchor words (Edits, Resolve, Claude, Terminal, Settings, Automation, bridge, mcp, popup, EDIT), which are spelled the same in the spoken text and in Whisper's output. Fall back to the silence gaps between paragraphs.
3. Inside each beat, spread the Roman caption words across the beat window, weighted by word length, snapping to the nearest Whisper word start wherever an English anchor exists.
4. Write `timeline.json` and `docs/beats.md`. **Never hard-code times from the script doc.**
5. Total length 95 to 140 s. If outside, STOP and tell me; I regenerate the voice.
6. Add 0.35 s of lead-in before B01 and 0.6 s after B16 for the loop.

---

## 6. Visual system: Desktop World, made realistic

The whole reel happens on one living Mac desktop. It zooms, tilts and re-frames, but never cuts to another world. The last frame returns to frame 1.

### 6.1 Frame and safe zones

| Item | Rule |
|---|---|
| Instagram UI zones | Nothing important in the top 110 px, the bottom 330 px, or the right 130 px below y 1000 |
| Margins | 60 px left and right |
| Captions | Centre, low third, above the bottom zone |
| Avatar | Lower left to centre, 380 to 520 px tall, never over a caption, command or menu path |

### 6.2 Realism kit

| Ingredient | Spec |
|---|---|
| Real UI | Screen recordings captured at 2x, shown in a **MacBook frame** (`device-in-scene`, `phone-mockup` blocks) at about 90 percent of the frame width; the finished reel in B12 shows in a **phone frame** at 70 percent of the frame height |
| Real window chrome | Keep the real macOS title bars and traffic lights from the recordings. Never redraw an app |
| Depth | Two layer soft shadows under every window (a tight contact shadow and a wide soft one). Background windows are pre-blurred 8 px; use **rack focus** (pre-rendered blur versions cross-faded) to move attention between windows |
| Light | One soft top-left key light on glass and window edges, a thin 1 px highlight on the top edge of every card, a faint 3 percent noise grain over the desktop |
| Motion | Slow push-in on every still moment (1.00 to 1.04), a slow camera drift on the grid, **cursor-follow zoom** on every recording (2x on click, ease in 0.4 s, hold at least 1.5 s, smoothed cursor path, click ripple) |
| Honesty | Real recordings, real output. No fake terminals, no fake timelines, no fake success states |

### 6.3 Glass cards (Playbook: liquid glass cards, pre-rendered)

| Property | Spec |
|---|---|
| Build | For each card position, render once a PNG of the desktop behind it blurred 28 px, cropped to the card, with the card's rounded mask. Animate **only transform and opacity** |
| Surface | Fill white at 8 percent over the blurred PNG, 1 px inner border white at 22 percent, a brighter 1 px arc along the top left, radius 36 px, noise 3 percent |
| Shadow | `0 2px 6px` at 35 percent black plus `0 24px 60px` at 45 percent black |
| Content | Flat line icon (28 px stroke), title in the display font, one line in mono if there is a command, a small saffron chip with the step id (E1 to E4, R1, R2, E+R) |
| Limit | No more than two glass cards on screen at once. No glow, no neon edge, no orbit |
| Entrance | Playbook **soft card entrance**: rise 24 px and fade in over 10 frames, easeOutCubic, cards leave with 6 frames of fade |

### 6.4 Captions (Playbook: word-synced and light-up chunk captions)

- Word by word, 1 to 3 words at a time (2 to 3 word chunks for steps). Display font ExtraBold. Only the **active word changes colour** (saffron for key words, white otherwise). Size 88 to 110 px with a 6 px navy outline and soft shadow.
- A chunk appears 1 to 2 frames early, holds at least 0.6 s. English technical words are never broken across lines.
- **One-word pop** only in the hook and for the step numerals. Not for the whole reel.

### 6.5 Cuts on the beat

Read the beat grid of the music bed with librosa. Every scene change and window snap lands on the nearest beat within 4 frames (**hard cut on the beat**). The voice never moves; the picture moves to the beat. Where a beat would split a spoken word, keep the word.

---

## 7. Effects used, by name (Video Playbook 2.2)

| Beat | Playbook effects |
|---|---|
| B01 Hook | One-word pop captions, kinetic typography on the title, slow push-in, soft card entrance, sting |
| B02 Proof | Device mockup (MacBook), cursor-follow zoom, **riser into impact** on the first populated clip, light-up chunk captions |
| B03 Problem | Two liquid glass cards, source chip ("Edits for Mac, Apple silicon" and "Resolve free edition"), select box snapping onto the locked row, rack focus between the cards |
| B04 Roadmap | **Chapter tracker** (three dots: Edits, Resolve, Together), step counter |
| B05 to B08 Edits steps | Device mockup, cursor-follow zoom, **digital zoom** (viewfinder lock) on the Enable Automation Server toggle, hand-drawn callouts or select box on the Copy button, animated checklist ticking per step, glass-wipe between steps, step counter, J-cut on the voice into each step |
| B09 Resolve 1 | **Zoom portal** from the Edits desktop into the Resolve desktop (a ring opens and the next scene is inside it), command chips flying out of the prompt bar, speed ramp on the Resolve restart |
| B10 Resolve 2 | Callout ring on the menu path, cursor-follow zoom, step counter, a green status pill |
| B11 Together | **Split screen** (Resolve left, Edits right), speed ramp on the long actions, number counter on the render percent, typing box for the two prompts |
| B12 Result | **Splash reveal (screen to world)** or **video inside a device**: the finished reel plays inside a phone frame, **freeze frame** for 0.4 s on the finished timeline with an outline and a label |
| B13 to B15 Fixes | **Card flip** (rotateY 0 to 180 over 12 frames, perspective 1200 px, content swapped at 90 degrees) for each error card, animated checklist for the three fixes, hand-drawn red circle on the blocking popup in B15 |
| B16 CTA | **End screen**, the word EDIT into a typing comment box, **seamless loop frame**, hold the last clean frame 0.6 s |
| Whole reel | Word-synced captions, hard cut on the beat, music ducking, **sparse sound** |

Left out on purpose, per the Playbook's lessons: orbit, orbit around a person, 3D emoji, hologram, headline storm, studio reveal, frame break, clone wave, 3D text.

---

## 8. Scene by scene (the shot list)

Times come from section 5. Avatar actions are in section 9.

| # | Beat | The picture | Motion and effects | Avatar | Notes |
|---|---|---|---|---|---|
| S01 | B01 | The navy desktop. Two app windows slide in, Edits left and Resolve right. A prompt bar types: "edit my reel". Title card: **CLAUDE + EDITS + RESOLVE** | Window snap on the first window with the sting, one-word pop on EDITS then RESOLVE, slow push | Enters bottom left, waves, then points at the windows | First 3 seconds must already show both apps, the host and a caption |
| S02 | B02 | E05: the Edits timeline fills with clips, subtitle blocks and a music track | Cursor-follow zoom on the first clip dropping in, riser into impact on it, speed ramp 4x during the fill, then 1x | Hands up in surprise | This is the proof. Show real output only |
| S03 | B03 | Two glass cards side by side: **Edits** with a chip "Apple silicon Mac" and **Resolve free** with a chip "outside control locked" | Rack focus from card 1 to card 2, a select box snaps onto the locked row, source chips under each fact | Shrugs, then points at the lock | Short. This is a friction line, not a lecture |
| S04 | B04 | The desktop clears. A chapter tracker with three dots: Edits, Resolve, Together | Step counter, dot 1 fills | Holds up one finger | Hold 1 s after the line |
| S05 | B05 | E01 inside the MacBook frame | Step badge E1, cursor-follow zoom on the download and the sign-in | Points at the window | The "Apple silicon" badge only if the recording shows it |
| S06 | B06 | E02 inside the MacBook frame | **Digital zoom** viewfinder locks on the Enable Automation Server toggle, select box on the Copy button, **token masked** | Points at the toggle | Mask check runs on this scene first |
| S07 | B07 | E03: Terminal, then Claude Desktop quit and reopen | Command chip flies from the Copy button to the Terminal, speed ramp on the quit and reopen, checklist ticks | Counts on fingers | **Command line masked** |
| S08 | B08 | E04: the tool check prompt and the tool list | Typing box, then the list lands, a green **Edits connected** pill, soft chime | Fist pump | Green appears here and on the Resolve pill only |
| S09 | B09 | The Edits desktop opens a ring (**zoom portal**) and the Resolve desktop is inside. R01 then R02 | Command chips (the three commands from section 2) fly out of the prompt bar and stack with ticks; the Resolve icon blinks off and on | Walks across to the right window, taps foot | Commands exactly as in section 2 |
| S10 | B10 | R03 then R04 | Callout ring on Workspace, then Scripts, then Claude_MCP_Bridge, click ripple, a green **davinci connected** pill | Points at the ring, then thumbs up | Hold the clean menu path for 1 s |
| S11 | B11 | Split screen: R05 on the left, E05 on the right. The two prompts type in turn | Typing boxes, speed ramp 4x, render percent counter, a **DONE** pill on the render, then an arrow from the Resolve render into the Edits timeline | Steps back, arms crossed, nods | Show only what is in the recordings |
| S12 | B12 | E06: the finished reel plays inside a phone frame at the centre | **Video inside a device**, freeze frame 0.4 s on the finished Edits timeline with an outline and the label "editable by hand", music drop for one line | Two thumbs up | Hold the finished reel at least 3 s |
| S13 | B13 | Glass error card 1: `Edits tools not showing`. Flips to the fix `Quit Claude Desktop fully, reopen` | Card flip, checklist item 1 ticks | Holds up one finger | One card at a time |
| S14 | B14 | Glass error card 2: `bridge is not running`. Flips to `Open a project, click Claude_MCP_Bridge again` | Card flip, tick 2. Use X01 inside the card if I have it | Two fingers | Small chip "once per Resolve launch" |
| S15 | B15 | Glass error card 3: `Claude stuck`. Flips to `Close the popup in Resolve` | Card flip, tick 3, hand-drawn red circle on the popup (X02 if I have it) | Three fingers, points at the popup | Captions move up 120 px while a card is on screen |
| S16 | B16 | The desktop pulls back to the exact first frame. The word **EDIT** appears large | **End screen**: the word types into a comment box, a DM paper plane flies out, sting. The frame ends on the opening frame | Waves, points down at the comment box | The last frame matches frame 0 |

---

## 9. Host avatar and sound

### Avatar

- The Day 1 rig and hoodie. **9 mouth shapes from Rhubarb** on `voice/voiceover.wav`, one swap per shape change. Blinks every 3 to 5 s, seeded so renders repeat. A small head bob on every saffron word. Body on twos, camera on ones.
- Acting beats make a cartoon feel human (wave, surprise, shrug, counted fingers, fist pump, nod). The host walks between windows in 10 to 14 frames. Never covers a command, a menu path, a mask or a caption.

### Sound (Playbook: sparse sound, ducking, J-cut)

| Layer | Spec |
|---|---|
| Voice | The ElevenLabs WAV. High-pass 80 Hz, gentle de-ess, 3:1 compression, about -16 LUFS before the mix. Use a **J-cut**: each step's first words start 6 to 10 frames before its picture |
| Music | CC0 or code-made bed from `assets/music/`, 15 to 20 dB under the voice, **sidechain ducked** while the voice speaks. A **music drop** to near silence for one line in S12 |
| **The 9 sound moments** | 1 the sting on the first window snap. 2 riser into impact on the first populated clip (S02). 3 one click on the Enable Automation Server toggle (S06). 4 a soft chime on **Edits connected** (S08). 5 a whoosh on the zoom portal (S09). 6 a click on the bridge menu item (S10). 7 a chime on **davinci connected** (S10). 8 a hit on the finished reel (S12). 9 the sting on the last beat (S16) |
| Everything else | Silent. No whoosh on every cut, no click on every ripple |
| Placement | A discrete sound never lands on a spoken word; it sits in the gaps or one frame after |
| Final | **-14 LUFS integrated, true peak -1 dB or lower, loudness range 4 to 7 LU, 48 kHz.** Check loudness in 5 s windows |

Every sound is CC0 or code-made and is listed in `assets/CREDITS.md`.

---

## 10. Do not do

- No cross dissolves, no glitch effects, no heavy blur on text.
- No more than three saffron elements competing in a frame. No text on top of text.
- Never show a fake terminal result, a fake Edits timeline or a fake Resolve screen.
- Never redraw an Instagram, Edits, Blackmagic or Anthropic logo as artwork.

---

## 11. Pipeline (with STOP gates)

1. **Preflight (STOP if anything required is missing).** List `voice/`, `recordings/`, `recordings/masks.json`, `assets/avatar/host_rig/`, `assets/music/`.
2. **Timing.** Section 5. Output `timeline.json` and `docs/beats.md`. **STOP** if the length is outside 95 to 140 s.
3. **Lip sync.** Rhubarb on the WAV, `build/mouth_cues.json`.
4. **Beat grid.** librosa on the music bed, `build/beats.json`.
5. **Look test (STOP, first and most important).** Build **S01, S03 and S06** completely: desktop, MacBook frame, one glass card, the mask, the host with lip sync, captions, sting. Render **4 stills** and a 10 s clip. I approve the look before anything else is built.
6. **Components.** `PromptBar`, `CmdChip`, `GlassCard` (pre-rendered blur), `DeviceFrame`, `StepBadge`, `ChapterTracker`, `CalloutRing`, `DigitalZoom`, `SelectBox`, `ClickRipple`, `StatusPill`, `Portal`, `SplitScreen`, `Counter`, `CardFlip`, `Checklist`, `TypingBox`, `CaptionEngine`, `MaskLayer`.
7. **Scenes.** Build S02, S04, S05 and S07 to S16.
8. **Stills (STOP).** A contact sheet of 12 stills at 2x. I approve.
9. **Render.** 2x JPEG frames at quality 0.97, 3 workers, Lanczos downscale. Scrub every shot change for blank frames.
10. **Privacy scan.** OCR every 2x frame of S06 and S07 and fail on any token-like string.
11. **Sound and mix.** Section 9. Transcribe the final mix with faster-whisper and confirm the voice is intact.
12. **Listen test (STOP).** I listen on headphones, a phone speaker, and watch muted with captions only.
13. **Encode** the deliverables. Write `REPORT.md`.

---

## 12. Quality bar

| Gate | Check |
|---|---|
| G1 hook | The first 3 seconds show both apps, the host and a caption |
| G2 timing | Every caption word starts within 3 frames of its spoken start |
| G3 lip sync | Mouth shapes follow the voice; no mouth movement during silence |
| G4 real proof | Edits steps, Resolve steps and the demo use real recordings; every visible command and menu name matches the recording exactly |
| G5 facts | Every claim on screen is in section 2, and every overlay string is in section 3b with its trigger word |
| G6 clarity | Each step stays readable at least 1 s after its spoken line ends; commands never cut off |
| G7 glass | At most two glass cards on screen; no live backdrop blur; no glow |
| G8 privacy | No token, email, API key or real name in any frame (OCR plus stills at 2x) |
| G9 frames | No blank or half-drawn frames at any shot change |
| G10 brand | Palette, fonts and sting match the brand kit; green and red only as specified |
| G11 audio | 9 sound moments only; -14 LUFS, true peak at or under -1 dB; voice clear on a phone speaker |
| G12 loop | The last frame equals frame 0 and the sting does not click at the loop |
| G13 text | No spelling mistakes, no em dashes or en dashes anywhere |
| G14 length | 95 to 140 s |

---

## 13. Deliverables

- `EDITS_RESOLVE_9x16.mp4` (master), `EDITS_RESOLVE_phone.mp4` (two pass, under 30 MB), `EDITS_RESOLVE_nomusic.mp4`
- Encode: H.264 High, `-crf 17 -preset slow -tune animation -pix_fmt yuv420p -movflags +faststart`, AAC 320 kbps 48 kHz
- **Teaser cut, 30 to 35 s:** B01, B02, B03, B12, B16
- `captions.srt` (Roman Hinglish), `cover.png`
- `timeline.json`, `docs/beats.md`, `assets/CREDITS.md`
- `REPORT.md`: what was built, which optional recordings were missing and what replaced them, privacy scan result, render time, problems and fixes

**Cover:** a frame from S08 or S10 with the green connected pill on the app window, the host smiling on the left, a big line **CLAUDE + EDITS + RESOLVE** in the display font, saffron on the plus signs. Inside the safe zones.

---

## 14. Hard rules

- HyperFrames for the picture. No Blender, no WebGL needed; the 3D look is CSS.
- No em dashes or en dashes in any text, file, caption or report.
- Never fake a terminal output, an Edits or Resolve screen, or a success state. A missing required recording means STOP.
- Never show, store or ask for my Access Token, tokens, passwords or API keys. Mask first, scan after.
- Only the main host avatar. Never my real face.
- Never delete files without asking me first.
- Instagram AI label on (AI voice and avatar). The caption says so.

---

## 15. Post pack

```
Maine Claude ko Instagram Edits aur DaVinci Resolve se jod diya. Ab edit bolkar hota hai. 🎬

Edits ka connection 4 steps mein, free Resolve ka bridge 2 steps mein, phir dono ek saath.

Commands aur prompts chahiye? Comment karo: EDIT 👇
Main DM mein poora guide bhej dunga.

Yeh reel Claude Code se banayi gayi hai. Voice made with AI.

#claudecode #instagramedits #davinciresolve #aitools #aiautomation
claude code hindi, instagram edits mac, davinci resolve free, claude mcp, ai video editing
```

AI label on. Pinned comment: "Comment EDIT, guide DM mein aa jayega 👇". The DM text is in `edits_resolve_reel_script.md`, section 5.

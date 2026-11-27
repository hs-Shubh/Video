# Version 4 plan: "something new every 3 to 4 seconds"

## 1. Audit: why version 3 still feels samey

Version 3 fixed the pacing *inside* one world: the camera cuts around the app screens every 2 seconds. But every cut is still **the same kind of picture**: a dark app UI. To a scrolling viewer, ten reframes of dark UI read as one long shot. The reference reels feel alive because they switch **worlds**, not framings:

| What the reference reels do | Version 3 today | Missing piece |
|---|---|---|
| Jump to the browser: typing in Google, a website loading | Never leaves the apps | **Browser moments** |
| Open GitHub, scroll a README, star count ticking | Commands only as text | **The source, shown** |
| App launch moments: icon bounce, splash screen, window flying open | Windows just appear | **App openings** |
| Joyful payoffs: things snapping together, confetti, "unlocked" | A green pill | **Celebration moments** |
| Real world B-roll: hands, phone, desk, a reaction | None | **Real world inserts** |
| Several zones alive at once: top, bottom, left, right | One panel plus the host | **Multi-zone layout** |
| Phone screen: the reel posted, comments, DMs arriving | None | **The phone world** |

**The rule for version 4:** every 3 to 4 seconds, change the **world**, not just the framing. Rotate between the 7 worlds below. Inside each world, something still moves every 1 to 2 seconds.

## 2. The 7 worlds

| # | World | Example in our reel | Who makes it |
|---|---|---|---|
| W1 | **App UI** (what we have) | Edits Settings toggle, Resolve menu | Done |
| W2 | **Browser** | Google search "instagram edits mac", the Edits download page, the GitHub repo of the Resolve plugin | **You record** (real browser, 10 to 15 s each) |
| W3 | **App launch** | Edits icon bouncing in the Dock and opening, the Resolve splash screen, `claude` starting in Terminal | **You record** |
| W4 | **Celebration motion graphics** | Claude, Edits and Resolve icons flying in and snapping together with a spark burst; "connected" with confetti; an "achievement unlocked" card per step (Level 1: Edits, Level 2: Resolve, Level 3: both) | **I build** |
| W5 | **Phone world** | Your phone: the finished reel playing in Instagram, a comment "EDIT" arriving, the DM with the guide popping in | **You record** your phone screen |
| W6 | **Real world B-roll** | Hands typing, a Mac on a desk, someone frustrated (problem beat), a reaction | **You film** on your phone, or free stock, or AI generated |
| W7 | **Kinetic text and stickers** | One huge word slammed on screen ("ATAKTE?", "3 STEPS", "BOOM"), sticker pops on the sides, a split screen that wipes | **I build** |

### The multi-zone layout (top, bottom, left and right always alive)
- **Top 60 percent:** the main world (W1, W2, W3, W5 or W6) changes every 3 to 4 s.
- **Side stickers:** small pop-ins (a check, an icon, an arrow, a number), alternating left and right about every 2 s.
- **Bottom:** captions always. The host pops in and out in a small corner bubble instead of standing there.
- **Full-frame takeovers:** about every 10 to 12 s a W4 or W7 moment takes the whole frame for 1 to 1.5 s, then hands back.

## 3. Beat by beat (voice and story unchanged)

| Time (s) | Beat | World sequence (about 3 to 4 s each) |
|---|---|---|
| 0 to 6.3 | Hook | W7 "EDIT BOLKAR" slam, W5 phone playing a finished reel, W4 three icons snapping together with a spark |
| 6.3 to 11.6 | Proof | W1 Edits timeline filling (real, if you record it), W7 "1 PROMPT" slam with clip icons raining onto tracks |
| 11.6 to 19.5 | Problem | W6 frustrated person at a laptop, W1 Mac "About This Mac" chip line, W4 a padlock snapping shut on Resolve |
| 19.5 to 23.4 | Roadmap | W4 a game-style level map: Edits, Resolve, Together |
| 23.4 to 29.7 | Edits 1 | W2 Google search, then the Edits site, W3 the installer and Edits opening |
| 29.7 to 37.7 | Edits 2 | W1 real Settings toggle (done), W4 "Server ON" switch with a spark |
| 37.7 to 44.6 | Edits 3 | W1 Copy click (done), W3 Terminal paste, Claude quitting and relaunching in the Dock |
| 44.6 to 49.6 | Edits 4 | W1 tool list, W4 **"Level 1 unlocked: Edits connected"** with confetti |
| 49.6 to 57.7 | Resolve 1 | W2 GitHub repo page with the star count, W3 `claude` launching in Terminal, the three commands |
| 57.7 to 64.1 | Resolve 2 | W3 Resolve splash screen, W1 menu path, W4 **"Level 2 unlocked: Resolve connected"** |
| 64.1 to 75.8 | Together | W4 the two app icons merging, W1 Resolve render and Edits timeline (split), W7 "DONO EK SAATH" |
| 75.8 to 80.0 | Result | W5 your phone playing the finished reel, W4 **"Level 3: reel ready"** |
| 80.0 to 96.4 | 3 fixes | W7 "GALTIYAN?" stamp, then per fix: W4 error card flip, W1 the real fix |
| 96.4 to 103.1 | CTA | W5 phone: a comment "EDIT" typed, the DM arriving, W7 the EDIT slam, loop to frame 0 |

## 4. What I need from you

### A. Mac screen recordings (Cmd+Shift+5, Record Entire Screen, Show Mouse Clicks on)
Wait 2 s before you start and 2 s at the end. Move calmly. Rename each file exactly as below.

| File | Record exactly this | Length |
|---|---|---|
| `W2_google.mov` | Open Chrome or Safari, click the search bar, type `instagram edits for mac` slowly, press Enter, click the Edits download result | 10 to 15 s |
| `W2_edits_site.mov` | The Edits for Mac page loading, scroll down once slowly | 8 s |
| `W2_github.mov` | Type `github.com/kingjamesch/davinci-resolve-mcp` in the address bar, press Enter, scroll the README slowly, rest on the star count | 12 s |
| `W3_edits_launch.mov` | Click Edits in the Dock and let it bounce and open to the Projects page | 6 s |
| `W3_resolve_launch.mov` | Click DaVinci Resolve in the Dock, record the splash screen and the project manager opening | 10 to 20 s (I speed it up) |
| `W3_claude_launch.mov` | Terminal open (run `PROMPT='%% '` first), type `claude`, press Enter, record the Claude Code welcome screen | 8 s |
| `W3_claude_relaunch.mov` | Quit Claude (Cmd+Q), then reopen it from the Dock | 6 s |
| `W1_edits_demo.mov` | **The most important one.** After the Terminal fix in DM_GUIDE.md, send the Edits prompt from Claude Code and record the Edits timeline filling until it stops | 30 to 90 s |
| `W1_about_mac.mov` | Apple menu > About This Mac, rest on the chip line (M1, M2 or later) | 5 s |

### B. Phone screen recordings (Control Center > Screen Recording)
| File | Record exactly this | Length |
|---|---|---|
| `W5_reel_playing.mp4` | Instagram open on a finished reel you made with Edits, playing full screen | 8 s |
| `W5_comment.mp4` | On any of your posts: tap comments, type `EDIT`, post it | 8 s |
| `W5_dm.mp4` | The DM inbox with the guide message arriving or open (test it with a second account) | 6 s |

### C. Real world B-roll (film on your phone, vertical, 4K or 1080p, 5 to 10 s each)
| File | Shot |
|---|---|
| `W6_hands_typing.mp4` | Close up of your hands typing on the Mac keyboard |
| `W6_desk.mp4` | Slow push towards your Mac on the desk, screen on |
| `W6_phone_scroll.mp4` | Your hand scrolling Instagram reels on the phone |
| `W6_reaction.mp4` | Optional: a "yes!" moment, hands only, or your face if you want it in the reel |

### D. Free stock or AI B-roll (only for shots you can't film)
Use only free-licence sites: **Pexels, Pixabay, Mixkit** (download the vertical 1080 x 1920 version). Or generate with **Gemini / Veo** and keep the AI label on.

Prompts that fit our navy and saffron look:
1. `Vertical 9:16, a young creator at a laptop at night, frustrated, hands on head, dark navy room, warm orange desk lamp, cinematic, 5 seconds`
2. `Vertical 9:16, macro shot of a glowing orange cable plugging into a laptop port, sparks, dark navy background, 4 seconds`
3. `Vertical 9:16, abstract tech loop, soft orange light streaks over a dark navy grid, slow camera push, 6 seconds, no text`
4. `Vertical 9:16, a phone on a desk lighting up with many notifications, dark room, warm light, 5 seconds`

**Please no Pinterest downloads or clips from other people's reels and videos.** They belong to their creators, and reused clips get reels muted or taken down.

### E. Decisions I need
1. **New on-screen words.** Version 4 adds short text beyond the brief's overlay sheet: "Level 1 unlocked", "GALTIYAN?", "BOOM", "DONO EK SAATH" and so on. OK?
2. **Your face** in any B-roll (W6 reaction), or hands only? The brief says never your real face, so the default is hands only.
3. **Length.** Keep the full 103 s, or also make a 45 to 60 s main cut? The research says shorter reels with a clean payoff often keep a higher share of viewers.

## 5. What I build myself (no input needed)

- **W4 celebrations:** icons flying in and snapping together with a spark burst, confetti on each "connected", achievement cards (Level 1, 2, 3) with a sound, a padlock snapping shut and open, and the two app icons merging.
- **W7 kinetic slams:** one huge word filling the frame for 0.8 to 1.2 s, with a whip or shake transition and a hit sound.
- **Side stickers** alternating left and right about every 2 s: check marks, arrows, small app glyphs, numbers.
- **Host as a corner bubble** that pops in and out.
- **More sound:** whooshes on world changes and pops on stickers, quiet and never on top of a word.

## 6. How we work, step by step

1. You answer the 3 decisions in section 4E.
2. Send what you can from 4A to 4D. **A and B matter most** (about 20 minutes of recording). C and D are extras.
3. I build W4 and W7 right away. They don't need your files.
4. When your recordings arrive, I mask anything private, place each one in its slot and send you 12 stills to approve.
5. Final render of all deliverables, plus the measured rhythm: worlds changed per 10 s, and the longest stretch without a new world.

Missing items fall back cleanly: no Google recording means a W7 slam in that slot, no phone recording means a W4 graphic. You can send things in batches.

# Edits and DaVinci Resolve capture guide

One document with everything you need to capture. Follow it top to bottom.

## What changes and what stays

| Stays as it is now (do not record) | Gets your real capture |
|---|---|
| Terminal and Claude Code windows (commands, `/mcp`, error line) | Instagram Edits app screens |
| Claude Desktop chat window | DaVinci Resolve screens |
| Host, captions, overlays, glass cards, sound, voice timing | The desktop that shows both apps side by side |

You can give me **screen recordings (best)** or **screenshots (works too)**. Every step below lists both. With screenshots I animate the cursor, clicks, zooms and the timeline filling between your "before" and "after" images. With recordings the motion is fully real.

---

## Part 0. Prepare your Mac once (15 minutes)

1. **Apps.**
   - Instagram Edits for Mac, latest version, signed in. It needs an Apple silicon Mac (M1 or later).
   - DaVinci Resolve, free edition, latest version. Note your exact version number (Resolve menu > About DaVinci Resolve) and tell me.
   - The Edits and Resolve connections from the reel already set up and working. You will show the setup steps again, but they must really work for the demo parts.
2. **Demo footage.** In Finder, create:
   - `Footage/day1` in your home folder, with 4 to 6 short clips (5 to 15 s each). Anything nice looking: travel, food, city.
   - An empty `Exports` folder in your home folder.
3. **A demo project in Resolve.** Open Resolve, create a new project named `Day 1 Demo`, leave it empty, quit Resolve.
4. **Look.**
   - System Settings > Appearance > **Dark**.
   - Plain dark wallpaper, desktop icons hidden (Finder > Settings > General: untick the items under "Show these items on the desktop").
   - Dock: keep it visible, remove apps you don't want seen.
5. **Privacy.**
   - **Do Not Disturb on** (Control Center > Focus).
   - Quit Mail, Messages, WhatsApp, Slack and anything that can show a popup.
   - Edits shows your Instagram handle and profile picture. If you don't want them seen, tell me and I'll cover them with a solid box.
   - The Edits Access Token: capture it normally. I cover it with a solid box on every frame, then scan every frame. You never need to hide it yourself.
6. **Screen size.** System Settings > Displays: keep the default resolution. Don't change it between captures.

## How to record

- Press **Cmd+Shift+5** > **Record Entire Screen**. Under Options, turn on **Show Mouse Clicks**, set Microphone to **None**, and choose where to save.
- To stop, click the stop button in the menu bar, or press Cmd+Ctrl+Esc.
- One step per file. Wait **2 seconds** before the first action and **2 seconds** after the last.
- Move the mouse calmly and **rest the pointer for 1 second** on each button before you click it.
- Loading and rendering waits are fine: I speed them up.
- If you make a mistake, record that file again from the start. Don't trim anything.

## How to take screenshots (if recording doesn't work)

- **Whole screen:** Cmd+Shift+3. Use this for every screenshot below, so all images match in size and position.
- Don't move or resize the app window between the screenshots of one step. I need the "before" and "after" images to line up exactly.
- Leave the mouse pointer out of the way at the edge of the screen. I draw my own pointer.
- Rename each screenshot to the exact name in the step.

---

## Part A. Instagram Edits

### A1. Download page and sign in (beat B05, about 6 s in the reel)

Steps:
1. Open Safari or Chrome and go to the Edits for Mac download page (`edits.instagram.com/desktop`). Scroll so the **Download** button is in the middle of the screen.
2. Start recording.
3. Rest on **Download**, click it.
4. Open Edits. If it shows the sign in screen, rest on **Sign in with Instagram** and click it, then finish signing in.
   - Already signed in? Then just open Edits and let its home screen load.
5. Wait 2 s, stop.

- Recording: `E01_edits_download.mov`
- Screenshots:
  - `E01_1_download_page.png`: the page with the Download button.
  - `E01_2_signin.png`: the Edits sign in screen, if you can get it.
  - `E01_3_home.png`: Edits home, signed in.

### A2. Settings, Automation, Enable Automation Server (beat B06, about 7.6 s)

Before you start, turn **Enable Automation Server OFF** so you can show it turning on.

Steps:
1. Edits open on its home or editor screen. Start recording.
2. Open **Settings** (where Edits keeps it, for example the gear icon or the Edits menu > Settings), and rest 1 s.
3. Click **Automation** and rest 1 s.
4. Rest on the **Enable Automation Server** switch, click it ON, rest 2 s.
5. Move to the **Copy** button for **Claude Code**, rest there 2 s. Don't click yet.
6. Stop.

- Recording: `E02_edits_settings.mov`
- Screenshots:
  - `E02_1_editor.png`: Edits before opening Settings.
  - `E02_2_settings.png`: the Settings window, first page.
  - `E02_3_automation_off.png`: the Automation page with the switch OFF.
  - `E02_4_automation_on.png`: the same page with the switch ON.

### A3. Copy button only (beat B07 start, about 1 s)

Only the click on Copy. The Terminal and Claude parts stay as they are now.

Steps:
1. Settings > Automation open, switch ON. Start recording.
2. Rest on **Copy** for Claude Code, click it. If it changes to "Copied" or similar, wait until that shows.
3. Wait 2 s, stop.

- Recording: `E03_edits_copy.mov`
- Screenshots: `E03_1_copy_before.png` and `E03_2_copy_after.png` (only needed if the button changes after the click).

### A4. Timeline filling from one prompt (beats B02 and B11 right side, about 5 s and 6 s)

This is the most important capture. It is the proof.

Steps:
1. In Edits, open an empty project (no clips on the timeline). Make the Edits window full screen or as large as possible, with the timeline clearly visible.
2. Start recording **before** you send the prompt, so the empty timeline is captured.
3. In Claude Code or Claude Desktop, send this prompt (you can do it on another screen or quickly switch back):
   `In Edits, create a 9:16 vertical video under 45 seconds from the render in ~/Exports. Add subtitles at the bottom center and choose an upbeat track from the library.`
   (For this capture, any clips in `~/Exports` work. If the Resolve render from A/B is not there yet, copy 2 or 3 clips from `Footage/day1` into `Exports`.)
4. Switch to Edits and keep recording while the clips, subtitles and music land on the timeline. Don't touch anything.
5. When everything has stopped moving, wait 3 s, stop. 45 to 120 s raw is fine.

- Recording: `E05_edits_timeline.mov`
- Screenshots, all with the window in the same place:
  - `E05_1_empty.png`: empty timeline.
  - `E05_2_clips.png`: clips on the timeline (take it as soon as the clips appear).
  - `E05_3_subtitles.png`: subtitles added.
  - `E05_4_full.png`: everything done: clips, subtitles, music, sound effects if any.

### A5. The finished reel and the post screen (beat B12, about 4 s)

Steps:
1. Same project as A4, finished. Start recording.
2. Press play and let the reel play for 5 s in the Edits preview.
3. Open the export or post screen and rest 3 s. **Don't press Post** unless you want to.
4. Stop.

- Recording: `E06_final_reel.mov`
- Also export the finished reel itself from Edits as a video file: `E06_reel_export.mp4`. I play it inside the phone frame, which looks far better than a recording of a preview.
- Screenshots: `E06_1_preview.png` (the preview playing) and `E06_2_post_screen.png`.

---

## Part B. DaVinci Resolve

### B1. Resolve with a project open (beats B09 and B14, background behind the Terminal)

Steps:
1. Open Resolve, open the `Day 1 Demo` project. Stay on the **Edit** page (the tabs at the bottom of Resolve).
2. Wait 2 s, take a screenshot. No recording needed.

- Screenshot: `R00_resolve_project.png`

### B2. Restart Resolve (beat B09 end, about 1 s, sped up)

Steps:
1. Resolve open with `Day 1 Demo`. Start recording.
2. Press **Cmd+Q** to quit Resolve (confirm if it asks).
3. Click Resolve in the Dock, wait for it to open, open `Day 1 Demo`.
4. Wait 2 s, stop.

- Recording: `R02_resolve_restart.mov`
- Screenshots: not needed. I can use `R00_resolve_project.png` with a quick fade.

### B3. Workspace > Scripts > Claude_MCP_Bridge (beat B10, about 4 s)

Steps:
1. Resolve open with `Day 1 Demo`. Start recording.
2. Rest on **Workspace** in the top menu bar, click it, rest 1 s.
3. Move down to **Scripts**, rest 1 s while the submenu opens.
4. Move to **Claude_MCP_Bridge**, rest 1 s, click it.
5. Wait 2 s, stop.

- Recording: `R03_bridge_menu.mov`
- Screenshots:
  - `R03_1_workspace_menu.png`: the Workspace menu open.
  - `R03_2_scripts_submenu.png`: the Scripts submenu open with Claude_MCP_Bridge visible.
  - Tip: Cmd+Shift+3 works while a menu is open. If the menu closes, use Cmd+Shift+5 > Options > Timer 5 seconds, then open the menu and wait.

### B4. Resolve doing the demo: import, timeline, render (beat B11 left side, about 6 s)

Steps:
1. Resolve open with `Day 1 Demo`, empty Media Pool, empty timeline. Start recording.
2. In Claude Code, send:
   `In Resolve, import everything in ~/Footage/day1, make a timeline called Day 1 and render it to ~/Exports.`
3. Switch to Resolve and record the clips arriving in the Media Pool, the **Day 1** timeline being built, and the render running on the **Deliver** page until it shows complete.
4. Wait 3 s, stop. 45 to 120 s raw is fine.

- Recording: `R05_resolve_demo.mov`
- Screenshots:
  - `R05_1_empty.png`: empty project.
  - `R05_2_media_pool.png`: clips in the Media Pool.
  - `R05_3_timeline.png`: the Day 1 timeline built.
  - `R05_4_rendering.png`: the render progress.
  - `R05_5_done.png`: the render finished.

### B5. A real blocking popup (beat B15, optional)

Only if you can trigger one naturally (for example a "Save project?" or "Media offline" dialog).

Steps:
1. With the popup on screen, start recording, wait 2 s, rest on its button, click it to close it, wait 2 s, stop.

- Recording: `X02_popup.mov`
- Screenshot: `X02_1_popup.png`

If you skip this, B15 keeps the clean illustrated popup card, marked as an illustration in REPORT.md.

---

## Part C. Both apps on one desktop (beats B01, B03, B04, B16: the opening and the end)

This is the very first frame people see, so make it neat.

Steps:
1. Open Edits with the finished timeline from A4, and Resolve with the Day 1 timeline from B4.
2. Place **Edits on the left half** of the screen and **Resolve on the right half**. They can overlap a little. Close everything else.
3. Take a screenshot.
4. Optional: record 5 s with the pointer resting still, as `D01_desktop_both.mov`.

- Screenshot: `D01_desktop_both.png`
- Extra screenshots:
  - `D01_edits_only.png`: Edits alone, same window position.
  - `D01_resolve_only.png`: Resolve alone, same window position.

  These are for B03 and B04, where one app is highlighted at a time.

---

## Checklist

Tick these off as you go. Recording or screenshots: either is fine for each line.

| Done | Part | Recording | Or screenshots |
|---|---|---|---|
| [ ] | A1 Download and sign in | `E01_edits_download.mov` | `E01_1` to `E01_3` |
| [ ] | A2 Settings, Automation | `E02_edits_settings.mov` | `E02_1` to `E02_4` |
| [ ] | A3 Copy button | `E03_edits_copy.mov` | `E03_1`, `E03_2` |
| [ ] | A4 Timeline filling | `E05_edits_timeline.mov` | `E05_1` to `E05_4` |
| [ ] | A5 Finished reel | `E06_final_reel.mov` + `E06_reel_export.mp4` | `E06_1`, `E06_2` + `E06_reel_export.mp4` |
| [ ] | B1 Resolve project | not needed | `R00_resolve_project.png` |
| [ ] | B2 Restart | `R02_resolve_restart.mov` | not needed |
| [ ] | B3 Bridge menu | `R03_bridge_menu.mov` | `R03_1`, `R03_2` |
| [ ] | B4 Resolve demo | `R05_resolve_demo.mov` | `R05_1` to `R05_5` |
| [ ] | B5 Popup (optional) | `X02_popup.mov` | `X02_1` |
| [ ] | C Both apps | `D01_desktop_both.mov` (optional) | `D01_desktop_both.png`, `D01_edits_only.png`, `D01_resolve_only.png` |
| [ ] | Your Resolve version number | | write it in your message |

## Export and send

1. **Recordings:** open each in QuickTime Player > **File > Export As > 1080p**. Keep the file names. This makes them small (about 20 to 80 MB each) and still sharp.
2. **Screenshots:** send them as they are (PNG).
3. Send everything **one of two ways**:
   - **Google Drive:** a folder named `First_Video_recordings`. Tell me when it's there; I read it through the Drive connector.
   - **GitHub:** the folder `First_Video/recordings/` on the branch `claude/dreamy-johnson-2s7i2c`. Each file must be under 100 MB.
4. In your message, tell me:
   - your Resolve version,
   - whether to cover your Instagram handle,
   - anything that looked different from this guide (menu names, button names). If the real app differs from the reel's overlays, the real app wins and I update the overlays.

## What I do next

1. Check every file, then cover the Access Token (and your handle if you want) with solid boxes on every frame. I OCR every frame and stop before export if anything shows.
2. Put your captures inside the MacBook frame (and the reel inside the phone frame). Add pointer, click and zoom effects where you used screenshots, and speed ramps where you recorded. Everything is fitted to the existing voice timing.
3. Send you 12 stills to approve, then render all deliverables again and rerun every gate.

# Screen recording guide (to replace the recreated screens)

The rest of the reel stays as it is: the voice timing, captions, host, overlays, glass cards, sound and mix. Only the picture inside the MacBook frame changes from recreated screens to your real recordings. I fit each recording to its beat with cursor follow zoom, speed ramps and the token mask.

## 1. Set up your Mac once, before recording

1. **Do Not Disturb on.** Quit Mail, Messages, Slack and anything else that can pop up.
2. **Dark mode on:** System Settings > Appearance > Dark.
3. **Hide personal details:**
   - Terminal: before each take run `PROMPT='%% '` (zsh) so the prompt shows only `%`, not your user name or Mac name.
   - Use a demo folder: create `~/Footage/day1` with 4 to 6 short clips, and an empty `~/Exports`.
   - Close Finder windows that show your name in the sidebar.
   - Claude Desktop shows your name or email in the bottom left of the sidebar. Collapse the sidebar if you can. If not, leave it and tell me: I will cover it with a solid mask.
   - Edits shows your Instagram handle. Tell me if you want it masked.
4. **Bigger text so it reads on a phone:**
   - Terminal: Settings > Profiles > Text > font size 18 or larger.
   - Claude Desktop: View > Zoom In once or twice.
   - Resolve and Edits: leave them at normal size; I zoom into them.
5. **Clean desktop:** hide desktop icons, use a plain dark wallpaper, and keep only the needed app windows open.
6. **Recording tool:** press Cmd+Shift+5, choose **Record Entire Screen**. Under Options, turn on **Show Mouse Clicks**, and set the microphone to **None**.

## 2. How to record each take

- One take per file. Wait **2 seconds** before the first action and **2 seconds** after the last one.
- Move the mouse calmly and **pause about 1 second** before each click, so I can zoom on the click.
- Natural speed is fine. I speed up waits (loading, rendering) with speed ramps.
- If something goes wrong, start that file again. Don't cut it yourself.

## 3. The recordings

Each beat shows how much screen time it has in the reel, so you know what must be visible. Raw takes can be longer.

| ID | File name | Beat (screen time) | Record exactly this |
|---|---|---|---|
| E01 | `E01_edits_download.mov` | B05 (6 s) | Browser on the Edits for Mac download page, click Download. Then Edits open on the sign in screen, click **Sign in with Instagram**, end on the signed in Edits home. If you are already signed in, record the download page and Edits opening signed in |
| E02 | `E02_edits_settings.mov` | B06 (7.6 s) | Edits open. Click Settings, click **Automation**, turn **Enable Automation Server** on, hover the **Copy** button for Claude Code for 2 s. The Access Token is on this screen: record it normally. I mask it from the first frame to the last, then OCR scan every frame |
| E03 | `E03_edits_terminal.mov` | B07 (6.5 s) | Click **Copy** for Claude Code. Open Terminal, paste (Cmd+V), press Enter, wait for the output. Then fully quit Claude Desktop (Cmd+Q) and reopen it from the Dock. The pasted command can contain the token: I mask that line too |
| E04 | `E04_edits_toolcheck.mov` | B08 (5.1 s) | In Claude Desktop, type `What tools does Edits have? Summarize them by category.`, press Enter, wait until the full list of tools is on screen, hold 3 s |
| E05 | `E05_edits_timeline.mov` | B02 (5 s) and B11 (right half, 11.5 s) | In Claude, type the prompt below and send it. Then switch to Edits and record the timeline filling with clips, subtitles and music until it stops. 45 to 90 s raw is fine |
| E06 | `E06_final_reel.mov` | B12 (3.8 s) | The finished reel playing in Edits for 5 s, then the export or post screen for 3 s. Do not press Post unless you want to |
| R01 | `R01_resolve_commands.mov` | B09 (7.5 s) | Resolve open with a project. In Claude Code (Terminal), run the three commands one by one, waiting for each output: `/plugin marketplace add kingjamesch/davinci-resolve-mcp`, then `/plugin install davinci-resolve@davinci-resolve-mcp`, then `/davinci-resolve:setup` |
| R02 | `R02_resolve_restart.mov` | B09 (end) | Quit Resolve (Cmd+Q), reopen it, open the same project |
| R03 | `R03_bridge_menu.mov` | B10 (6.4 s) | In Resolve, click **Workspace** > **Scripts** > **Claude_MCP_Bridge**. Pause 1 s on each menu before moving on |
| R04 | `R04_mcp_connected.mov` | B10 (end) | In Claude Code, type `/mcp`, press Enter, hold 3 s on the list showing **davinci** connected |
| R05 | `R05_resolve_demo.mov` | B11 (left half, 11.5 s) | In Claude Code, type the Resolve prompt below and send it. Record Resolve importing the clips, building the Day 1 timeline and rendering to the end. 45 to 90 s raw is fine |
| X01 | `X01_bridge_not_running.mov` | B14, optional | Only if it happens to you: the real "bridge is not running" message |
| X02 | `X02_popup.mov` | B15, optional | Only if it happens to you: a Resolve popup that blocks the bridge, then you closing it |

Prompts to type (they match the on screen text in the reel):

- **R05:** `In Resolve, import everything in ~/Footage/day1, make a timeline called Day 1 and render it to ~/Exports.`
- **E05:** `In Edits, create a 9:16 vertical video under 45 seconds from the render in ~/Exports. Add subtitles at the bottom center and choose an upbeat track from the library.`

If Claude or the apps show different words, menu names or output than the reel expects, **that is fine**: the recording wins, and I update the overlays to match and list the differences in REPORT.md.

If X01 or X02 are missing, B14 and B15 keep their clean fix cards and are marked as illustrations in REPORT.md.

## 4. Export and send

1. Open each file in QuickTime Player > **File > Export As > 1080p**. This keeps the files small (about 20 to 80 MB each) and sharp enough for my 2x zoom.
2. Keep the exact file names from the table (`.mov` is fine).
3. Send them **one of two ways**:
   - **GitHub:** put them in `First_Video/recordings/` on the branch `claude/dreamy-johnson-2s7i2c` and push. Each file must be under 100 MB.
   - **Google Drive:** put them in a folder named `First_Video_recordings` and tell me. I can read it through the Drive connector.
4. Optional: if you know where the token is on screen, add `recordings/masks.json` with the box in pixels, for example `{"E02": [[x, y, w, h]], "E03": [[x, y, w, h]]}`. If you don't, I find the boxes myself and show you stills before rendering.

## 5. What I do when they arrive

1. Check every file: length, resolution, the correct screens.
2. Mask the token in E02 and E03 with a solid box from the first frame to the last, then OCR every frame. If any token is visible anywhere, I stop and tell you before exporting anything.
3. Put each recording inside the MacBook frame (and the phone frame for E06). Add cursor follow zoom on each click, speed ramps on waits, and fit everything to the existing voice timing.
4. Show you 12 stills for approval, then render the master, phone copy, no music version, teaser, srt and cover again, and rerun all gates.

# DM guide for the EDIT comment automation

Sent automatically when someone comments **EDIT**. Generic for everyone: no personal names, folders or paths. Instagram caps an automated DM at about 1000 characters, so the guide is split into 3 messages, sent one after another. Each one is under that limit.

---

## Message 1 of 3: Edits

```
Yeh lo, Claude + Edits + DaVinci Resolve setup 👇 (1/3)

EDITS (Mac with Apple silicon, M1 ya naya)
1. edits.instagram.com/desktop se Edits for Mac download karo, Instagram se login karo.
2. Edits mein Settings > Automation kholo, "Enable Automation Server" ON karo.
3. "Connect an AI client" mein Claude Code ke saamne Copy dabao.
4. Terminal kholo, paste karo, Enter. (Claude chat mein paste mat karna, sirf Terminal mein.)
5. Claude ko poora band karo (Cmd+Q) aur dobara kholo.
6. Claude Code se poochho: "What tools does Edits have? Summarize them by category."
Tools ki list aa gayi = connected ✅

⚠️ Access Token kisi ko mat dikhana, screen record ya share mat karna. Galti se dikh gaya toh Settings > Automation mein Regenerate dabao.
```

## Message 2 of 3: DaVinci Resolve

```
RESOLVE (free ya Studio, macOS) (2/3)

1. Resolve kholo aur koi bhi project open karo.
2. Claude Code mein yeh 3 commands ek ek karke chalao:
/plugin marketplace add kingjamesch/davinci-resolve-mcp
/plugin install davinci-resolve@davinci-resolve-mcp
/davinci-resolve:setup
3. Resolve band karke dobara kholo, project open karo.
4. Resolve mein Workspace > Scripts > Claude_MCP_Bridge pe click karo.
5. Claude Code mein /mcp likho. "davinci" connected dikhna chahiye ✅

Note: bridge har baar Resolve kholne ke baad ek baar click karna padta hai.
```

## Message 3 of 3: Both together, and fixes

```
DONO EK SAATH (3/3)

Apne clips ek folder mein rakho, aur ek khaali folder banao exports ke liye. Phir Claude Code mein bolo (folder names apne daalo):

"In Resolve, import everything in [CLIPS FOLDER], make a timeline called Day 1 and render it to [EXPORT FOLDER]."

Phir:
"In Edits, create a 9:16 vertical video under 45 seconds from the render in [EXPORT FOLDER]. Add subtitles at the bottom center and choose an upbeat track from the library."

Reel Edits ki timeline pe aa jayegi. Haath se tweak karo aur post karo 🎬

ATAK GAYE?
1. Edits ke tools nahi dikh rahe: Claude poora band karke dobara kholo.
2. "bridge is not running": Resolve mein project kholo, Claude_MCP_Bridge dobara click karo.
3. Claude atak gaya: Resolve mein koi popup khula hoga, use band karo.
```

---

## Notes for setting up the automation

- **Trigger:** a comment containing `EDIT` (any case) on this reel. Reply publicly with a short line, for example "DM check karo 👇", and send the 3 messages to the commenter.
- **Spacing:** send the messages one after another, 2 to 3 seconds apart, so they arrive in order.
- **Placeholders:** the quotes and `[CLIPS FOLDER]` and `[EXPORT FOLDER]` are meant for the viewer to replace. Paste the text exactly as written.
- **Requirements a viewer needs:** a Mac with Apple silicon for Edits, a Claude plan that includes Claude Code, and DaVinci Resolve on macOS. Message 1 and 2 say this up front.
- **Lesson from your own test:** step 4 in message 1 says the command goes in **Terminal**, not in the Claude chat. Pasting it into the chat is exactly what stopped Edits from connecting in your recording.
- **Before it goes live:** run through the 3 messages once yourself on a clean setup. Check that the menu names and the plugin commands still match the current Edits and Resolve versions. The Resolve plugin is a small community project and could change.

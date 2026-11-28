# Voice script with expression (for ElevenLabs)

Same 16 beats and **the same words** as now, so the captions and overlays still fit. Only the **delivery** changes: where to pause, go loud, go soft, get excited or sound let down.

## How to read the marks

| Mark | Meaning |
|---|---|
| `/` | Short breath, about 0.3 s |
| `//` | Real pause, about 0.7 s |
| **BOLD CAPS** | Hit this word harder and a little louder |
| *(low)* | Drop the volume, closer to the mic, like telling a secret |
| *(up)* | Lift the energy, smile while speaking |
| Energy 1 to 5 | 1 = calm and soft, 5 = big excitement |

---

## Part 1: performance script (read this if you record your own voice)

| Beat | Energy | Delivery | Line |
|---|---|---|---|
| B01 Hook | 5 | Fast, proud, like sharing a secret win. Smile. Slight pause before "bolkar" | Maine **CLAUDE** ko / Instagram **EDITS** aur DaVinci **RESOLVE** se jod diya. // Ab edit... / **BOLKAR** hota hai. |
| B02 Proof | 4 | Showing off, quick list, each item a little louder | Dekho: // **ek prompt**, / aur **clips**, / **subtitles**, / **music**, / sab timeline pe lag gaye. |
| B03 Problem | 2 | Let down, slower. Sigh before "Par". Go *(low)* on Blackmagic, like it's unfair | *(sigh)* Par log yahin / **ATAKTE** hain. // Edits sirf **Apple silicon** Mac pe chalta hai, / aur free Resolve mein / *(low)* Blackmagic bahar se control / **BAND** rakhta hai. |
| B04 Roadmap | 3 | Calm, clear, counting on fingers, a beat between each | Pehle **Edits.** // Phir **Resolve.** // Phir dono / **EK SAATH.** |
| B05 Edits 1 | 3 | Teacher voice, steady, friendly | **Edits ek.** // Instagram ki site se Mac ke liye Edits **download** karo, / aur apne Instagram se **sign in** karo. |
| B06 Edits 2 | 3 | Steady, slow on the menu names so people can follow | **Edits do.** // **Settings** kholo, / **Automation** pe jao, / aur **Enable Automation Server** on karo. // Wahin Claude Code ke liye **Copy** dikhega. |
| B07 Edits 3 | 3 | Brisk, step by step, slight warning tone on "poora band" | **Edits teen.** // Copy dabao, / **Terminal** mein paste karke Enter. // Phir Claude Desktop / **POORA BAND** karke / dobara kholo. |
| B08 Edits 4 | 3 then 5 | Curious question, then a small pause, then a happy "connected" | **Edits chaar.** // Claude se poochho: / Edits ke **tools** kya hain? // List aa gayi... / toh *(up)* **CONNECTED!** |
| B09 Resolve 1 | 3 | Fresh start, a new chapter, a bit lower | *(up)* Ab **RESOLVE.** // Free edition mein bridge / **andar se** chalta hai. // Claude Code mein **teen commands** paste karo, / phir Resolve ek baar **restart** karo. |
| B10 Resolve 2 | 3 then 5 | Slow on the menu path, then the payoff, excited | Phir **Workspace**, / **Scripts**, / **Claude MCP Bridge** / pe ek click. // Slash MCP mein / *(up)* **DAVINCI CONNECTED** dikhega! |
| B11 Together | 4 | Build up, faster, like the magic part. Slightly bigger on each command | Ab / **DONO EK SAATH.** // Bolo: / Resolve mein is folder ke clips **import** karo, / **timeline** banao, / **render** karo. // Phir bolo: / Edits mein is render se **vertical reel** banao, / **subtitles** aur **music** ke saath. |
| B12 Result | 5 | Proud, relaxed, smiling. A short pause after "taiyaar" | Reel timeline pe / **TAIYAAR.** // Haath se **tweak** karo, / aur seedha **POST** karo. |
| B13 Fix 1 | 2 then 3 | Sympathetic, *(low)*, like a friend. Then helpful | *(low)* Atak gaye? // *(up)* **Teen fix.** // **Ek:** / Claude ko Edits ke tools nahi dikh rahe? // Claude Desktop **poora band** karke / dobara kholo. |
| B14 Fix 2 | 3 | Quote the error a little flat, like reading it, then calm fix | **Do:** / "bridge is not running"? // Resolve mein **project kholo** / aur bridge **dobara click** karo. |
| B15 Fix 3 | 3 | Light, almost amused, it's an easy fix | **Teen:** / Claude atak gaya? // Resolve mein koi **popup** khula hoga. / Use **band** karo. *(light laugh)* |
| B16 CTA | 4, then 2, then 4 | Big ask, then *(low)* reveal, then a warm smile on the last word | Poora **guide** chahiye? // Comment karo / **EDIT.** // Commands **DM** mein aa jayenge. // *(low)* Aur yeh reel... / Claude ne / *(up)* **BANAYI** hai. |

---

## Part 2: ElevenLabs paste text (audio tags)

Use the model **Eleven v3**. It understands audio tags in square brackets, which are not spoken. Paste everything in the box below, keeping the blank lines: 16 paragraphs = 16 beats.

```
[excited] Maine Claude ko Instagram Edits aur DaVinci Resolve se jod diya. [short pause] Ab edit... BOLKAR hota hai.

[confident] Dekho: [short pause] ek prompt, aur clips, subtitles, music, sab timeline pe lag gaye.

[sighs] Par log yahin atakte hain. [disappointed] Edits sirf Apple silicon Mac pe chalta hai, aur free Resolve mein [whispers] Blackmagic bahar se control band rakhta hai.

[calm] Pehle Edits. [short pause] Phir Resolve. [short pause] Phir dono... ek saath.

[friendly] Edits ek. Instagram ki site se Mac ke liye Edits download karo, aur apne Instagram se sign in karo.

[friendly] Edits do. Settings kholo, Automation pe jao, aur Enable Automation Server on karo. Wahin Claude Code ke liye Copy dikhega.

[friendly] Edits teen. Copy dabao, Terminal mein paste karke Enter. [serious] Phir Claude Desktop poora band karke dobara kholo.

[curious] Edits chaar. Claude se poochho: Edits ke tools kya hain? [short pause] List aa gayi... [excited] toh connected!

[energetic] Ab Resolve. [calm] Free edition mein bridge andar se chalta hai. Claude Code mein teen commands paste karo, phir Resolve ek baar restart karo.

[calm] Phir Workspace, Scripts, Claude MCP Bridge pe ek click. [excited] Slash MCP mein davinci connected dikhega!

[excited] Ab dono ek saath. Bolo: Resolve mein is folder ke clips import karo, timeline banao, render karo. Phir bolo: Edits mein is render se vertical reel banao, subtitles aur music ke saath.

[proud] Reel timeline pe taiyaar. [short pause] Haath se tweak karo, aur seedha post karo.

[softly] Atak gaye? [short pause] [friendly] Teen fix. Ek: Claude ko Edits ke tools nahi dikh rahe? Claude Desktop poora band karke dobara kholo.

[matter-of-fact] Do: bridge is not running? Resolve mein project kholo aur bridge dobara click karo.

[amused] Teen: Claude atak gaya? Resolve mein koi popup khula hoga. Use band karo. [chuckles]

[excited] Poora guide chahiye? Comment karo EDIT. Commands DM mein aa jayenge. [whispers] Aur yeh reel... [warmly] Claude ne banayi hai.
```

### ElevenLabs settings
- **Model:** Eleven v3, which supports the tags. If your model reads the tags out loud, delete everything in `[ ]`. The `...` and `!` still shape the delivery.
- **Voice:** your clone (Bhavesh PVC).
- **Stability:** **Creative** or **Natural** for more emotion. Robust sounds flatter.
- **Hindi pronunciation:** if a Hindi word sounds off, write just that word in Devanagari, as in your old paste file. The tags stay in English.
- **Generate 3 takes** and pick the most human one. Listen especially to B03 (the sigh), B08 and B10 ("connected!"), and B16 (the whisper reveal).
- **Download as WAV** from History.

### Even more human (optional, best result)
Record your own voice with the Part 1 script. A phone in a quiet room with soft furnishings works fine; hold it 15 to 20 cm from your mouth. Then either send me that recording directly, or use it to improve your ElevenLabs clone. A real human read always beats a generated one, and I re-time everything to whatever you send.

## After you send the new voice

1. I re-run the timing (word timestamps, the 16 beats), the lip sync and the mix.
2. All scenes, captions and overlays move to the new timing automatically.
3. Length check: the brief allows 95 to 140 s. Pauses add a few seconds, so expect about 105 to 115 s.

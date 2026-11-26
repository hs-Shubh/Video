#!/bin/bash
# Full re-render and delivery: 2x render, privacy scan (stops before export on a hit), encodes, srt, gates.
set -e
cd "$(dirname "$0")/../reel"
L=/root/.claude/skills/synced/3760d85d-6a56-42d7-8390-c125f4506a8a_bb53e082-e39b-47df-a8aa-e87bfdf4657e/hyperframes/scripts/plugin-cli.mjs
s=$(date +%s)
node $L render --resolution portrait-4k --workers 4 --crf 12 -o ../build/render/master_2x.mp4 > ../build/render/render.log 2>&1
echo "RENDER_SECONDS $(( $(date +%s)-s ))"
cd ../build
rm -rf ocr_frames
python3 -I ocr_scan.py > privacy_scan.log 2>&1
python3 -c "import json,sys; d=json.load(open('privacy_scan.json')); print('PRIVACY', d['pass'], d['frames_scanned'], len(d['token_like_hits'])); sys.exit(0 if d['pass'] else 3)"
python3 post.py encode > post_encode.log 2>&1
python3 post.py srt
python3 post.py gates > gates.log 2>&1
echo "PIPELINE_DONE $(( $(date +%s)-s ))"

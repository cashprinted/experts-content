#!/bin/bash
# render_variants.sh <project dir> A B ...  : rebuild index.html for each variant right before its 60 fps render
set -e
cd "$1"; shift
export HYPERFRAMES_BROWSER_PATH=$(ls /opt/pw-browsers/chromium_headless_shell-*/*/chrome-headless-shell | head -1)
mkdir -p renders
for V in "$@"; do
  python3 build.py $V
  npx hyperframes render -q delivery -f 60 -w 4 -o renders/silent_$V.mp4 > renders/render_$V.log 2>&1
  echo "rendered $V"
done

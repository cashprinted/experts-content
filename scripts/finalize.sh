#!/bin/bash
# finalize.sh <project dir> <Concept> A B : mux silent render + mix, crop 4:5, write renders/final/
set -e
cd "$1"; C=$2; shift 2
mkdir -p renders/final
for V in "$@"; do
  o=renders/final/Experts-2026-W48-$C-$V-1080x1920.mp4
  ffmpeg -v error -y -i renders/silent_$V.mp4 -i renders/mix_$V.wav -map 0:v -map 1:a -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 60 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $o
  ffmpeg -v error -y -i $o -vf crop=1080:1350:0:165 -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 60 -c:a copy -movflags +faststart renders/final/Experts-2026-W48-$C-$V-1080x1350.mp4
done
ls -la renders/final

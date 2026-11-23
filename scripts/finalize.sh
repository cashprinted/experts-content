#!/bin/bash
# finalize.sh <project dir> <Concept> A B : mux silent render + mix, crop 4:5, write renders/final/
set -e
cd "$1"; C=$2; shift 2
mkdir -p renders/final
for V in "$@"; do
  # master: the linear loudnorm in mix.py can stop short of -14 when the true-peak ceiling binds;
  # add the missing gain and a true-peak limiter at -1.5 dBTP so the delivered AAC lands at -14 LUFS
  I=$(ffmpeg -nostats -i renders/mix_$V.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | awk '{print $2}')
  G=$(python3 -c "print(round(-14.0 - ($I), 2))")
  ffmpeg -v error -y -i renders/mix_$V.wav -af "volume=${G}dB,alimiter=limit=0.79:level=false:attack=1:release=60,aresample=192000,alimiter=limit=0.82:level=false,aresample=48000" -c:a pcm_f32le renders/master_$V.wav
  o=renders/final/Experts-2026-W48-$C-$V-1080x1920.mp4
  ffmpeg -v error -y -i renders/silent_$V.mp4 -i renders/master_$V.wav -map 0:v -map 1:a -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 60 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $o
  ffmpeg -v error -y -i $o -vf crop=1080:1350:0:165 -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 60 -c:a copy -movflags +faststart renders/final/Experts-2026-W48-$C-$V-1080x1350.mp4
done
ls -la renders/final

#!/bin/bash
# final_check.sh <dir with finals> : fps, pix_fmt, audio, duration, integrated loudness and true peak per file
for f in "$1"/*.mp4; do
  v=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,pix_fmt -of csv=p=0 "$f")
  a=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate -of csv=p=0 "$f")
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  l=$(ffmpeg -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|^\s+Peak:" | awk '{print $2}' | tr '\n' ' ')
  echo "$(basename $f) | $v | audio $a | ${d}s | LUFS/TP $l"
done

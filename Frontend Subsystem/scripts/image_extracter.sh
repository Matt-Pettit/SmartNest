#!/bin/bash

for file in split/*.mp4; do
    filename=$(basename "$file" .mp4)
    ffmpeg -i "$file" -vf "select=eq(n\,100)" -f image2 "split/${filename}.jpg"
done
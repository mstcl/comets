#!/usr/bin/env bash

../scripts/ssdraw ./*.?????
for f in *.?????.ras
do
	convert "$f" "$f.jpg"
done
cat ./*.jpg > crash.mjpeg
ffmpeg -y -i crash.mjpeg -qscale 0 crash.mpeg # flag y will overwrite crash.mpeg automatically
rm -f crash.mjpeg
rm -f ./*.ras*

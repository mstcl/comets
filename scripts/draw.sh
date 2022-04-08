#! /bin/bash

../scripts/ssdraw *.?????
for f in *.?????.ras
do
	convert $f $f.jpg
done
cat *.jpg > crash.mjpeg
ffmpeg -i crash.mjpeg -qscale 0 crash.mpeg
rm -f crash.mjpeg
rm -f *.?????.ras*

#! /bin/bash

./ssdraw *.?????
for f in *.?????.ras
do
	convert $f $f.jpg
done
cat *.jpg > movie.mjpeg
ffmpeg -i movie.mjpeg -qscale 0 movie.mpeg
vlc movie.mpeg
rm -f movie.mjpeg
rm -f *.ras*

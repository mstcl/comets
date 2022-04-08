#!/usr/bin/env bash

mkdir -p bt_files

for f in *.?????
do
	../scripts/ss2bt $f
    mv "${f}.bt" bt_files/
done

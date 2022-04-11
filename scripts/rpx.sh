#!/usr/bin/env bash

../scripts/ss2bt sl9.ss
touch sl9_crash.bt > /dev/null 2>&1
../scripts/rpx.py
sleep 2
../scripts/bt2ss sl9_crash.bt

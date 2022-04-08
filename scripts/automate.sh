#!/usr/bin/env bash

../scripts/rpg > sl9_stats.txt
sleep 1
../scripts/rpx.sh > /dev/null 2>&1
sleep 1
../scripts/pkdgrav ss.par > /dev/null 2>&1
sleep 1
../scripts/batch_convert_ss2bt.sh > /dev/null 2>&1
sleep 1
../scripts/draw.sh > /dev/null 2>&1
sleep 1
../scripts/plot_range_from_bt.py

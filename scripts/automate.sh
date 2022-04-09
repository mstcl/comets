#!/usr/bin/env bash

../scripts/rpg > sl9_stats.txt
echo "• rpg run & sl9_stats.txt generated."
sleep 1
../scripts/get_dynamical_time.py > /dev/null 2>&1
echo "• dDelta in ss.par updated."
sleep 1
../scripts/rpx.sh > /dev/null 2>&1
echo "• tubber pile given initial conditions."
sleep 1
../scripts/pkdgrav ss.par > /dev/null 2>&1
echo "• pkdgrav integration complete."
sleep 1
../scripts/batch_convert_ss2bt.sh > /dev/null 2>&1
echo "• non-bin files converted."
sleep 1
../scripts/draw.sh > /dev/null 2>&1
echo "• movie generated."
sleep 1
../scripts/plot_and__analyse_bt.py > /dev/null 2>&1
echo "• metadata extracted."
echo "Done!."

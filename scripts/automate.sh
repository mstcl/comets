#!/usr/bin/env bash

# To simply redo any part of the process without redoing everything, comment out the appropriate lines
# But keep the sleep commands or else there might be errors with python opening and closing files

../scripts/rpg > sl9_stats.txt
echo "• rpg run & sl9_stats.txt generated."

sleep 0.1
../scripts/get_dynamical_time.py > /dev/null 2>&1
echo "• dDelta in ss.par updated."

sleep 0.1
../scripts/rpx.sh > /dev/null 2>&1
echo "• rubber pile given initial conditions."

sleep 0.1
../scripts/pkdgrav ss.par > /dev/null 2>&1
echo "• pkdgrav integration complete."

sleep 0.1
../scripts/batch_convert_ss2bt.sh > /dev/null 2>&1
echo "• non-bin files converted."

sleep 0.1
../scripts/draw.sh > /dev/null 2>&1
echo "• movie generated."

sleep 1
../scripts/plot_and_analyse_bt.py
echo "• metadata extracted."

echo "Done!"

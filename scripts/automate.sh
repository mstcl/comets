#!/usr/bin/env bash

# To simply redo any part of the process without redoing everything, comment out the appropriate lines
# But keep the sleep commands or else there might be errors with python opening and closing files

# ############
# #  1. RPG  #
# ############

# ../scripts/rpg > sl9_stats.txt
# echo "• rpg run & sl9_stats.txt generated."

# ##############################
# #  2. CHANGE DYNAMICAL TIME  #
# ##############################

# sleep 0.1
# ../scripts/get_dynamical_time.py > /dev/null 2>&1
# echo "• dDelta in ss.par updated."

# ###########################
# #  3. INITIAL CONDITIONS  #
# ###########################

# sleep 0.1
# ../scripts/rpx.sh > /dev/null 2>&1
# echo "• rubber pile given initial conditions."

# ############################
# #  4. PKDGRAV INTEGRATION  #
# ############################

# sleep 0.1
# ../scripts/pkdgrav ss.par > /dev/null 2>&1
# echo "• pkdgrav integration complete."

# ################################################
# #  5. CONVERT ALL SIMULATION FILES TO NON-BIN  #
# ################################################

# sleep 0.1
# ../scripts/batch_convert_ss2bt.sh > /dev/null 2>&1
# echo "• non-bin files converted."

# ##############################################
# #  6. CREATE A VIDEO OUTPUT FILE (OPTIONAL)  #
# ##############################################

# sleep 0.1
# ../scripts/draw.sh > /dev/null 2>&1
# echo "• movie generated."

# ######################
# #  7. DATA ANALYSIS  #
# ######################

sleep 0.1 # set this to around 0.5-0.8 if rerunning data analysis only
../scripts/plot_and_analyse_bt.py
echo "• metadata extracted."

echo "Done!"

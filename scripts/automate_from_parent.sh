#!/usr/bin/env bash

parent_dir=$PWD
cd "$1" || exit
../scripts/automate.sh
cd "$parent_dir" || exit

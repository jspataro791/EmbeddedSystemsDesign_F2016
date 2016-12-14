#!/bin/bash

pkill python2

cd main_ui

python2 main_ui.py &
echo "UI STARTED"

cd ..

cd pixy_io

python2 backup_pixy.py &
echo "AI STARTED"
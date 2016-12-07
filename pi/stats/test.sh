#!/bin/bash

echo "[STARTING STATS TEST]"

read -n 1 -s

echo "STATS should get a FRUIT..."
echo -n "FRUIT" | ncat -u 127.0.0.1 4001

read -n 1 -s

echo "STATS should get a LEFT turn for PACMAN"
echo -n "&P:LEFT" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a RIGHT turn for PACMAN"
echo -n "&P:RIGHT" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a LEFT turn for GHOST"
echo -n "&G:LEFT" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a LEFT turn for PACMAN"
echo -n "&G:RIGHT" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a DEBUG from PACMAN"
echo -n "&P:D0FirstDebugMessage" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should now detect +4 missing DEBUG messages on PACMAN"
echo -n "&P:D5SkippedFourMessages" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a DEBUG from GHOST"
echo -n "&G:D0FirstDebugMessage" | ncat -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should now detect +4 missing DEBUG messages on GHOST"
echo -n "&G:D5SkippedFourMessages" | ncat -u 127.0.0.1 4001

read -n 1 -s

echo "STATS should now get some message from AI"
echo -n "Hi, it's me, AI!" | ncat -u 127.0.0.1 7200

read -n 1 -s

echo "STATS should now get some message from PIXYIO"
echo -n "Hi, it's me, PixyIO!" | ncat -u 127.0.0.1 7300

read -n 1 -s



echo "STATS should now exit"
echo -n "EXIT" | ncat -u 127.0.0.1 4001

#!/bin/bash

echo "[STARTING STATS TEST]"

read -n 1 -s

echo "STATS should get a FRUIT..."
echo -n "FRUIT" | nc -u 127.0.0.1 4001

read -n 1 -s

echo "STATS should get a LEFT turn for PACMAN"
echo -n "&P:LEFT" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a RIGHT turn for PACMAN"
echo -n "&P:RIGHT" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a LEFT turn for GHOST"
echo -n "&G:LEFT" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a LEFT turn for PACMAN"
echo -n "&G:RIGHT" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a DEBUG from PACMAN"
echo -n "&P:D0FirstDebugMessage" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should now detect +4 missing DEBUG messages on PACMAN"
echo -n "&P:D5SkippedFourMessages" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should get a DEBUG from GHOST"
echo -n "&G:D0FirstDebugMessage" | nc -u 127.0.0.1 4001

read -n 1 -s


echo "STATS should now detect +4 missing DEBUG messages on GHOST"
echo -n "&G:D5SkippedFourMessages" | nc -u 127.0.0.1 4001

read -n 1 -s

echo "STATS should now get some message from AI"
echo -n "Hi, it's me, AI!" | nc -u 127.0.0.1 7200

read -n 1 -s

echo "STATS should now get some message from PIXYIO"
echo -n "Hi, it's me, PixyIO!" | nc -u 127.0.0.1 7300

read -n 1 -s



echo "STATS should now exit"
echo -n "EXIT" | nc -u 127.0.0.1 4001

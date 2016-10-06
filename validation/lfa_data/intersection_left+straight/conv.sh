#!/bin/bash

dir = pwd;
cd  $dir;
mogrify -define showkernel=1 -morphology Convolve '8x1: 1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0' -path ./conv

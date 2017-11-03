#!/bin/bash

DispyPath=~/.local/lib/python2.7/site-packages/dispy
LogPath=./

for i in 01 02 03 04 05 06 07 08 09 10 11
do
  ssh tev${i}.phys.washington.edu "nohup python ${DispyPath}/dispynode.py --clean --daemon --serve 1 > ${LogPath}/${i}.log &"
done


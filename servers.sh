#!/bin/bash

PidsPath=/phys/groups/tev/scratch3/users/WHHV/.var/run
DispyPath=~/.local/lib/python2.7/site-packages/dispy
LogPath=/phys/groups/tev/scratch3/users/WHHV/logs

case "$1" in
start)
  if [ -f ${PidsPath}/reco_dispy.pids ]; then
    echo "dispy servers already running!"
    exit 1
  fi
  declare -a Pids
  Idx=0
  for i in 01 02 03 04 05 06 07 08 09 10 11
  do
    Log=${LogPath}/tev${i}_reco_dispy.log
    Pids[$Idx]=$(ssh tev${i}.phys.washington.edu "nohup python ${DispyPath}/dispynode.py --clean --daemon > ${Log} &" | grep -Eo '[0-9]+$')
    echo $'\t'"Started dispy server with pid=${Pids[$Idx]} on tev${i} with log at ${Log}"
    Idx=$((Idx+1))
  done
  echo "${Pids[*]}" > ${PidsPath}/reco_dispy.pids
  ;;
stop)
  if [ ! -f ${PidsPath}/reco_dispy.pids ]; then
    echo "No pids file found at ${PidsPath}/reco_dispy.pids."
    exit 1
  fi
  read -a Pids < ${PidsPath}/reco_dispy.pids
  Idx=0
  for i in 01 02 03 04 05 06 07 08 09 10 11; do
    ssh tev${i}.phys.washington.edu "kill ${Pids[$Idx]}"
    echo "Stopped dispy server with pid=${Pids[$Idx]} on tev${i}."
    Idx=$((Idx+1))
  done
  rm ${PidsPath}/reco_dispy.pids
  ;;
restart)
  $0 stop
  $0 start
  ;;
status)
  if [ -f ${PidsPath}/reco_dispy.pids ]; then
    echo dispy servers are running.
  else
    echo dispy servers are not running.
  fi
  ;;
*)
  echo "Usage: $0 {start|stop|status|restart}"
esac

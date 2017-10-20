#!/bin/bash
chmod a+x generator_setup.sh

RunNum=304795
EventsPerBatch=5000
StartingBatch=1
EndingBatch=20

echo "Starting the Generation Step"

(
source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
for ((i=StartingBatch ; i <= EndingBatch ; i++))
do
  # The generator has trouble cleaning up its temporary files, so do so for it.
  rm -r PROC_HAHM_variableMW_v3_UFO_*
  EVNTFile="${RunNum}.${EventsPerBatch}.${i}.EVNT"
  echo "$EVNTFile"
  FirstEvent=$(($EventsPerBatch*($i-1)+1))
  echo "$FirstEvent"
  Generate_tf.py --jobConfig hss-runner.py --maxEvents $EventsPerBatch --runNumber $RunNum --firstEvent $FirstEvent --outputEVNTFile $EVNTFile --ecmEnergy 13000
done
)

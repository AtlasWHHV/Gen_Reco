#!/bin/bash
chmod a+x generator_setup.sh

RunNum=304795
EventsPerBatch=1
StartingBatch=1
EndingBatch=1
MaxSeed=$((30081*30081))

source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
(
for ((i=StartingBatch ; i <= EndingBatch ; i++))
do
  # The generator has trouble cleaning up its temporary files, so do so for it.
  rm -r PROC_HAHM_variableMW_v3_UFO_*
  EVNTFile="${RunNum}.${EventsPerBatch}.${i}.evnt.pool.root"
  FirstEvent=$(($EventsPerBatch*($i-1)+1))
  Seed=$(($(date +"%s") % MaxSeed))
  echo "MC Seed = $Seed"
  Generate_tf.py --jobConfig hss-runner.py --maxEvents $EventsPerBatch --runNumber $RunNum --firstEvent $FirstEvent --outputEVNTFile $EVNTFile --ecmEnergy 13000 --randomSeed $Seed
done
)

#!/bin/bash
chmod a+x simulator_setup.sh

RunNumber=304795
RDOFile="${RunNumber}.1.1.RDO"
ESDFile="${RunNumber}.1.1.ESD"

(
  Reco_tf.py  --inputRDOFile $RDOFile --outputESDFile $ESDFile --maxEvents=-1 --skipEvents 0  --DBRelease current  --autoConfiguration='everything'  
)


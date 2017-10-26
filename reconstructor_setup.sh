#!/bin/bash
chmod a+x reconstructor_setup.sh

RunNumber=304795
RDOFile="${RunNumber}.1.1.rdo.pool.root"
ESDFile="${RunNumber}.1.1.esd.pool.root"
AODFile="${RunNumber}.1.1.aod.pool.root"

(
  source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
  Reco_tf.py  --inputRDOFile $RDOFile --outputESDFile $ESDFile --outputAODFile $AODFile --maxEvents=-1 --skipEvents 0  --DBRelease current  --autoConfiguration='everything'  
)


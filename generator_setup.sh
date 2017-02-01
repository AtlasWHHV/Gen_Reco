#!/bin/bash
chmod a+x generator_setup.sh

#################################################################
echo """ PLEASE EDIT THESE VARIABLES FOR YOUR NEEDS."""
#################################################################
Num_Events=5000
EVNTFile="5000_events_v2.EVNT"
DAODFile="5000_events_v2.pool.root"
Run_Num=304795



echo "Starting the Generation Step"

(

source $AtlasSetup/scripts/asetup.sh here,19.2.4.14

#Below, edit the output file, and max events for what you need

Generate_tf.py --jobConfig hss-runner.py --maxEvents $Num_Events --runNumber $Run_Num --outputEVNTFile $EVNTFile --ecmEnergy 13000
)

echo "Starting the RECO step"

(
source $AtlasSetup/scripts/asetup.sh 20.1.8.3,AtlasDerivation,gcc48,here


#Change the input event file and output daod file
Reco_tf.py --inputEVNTFile $EVNTFile --outputDAODFile $DAODFile --reductionConf TRUTH0
)






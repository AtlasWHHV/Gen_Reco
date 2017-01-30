#!/bin/bash


#################################################################
echo """ PLEASE EDIT THESE VARIABLES FOR YOUR NEEDS."""
#################################################################
Num_Events=10
EVNTFile="10_events_v2.EVNT"
DAODFile="10_events_v2.pool.root"
Run_Num=304795


##########################
#---Modular ROOT Setup---#
##########################

#source /phys/users/gwatts/bin/CommonScripts/configASetup.sh
#lsetup "root 5.34.25-x86_64-slc6-gcc48-opt"


echo "Starting the Generation Step"

(
#asetup here,19.2.4.14
source $AtlasSetup/scripts/asetup.sh here,19.2.4.14

#Below, edit the output file, and max events for what you need

Generate_tf.py --jobConfig hss-runner.py --maxEvents $Num_Events --runNumber $Run_Num --outputEVNTFile $EVNTFile --ecmEnergy 13000
)

echo "Starting the RECO step"

(
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup 20.1.8.3,AtlasDerivation,gcc48,here

#Change the input event file and output daod file
Reco_tf.py --inputEVNTFile $EVNTFile --outputDAODFile $DAODFile --reductionConf TRUTH0
)

#python /phys/users/arbo94/Desktop/alert.py /phys/users/arbo94/Desktop/done.py




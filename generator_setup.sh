#################################################################
""" PLEASE EDIT BEFORE YOU RUN THIS IN A PERSONAL LOCATION"""
#################################################################

group_folder_loc="/phys/groups/tev/scratch1/users/WHHV/"
Num_Events=10
EVNTFile="10_events.EVNT"
DAODFile="10_events.pool.root"
cd $group_folder_loc


##########################
#---Modular ROOT Setup---#
##########################
T_Resources="/phys/groups/tev/scratch4/users/tommeyer"
TMVA_SOURCE="test/setup.sh"



source /phys/users/gwatts/bin/CommonScripts/configASetup.sh

lsetup "root 5.34.25-x86_64-slc6-gcc48-opt"
export PATH=/usr/bin:$PATH
TMVA_PATH=""$T_Resources"/TMVA-v5"
source "$TMVA_PATH"/"$TMVA_SOURCE" "$TMVA_PATH"
echo -e "ROOT v5.34 with TMVA is now setup\n"

echo "Starting the Generation Step"
#assuming youve loaded up on bash.
(
asetup here,19.2.4.14

#Below, edit the output file, and max events for what you need

Generate_tf.py --jobConfig hss-runner.py --maxEvents $Num_Events --runNumber 304795 --outputEVNTFile $EVNTFile --ecmEnergy 13000
)

echo "Starting the RECO step"

(
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup 20.1.8.3,AtlasDerivation,gcc48,here

#Change the input event file and output daod file
Reco_tf.py --inputEVNTFile $EVNTFile --outputDAODFile $DAODFile --reductionConf TRUTH3
)

#python /phys/users/arbo94/Desktop/alert.py /phys/users/arbo94/Desktop/done.py






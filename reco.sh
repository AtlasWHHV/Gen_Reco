#!/bin/bash

source /phys/users/gwatts/bin/CommonScripts/configASetup.sh

VersionNumber=$1
MaxEvents=$2
SkipEvents=$3
EVNTFile=$4

HITSFile="${VersionNumber}.hits.pool.root"
RDOFile="${VersionNumber}.rdo.pool.root"
ESDFile="${VersionNumber}.esd.pool.root"
AODFile="${VersionNumber}.aod.pool.root"

GeometryVersion=ATLAS-R2-2015-03-01-00_VALIDATION
ConditionsTag=OFLCOND-RUN12-SDR-20

(
  source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
  Sim_tf.py --inputEVNTFile $EVNTFile --geometryVersion $GeometryVersion --conditionsTag $ConditionsTag --outputHITSFile $HITSFile --physicsList "FTFP_BERT" --postInclude "PyJobTransforms/UseFrontier.py" --preInclude "EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py" --maxEvents $MaxEvents --skipEvents $SkipEvents --randomSeed "8" --simulator "MC12G4" --truthStrategy "MC12"

)
    
(
  source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
  Digi_tf.py --inputHitsFile $HITSFile --outputRDOFile $RDOFile --maxEvents -1 --geometryVersion $GeometryVersion --conditionsTag $ConditionsTag  
)

(
  source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
  Reco_tf.py  --inputRDOFile $RDOFile --outputESDFile $ESDFile --maxEvents -1 --DBRelease current  --autoConfiguration='everything'  
  Reco_tf.py --inputESDFile $ESDFile --outputAODFile $AODFile --maxEvents -1 --DBRelease current --autoConfiguration='everything'
)    

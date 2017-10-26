#!/bin/bash
chmod a+x simulator_setup.sh

RunNumber=304795
EVNTFile="${RunNumber}.1.1.evnt.pool.root"
HITSFile="${RunNumber}.1.1.hits.pool.root"

(
  source $AtlasSetup/scripts/asetup.sh here,19.2.4.14
  Sim_tf.py --inputEVNTFile $EVNTFile  --DataRunNumber $RunNumber   --geometryVersion ATLAS-R2-2015-03-01-00_VALIDATION --conditionsTag OFLCOND-RUN12-SDR-20 --outputHITSFile $HITSFile --physicsList "FTFP_BERT" --postInclude "PyJobTransforms/UseFrontier.py" --preInclude "EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py" --maxEvents -1 --randomSeed "8" --simulator "MC12G4" --truthStrategy "MC12"

)

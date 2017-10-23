#!/bin/bash
chmod a+x digitizer_setup.sh

RunNumber=304795
HITSFile="${RunNumber}.1.1.HITS"
RDOFile="${RunNumber}.1.1.RDO"

(
  Digi_tf.py --inputHitsFile $HITSFile --outputRDOFile $RDOFile --maxEvents -1 --skipEvents 0 --geometryVersion ATLAS-R2-2015-03-01-00_VALIDATION  --conditionsTag OFLCOND-RUN12-SDR-20  
)




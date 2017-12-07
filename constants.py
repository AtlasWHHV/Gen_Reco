# Note: this directory should contain the Gen_Reco repository.
root_dir = '/phys/groups/tev/scratch3/users/WHHV'
evnt_dir = root_dir + '/evnts'
tmp_dir = root_dir + '/tmp'
log_dir = root_dir + '/logs'
aod_dir = root_dir + '/aod'
reco = root_dir + '/Gen_Reco/reco.py'

gen_release = '19.2.4.14'
run_number = 304795
gen_job_config = 'hss-runner.py'

class Tag:
  def __init__(self, command, release, tag):
    self.command = command
    self.release = release
    self.tag = tag

s2608_tag = Tag("Sim_tf.py --physicsList 'FTFP_BERT' --truthStrategy 'MC12' --simulator 'MC12G4' --DBRelease 'default:current' --conditionsTag 'default:OFLCOND-RUN12-SDR-19' --preInclude 'EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py' --geometryVersion 'default:ATLAS-R2-2015-03-01-00_VALIDATION' --postInclude 'default:PyJobTransforms/UseFrontier.py' --inputEVNTFile {} --outputHITSFile {}", 'AtlasProduction,19.2.3.7', 's2608')
r7773_tag = Tag("""Reco_tf.py --digiSteeringConf 'StandardSignalOnlyTruth' --conditionsTag 'default:OFLCOND-MC15c-SDR-09' --ignorePatterns 'Py:TrigConf2COOLLib.py.+ERROR.===================================+' --pileupFinalBunch '6' --numberOfHighPtMinBias '0.12268057' --autoConfiguration 'everything' --postInclude 'default:RecJobTransforms/UseFrontier.py' --numberOfLowPtMinBias '39.8773194' --steering 'doRDO_TRIG' --preInclude 'HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_v3.py' 'RDOtoRDOTrigger:RecExPers/RecoOutputMetadataList_jobOptions.py' --postExec 'all:CfgMgr.MessageSvc().setError+=["HepMcParticleLink"]' 'ESDtoAOD:fixedAttrib=[s if "CONTAINER_SPLITLEVEL = \\\\\'99\\\\\'" not in s else "" for s in svcMgr.AthenaPoolCnvSvc.PoolAttributes];svcMgr.AthenaPoolCnvSvc.PoolAttributes=fixedAttrib' --preExec 'all:rec.Commissioning.set_Value_and_Lock(True);from AthenaCommon.BeamFlags import jobproperties;jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0);from LArROD.LArRODFlags import larRODFlags;larRODFlags.NumberOfCollisions.set_Value_and_Lock(20);larRODFlags.nSamples.set_Value_and_Lock(4);larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True);larRODFlags.firstSample.set_Value_and_Lock(0);larRODFlags.useHighestGainAutoCorr.set_Value_and_Lock(True)' 'RAWtoESD:from CaloRec.CaloCellFlags import jobproperties;jobproperties.CaloCellFlags.doLArCellEmMisCalib=False' 'ESDtoAOD:TriggerFlags.AODEDMSet="AODSLIM"' --triggerConfig 'RDOtoRDOTrigger=MCRECO:DBF:TRIGGERDBMC:2046,20,56' --geometryVersion 'default:ATLAS-R2-2015-03-01-00' --numberOfCavernBkg '0' --inputHITSFile {} --outputAODFile {} --jobNumber 1""", 'AtlasProd1,20.7.5.1.1', 'r7773')
p2952_tag = Tag('''Reco_tf.py --reductionConf 'EXOT15' --passThrough 'True' --athenaMPMergeTargetSize 'DAOD_*:0' --preExec 'default:from BTagging.BTaggingFlags import BTaggingFlags;BTaggingFlags.CalibrationTag = "BTagCalibRUN12-08-18"' --inputAODFile {} --outputDAODFile {}''', 'AtlasDerivation,20.7.8.7', 'p2952')
tags = [s2608_tag, r7773_tag, p2952_tag]

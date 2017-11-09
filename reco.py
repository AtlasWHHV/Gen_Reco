import constants
import os
import stat
import shutil
import subprocess32

def reco(evnt_file, version, aod_dir, num_events, skip_events, geometry_version, conditions_tag, sim_release, dig_release, reco_release, log_file, tmp_dir):
  hits_file = version + '.hits.pool.root'
  rdo_file = version + '.rdo.pool.root'
  esd_file = version + '.esd.pool.root'
  aod_file = version + '.aod.pool.root'
  log_file_handle = open(log_file, 'w+')
  source_arg = '. /phys/users/gwatts/bin/CommonScripts/configASetup.sh && . $AtlasSetup/scripts/asetup.sh here,'
  hits_arg = source_arg + '{} && Sim_tf.py --inputEVNTFile {} --geometryVersion {} --conditionsTag {} --outputHITSFile {}  --physicsList "FTFP_BERT" --postInclude "PyJobTransforms/UseFrontier.py" --preInclude "EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py" --maxEvents {} --skipEvents {} --randomSeed "8" --simulator "MC12G4" --truthStrategy "MC12"'.format(sim_release, evnt_file, geometry_version, conditions_tag, hits_file, num_events, skip_events)
  rdo_arg = source_arg + '{} && Digi_tf.py --inputHitsFile {} --outputRDOFile {} --geometryVersion {} --conditionsTag {}'.format(dig_release, hits_file, rdo_file, geometry_version, conditions_tag)
  esd_arg = source_arg + '{} && Reco_tf.py  --inputRDOFile {} --outputESDFile {} --DBRelease current  --autoConfiguration="everything"'.format(reco_release, rdo_file, esd_file)
  aod_arg = source_arg + '{} && Reco_tf.py --inputESDFile {} --outputAODFile {} --DBRelease current --autoConfiguration="everything"'.format(reco_release, esd_file, aod_file)
  for arg, output in zip((hits_arg, rdo_arg, esd_arg, aod_arg), (hits_file, rdo_file, esd_file, aod_file)):
    try:
      subprocess.check_call(arg, executable='/bin/bash', cwd=tmp_dir, shell=True, stdout=log_file_handle, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      print('reco.py: {}'.format(e))
    # Remove all non-essential files after each step.
    for entry in os.listdir(tmp_dir):
      entry_path = os.path.join(tmp_dir, entry)
      try:
        if os.path.isfile(entry_path) and entry != output:
          os.remove(entry_path)
        elif os.path.isdir(entry_path):
          shutil.rmtree(entry_path)
      except OSError as e:
        print('reco.py: {}'.format(e))
  # move the aod file to the output directory, and make it immutable so that
  # it is not accidentally deleted.
  os.rename(os.path.join(tmp_dir, aod_file), os.path.join(aod_dir, aod_file))
  aod_file_path = os.path.join(aod_dir, aod_file)
  st = os.stat(aod_file_path)
  not_writable = ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
  os.chmod(aod_file_path, st.st_mode & not_writable) 
  shutil.rmtree(tmp_dir)

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Perform simulation, digitization and reconstruction on a given event file.')
  parser.add_argument('evnt_file', help='The event file.')
  parser.add_argument('version', help='The name (without file extensions) of the output AOD file.')
  parser.add_argument('--aod_dir', default=constants.aod_dir, help='The path of the aod directory.')
  parser.add_argument('-n', '--num_events', type=int, default=-1, help='The number of events.')
  parser.add_argument('-s', '--skip_events', type=int, default=0, help='The number of events to skip.')
  parser.add_argument('--geometry_version', default=constants.geometry_version, help='Geometry version for simulation and digitization.')
  parser.add_argument('--conditions_tag', default=constants.conditions_tag, help='Conditions tag for simulation and digitization.')
  parser.add_argument('--sim_release', default=constants.sim_release, help='The athena release to use for simulation.')
  parser.add_argument('--dig_release', default=constants.dig_release, help='The athena release to use for digitization.')
  parser.add_argument('--reco_release', default=constants.reco_release, help='The athena release to use for reconstruction.')
  parser.add_argument('--log_file', default=os.path.join(constants.log_dir, 'reco.log'), help='The log file.')
  parser.add_argument('--tmp_dir', default=os.path.join(constants.tmp_dir, 'reco'), help='The tmp dir.')
  args = parser.parse_args()
  reco(args.evnt_file, args.version, args.aod_dir, args.num_events, args.skip_events, args.geometry_version, args.conditions_tag, args.sim_release, args.dig_release, args.reco_release, args.log_file, args.tmp_dir)

if __name__ == '__main__':
  main()

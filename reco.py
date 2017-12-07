import constants
import os
import stat
import shutil
import subprocess32
import string

def reco(evnt_file, version, output_dir, num_events, skip_events, log_file, tmp_dir):
  log_file_handle = open(log_file, 'w+')
  asetup = '. /phys/users/gwatts/bin/CommonScripts/configASetup.sh && . $AtlasSetup/scripts/asetup.sh'
  input_file = evnt_file
  for tag in constants.tags:
    output_file = string.split(input_file, sep='/')[-1] + '_' + tag.tag
    command = tag.command.format(input_file, output_file) + ' --maxEvents {} --skipEvents {}'.format(num_events, skip_events)
    arg = '{} {} && {}'.format(asetup, tag.release, command)
    print('{} arg: {}'.format(tag.tag, arg))
    try:
      subprocess32.check_call(arg, executable='/bin/bash', cwd=tmp_dir, shell=True, stdout=log_file_handle, stderr=subprocess32.STDOUT)
    except subprocess32.CalledProcessError as e:
      print('reco.py: {}'.format(e))
      break
    input_file = output_file
  # move the aod file to the output directory, and make it immutable so that
  # it is not accidentally deleted.
  os.rename(os.path.join(output_dir, output_file), os.path.join(output_dir, output_file))
  output_file_path = os.path.join(output_dir, output_file)
  st = os.stat(output_file_path)
  not_writable = ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
  os.chmod(output_file_path, st.st_mode & not_writable) 

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Perform simulation, digitization and reconstruction on a given event file.')
  parser.add_argument('evnt_file', help='The event file.')
  parser.add_argument('version', help='The name (without file extensions) of the output AOD file.')
  parser.add_argument('--output_dir', default=constants.aod_dir, help='The path of the output directory.')
  parser.add_argument('-n', '--num_events', type=int, default=-1, help='The number of events.')
  parser.add_argument('-s', '--skip_events', type=int, default=0, help='The number of events to skip.')
  parser.add_argument('--log_file', default=os.path.join(constants.log_dir, 'reco.log'), help='The log file.')
  parser.add_argument('--tmp_dir', default=os.path.join(constants.tmp_dir, 'reco'), help='The tmp dir.')
  args = parser.parse_args()
  reco(args.evnt_file, args.version, args.output_dir, args.num_events, args.skip_events, args.log_file, args.tmp_dir)

if __name__ == '__main__':
  main()

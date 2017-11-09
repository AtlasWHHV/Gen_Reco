import argparse
import os
import stat
import shutil
import tempfile
import subprocess32
import time
import constants

def gen(batch_size, num_batches, evnt_dir, release, job_config, run_number):
  max_seed = 30081**2
  processes = []
  tmp_dirs = []
  evnt_files = []
  for i in range(1, num_batches+1):
    evnt_file = os.path.join(evnt_dir, '{}.{}.{}.evnt.pool.root'.format(run_number, batch_size, i))
    evnt_files.append(evnt_file)
    first_event = num_batches * (i - 1) + 1
    seed = int(time.time()) % max_seed
    log_file_handle = open(os.path.join(constants.log_dir, 'gen{}.log'.format(i)), 'w+')
    tmp_dir = tempfile.mkdtemp(dir=constants.tmp_dir)
    tmp_dirs.append(tmp_dir)
    arg = '. /phys/users/gwatts/bin/CommonScripts/configASetup.sh && . $AtlasSetup/scripts/asetup.sh here,{} && Generate_tf.py --jobConfig {} --maxEvents {} --runNumber {} --firstEvent {} --outputEVNTFile {} --ecmEnergy 13000 --randomSeed {}'.format(release, job_config, batch_size, run_number, first_event, evnt_file, seed)
    process = subprocess32.Popen(arg, executable='/bin/bash', cwd=tmp_dir, shell=True, stdout=log_file_handle, stderr=subprocess32.STDOUT)
    processes.append(process)
  for i, process in enumerate(processes):
    return_code = process.wait()
    if return_code != 0:
      print ('ERROR: Generation of batch {} failed with code: {}'.format(i, return_code))
  not_writable = ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
  for evnt_file in evnt_files:
    st = os.stat(evnt_file)
    os.chmod(evnt_file, st.st_mode & not_writable)
  for tmp_dir in tmp_dirs:
    shutil.rmtree(tmp_dir)

def main():
  parser = argparse.ArgumentParser(description='Generates events according to a hidden valley theory.')
  parser.add_argument('-b', '--batch_size', type=int, default=5000, help='The number of events to generate in each batch.')
  parser.add_argument('-n', '--num_batches', type=int, default=20, help='The number of batches to generate.')
  parser.add_argument('--evnt_dir', default=constants.evnt_dir, help='The directory in which to store events.')
  parser.add_argument('-r', '--release', default=constants.gen_release, help='The athena release to use.')
  parser.add_argument('--job_config', default=constants.gen_job_config, help='The job configuration script for generating the events.')
  parser.add_argument('--run_number', default=constants.run_number, help='The run number.')
  args = parser.parse_args()
  gen(args.batch_size, args.num_batches, os.path.abspath(args.evnt_dir), args.release, os.path.abspath(args.job_config), args.run_number)

if __name__ == '__main__':
  main()

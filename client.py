from __future__ import division
import argparse
import distributed
import webbrowser
import glob
import math
import string
import constants
import datetime
import os
import shutil
import pickle
import subprocess32
import sys

def compute(version_number, max_events, skip_events, event_file, log_dir, tmp_dir, aod_dir, reco, job_id):
  ''' Runs reco.py with the given parameters. '''
  import subprocess32, shutil, socket, os
  log_dir = os.path.join(log_dir, 'job{:0>4}'.format(job_id))
  tmp_dir = os.path.join(tmp_dir, 'job{:0>4}'.format(job_id))
  try:
    os.makedirs(log_dir)
    os.makedirs(tmp_dir)
  except OSError as e:
    print(e)
  athena_log = os.path.join(log_dir, 'athena.log')
  arg = 'nice {} {} -n {} -s {} --log_file {} --tmp_dir {} --output_dir {} {} {}'.format(sys.executable, reco, max_events, skip_events, athena_log, tmp_dir, aod_dir, event_file, version_number)
  with open(os.path.join(log_dir, 'reco.log'), 'w+') as fh:
    subprocess32.check_call(arg, executable='/bin/bash', shell=True, stdout=fh, stderr=subprocess32.STDOUT, cwd=os.getcwd(), env=os.environ.copy())
  try:
    shutil.rmtree(log_dir)
    shutil.rmtree(tmp_dir)
  except OSError as e:
    print(e)
  return socket.gethostname()

def get_failed_jobs(tmp_dir, aod_dir):
  with open(os.path.join(tmp_dir, 'jobs.args'), 'rb') as fj_handle:
    job_args = pickle.load(fj_handle)
  output_files = [os.path.basename(x) for x in glob.glob(os.path.join(aod_dir, '*.aod.pool.root'))]
  failed_jobs = []
  for job_arg in job_args:
    aod_file = '{}.aod.pool.root'.format(job_arg[0])
    if aod_file not in output_files:
      failed_jobs.append(job_arg)
  return failed_jobs

def get_job_args(batch_size, evnt_dir, log_dir, tmp_dir, output_dir):
  evnt_files = glob.glob(evnt_dir + '/*.evnt.pool.root')
  print ('[client]: Found evnt files:')
  for ii, evnt_file in enumerate(evnt_files):
    print('\t[{}] {}'.format(ii+1, evnt_file))
  job_id = 0
  job_args = []
  reco = os.path.join(os.getcwd(), 'reco.py')
  for evnt_file in evnt_files:
    rel_evnt_file = string.split(evnt_file, sep='/')[-1]
    run_number, evnt_batch_size, evnt_batch_number = string.split(rel_evnt_file, sep='.')[:3]
    evnt_version = "{}.{}.{}".format(run_number, evnt_batch_size, evnt_batch_number)
    evnt_batch_size = int(evnt_batch_size)
    job_skip_events = 0
    for _ in range(int(math.ceil(evnt_batch_size / batch_size))):
      job_batch_size = min(batch_size, evnt_batch_size - job_skip_events)
      job_version_number = "{}.{}.{}".format(evnt_version, job_batch_size, job_skip_events)
      job_args.append((job_version_number, job_batch_size, job_skip_events, evnt_file, log_dir, tmp_dir, output_dir, reco, job_id))
      job_skip_events += job_batch_size
      job_id += 1
  with open(os.path.join(tmp_dir, 'jobs.args'), 'wb+') as fj_handle:
       pickle.dump(job_args, fj_handle)
  return job_args

def check_jobs(jobs, job_args, tmp_dir, timestamp):
  failed_jobs = []
  for job_arg, job in zip(job_args, jobs):
    job_id = job_arg[-1]
    print ('[client]: Waiting for job {:0>4}'.format(job_id))
    try:
      host = job.result()
      print('[{}]: Executed job {:0>4}'.format(host, job_id))
    except Exception as e:
      print(e)
      failed_jobs.append(job_arg)
  if len(failed_jobs) != 0:
    print('[client]: The following jobs failed ({} in total): '.format(len(failed_jobs)))
    for job in failed_jobs:
      print('\tjob {:0>4}'.format(job[-1]))
    print('[client]: Run "python client.py -r {}" to redispatch failed jobs.'.format(timestamp))

def dispatch_computations(job_args, tmp_dir, timestamp):
  client = distributed.Client('localhost:8786')
  webbrowser.open('http://localhost:8787')
  jobs = []
  for job_arg in job_args:
    job = client.submit(compute, *job_arg)
    jobs.append(job)
  check_jobs(jobs, job_args, tmp_dir, timestamp)

def clean():
  for dir in (constants.log_dir, constants.tmp_dir):
    for entry in os.listdir(dir):
      entry_path = os.path.join(dir, entry)
      try:
        if os.path.isfile(entry_path):
          os.remove(entry_path)
        elif os.path.isdir(entry_path):
          shutil.rmtree(entry_path, ignore_errors=True)
      except OSError as e:
        print('[client]: clean: {}'.format(e))
  for entry in glob.glob('./_dispy_*'):
    try:
      os.remove(entry)
    except OSError as e:
      print('[client]: clean: {}'.format(e))

def main():
  parser = argparse.ArgumentParser(description='Dispatch reco jobs to tev machines.')
  parser.add_argument('-b', '--batch_size', type=int, default=50, help='The number of events to reco in each job.')
  parser.add_argument('--evnt_dir', default='/phys/groups/tev/scratch3/users/WHHV/evnts/tiny', help='Directory that contains evnt files.')
  parser.add_argument('-t', '--test', action='store_true', help='Attempts to find evnt files (and do cleaning, if --clean or -c is specified), but does not actually distribute jobs. Useful if you want to check that your parameters are correct without committing to actual computation.')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', '--clean', action='store_true', help='Remove old recovery, temporary, and log files.')
  group.add_argument('-r', '--redispatch_timestamp', dest='timestamp', default=None, help='The timestamp of a run, the failed jobs of which will be redispatched.')
  args = parser.parse_args()
  if args.clean:
    clean()
  if args.timestamp:
    timestamp = args.timestamp
  else:
    timestamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
  log_dir = os.path.join(constants.log_dir, timestamp)
  tmp_dir = os.path.join(constants.tmp_dir, timestamp)
  aod_dir = os.path.join(constants.aod_dir, timestamp)
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)
  if not os.path.exists(aod_dir):
    os.makedirs(aod_dir)
  if args.timestamp:
    failed_jobs = get_failed_jobs(tmp_dir, aod_dir)
    dispatch_computations(failed_jobs, tmp_dir, timestamp)
  else:
    job_args = get_job_args(args.batch_size, args.evnt_dir, log_dir, tmp_dir, aod_dir)
    if args.test:
      for job_arg in job_args:
        job_version_number, job_batch_size, job_skip_events, evnt_file, _, _, _, _, job_id = job_arg
        print("[client]: job {:0>4}: version={}, batch_size={}, skip_events={}, evnt_file={}".format(job_id, job_version_number, job_batch_size, job_skip_events, evnt_file))
    else:
      dispatch_computations(job_args, tmp_dir, timestamp)
  if args.test:
    shutil.rmtree(log_dir)
    shutil.rmtree(tmp_dir)
    shutil.rmtree(aod_dir)
if __name__ == '__main__':
  main()

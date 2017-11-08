from __future__ import division
import argparse
import dispy
import dispy.httpd
import webbrowser
import glob
import math
import string
import constants
import datetime
import os
import shutil
import pickle

def compute(version_number, max_events, skip_events, event_file, log_dir, tmp_dir, job_id):
  ''' Runs reco.py with the given parameters. '''
  import subprocess, constants, socket, os
  log_file = os.path.join(log_dir, 'job{}.log'.format(job_id))
  tmp_dir = os.path.join(tmp_dir, 'job{}'.format(job_id))
  os.makedirs(tmp_dir)
  arg = 'nice python {} -n {} -s {} --log_file {} --tmp_dir {} {} {}'.format(constants.reco, max_events, skip_events, log_file, tmp_dir, event_file, version_number)
  subprocess.check_call(arg, executable='/bin/bash', shell=True)
  return socket.gethostname()

def get_job_args(batch_size, evnt_dir):
  evnt_files = glob.glob(evnt_dir + '/*.evnt.pool.root')
  print ('Found evnt files:')
  for ii, evnt_file in enumerate(evnt_files):
    print('\t[{}] {}'.format(ii+1, evnt_file))
  job_id = 0
  job_args = []
  for evnt_file in evnt_files:
    rel_evnt_file = string.split(evnt_file, sep='/')[-1]
    run_number, evnt_batch_size, evnt_batch_number = string.split(rel_evnt_file, sep='.')[:3]
    evnt_version = "{}.{}.{}".format(run_number, evnt_batch_size, evnt_batch_number)
    evnt_batch_size = int(evnt_batch_size)
    job_skip_events = 0
    for _ in range(int(math.ceil(evnt_batch_size / batch_size))):
      job_batch_size = min(batch_size, evnt_batch_size - job_skip_events)
      job_version_number = "{}.{}.{}".format(evnt_version, job_batch_size, job_skip_events)
      job_args.append((job_version_number, job_batch_size, job_skip_events, evnt_file, log_dir, tmp_dir, job_id))
      job_skip_events += job_batch_size
      job_id += 1
  return job_args

def dispatch_computations(job_args, timestamp, test, local):
  log_dir = os.path.join(constants.log_dir, timestamp)
  tmp_dir = os.path.join(constants.tmp_dir, timestamp)
  os.makedirs(log_dir)
  os.makedirs(tmp_dir)
  if not test and not local:
    cluster = dispy.JobCluster(compute, depends=[constants])
    http_server = dispy.httpd.DispyHTTPServer(cluster)
    webbrowser.open('http://localhost:8181')
    jobs = []
  job_args_dict = {}
  for job_arg in job_args:
    job_version_number, job_batch_size, job_skip_events, evnt_file, log_dir, tmp_dir, job_id = job_arg
    job_args_dict[job_id] = job_arg
    if test:
      print("job {:0>4}: version={}, batch_size={}, skip_events={}, evnt_file={}".format(job_id, job_version_number, job_batch_size, job_skip_events, evnt_file))
    elif not local:
      job = cluster.submit(*job_arg)
      job.id = job_id
      jobs.append(job)
    else:
      compute(*job_arg)
  if not test and not local:
    failed_jobs = []
    for job in jobs:
      host = job()
      if host is None:
        failed_jobs.append(job_args_dict[job.id])
        print('ERROR: job {:0>4} failed!'.format(job.id))
      else:
        print('{} executed job {:0>4} from {} to {}'.format(host, job.id, job.start_time, job.end_time))
    if len(failed_jobs) != 0:
      print('The following jobs failed ({} in total): '.format(len(failed_jobs)))
      for job in jobs:
        print('\tjob {}'.format(job[-1]))
      with open(os.path.join(tmp_dir, 'failed_jobs.args')) as fj_handle:
        pickle.dump(failed_jobs, fj_handle)
    cluster.print_status()
    http_server.shutdown()

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
        print('clean: {}'.format(e))
  for entry in glob.glob('./_dispy_*'):
    try:
      os.remove(entry)
    except OSError as e:
      print('clean: {}'.format(e))

def main():
  parser = argparse.ArgumentParser(description='Dispatch reco jobs to tev machines.')
  parser.add_argument('-b', '--batch_size', type=int, default=50, help='The number of events to reco in each job.')
  parser.add_argument('--evnt_dir', default='/phys/groups/tev/scratch3/users/WHHV/evnts/tiny', help='Directory that contains evnt files.')
  parser.add_argument('-t', '--test', action='store_true', help='Attempts to find evnt files (and do cleaning, if --clean or -c is specified), but does not actually distribute jobs. Useful if you want to check that your parameters are correct without committing to actual computation.')
  parser.add_argument('-l', '--local', action='store_true', help='Runs all computations locally, without using dispy servers. Useful for debugging computation function.')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', '--clean', action='store_true', help='Remove old recovery, temporary, and log files.')
  group.add_argument('-r', '--redispatch_timestamp', dest='timestamp', default=None, help='The timestamp of a run, the failed jobs of which will be redispatched.')
  args = parser.parse_args()
  if args.clean:
    clean()
  if args.timestamp:
    tmp_dir = os.path.join(constants.tmp_dir, args.timestamp)
    with open(tmp_dir, 'failed_jobs.args') as fj_handle:
      failed_jobs = pickle.load(fj_handle)
    dispatch_computations(failed_jobs, timestamp, args.test, args.local)
  else:
    job_args = get_job_args(args.batch_size, args.evnt_dir)
    timestamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    dispatch_computations(job_args, timestamp, args.test, args.local)

if __name__ == '__main__':
  main()

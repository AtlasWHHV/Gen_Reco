from __future__ import division

def compute(version_number, max_events, skip_events, event_file):
  ''' Runs reco.sh with the given parameters, using a tmp folder to clean up intermediary files. '''
  import tempfile, subprocess, os, stat, shutil, socket, string, constants
  log_file_handle, _ = tempfile.mkstemp(dir=constants.log_dir, prefix=(string.split(socket.gethostname(), sep='.')[0]+'_'), suffix='.log')
  tmp_dir = tempfile.mkdtemp(dir=constants.tmp_dir)
  arg = '{} {} {} {} {}'.format(constants.reco, version_number, max_events, skip_events, event_file)
  process = subprocess.Popen(arg, executable='/bin/bash', cwd=tmp_dir, shell=True, stdout=log_file_handle, stderr=subprocess.STDOUT)
  process.wait()
  # move the aod file to the output directory, and make it immutable so that
  # it is not accidentally deleted.
  output_file = '{}.aod.pool.root'.format(version_number)
  os.rename(tmp_dir + '/' + output_file, constants.aod_output_dir + '/' + output_file)
  output_file = constants.aod_output_dir + '/' + output_file
  st = os.stat(output_file)
  not_writable = ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
  os.chmod(output_file, st.st_mode & not_writable)
  shutil.rmtree(tmp_dir)
  return (socket.gethostname(), output_file)

def dispatch_computations(batch_size, evnt_dir, test, local):
  import dispy, dispy.httpd, glob, math, string, constants
  if not test and not local:
    cluster = dispy.JobCluster(compute, depends=[constants])
    http_server = dispy.httpd.DispyHTTPServer(cluster)
    jobs = []
  evnt_files = glob.glob(evnt_dir + '/*.evnt.pool.root')
  print ('Found evnt files:')
  for ii, evnt_file in enumerate(evnt_files):
    print('\t[{}] {}'.format(ii+1, evnt_file))
  job_id = 0
  for evnt_file in evnt_files:
    rel_evnt_file = string.split(evnt_file, sep='/')[-1]
    run_number, evnt_batch_size, evnt_batch_number = string.split(rel_evnt_file, sep='.')[:3]
    evnt_version = "{}.{}.{}".format(run_number, evnt_batch_size, evnt_batch_number)
    evnt_batch_size = int(evnt_batch_size)
    job_skip_events = 0
    for _ in range(int(math.ceil(evnt_batch_size / batch_size))):
      job_batch_size = min(batch_size, evnt_batch_size - job_skip_events)
      job_version_number = "{}.{}.{}".format(evnt_version, job_batch_size, job_skip_events)
      if test:
        print("job {}: version={}, batch_size={}, skip_events={}, evnt_file={}".format(job_id, job_version_number, job_batch_size, job_skip_events, evnt_file))
      elif not local:
        job = cluster.submit(job_version_number, job_batch_size, job_skip_events, evnt_file)
        job.id = job_id
        jobs.append(job)
      else:
        compute(job_version_number, job_batch_size, job_skip_events, evnt_file)
      job_skip_events += job_batch_size
      job_id += 1
  if not test and not local:    
    for job in jobs:
      host, aod_file = job()
      print('{} executed job {} from {} to {} creating {}'.format(host, job.id, job.start_time, job.end_time, aod_file))
    cluster.print_status()
    http_server.shutdown()

def clean():
  import constants, os, shutil, glob
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
  import argparse

  parser = argparse.ArgumentParser(description='Dispatch reco jobs to tev machines.')
  parser.add_argument('-b', '--batch_size', type=int, default=50, help='The number of events to reco in each job.')
  parser.add_argument('--evnt_dir', default='/phys/groups/tev/scratch3/users/WHHV/evnts/small', help='Directory that contains evnt files.')
  parser.add_argument('-c', '--clean', action='store_true', help='Remove old recovery, temporary, and log files.')
  parser.add_argument('-t', '--test', action='store_true', help='Attempts to find evnt files (and do cleaning, if --clean or -c is specified), but does not actually distribute jobs. Useful if you want to check that your parameters are correct without committing to actual computation.')
  parser.add_argument('-l', '--local', action='store_true', help='Runs all computations locally, without using dispy servers. Useful for debugging computation function.')
  args = parser.parse_args()
  if args.clean:
    clean()
  dispatch_computations(args.batch_size, args.evnt_dir, args.test, args.local)

if __name__ == '__main__':
  main()

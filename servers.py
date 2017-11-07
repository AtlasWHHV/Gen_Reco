import argparse
import constants
import os
import subprocess
import shutil
import pickle

def start(pids_file):
  if os.path.isfile(pids_file):
    print('dispy servers are already running!')
    exit(1)
  dispynode = os.path.join(constants.dispy_dir, 'dispynode.py')
  processes = []
  for server in constants.servers:
    log_file = os.path.join(constants.log_dir, server + '_reco_dispy.log')
    arg = 'ssh {} "nohup python {} --clean --daemon > {} &" | grep -Eo "[0-9]+$"'.format(server, dispynode, log_file)
    process = subprocess.Popen(arg, executable='/bin/bash', shell=True, stdout=subprocess.PIPE)
    processes.append(process)
  pids = []
  for process in processes:
    pid, _ = process.communicate()
    pids.append(pid)
  with open(pids_file, 'wb+') as pids_file_handle:
    pickle.dump(pids, pids_file_handle)

def stop(pids_file):
  if not os.path.isfile(pids_file):
    print('dispy servers are not running!')
    exit(1)
  with open(pids_file, 'rb') as pids_file_handle:
    pids = pickle.load(pids_file_handle)
    processes = []
    for server, pid in zip(constants.servers, pids):
      arg = 'ssh {} "kill {}"'.format(server, pid)
      process = subprocess.Popen(arg, executable='/bin/bash', shell=True)
      processes.append(process)
  for process in processes:
    process.wait()
  os.remove(pids_file)

def status(pids_file):
  if os.path.isfile(pids_file):
    with open(pids_file, 'rb') as pids_file_handle:
      pids = pickle.load(pids_file_handle)
      print('Active dispy servers ({} in total):'.format(len(pids)))
      print('')
      for server, pid in zip(constants.servers, pids):
        print('\thost: {}\tpid: {}'.format(server, pid))
  else:
    print('No dispy servers are currently active.')

def main():
  parser = argparse.ArgumentParser(description='Manage dispy servers.')
  parser.add_argument('command', choices=['start', 'stop', 'restart', 'status'])
  args = parser.parse_args()
  pids_file = os.path.join(constants.pids_dir, 'reco_dispy.pids')
  if args.command == 'start':
    start(pids_file)
  elif args.command == 'stop':
    stop(pids_file)
  elif args.command == 'restart':
    stop(pids_file)
    start(pids_file)
  elif args.command == 'status':
    status(pids_file)

if __name__ == '__main__':
  main()

# Gen_Reco
This repository contains scripts that perform the four steps necessary to create synthetic data from atlas based on the hidden valley theory: generation, simulation, digitization, and reconstruction. Note that more information can be found in the full_chain_simulation document, or on the cern wiki. 

## Generation
Generation is the process of creating event data for a particular model of physics, in this case a hidden valley model. Event data describes the chain of particles that are created as a result of high-energy particle beams colliding in ATLAS, but does not take into account the properties of the detector. This step is based on the Feynman diagrams describing the model, and the properties of the particle beams.

## Simulation
Simulation is the process of taking event data and simulating the effects of the detector. For example, a particle might scatter off part of the detector, depositing some energy and changing its trajectory.

## Digitization
Digitization is the process of taking hits data from simulation and calculating the response of the detector to the particles. This produces the raw digital output that you would see at the real ATLAS detector.

## Reconstruction
Reconstruction is the process of taking raw data from digitization and reconstructing likely particle tracks and energy deposits. This is known as event summary data. This data is then used to construct analysis object data, which is similar to the initial event data, except that instead of dealing with truth, we now have probabilities of possible events. In our project, relevant variables are extracted from this file and used to train the neural network.

# Getting Started
This section will provide you with the steps necessary to obtain a copy of the project and run it on your machine for development/testing purposes. See deployment for details on running a full-scale job.

## Prerequisites
This project is designed to run on the UW Physics Department tev machines using python 2.7, although it could be amended to run on another system, provided that atlas is setup. If you do not know how to access the tev machines, please consult the relevant documentation on the group [website](charm.epe.phys.washington.edu:8080).

Once you are on the tev machines, the first thing to do is to [download](https://help.github.com/articles/cloning-a-repository/) the repository code. Note that, when operating a terminal on the tev machines, you should always be using bash. You can start bash simply by typing `bash` into a terminal.

Once you have cloned the repository and are in bash, run `. package_setup.sh`. This will install the necessary python packages, and run a simple test that should print out version numbers for these packages.

## Installation
The settings for the project are stored in the constants.py and hostfile.txt files. In these files you can edit the list of tev servers to use, the root directory for the project, and settings relating to the athena scripts.

To check that you have everything setup correctly, run (on tev01):
```
python ~/.local/lib/python2.7/site-packages/distributed/cli/dask_ssh.py --scheduler tev01 --hostfile hostfile.txt
```
Then, run `python client.py -t` on another terminal. Press Ctrl + C on the first terminal to terminate the servers.

## Running
The files in this repository can be split into two main categories: generation (generate.py, hss-runner.py, MadGraphControl_HSS.py) and simulation/digitization/reconstruction (client.py, reco.py), usually referred to as simply reconstruction, or reco.

### Generation
hss-runner.py and MadGraphControl_HSS.py are configuration files for athena event generation: they specify details regarding the hidden valley model and how it should be generated. They should generally not be modified unless the parameters of the project change. generate.py is a script that runs the athena event generation, creating a set of event files. Run `python generate.py -h` to see a complete listing of available options (this also works on client.py, servers.py, and reco.py).

### Reconstruction
reco.py is similar to generate.py, but instead of generation, it performs the full simulation/digitization/reconstruction process on a given event file. This file can be run directly for testing purposes, but in deployment, it should only be run indirectly through client.py. client.py is a script that manages distributed computation across the tev machines: it essentially splits up the job of reconstructing a large set of events into small batches called jobs, and distributes these jobs to the tev machines. However, before this can be done, you must run dask-ssh as shown in the installation section, which primes the tev machines listed in hostfile.txt so that they are ready to receive jobs from client.py.

# Deployment
Once you're comfortable with how the scripts work, and you've modified the settings as appropriate, you're ready to run a full-blown generation/reconstruction cycle. There are 4 steps to follow:
1. Run `python generate.py -b BATCHSIZE -n NUM_BATCHES --evnt_dir EVNT_DIR`
2. Run `python ~/.local/lib/python2.7/site-packages/distributed/cli/dask-ssh.py --scheduler tev01 --hostfile hostfile.txt --nthreads 8` (Find an appropriate number of threads such that the system does not reach 100% memory utilization, which can severely slow down computation).
3. Run `python client.py -b BATCH_SIZE --evnt_dir EVNT_DIR` where BATCH_SIZE is the size of each job sent to each tev machine (around 10-50 is probably a good number), and EVNT_DIR should be the same as in step 1. It's a good idea to run this command with `-t` first, to make sure that your settings are correct.
4. Analyze the logs from the run, and diagnose the causes of any failures. Once these issues are resolved, Run `python client.py -r TIMESTAMP`, where TIMESTAMP is the timestamp shown by step 3, to rerun the failed jobs. Repeat this step as necessary.

# Authors
* Andrew Arbogast - *created the repository, created the initial script on which later work was based*
* Nicolas Copernicus - *added the athena event generation job configuration scripts*
* Alex Schuy - *added the distributed computation scripts*

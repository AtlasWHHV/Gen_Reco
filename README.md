# Gen_Reco
Performs the four steps necessary to create synthetic data from atlas based on the hidden valley theory: generation, simulation, digitization, and reconstruction. Note that more information can be found in the full_chain_simulation document, or on the cern wiki. 

## Generation
Generation is the process of creating event data for a particular model of physics, in this case a hidden valley model. Event data describes the chain of particles that are created as a result of high-energy particle beams colliding in ATLAS, but it does not take into account the properties of the detector. This step is based on the Feynman diagrams describing the model, and the properties of the particle beams.

Generation can be performed by executing generator_setup.sh. This runs Generate_tf.py, an ATLAS tool, using appropriate options. The physics of the model we are testing is described in hss-runner.py, which is passed to Generate_tf.py. Events are created in batches which can be specified in generator_setup.sh, and are outputted with names of the form [run_number].[events_per_batch].[batch_number].evnt.pool.root. Note that the files are POOL and ROOT files.

Simulation, Digitization, and Reconstruction can be performed by executing scripts simulator_setup.sh, digitizer_setup.sh, and reconstructor_setup.sh, respectively, which execute other ATLAS tools.

## Simulation
Simulation is the process of taking event data and simulating the effects of the detector. For example, a particle might scatter off part of the detector, depositing some energy and changing its trajectory.

## Digitization
Digitization is the process of taking hits data from simulation and calculating the response of the detector to the particles. This produces the raw digital output that you would see at the real ATLAS detector.

## Reconstruction
Reconstruction is the process of taking raw data from digitization and reconstructing likely particle tracks and energy deposits. This is known as event summary data. This data is then used to construct analysis object data, which is similar to the initial event data, except that instead of dealing with truth, we now have probabiltiies of possible events. In our project, relevant variables are extracted from this file and used to train the neural network.

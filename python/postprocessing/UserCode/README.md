`UPDATE:` This repo has been updated on 20/01/2020 in order to include all changes from the CENTRAL repo of NanoTools.

# Instalation

```
cmsrel CMSSW_10_2_0
cd CMSSW_10_2_0/src/
cmsenv
git clone https://gitlab.cern.ch/brochero/nanoaodtociemat.git PhysicsTools/NanoAODTools
scram b -j 20
cd PhysicsTools/NanoAODTools
```

# To run local test

1. Modify the input file in `python/postprocessing/CIEMAT/postprocNanoAODCIEMAT.py`
2. Read the helper:

```
python python/postprocessing/CIEMAT/postprocNanoAODCIEMAT.py --help
```

3. To run (example):

```
python python/postprocessing/CIEMAT/postprocCIEMAT.py --Year 2016 --DataSet "mujets" -n 100
```
4. Output: Now there are two outputs: 
  - `filename_Skim,root`: Contains the Skimmed flat tree with the additional branches. 
  - `filename_Skim,root.hist`: Contains the histogram with the info if the events processed, weights, etc.

# CRAB

1. Go to the crab directory `PhysicsTools/NanoAODTools/crab`
2. Open `crab_script.py` to modify the "Year" and DataSet. For crab, it cant be done from command line with the --Year --DataSet :(
3. Open `crab_cfg.py` to modify:

```
# The DataSet
config.Data.inputDataset = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM'

# Number of jobs
config.Data.unitsPerJob = 5

# Site to store the output
config.Site.storageSite = "T2_CH_CERN"

```

## To Run:

```
crab submit -c crab_cfg.py
```

remember to do:

```
voms-proxy-init --voms cms
```

in advance

That is all!

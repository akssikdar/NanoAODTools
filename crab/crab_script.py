#!/usr/bin/env python
import os, sys,argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

## Manual Configuration
# choices=["2016","2017","2018"]
Year = "2018"
# choices=["mc","top","mujets","ejets","mumu","ee","mue"]
DataSet = "mujets"

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# -- My Modules
from PhysicsTools.NanoAODTools.postprocessing.UserCode.createNanoAODSkim import *

if DataSet == "mc" or DataSet == "top":
    # -- MC Modules
    # - JES
    from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
    # - PileUp
    from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
    # - b-tagging SF
    from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

    if Year == "2016":
        module_JES = jetmetUncertainties2016All()
        module_PU  = puWeight_2016()
        module_btag= btagSFdeep2016()
    if Year == "2017":
        module_JES = jetmetUncertainties2017All()
        module_PU  = puWeight_2017()
        module_btag= btagSFdeep2017()
    if Year == "2018":
        module_JES = jetmetUncertainties2018All()
        module_PU  = puWeight_2018()
        module_btag= btagSFdeep2018()

    MyModules = [#module_JES,
                 #module_PU,
                 #module_btag,
                 createNanoAODSkim(InpSample=DataSet,InpYear=Year,InpOutName=["DirectoryCrabMC","_Skim.root"],InpCRAB=True)]

# is Data?
else:
    MyModules = [createNanoAODSkim(InpSample=DataSet,InpYear=Year,InpOutName=["DirectoryCrabData","_Skim.root"],InpCRAB=True)]


p=PostProcessor("NanoResults",inputFiles(),
		cut = None, branchsel = "keep_and_drop_in.txt",
		modules = MyModules,
		compression = 'LZMA:9', 
		friend = False, 
		postfix = None, 
		noOut = False, 
		justcount = False, 
		prefetch = False, 
		longTermCache = False, 
		maxEntries = None, 
		firstEntry = 0, 
		outputbranchsel = "keep_and_drop_out.txt",
                # for CRAB
		provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()
print "DONE"

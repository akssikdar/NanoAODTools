#!/usr/bin/env python
import os, sys,argparse
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True

parser = argparse.ArgumentParser(description="W-Helicity From NanoAOD")
parser.add_argument('--NanoInput', '-nano', type=str, default="none",
                    help='Dataset to be processed.')
parser.add_argument('--Year', '-y', type=str, default="2016",
                    help='Data period')
parser.add_argument('--DataSet', '-ds', type=str, default="mc",
             choices=["mc","top","mujets","ejets","mumu","ee","mue"],
                    help='DataSet to be processed')
parser.add_argument('--OuputDir', '-o', type=str, default="none",
                    help='Output directory name.')
parser.add_argument('--Entries', '-n', type=int, default=None,
                    help='Number of entries')

args = parser.parse_args()


from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

## -- Provide the full path for Input files
if args.NanoInput == "none":
    # 2017 MC
    #NanoFileName = "root://cms-xrd-global.cern.ch///store/mc/RunIIFall17NanoAODv6/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7_ext1-v1/260000/C5B85D05-B55E-0043-9941-5EB28BA97047.root" 
    # 2017 Data
    NanoFileName = "root://cms-xrd-global.cern.ch///store/data/Run2017B/SingleElectron/NANOAOD/Nano25Oct2019-v1/20000/57B961B0-DCB3-6C48-864B-9C9EC7263E7D.root"
    # 2016 Data
    #NanoFileName = "root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv5/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/250000/4EC4EB5B-5F1A-654C-9974-59E21D90A4CC.root"
else:
    NanoFileName = args.NanoInput

# Get name of the file
FullPathFileName = NanoFileName.split('/')
nFPFN = len(FullPathFileName)

# DirName (Structure from DAS path)
OutRefFileName = ['Dir','FileName.root']

outpath = os.getcwd() + "/"
if args.OuputDir != "none":
    outpath = args.OuputDir + "/"

#if nFPFN > 4 and "xrd-global" in NanoFileName:
if nFPFN > 4 and "xrootd-cms.infn.it" in NanoFileName:
    OutRefFileName[0] = outpath + FullPathFileName[nFPFN-5]
else:
    print "Name for output-directory not available from the input..."
    OutRefFileName[0] = outpath + "NanoResults"
    
print "Output directory set to " + OutRefFileName[0]

if os.path.exists(OutRefFileName[0]):
    print ("WARNING: " + str(OutRefFileName[0]) + " directory exits! Files can be overwrote!")
else:
    print ("Creating " + str(OutRefFileName[0]) + " directory...")
    os.makedirs(OutRefFileName[0])

# FileName
if nFPFN > 0:
    OutRefFileName[1] = FullPathFileName[nFPFN-1]
    OutRefFileName[1] = OutRefFileName[1].replace('.root','_Skim.root')
else:
    print "Problems defining the outputname..."
    exit

# - CIEMAT Module
from PhysicsTools.NanoAODTools.postprocessing.UserCode.createNanoAODSkim import *


if args.DataSet == "mc" or args.DataSet == "top":
    # -- MC Modules
    # - JES
    from  PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
    # - PileUp
    from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
    # - b-tagging SF
    from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

    if args.Year == "2016":
	module_JES = jetmetUncertainties2016All()
	module_PU  = puWeight_2016()
	module_btag= btagSFdeep2016()
    if args.Year == "2017":
	module_JES = jetmetUncertainties2017All()
	module_PU  = puWeight_2017()
	module_btag= btagSFdeep2017()
    if args.Year == "2018":
	module_JES = jetmetUncertainties2018All()
	module_PU  = puWeight_2018()
	module_btag= btagSFdeep2018()

    MyModules = [#module_JES,
		 #module_PU,
		 #module_btag,
		 createNanoAODSkim(InpSample=args.DataSet,InpYear=args.Year,InpOutName=OutRefFileName,InpCRAB=False)]
    
# is Data?
else:    
    MyModules = [createNanoAODSkim(InpSample=args.DataSet,InpYear=args.Year,InpOutName=OutRefFileName,InpCRAB=False)]

# -- Process
p=PostProcessor(OutRefFileName[0],[NanoFileName],
		cut = None,
		modules = MyModules,
		branchsel = os.environ["CMSSW_BASE"]+"/src/PhysicsTools/NanoAODTools/python/postprocessing/UserCode/keep_and_drop_in.txt",
		compression = 'LZMA:9', 
		friend = False, 
		postfix = None, 
		jsonInput = None, 
		noOut = False, 
		justcount = False, 
		prefetch = False, 
		longTermCache = False, 
		maxEntries = args.Entries, 
		firstEntry = 0, 
		outputbranchsel = os.environ["CMSSW_BASE"]+"/src/PhysicsTools/NanoAODTools/python/postprocessing/UserCode/keep_and_drop_out.txt")

p.run()

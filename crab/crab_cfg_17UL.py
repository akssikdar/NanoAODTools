from CRABClient.UserUtilities import config
config = config()
config.section_("General")
config.General.workArea = 'crab_projects'

#---------------------
#2018 nanoAOD samples tag
#---------------------


#config.General.requestName = 'SingleMuon_2018D'

config.General.transferLogs=True

config.section_("JobType")
# Additional configuration to request nodes with higher RAM
# config.JobType.maxMemoryMB = 3500
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py','../python/postprocessing/UserCode/keep_and_drop_in.txt','../python/postprocessing/UserCode/keep_and_drop_out.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
## It does not save the input NANOAOD with the additional collections 
config.JobType.disableAutomaticOutputCollection = False
## Name of the output files
config.JobType.outputFiles = ['tree.root.hist']

config.section_("Data")

#---------------------
#2018 nanoAOD samples
#---------------------
##SingleMuon
#config.Data.inputDataset = '/SingleMuon/Run2018A-Nano25Oct2019-v1/NANOAOD'
##EGamma
#config.Data.inputDataset = '/EGamma/Run2018A-Nano25Oct2019-v1/NANOAOD'
##TTbar

# JSON file for DATA: 2018
#config.Data.lumiMask     = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Data.outputDatasetTag = '2018_skim4_WW'
config.Data.outLFNDirBase = '/store/group/phys_top/asikdar/LUT_Nano/2018_skim4/'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1

#config.Data.outLFNDirBase = '/store/user/%s/2017_NanoAOD-v6' % (getUsernameFromSiteDB())
#config.Data.outLFNDirBase = '/store/group/phys_top/asikdar/LUT_Nano/2017_skim5/'
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

from CRABClient.UserUtilities import config
config = config()
config.section_("General")
config.General.workArea = 'crab_projects'

#---------------------
#2018 nanoAOD samples tag
#---------------------
##SingleMuon
#config.General.requestName = 'SingleMuon_2018A_NanoAODv9'
#config.General.requestName = 'SingleMuon_2018B_NanoAODv9'
#config.General.requestName = 'SingleMuon_2018C_NanoAODv9'
config.General.requestName = 'SingleMuon_2018D_NanoAODv9'
##EGamma
#config.General.requestName = 'EGamma_2018A_NanoAODv9'
#config.General.requestName = 'EGamma_2018B_NanoAODv9'
#config.General.requestName = 'EGamma_2018C_NanoAODv9'
#config.General.requestName = 'EGamma_2018D_NanoAODv9'
##TTbar
#config.General.requestName = 'TTTo2L2Nu_2018_NanoAODv9'
#config.General.requestName = 'TTToSemiLeptonic_2018_NanoADOv9'
#config.General.requestName = 'TTToHadronic_2018_NanoADOv9'
##DYJets
#config.General.requestName = 'DYJetsToLL_M-10to50_2018_NanoADOv9'
#config.General.requestName = 'DYJetsToLL_0J_2018_NanoADOv9'
#config.General.requestName = 'DYJetsToLL_1J_2018_NanoADOv9'
#config.General.requestName = 'DYJetsToLL_2J_2018_NanoADOv9'
##SingleTop
#config.General.requestName = 'ST_tW_top_5f_2018_NanoADOv9'
#config.General.requestName = 'ST_tW_antitop_5f_2018_NanoADOv9'
#config.General.requestName = 'ST_t-channel_top_4f_2018_NanoADOv9'
#config.General.requestName = 'ST_t-channel_antitop_4f_2018_NanoADOv9'
#config.General.requestName = 'ST_s-channel_4f_leptonDecays_2018_NanoADOv9'
##WJets
#config.General.requestName = 'WJetsToLNu_0J_2018_NanoADOv9'
#config.General.requestName = 'WJetsToLNu_1J_2018_NanoADOv9'
#config.General.requestName = 'WJetsToLNu_2J_2018_NanoADOv9'
##Dibosons
#config.General.requestName = 'WW_2018_NanoAODv9'
#config.General.requestName = 'WZ_2018_NanoAODv9'
#config.General.requestName = 'ZZ_2018_NanoAODv9'

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
#config.Data.inputDataset = '/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
#config.Data.inputDataset = '/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
#config.Data.inputDataset = '/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
config.Data.inputDataset = '/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
##EGamma
#config.Data.inputDataset = '/EGamma/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
#config.Data.inputDataset = '/EGamma/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
#config.Data.inputDataset = '/EGamma/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
#config.Data.inputDataset = '/EGamma/Run2018D-UL2018_MiniAODv2_NanoAODv9-v3/NANOAOD'
##TTbar
#config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
##DYJets
#config.Data.inputDataset = '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
##SingleTop
#config.Data.inputDataset = '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
#config.Data.inputDataset = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
#config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/ST_s-channel_4f_leptonDecays_TuneCP5CR1_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
##WJets
#config.Data.inputDataset = '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
##Dibosons
#config.Data.inputDataset = '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
#config.Data.inputDataset = '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'

##JSON file for DATA: 2018
config.Data.lumiMask     = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

##SingleMuon
#config.Data.outputDatasetTag = '2018A_skim4_SingleMuon'
#config.Data.outputDatasetTag = '2018B_skim4_SingleMuon'
#config.Data.outputDatasetTag = '2018C_skim4_SingleMuon'
config.Data.outputDatasetTag = '2018D_skim4_SingleMuon'
##EGamma
#config.Data.outputDatasetTag = '2018A_skim4_EGamma'
#config.Data.outputDatasetTag = '2018B_skim4_EGamma'
#config.Data.outputDatasetTag = '2018C_skim4_EGamma'
#config.Data.outputDatasetTag = '2018D_skim4_EGamma'
##SingleTop
#config.Data.outputDatasetTag = '2018_skim4_ST_t_channel_top'
#config.Data.outputDatasetTag = '2018_skim4_ST_t_channel_antitop'
#config.Data.outputDatasetTag = '2018_skim4_ST_s_channel'
#config.Data.outputDatasetTag = '2018_skim4_WJetsToLNu_0J'
#config.Data.outputDatasetTag = '2018_skim4_WJetsToLNu_1J'
#config.Data.outputDatasetTag = '2018_skim4_WJetsToLNu_2J'
#config.Data.outputDatasetTag = '2018_skim4_WW'
#config.Data.outputDatasetTag = '2018_skim4_WZ'
#config.Data.outputDatasetTag = '2018_skim4_ZZ'

config.Data.outLFNDirBase = '/store/group/phys_top/asikdar/LUT_Nano/2018_skim4/'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1

config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

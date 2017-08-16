from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.requestName = 'Bfinder_Run2016B-23Sep2016-v3'
# request name is the name of the folder where crab log is saved

config.General.workArea = 'crab3_projects'
config.General.transferOutputs = True
config.General.transferLogs = False


config.section_('JobType')
# set here the path of your working area
config.JobType.psetName = 'Bfinder_pp_80x_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['bfinder.root']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset ='/Charmonium/Run2016B-23Sep2016-v3/AOD'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10

# set here the path of a storage area you can write to
config.Data.outLFNDirBase = '/store/user/gghillar/Bfinder_Run2016/B'
config.Data.lumiMask='https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_MuonPhys.txt'

config.Data.publication= False
config.Data.outputDatasetTag='Bfinder_Run2016B-23Sep2016-v3'
############## 

#config.Data.ignoreLocality = True

config.section_("Site")

# set here a storage site you can write to
config.Site.storageSite = 'T2_PT_NCG_Lisbon'

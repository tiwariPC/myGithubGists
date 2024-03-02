name = 'HLTRun_DeepCSV'
runATCAF = False

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.workArea = 'crab_'+name
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'hlt_DeepCSV_run'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'hlt_DeepCSV_run.py'
config.JobType.maxMemoryMB = 2400
config.JobType.numCores = 4
config.JobType.outputFiles = ['outputFULL.root','DQMIO.root']

config.Data.inputDBS = 'global'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.publication = False

config.Data.inputDataset = '/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16DR-FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/GEN-SIM-RAW'
config.Data.unitsPerJob = 1000
config.Data.totalUnits = -1
config.Data.outputDatasetTag = 'HLT_DeepCSV_Run'
config.Data.outLFNDirBase = '/store/user/%s/t3store2/HLTRun' % (getUsernameFromSiteDB())
config.Site.storageSite = 'T2_IN_TIFR'
if runATCAF :
   config.Site.whitelist = ['T3_CH_CERN_CAF']
   config.Site.ignoreGlobalBlacklist = True
   config.Data.ignoreLocality = True

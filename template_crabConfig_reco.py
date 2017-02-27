from WMCore.Configuration import Configuration
import time

config = Configuration()

config.section_("General")
config.General.requestName = 'EmJetSignalMCReco' + time.strftime("-%Y%m%d-%H%M%S")
config.General.workArea = 'crabTasks/' + config.General.requestName
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
# Name of the CMSSW configuration file
config.JobType.psetName    = 'test/aodsim_RunIISpring16DR80_cfg.py'
# config.JobType.pyCfgParams = ['crab=1']
# config.JobType.scriptArgs  = ''
config.JobType.maxMemoryMB = 4000

config.section_("Data")
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.inputDataset = '${inputdataset}'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = ${filesperjob}
config.Data.totalUnits = ${totalfiles}
config.Data.publication = True
config.Data.outLFNDirBase = '${lfndirbase}'
config.Data.ignoreLocality = True

# This string is used to construct the output dataset name
config.Data.outputDatasetTag = '${datasettag}'

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = '${storagesite}'


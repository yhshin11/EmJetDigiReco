# EmJetDigiReco

Scripts to facilitate running DIGI-RECO steps to produce AODSIM-tier MC samples for the Emerging Jet analysis

## Instructions for RunIISummer16DR80Premix
```
# Setup CMSSW
cmsrel CMSSW_8_0_21
cd CMSSW_8_0_21/src
cmsenv

# Source CRAB script, e.g. for bash shell:
source /cvmfs/cms.cern.ch/crab3/crab.sh

# Obtain grid proxy
voms-proxy-init -voms cms -rfc

git clone git@github.com:yhshin11/EmJetDigiReco.git
cd EmJetDigiReco
git fetch --tags
# Checkout specific tag, e.g. v2017-02-20
git checkout tags/v2017-02-20
# Optional step: Do this if you want to track local changes in git
# git checkout -b my_branch

# IMPORTANT: Edit main script to change lfndirbase, storagesite, etc
vim runRecoJobs.py
# Run main script
python runRecoJobs.py
```

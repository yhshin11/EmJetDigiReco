import os
import subprocess
import sys
from string import Template
from collections import OrderedDict
from pprint import pprint
from dataset_management.parse_datasets_emjet import get_dataset_dict

def getjobname_fromstring(mass_X_d, mass_pi_d, tau_pi_d):
    jobname = 'mass_X_d_%s_mass_pi_d_%s_tau_pi_d_%s' % (mass_X_d, mass_pi_d, tau_pi_d)
    return jobname

def execute(args):
    """Wrapper function to execute arbitrary shell commands"""
    print '################################'
    print 'args: ', args
    p = subprocess.Popen(args, shell=True, executable='/bin/bash')
    # p = subprocess.call(args, shell=True, executable='/bin/bash')
    p.wait()
    return p
    print '################################'

dataset_dict = get_dataset_dict('dataset_management/datasets_emjet_gensim.txt')
dataset_dict_filtered = { k:v for (k,v) in dataset_dict.items() if k[0] == '1000' }

jobdirname = 'jobs'
crabconfigname = 'crabConfig.py'

for key, val in dataset_dict_filtered.items():
    ########################################
    # Generate CRAB config file
    ########################################
    mass_X_d  = key[0]
    mass_pi_d = key[1]
    tau_pi_d  = key[2]
    inputdataset   = val
    jobname = getjobname_fromstring(mass_X_d, mass_pi_d, tau_pi_d)
    if not os.path.exists(os.path.join(jobdirname, jobname)):
        os.makedirs(os.path.join(jobdirname, jobname))

    kwdict_crab = {}
    kwdict_crab['jobname'] = jobname
    kwdict_crab['datasettag'] = 'AODSIM'
    kwdict_crab['filesperjob'] = 1
    kwdict_crab['totalfiles'] = 10000
    kwdict_crab['lfndirbase'] = '/store/user/yoshin/EmJetMC/AODSIM/'
    kwdict_crab['storagesite'] = 'T3_US_UMD'
    kwdict_crab['inputdataset'] = inputdataset

    crabconfigtemplate = open('template_crabConfig_reco.py', 'r')
    crabconfigpath = os.path.join(jobdirname, jobname, crabconfigname)
    crabconfigfile = open(crabconfigpath, 'w')
    for line in crabconfigtemplate:
        t = Template(line)
        subline = t.substitute(kwdict_crab)
        # print subline.rstrip('\n')
        crabconfigfile.write(subline)
    crabconfigfile.close()


for key, val in dataset_dict_filtered.items():
    mass_X_d  = key[0]
    mass_pi_d = key[1]
    tau_pi_d  = key[2]
    jobname = getjobname_fromstring(mass_X_d, mass_pi_d, tau_pi_d)
    ########################################
    # Submit CRAB tasks
    ########################################
    print os.getcwd()
    crabconfigpath = os.path.join(jobdirname, jobname, crabconfigname)
    # crabcommand =  './crab_wrapper.sh %s %s %s' % ('--skip-estimates', '--dryrun', crabconfigpath)
    crabcommand =  './crab_wrapper.sh %s %s %s' % ('', '', crabconfigpath)
    print 'crabcommand: ', crabcommand
    print 'Executing crabcommand'
    p=subprocess.Popen(crabcommand, shell=True)
    p.wait()


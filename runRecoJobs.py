import os
import subprocess
import sys
from string import Template
from collections import OrderedDict
from pprint import pprint
from dataset_management.parse_datasets_emjet import get_dataset_dict

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testing', action='store_true', help='Enable testing mode. Submits single dataset.')
args = parser.parse_args()
testing = args.testing
print testing

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

# Get dataset dictionary in form: { (mass_X_d, mass_pi_d, tau_pi_d) : dataset_name }
dataset_dict = get_dataset_dict('dataset_management/datasets_emjet_gensim_2017-09-06b.txt')
run_filtered_only = 1
if not run_filtered_only:
    # Run all datasets
    dataset_dict_filtered = { k:v for (k,v) in dataset_dict.items() }
else:
    # Run only mass_X_d_1000 datasets
    dataset_dict_filtered = { k:v for (k,v) in dataset_dict.items() if k[0] != '1000' }
if testing:
    dataset_dict_filtered = { k:v for (k,v) in dataset_dict.items() if k[0] == '1000' and k[1] == '2' and k[2] == '5' }

jobdirname = 'jobs'
crabconfigname = 'crabConfig.py'

for key, val in dataset_dict_filtered.items():
    print key, val

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

    # Tag for output dataset to avoid collision
    tagname = 'v2017-09-11b'
    kwdict_crab = {}
    kwdict_crab['jobname'] = jobname
    kwdict_crab['requestname'] =  'EmJetSignalMCReco'
    kwdict_crab['datasettag'] = 'RunIISummer16DR80Premix_private-AODSIM-' + tagname
    if testing: kwdict_crab['datasettag'] += '-test'
    kwdict_crab['filesperjob'] = 1
    kwdict_crab['totalfiles'] = 10000
    # kwdict_crab['lfndirbase'] = '/store/user/yoshin/EmJetMC/AODSIM/%s/' % tagname
    kwdict_crab['lfndirbase'] = '/store/user/eno/EmJetMC/AODSIM/%s/' % tagname
    if testing: kwdict_crab['lfndirbase'] += 'test/'
    # kwdict_crab['storagesite'] = 'T3_US_UMD'
    kwdict_crab['storagesite'] = 'T3_US_FNALLPC'
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


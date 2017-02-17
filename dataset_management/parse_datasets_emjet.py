# from pprint import pprint

def get_dataset_dict(filename = 'datasets_emjet_gensim.txt'):
    """Parses input file containing lines of EmJet GENSIM datasets into a dictionary.
    Returned dictionary is of the form: dictionary[(mass_X_d, mass_pi_d, tau_pi_d)] = DATASETNAME,
    where mass_X_d, mass_pi_d, tau_pi_d are string representations of the parameter values.
    E.g. dictionary[('1000', '1', '0p001')] = '/EmergingJets_mass_X_d_1000_mass_pi_d_1_tau_pi_d_0p001_TuneCUETP8M1_13TeV_pythia8Mod/yoshin-mass_X_d_1000_mass_pi_d_1_tau_pi_d_0p001-5d731f1bf4c9a8891d89827c732d4510/USER'
    """
    f = open(filename, 'r')
    datasets_emjet = {}
    for line in f:
        splitstring = line.split('_')
        mass_X_d = splitstring[4]
        mass_pi_d = splitstring[8]
        tau_pi_d = splitstring[12]

        datasets_emjet[(mass_X_d, mass_pi_d, tau_pi_d)] = line.rstrip()
    return datasets_emjet

# datasets_emjet_filtered = {}
# for key, val in datasets_emjet.items():
#     if key[0] == '1000': datasets_emjet_filtered[key] = val

# pprint(datasets_emjet_filtered)

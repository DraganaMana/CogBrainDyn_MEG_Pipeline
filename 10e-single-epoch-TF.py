# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 16:39:02 2019

@author: Dragana
"""

import os.path as op
import numpy as np
import matplotlib.pyplot as plt

import mne
from mne.parallel import parallel_func

import config

freqs = np.arange(3, 60) # Used initially for Replay and then for Play
n_cycles = freqs / 3.

TF_epochs = ['TF1', 'TF2', 'TF3', 'TF4', 'TF5', 'TF6', 'TF7', 'TF8', 'TF9', 'TF10',
             'TF11', 'TF12', 'TF13', 'TF14', 'TF15', 'TF16', 'TF17', 'TF18', 'TF19', 'TF20',
             'TF21', 'TF22', 'TF23', 'TF24', 'TF25', 'TF26', 'TF27', 'TF28', 'TF29', 'TF30']

def run_time_frequency(subject):
    print("Processing subject: %s" % subject)
    meg_subject_dir = op.join(config.meg_dir, subject)
    extension = config.name_ext + '_cleaned-epo'
    fname_in = op.join(meg_subject_dir,
                       config.base_fname.format(**locals()))
    print("Input: ", fname_in)

    epochs = mne.read_epochs(fname_in)

    for condition in config.time_frequency_conditions:
        
        these_epochs = epochs[condition]
        
        i=1
        for j in range(len(these_epochs)):
        #        for single_epoch in these_epochs:

            single_epoch = these_epochs[j]
            power, itc = mne.time_frequency.tfr_morlet(
                single_epoch, freqs=freqs, return_itc=True, n_cycles=n_cycles, n_jobs=5)
    
            power.save(
                op.join(meg_subject_dir, '%s_%s_power_%s_epoch-TF%s-tfr.h5'
                        % (config.study_name, subject,
                           condition.replace(op.sep, ''), str(i))), overwrite=True)
#            itc.save(
#                op.join(meg_subject_dir, '%s_%s_itc_%s_epoch-%s-TFtfr.h5'
#                        % (config.study_name, subject,
#                           condition.replace(op.sep, ''), str(i))), overwrite=True)
            i=i+1
#    
#            if config.plot:
#                power.plot_joint(baseline=(-0.3, -0.1), mode='percent', tmin=-0.5, tmax=1.25,
#                                 timefreqs=[(.15, 10), (0.6, 20)])
##                plt.savefig('%s_%s_%s_%s.png' %(config.study_name, subject,
##                                             condition.replace(op.sep, ''), 'TFpercent'))
#                plt.close()
        


parallel, run_func, _ = parallel_func(run_time_frequency, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)
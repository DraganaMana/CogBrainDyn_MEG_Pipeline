# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:10:56 2019

@author: Dragana
"""

import os.path as op

import mne
import numpy as np

import config

subject = 'hm070076' #'at140305','hm070076', 'fr190151'
#runs = ['Run01']
runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
meg_subject_dir = op.join(config.meg_dir, subject)

###############################################################################

# Read raw files from MEG room
""" 
for run in runs:
    extension = run + '_raw'
    raw_MEG = op.join(meg_subject_dir,
                               config.base_fname.format(**locals()))
    
    raw = mne.io.read_raw_fif(raw_MEG,
                                  allow_maxshield=config.allow_maxshield,
                                  preload=True, verbose='error')
#    raw.pick_types('grad')
    # plot raw data
    raw.plot(n_channels=50, butterfly=False, group_by='original')
    # plot power spectral densitiy
    raw.plot_psd(area_mode='range', tmin=10.0, tmax=100.0,
                         fmin=0.3, fmax=100., average=True)
    
# Read delay files
#raw_MEG = op.join('D:/ScaledTime/Delay_check/', 'ScaledTime_delayCheck_vis_pointCross2.fif')
raw_MEG = op.join('D:/ScaledTime/Delay_check/', 'ScaledTime_delayCheck_vis_pointPoint.fif')
raw = mne.io.read_raw_fif(raw_MEG, allow_maxshield=True, preload=True, verbose='error')
raw.plot(n_channels=50, butterfly=False, group_by='original')
   
# Read files after 01-import_and_filter.py - filtered files

for run in runs:
    extension = run + '_filt_raw'
    raw_filt = op.join(meg_subject_dir,
                            config.base_fname.format(**locals()))
    raw = mne.io.read_raw_fif(raw_filt, allow_maxshield=True)
    # plot raw data
    raw.plot(n_channels=50, butterfly=False, group_by='position')
    # plot power spectral densitiy
    raw.plot_psd(area_mode='range', tmin=10.0, tmax=100.0,
                 fmin=0., fmax=50., average=True)
    
# Read files after 02-apply_maxwell_filter.py

for run in runs:
    extension = run + '_sss_raw'
    raw_sss = op.join(meg_subject_dir,
                                config.base_fname.format(**locals()))
    raw = mne.io.read_raw_fif(raw_sss, allow_maxshield=True)
    #  plot maxfiltered data
    raw.plot(n_channels=50, butterfly=True, group_by='position')
    

    
# Read files (events) after 03-extract_events.py
for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
    events = mne.read_events(eve_fname)

figure = mne.viz.plot_events(events)
figure.show()
"""


## Read files after 04-make_epochs.py
#extension = '-int-P-1-2-3_cleaned-epo'
#fname_in = op.join(meg_subject_dir,
#               config.base_fname.format(**locals()))
#epochs = mne.read_epochs(fname_in, preload=True)
#epochs.plot_psd(fmin=2., fmax=40.)
#
#
## Read files from 10-TF
#for condition in config.time_frequency_conditions:
#    power_name = op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
#                    % (config.study_name, subject,
#                       condition.replace(op.sep, '')))
#    power = mne.time_frequency.read_tfrs(power_name)
#    power[0].plot_joint(baseline=(-1.5, -0.8), mode='mean', tmin=-1.5, tmax=1.25,
#                 timefreqs=[(.15, 10), (0.6, 20)])
#        

#%% Plot average PSD

# Read files after 04-make_epochs.py
extension = '-int-P-1-2-3_cleaned-epo'
fname_in = op.join(meg_subject_dir,
               config.base_fname.format(**locals()))
epochs = mne.read_epochs(fname_in, preload=True)
epochs.plot_psd(fmin=2., fmax=40.)



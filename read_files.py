# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:10:56 2019

@author: Dragana
"""

import os.path as op

import mne

import config

subject = 'lk160274'
runs = ['Run05']
meg_subject_dir = op.join(config.meg_dir, subject)


###############################################################################

# Read raw files from MEG room

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
    #  plot maxfiltered data
    raw_sss.plot(n_channels=50, butterfly=True, group_by='position')
    
# Read files (events) after 03-extract_events.py
    
    for run in runs:
        raw_fname_in = op.join(meg_subject_dir,
                               config.base_fname.format(**locals()))
        eve_fname = op.splitext(raw_fname_in)[0] + '-int123-eve.fif'
        events = mne.read_events(eve_fname)
        
        figure = mne.viz.plot_events(events)
        figure = mne.viz.plot_events(events, sfreq=raw.info['sfreq'],
                                         first_samp=raw.first_samp)
        figure.show()
        
# Read files after 04-make_epochs.py
        
    for run in runs:
        extension = '-int123-epo'
        epochs_fname = op.join(meg_subject_dir,
                           config.base_fname.format(**locals()))
        
        
        
        
        
    
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:10:56 2019

@author: Dragana
"""

import os.path as op

import mne
import numpy as np
import itertools  

import config

subject = 'hm070076'
runs = ['Run01']
#runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
meg_subject_dir = op.join(config.meg_dir, subject)


###############################################################################
"""
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
    raw = mne.io.read_raw_fif(raw_sss, allow_maxshield=True)
    #  plot maxfiltered data
    raw.plot(n_channels=50, butterfly=True, group_by='position')
    
"""
    
# Read files (events) after 03-extract_events.py
for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
    events = mne.read_events(eve_fname)
        
    # Move the escaped triggers
    numrows = len(events)
    i=0
    for nrows in range(numrows):
        if events[nrows][2]>2048:
            events[nrows][2] = events[nrows][2] - 2048
            i=i+1
    #
        
    # Calculate the interval lengths
    int_dur = []
    i=0
#    events_ints = np.array(np.zeros((90,3)), np.int64)
    events_int1 = []
    events_int2 = []
    events_int3 = []
    int_start=0
    int_end=0
    numrows = len(events)
    for nrows in range(numrows-2):
        # For int 1.45
        if (events[nrows][2]==15 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            events_int1.append([events[nrows+1][0], events[nrows+1][1], 1])
            events_int1.append([events[nrows+2][0], events[nrows+2][1], 2])
        # For int 2.9
        elif (events[nrows][2]==35 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            events_int2.append([events[nrows+1][0], events[nrows+1][1], 3])
            events_int2.append([events[nrows+2][0], events[nrows+2][1], 4])
        # For int 5.8
        elif (events[nrows][2]==55 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            events_int3.append([events[nrows+1][0], events[nrows+1][1], 5])
            events_int3.append([events[nrows+2][0], events[nrows+2][1], 6])
            
    # Count the number of a given interval production
#    int1 = 0
#    int2 = 0
#    int3 = 0
#    for i in range(len(events_ints)):
#        if events_ints[i][2]==1:
#            int1 += 1
#        elif events_ints[i][2]==3:
#            int2 += 1
#        elif events_ints[i][2]==5:
#            int3 += 1
    
    # int_dur is a list containing the interval lengths
    int1_dur = []
    int2_dur = []
    int3_dur = []
    int_dur = [int1_dur, int2_dur, int3_dur]
    all_events = [events_int1, events_int2, events_int3]
    for (x, y) in zip(all_events, int_dur):
        numrows = len(x)
        for nrows in range(0, numrows-1, 2):
            int_start = x[nrows][0]
            int_end = x[nrows+1][0]
            y.append((int_end - int_start)*(1/500))
    
    
    # Calculate the standard deviations of the productions within a block
    int1_st = np.std(int1_dur)
    int1_st = np.std(int1_dur)
    int1_st = np.std(int1_dur)
    
    figure = mne.viz.plot_events(events_ints)
    figure.show()

"""
# Read files after 04-make_epochs.py
#        
#    for run in runs:
#        extension = '-int123-epo'
#        epochs_fname = op.join(meg_subject_dir,
#                           config.base_fname.format(**locals()))
"""
        
        
        
        
    
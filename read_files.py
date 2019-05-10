# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:10:56 2019

@author: Dragana
"""

import os.path as op

import mne
import numpy as np
from itertools import *
import itertools

import config

subject = 'fr190151'
#runs = ['Run01']
runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
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
events_int1 = []
events_int2 = []
events_int3 = []

for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
    events = mne.read_events(eve_fname)
        
    # Change the escaped triggers
    numrows = len(events)
    i=0
    for nrows in range(numrows):
        if events[nrows][2]>2048:
            events[nrows][2] = events[nrows][2] - 2048
            i=i+1


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
    
# Calculate the standard deviations of the productions of a pax
int1_sd = np.std(int1_dur)
int2_sd = np.std(int2_dur)
int3_sd = np.std(int3_dur)

# Calculate the means of the productions of a pax
int1_mean = np.mean(int1_dur)
int2_mean = np.mean(int2_dur)
int3_mean = np.mean(int3_dur)

# Finds the positions of the outliers
int1_outliers = []
for i in range(len(int1_dur)):
    if (int1_dur[i] < (int1_mean-(3*int1_sd))) or (int1_dur[i] > (int1_mean+(3*int1_sd))):
        int1_outliers.append(i)
int2_outliers = []
for j in range(len(int2_dur)):
    if (int2_dur[j] < (int2_mean-(3*int2_sd))) or (int2_dur[j] > (int2_mean+(3*int2_sd))):
        int2_outliers.append(j)
int3_outliers = []
for k in range(len(int3_dur)):
    if (int3_dur[k] < (int3_mean-(3*int3_sd))) or (int3_dur[k] > (int3_mean+(3*int3_sd))):
        int3_outliers.append(k)
        
        
# Create a different list with the outliers.
        # Their values correspond to the values in events_intx which need to be removed
int1_outliers_events = []
for x in range(len(int1_outliers)):
    int1_outliers_events.append(int1_outliers[x]*2 - 1)
    int1_outliers_events.append(int1_outliers[x]*2)
int2_outliers_events = []
for x in range(len(int2_outliers)):
    int2_outliers_events.append(int2_outliers[x]*2 - 1)
    int2_outliers_events.append(int2_outliers[x]*2)
int3_outliers_events = []
for x in range(len(int3_outliers)):
    int3_outliers_events.append(int3_outliers[x]*2 - 1)
    int3_outliers_events.append(int3_outliers[x]*2)

# Remove the outliers
int1_outliers_events.sort(reverse=True)        
for i in range(len(int1_outliers_events)):
    del events_int1[int1_outliers_events[i]]

int2_outliers_events.sort(reverse=True)  
for i in range(len(int2_outliers_events)):
    del events_int2[int2_outliers_events[i]]
      
int3_outliers_events.sort(reverse=True)
for i in range(len(int3_outliers_events)):
    del events_int3[int3_outliers_events[i]]

events_int1 = np.array(events_int1)
events_int2 = np.array(events_int2)
events_int3 = np.array(events_int3)
events_ints= np.concatenate((events_int1, events_int2, events_int3))
    
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
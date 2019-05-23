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

subject = 'at140305'
#runs = ['Run01']
runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05']
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
    raw.plot_psd(area_mode='range', tmin=10.0, tmax=100.0,ih190084
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
    

    
# Read files (events) after 03-extract_events.py
for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
    events = mne.read_events(eve_fname)

figure = mne.viz.plot_events(events)
figure.show()
"""

## Read the events files, change the events values, calculate the durations, 
    ## exclude the outliers, divide the events in short, correct and long.
    ## All is done for each of the 3 different intervals. 
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

    print(run)
    int_start=0
    int_end=0
    numrows = len(events)
    for nrows in range(numrows-2):
        # For int 1.45
        if (events[nrows][2]==15 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            # First button press to start the interval
            events_int1.append([events[nrows+1][0], events[nrows+1][1], 1, int(run[-1:])])
            # Second button press to end the interval
            events_int1.append([events[nrows+2][0], events[nrows+2][1], 2, int(run[-1:])])
        # For int 2.9
        elif (events[nrows][2]==35 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            events_int2.append([events[nrows+1][0], events[nrows+1][1], 3, int(run[-1:])])
            events_int2.append([events[nrows+2][0], events[nrows+2][1], 4, int(run[-1:])])
        # For int 5.8
        elif (events[nrows][2]==55 and events[nrows+1][2]==2048 and events[nrows+2][2]==2048):
            events_int3.append([events[nrows+1][0], events[nrows+1][1], 5, int(run[-1:])])
            events_int3.append([events[nrows+2][0], events[nrows+2][1], 6, int(run[-1:])])
  
# int_dur is a list containing the interval lengths
int1_dur = []
int2_dur = []
int3_dur = []
int_dur = []
all_events = []
int_dur = [int1_dur, int2_dur, int3_dur]
all_events = [events_int1, events_int2, events_int3]
for (x, y) in zip(all_events, int_dur):
    numrows = len(x)
    for nrows in range(0, numrows-1, 2):
        int_start = x[nrows][0]
        int_end = x[nrows+1][0]
        y.append([(int_end - int_start)*(1/500), nrows])
      
# Sort the durations from smallest to biggest
int1_dur.sort(key=lambda int1_dur: int1_dur[0])
int2_dur.sort(key=lambda int2_dur: int2_dur[0])
int3_dur.sort(key=lambda int3_dur: int3_dur[0])
    
# Calculate the standard deviations of the productions of a pax
int1_sd = np.std([column[0] for column in int1_dur])
int2_sd = np.std([column[0] for column in int2_dur])
int3_sd = np.std([column[0] for column in int3_dur])

# Calculate the means of the productions of a pax
int1_mean = np.mean([column[0] for column in int1_dur])
int2_mean = np.mean([column[0] for column in int2_dur])
int3_mean = np.mean([column[0] for column in int3_dur])

# Finds the positions of the outliers
int1_outliers = []
for i in range(len(int1_dur)):
    if (int1_dur[i][0] < (int1_mean-(3*int1_sd))) or (int1_dur[i][0] > (int1_mean+(3*int1_sd))):
        int1_outliers.append(i)
int2_outliers = []
for j in range(len(int2_dur)):
    if (int2_dur[j][0] < (int2_mean-(3*int2_sd))) or (int2_dur[j][0] > (int2_mean+(3*int2_sd))):
        int2_outliers.append(j)
int3_outliers = []
for k in range(len(int3_dur)):
    if (int3_dur[k][0] < (int3_mean-(3*int3_sd))) or (int3_dur[k][0] > (int3_mean+(3*int3_sd))):
        int3_outliers.append(k)
        
        
# Create a different list with the outliers.
        # Their values correspond to the values in events_intx which need to be removed
int1_outliers_events = []
for x in range(len(int1_outliers)):
    int1_outliers_events.append(int1_outliers[x]*2)
    int1_outliers_events.append(int1_outliers[x]*2+1)
int2_outliers_events = []
for x in range(len(int2_outliers)):
    int2_outliers_events.append(int2_outliers[x]*2)
    int2_outliers_events.append(int2_outliers[x]*2+1)
int3_outliers_events = []
for x in range(len(int3_outliers)):
    int3_outliers_events.append(int3_outliers[x]*2)
    int3_outliers_events.append(int3_outliers[x]*2+1)

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

# Create arrays from the lists
events_int1 = np.asarray(events_int1, dtype=np.float32)
events_int2 = np.asarray(events_int2, dtype=np.float32)
events_int3 = np.asarray(events_int3, dtype=np.float32)
events_ints= np.concatenate((events_int1, events_int2, events_int3))

# int_dur is a list containing the interval lengths but without the outliers
int1_dur_no = []
int2_dur_no = []
int3_dur_no = []
int_dur_no = []
all_events = []
all_events = [events_int1, events_int2, events_int3]
int_dur_no = [int1_dur_no, int2_dur_no, int3_dur_no]
for (x, y) in zip(all_events, int_dur_no):
    numrows = len(x)
    for nrows in range(0, numrows-1, 2):
        int_start = x[nrows][0]
        int_end = x[nrows+1][0]
        y.append([(int_end - int_start)*(1/500), nrows])

# Sort the durations in events_intx from smallest to biggest
int1_dur_no.sort(key=lambda int1_dur_no: int1_dur_no[0])
int2_dur_no.sort(key=lambda int2_dur_no: int2_dur_no[0])
int3_dur_no.sort(key=lambda int3_dur_no: int3_dur_no[0])

# Divide the events to short, correct and long 
# int1
num_int1 = int(len(int1_dur_no))
dur_int1_short = int1_dur_no[0:((num_int1//3))]
dur_int1_correct = int1_dur_no[(num_int1//3):((2*(num_int1//3))+((num_int1%3)))]
dur_int1_long = int1_dur_no[((2*(num_int1//3))+((num_int1%3))):]

# int2
num_int2 = int(len(int2_dur_no))
dur_int2_short = int2_dur_no[0:((num_int2//3))]
dur_int2_correct = int2_dur_no[(num_int2//3):((2*(num_int2//3))+((num_int2%3)))]
dur_int2_long = int2_dur_no[((2*(num_int2//3))+((num_int2%3))):]

# int3
num_int3 = int(len(int3_dur_no))
dur_int3_short = int3_dur_no[0:((num_int3//3))]
dur_int3_correct = int3_dur_no[(num_int3//3):((2*(num_int3//3))+((num_int3%3)))]
dur_int3_long = int3_dur_no[((2*(num_int3//3))+((num_int3%3))):]

# Take the positions of the interval lengths from eve_intx_short, 
# and take these triggers from events_intx
# Interval 1
events_int1_short = []
for x in range(len(dur_int1_short)):
    position = dur_int1_short[x][1]
    events_int1_short.append(events_int1[position])
    events_int1_short.append(events_int1[position+1])
events_int1_correct = []
for x in range(len(dur_int1_correct)):
    position = dur_int1_correct[x][1]
    events_int1_correct.append(events_int1[position])
    events_int1_correct.append(events_int1[position+1])    
events_int1_long = []
for x in range(len(dur_int1_long)):
    position = dur_int1_long[x][1]
    events_int1_long.append(events_int1[position])
    events_int1_long.append(events_int1[position+1])  
# Interval 2   
events_int2_short = []
for x in range(len(dur_int2_short)):
    position = dur_int2_short[x][1]
    events_int2_short.append(events_int2[position])
    events_int2_short.append(events_int2[position+1])
events_int2_correct = []
for x in range(len(dur_int2_correct)):
    position = dur_int2_correct[x][1]
    events_int2_correct.append(events_int2[position])
    events_int2_correct.append(events_int2[position+1])    
events_int2_long = []
for x in range(len(dur_int2_long)):
    position = dur_int2_long[x][1]
    events_int2_long.append(events_int2[position])
    events_int2_long.append(events_int2[position+1])   
# Interval 3
    events_int3_short = []
for x in range(len(dur_int3_short)):
    position = dur_int3_short[x][1]
    events_int3_short.append(events_int3[position])
    events_int3_short.append(events_int3[position+1])
events_int3_correct = []
for x in range(len(dur_int3_correct)):
    position = dur_int3_correct[x][1]
    events_int3_correct.append(events_int3[position])
    events_int3_correct.append(events_int3[position+1])    
events_int3_long = []
for x in range(len(dur_int3_long)):
    position = dur_int3_long[x][1]
    events_int3_long.append(events_int3[position])
    events_int3_long.append(events_int3[position+1])  

# Change the type of the events to array
# Interval 1
events_int1_short = np.asarray(events_int1_short, dtype=np.float32)
events_int1_correct = np.asarray(events_int1_correct, dtype=np.float32)
events_int1_long = np.asarray(events_int1_long, dtype=np.float32)
# Interval 2
events_int2_short = np.asarray(events_int2_short, dtype=np.float32)
events_int2_correct = np.asarray(events_int2_correct, dtype=np.float32)
events_int2_long = np.asarray(events_int2_long, dtype=np.float32)
# Interval 3
events_int3_short = np.asarray(events_int3_short, dtype=np.float32)
events_int3_correct = np.asarray(events_int3_correct, dtype=np.float32)
events_int3_long = np.asarray(events_int3_long, dtype=np.float32)
#############################################
# Change the trigger values for the events 
# int 1 - 11 & 12
# int 1 - short - 13 & 14
# int 1 - correct - 15 & 16 
# int 1 - long - 17 & 18
#
# int 2 - 21 & 22
# int 2 - short - 23 & 24
# int 2 - correct - 25 & 26 
# int 2 - long - 27 & 28
#
# int 3 - 31 & 32
# int 3 - short - 33 & 34
# int 3 - correct - 35 & 36 
# int 3 - long - 37 & 38
#
# Interval 1
for i in range(len(events_int1_short)):
    if events_int1_short[i,2] == 1:
        events_int1_short[i,2] = 13
    elif events_int1_short[i,2] == 2:
        events_int1_short[i,2] = 14
for i in range(len(events_int1_correct)):
    if events_int1_correct[i,2] == 1:
        events_int1_correct[i,2] = 15
    if events_int1_correct[i,2] == 2:
        events_int1_correct[i,2] = 16
for i in range(len(events_int1_long)):
    if events_int1_long[i,2] == 1:
        events_int1_long[i,2] = 17
    if events_int1_long[i,2] == 2:
        events_int1_long[i,2] = 18
# Interval 2
for i in range(len(events_int2_short)):
    if events_int2_short[i,2] == 1:
        events_int2_short[i,2] = 23
    if events_int2_short[i,2] == 2:
        events_int2_short[i,2] = 24
for i in range(len(events_int2_correct)):
    if events_int2_correct[i,2] == 1:
        events_int2_correct[i,2] = 25
    if events_int2_correct[i,2] == 2:
        events_int2_correct[i,2] = 26
for i in range(len(events_int2_long)):
    if events_int2_long[i,2] == 1:
        events_int2_long[i,2] = 27
    if events_int2_long[i,2] == 2:
        events_int2_long[i,2] = 28
# Interval 3
for i in range(len(events_int3_short)):
    if events_int3_short[i,2] == 1:
        events_int3_short[i,2] = 33
    if events_int3_short[i,2] == 2:
        events_int3_short[i,2] = 34
for i in range(len(events_int3_correct)):
    if events_int3_correct[i,2] == 1:
        events_int3_correct[i,2] = 35
    if events_int3_correct[i,2] == 2:
        events_int3_correct[i,2] = 36
for i in range(len(events_int3_long)):
    if events_int3_long[i,2] == 1:
        events_int3_long[i,2] = 37
    if events_int3_long[i,2] == 2:
        events_int3_long[i,2] = 38


# Save the short, correct and long events in the separate Run0x files
#short_events_int1_run01 = np.array(np.zeros((45,3)), np.int64)
for k in runs:
    for j in [events_int1_short, events_int1_correct, events_int1_long]:
#        count = 0
#        for i in range(len(j)):
#            if events_int1_short[i,3] == k:
#                count += 1
#            events = np.array(np.zeros((count,3)), np.int64)
        events = []
        for i in range(len(j)):
            if events_int1_short[i,3] == k:
                events.append([events_int1_short[i,0],events_int1_short[i,1],events_int1_short[i,2]])
        
        
#eve_int1_short = np.array(eve_int1_short)
#eve_int2_short = np.array(eve_int2_short)
#eve_int3_short = np.array(eve_int3_short)
#events_ints_short= np.concatenate((eve_int1_short, eve_int2_short, eve_int3_short))
        
"""
To be done:
    - Turn the list of lists or whatever into arrays at the end.
    - Take the number of rows and columns of the lists
    and create np.arrays with these dimensions.
    - Iterate throug the list of lists or whatever and add the proper values
    to the np.arrays. 
    - Save the np.arrays as separate event files in the case of short, correct
    and long produced intervals. 
"""

# Plot the events
figure = mne.viz.plot_events(events_ints_short)
figure.show()

"""
# Read files after 04-make_epochs.py
#        
#    for run in runs:
#        extension = '-int123-epo'
#        epochs_fname = op.join(meg_subject_dir,
#                           config.base_fname.format(**locals()))
""" 




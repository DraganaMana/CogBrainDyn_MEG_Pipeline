#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:24:26 2019

@author: dm258725
"""
import os.path as op

import mne
import numpy as np
from warnings import warn

import config

# Relevant triggers for Replay, 19, 39, 59 


#subject = 'hm070076' #'at140305','hm070076', 'fr190151'
#runs = ['Run01']
#runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
#subjects=['hm070076']


## Read the events files, change the events values, calculate the durations, 
    ## exclude the outliers, divide the events in short, correct and long.
    ## All is done for each of the 3 different intervals. 
for subject in config.subjects_list:
#for subject in subjects:
    
    meg_subject_dir = op.join(config.meg_dir, subject)
    
    events_int1 = []
    events_int2 = []
    events_int3 = []
    
    # int_dur is a list containing the interval lengths
    int1_dur = []
    int2_dur = []
    int3_dur = []
        
    # Counters for the nrows of the intervals
    n1=0
    n2=0
    n3=0
    
    for run in config.runs:
        extension = run + '_sss_raw'
        raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
        # This is the file of the original events file, 
        # in other words, this code doesn't find the events,
        # but only reads the events file and alters it. 
        eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
        print("Processing eve file: %s" % eve_fname)
    #    raw = mne.io.read_raw_fif(raw_fname_in)
    
        if not op.exists(eve_fname):
            warn('Run %s not found for subject %s ' %
                 (eve_fname, subject))
            continue
        
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
        for nrows in range(numrows-3):
            # For int 1.45 
            if events[nrows][2]==19 and events[nrows+1][2]==20 and events[nrows+2][2]==2048 and events[nrows+3][2]==21:
                events_int1.append([events[nrows+2][0], events[nrows+2][1], 1, int(run[-1:])])
                #
                int_start = events[nrows][0]
                int_end = events[nrows+3][0]
                #
                int1_dur.append([(int_end - int_start)*(1/500), n1])
                #
                n1 = n1 + 1
            # For int 2.9
            if events[nrows][2]==39 and events[nrows+1][2]==40 and events[nrows+2][2]==2048 and events[nrows+3][2]==41:
                events_int2.append([events[nrows+2][0], events[nrows+2][1], 3, int(run[-1:])])
                #
                int_start = events[nrows][0]
                int_end = events[nrows+3][0]
                #
                int2_dur.append([(int_end - int_start)*(1/500), n2])
                #
                n2 = n2 + 1
            # For int 5.8
            if events[nrows][2]==59 and events[nrows+1][2]==60 and events[nrows+2][2]==2048 and events[nrows+3][2]==61:
                events_int3.append([events[nrows+2][0], events[nrows+2][1], 5, int(run[-1:])])
                #
                int_start = events[nrows][0]
                int_end = events[nrows+3][0]
                #
                int3_dur.append([(int_end - int_start)*(1/500), n3])
                #
                n3 = n3 + 1
      

    int_dur = [int1_dur, int2_dur, int3_dur]
    all_events = [events_int1, events_int2, events_int3]

#    import operator
    # Sort the durations from smallest to biggest
    int1_dur = sorted(int1_dur, key=lambda int1_dur: int1_dur[0])
#    int1_dur.sort(key = operator.itemgetter(0))
#    int1_dur.sort(key=lambda int1_dur: int1_dur[0])
    int2_dur = sorted(int2_dur, key=lambda int2_dur: int2_dur[0])
    int3_dur = sorted(int3_dur, key=lambda int3_dur: int3_dur[0])
        
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
            
    # Remove the outliers from the events_intx lists  <---- I shouldn't do this
    int1_outliers.sort(reverse=True)        
    for i in range(len(int1_outliers)):
        del int1_dur[int1_outliers[i]] # delete the outlier from the list
    int2_outliers.sort(reverse=True)  
    for i in range(len(int2_outliers)):
        del int2_dur[int2_outliers[i]]
    int3_outliers.sort(reverse=True)
    for i in range(len(int3_outliers)):
        del int3_dur[int3_outliers[i]]
    
    # Create arrays from the lists
    events_int1 = np.asarray(events_int1, dtype=np.float32)
    events_int2 = np.asarray(events_int2, dtype=np.float32)
    events_int3 = np.asarray(events_int3, dtype=np.float32)
    events_ints= np.concatenate((events_int1, events_int2, events_int3))
    
    # int_dur is a list containing the interval lengths but without the outliers
    int1_dur_no = int1_dur
    int2_dur_no = int2_dur
    int3_dur_no = int3_dur
    int_dur_no = []
    all_events = []
    all_events = [events_int1, events_int2, events_int3]
    int_dur_no = [int1_dur_no, int2_dur_no, int3_dur_no]
    
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
    events_int1_correct = []
    for x in range(len(dur_int1_correct)):
        position = dur_int1_correct[x][1]
        events_int1_correct.append(events_int1[position])
    events_int1_long = []
    for x in range(len(dur_int1_long)):
        position = dur_int1_long[x][1]
        events_int1_long.append(events_int1[position])
    # Interval 2   
    events_int2_short = []
    for x in range(len(dur_int2_short)):
        position = dur_int2_short[x][1]
        events_int2_short.append(events_int2[position])
    events_int2_correct = []
    for x in range(len(dur_int2_correct)):
        position = dur_int2_correct[x][1]
        events_int2_correct.append(events_int2[position])
    events_int2_long = []
    for x in range(len(dur_int2_long)):
        position = dur_int2_long[x][1]
        events_int2_long.append(events_int2[position])
    # Interval 3
        events_int3_short = []
    for x in range(len(dur_int3_short)):
        position = dur_int3_short[x][1]
        events_int3_short.append(events_int3[position])
    events_int3_correct = []
    for x in range(len(dur_int3_correct)):
        position = dur_int3_correct[x][1]
        events_int3_correct.append(events_int3[position])
    events_int3_long = []
    for x in range(len(dur_int3_long)):
        position = dur_int3_long[x][1]
        events_int3_long.append(events_int3[position])
    
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
    
    # The first values indicate the button press which is a reaction to the cross.
    # The second values aren't the second button press but the pressStart2
    
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
            events_int1_short[i,2] = 113
    for i in range(len(events_int1_correct)):
        if events_int1_correct[i,2] == 1:
            events_int1_correct[i,2] = 115
    for i in range(len(events_int1_long)):
        if events_int1_long[i,2] == 1:
            events_int1_long[i,2] = 117

    # Interval 2
    for i in range(len(events_int2_short)):
        if events_int2_short[i,2] == 3:
            events_int2_short[i,2] = 223
    for i in range(len(events_int2_correct)):
        if events_int2_correct[i,2] == 3:
            events_int2_correct[i,2] = 225
    for i in range(len(events_int2_long)):
        if events_int2_long[i,2] == 3:
            events_int2_long[i,2] = 227

    # Interval 3
    for i in range(len(events_int3_short)):
        if events_int3_short[i,2] == 5:
            events_int3_short[i,2] = 333
    for i in range(len(events_int3_correct)):
        if events_int3_correct[i,2] == 5:
            events_int3_correct[i,2] = 335
    for i in range(len(events_int3_long)):
        if events_int3_long[i,2] == 5:
            events_int3_long[i,2] = 337

    
    
    # Save the short, correct and long events in the separate Run0x files
    diff_eve = [events_int1_short, events_int1_correct, events_int1_long, 
                events_int2_short, events_int2_correct, events_int2_long,
                events_int3_short, events_int3_correct, events_int3_long]
    diff_eve_str = ['events_int1_short', 'events_int1_correct', 'events_int1_long',
                    'events_int2_short', 'events_int2_correct', 'events_int2_long',
                    'events_int3_short', 'events_int3_correct', 'events_int3_long']
    
    name_ext = 'R-int123-scl'
    
    for k, run in enumerate(config.runs):
        events = []
        for (eve,eve_name) in zip(diff_eve, diff_eve_str):
            for i in range(len(eve)):
                if eve[i,3] == (k+1):
                    events.append([eve[i,0], eve[i,1], eve[i,2]])
        if events: # checks if the events is not an empty array
            # Turn events from list of lists in an array
            events = np.asarray(events, dtype=np.int)
            # Set directory where events are saved
#            eve_dir = op.join(config.meg_dir, subject)
            # Set filename for the events
        #   eve_fname_out = op.splitext(raw_fname_in)[0] + '_' + eve_name + '-eve.fif'
            eve_fname_out = meg_subject_dir + '/' + subject + '_' + 'ScaledTime' + '_' + run + '_sss_raw_' + name_ext + '-eve.fif'
            # Save the events in a file
            print("%s, writing events: %s" % (run, eve_fname_out))
            mne.write_events(eve_fname_out, events)
            # Plot the events
            if config.plot:
                figure = mne.viz.plot_events(events)
                figure.show()
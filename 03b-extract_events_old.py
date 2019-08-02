# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:48:20 2019

@author: Dragana
"""

"""
============================================
03. Extract events from the stimulus channel
============================================

Here, all events present in the stimulus channel indicated in
config.stim_channel are extracted.
The events are saved to the subject's MEG directory.
This is done early in the pipeline to avoid distorting event-time,
for instance by resampling.
"""

import os.path as op

import mne
import numpy as np
from mne.parallel import parallel_func
#from mne.event import define_target_events

import numpy as np
from warnings import warn

import config


def run_events(subject):
    print("Processing subject: %s" % subject)
    MFmeg_subject_dir = op.join(config.MFmeg_dir, subject)

    for run in config.runs:
        extension = run + '_' + config.name_ext + '_sss_raw'
        raw_fname_in = op.join(MFmeg_subject_dir,
                               config.base_fname.format(**locals()))
        eve_fname_out = op.splitext(raw_fname_in)[0] + '_' + config.name_ext +'-eve.fif'
        
        if not op.exists(raw_fname_in):
            warn('Run %s not found for subject %s ' %
                 (raw_fname_in, subject))
            continue

        raw = mne.io.read_raw_fif(raw_fname_in)
        
        events = mne.find_events(raw, stim_channel=config.stim_channel,
                                 consecutive=True,
                                 min_duration=config.min_event_duration,
                                 shortest_event=config.shortest_event)
        if config.trigger_time_shift:
            events = mne.event.shift_time_events(events,
                                                 np.unique(events[:, 2]),
                                                 config.trigger_time_shift,
                                                 raw.info['sfreq'])
        
        # XXX shift events by trigger
#        if config.trigger_offset:
#            events = mne.event.shift_time_events(
#                    events,
#                    np.unique(events[:,2]),
#                    config.trigger_offset,
#                    raw.info['sfreq'],
#                    )
#-----------------------------------
        # Epochs by sub-blocks of intervals
        events_ints = np.array(np.zeros((45,3)), np.int64)
        numrows = len(events)
        i=0
        for nrows in range(numrows):
            if (events[nrows][2]==1 and events[nrows+1][2]==13):
                events_ints[i][0]=events[nrows][0]
                events_ints[i][1]=events[nrows][1]
                events_ints[i][2]=1
                i=i+1
            elif (events[nrows][2]==3 and events[nrows+1][2]==33):
                events_ints[i][0]=events[nrows][0]
                events_ints[i][1]=events[nrows][1]
                events_ints[i][2]=2
                i=i+1
            elif (events[nrows][2]==5 and events[nrows+1][2]==53):
                events_ints[i][0]=events[nrows][0]
                events_ints[i][1]=events[nrows][1]
                events_ints[i][2]=3
                i=i+1
        events_ints 
#        
#-----------------------------------
#        # First button press
#        events_ints = np.array(np.zeros((45,3)), np.int64)
#        numrows = len(events)
#        i=0
#        for nrows in range(numrows):
#            if (events[nrows][2]==15 and events[nrows+1][2]==2048) or (events[nrows][2]==35 and events[nrows+1][2]==2048) or (events[nrows][2]==55 and events[nrows+1][2]==2048):
#                events_ints[i][0]=events[nrows+1][0]
#                events_ints[i][1]=events[nrows+1][1]
#                events_ints[i][2]=5
#                i=i+1
#        events_ints 
#-----------------------------------
        # Seconds button press
#        events_ints = np.array(np.zeros((45,3)), np.int64)
#        numrows = len(events)
#        i=0
#        for nrows in range(numrows-2):
#            if (events[nrows][2]==15 and events[nrows+2][2]==2048) or (events[nrows][2]==35 and events[nrows+2][2]==2048) or (events[nrows][2]==55 and events[nrows+2][2]==2048):
#                events_ints[i][0]=events[nrows+2][0]
#                events_ints[i][1]=events[nrows+2][1]
#                events_ints[i][2]=5
#                i=i+1
#        events_ints 
#        print(events_ints)
#
#        
#-----------------------------------
        """
        events_ints = np.array(np.ones((45,3)), np.int64)
        numrows = len(events)
        i=0
        for nrows in range(numrows):
            if events[nrows][2]==2 and (events[nrows+1][2]==2052 or events[nrows+1][2]==2084):
                events[nrows+1][2]=5  
                events_ints[i][0]=events[nrows+1][0]
                events_ints[i][1]=events[nrows+1][1]
                events_ints[i][2]=events[nrows+1][2]
                i=i+1
        events_ints 
"""
#-----------------------------------
## [Play] Different events for the 3 different intervals
#        events_ints = np.array(np.zeros((45,3)), np.int64)
#        numrows = len(events)
#        i=0
#        for nrows in range(numrows):
#            if (events[nrows][2]==15 and events[nrows+1][2]==2048): 
#                events_ints[i][0]=events[nrows+1][0]
#                events_ints[i][1]=events[nrows+1][1]
#                events_ints[i][2]=1
#                i=i+1
#            elif (events[nrows][2]==35 and events[nrows+1][2]==2048):
#                events_ints[i][0]=events[nrows+1][0]
#                events_ints[i][1]=events[nrows+1][1]
#                events_ints[i][2]=2  
#                i=i+1
#            elif (events[nrows][2]==55 and events[nrows+1][2]==2048):
#                events_ints[i][0]=events[nrows+1][0]
#                events_ints[i][1]=events[nrows+1][1]
#                events_ints[i][2]=3    
#                i=i+1
#        events_ints 
        
## [Replay] Different events for the 3 different intervals
#        events_Rints = np.array(np.zeros((45,3)), np.int64)
#        numrows = len(events)
#        i=0
#        for nrows in range(numrows):
#            if ((events[nrows][2]==19 or events[nrows][2]==20) and events[nrows+1][2]==2048): 
#                events_Rints[i][0]=events[nrows+1][0]
#                events_Rints[i][1]=events[nrows+1][1]
#                events_Rints[i][2]=4
#                i=i+1
#            elif ((events[nrows][2]==39 or events[nrows][2]==40) and events[nrows+1][2]==2048):
#                events_Rints[i][0]=events[nrows+1][0]
#                events_Rints[i][1]=events[nrows+1][1]
#                events_Rints[i][2]=5  
#                i=i+1
#            elif ((events[nrows][2]==59 or events[nrows][2]==60) and events[nrows+1][2]==2048):
#                events_Rints[i][0]=events[nrows+1][0]
#                events_Rints[i][1]=events[nrows+1][1]
#                events_Rints[i][2]=6    
#                i=i+1
#        events_Rints 

#        int01=1.45
#        int02=2.9
#        int03=5.8
#        int_matrix = [[int01, int02, int03],
#                      [int01, int03, int02],
#                      [int02, int03, int01],
#                      [int02, int01, int03],
#                      [int03, int01, int02],
#                      [int03, int02, int01]]
##        if run == 'Run01':
#            
#        eve_int02 = events_ints[0:15]
#        eve_int01 = events_ints[15:30]
#        eve_int03 = events_ints[30:45]
#        
#----------------------------------------------------------
#        # append and sort  
##        events_2 = events + events_1
#        events_2 = np.vstack((events, events_1))
#        events_2=events_2[np.argsort(events_2[:,0])]
##        np.sort(events_2, axis=0)
##        #### Taking the 2.9 durations
#        reference_id = 5  # button press 
#        target_id = 10  # start of int 2
#        sfreq = raw.info['sfreq']  # sampling rate
#        tmin = 0.001  # trials leading to very early responses will be rejected
#        tmax = 73  # ignore face stimuli followed by button press later than 590 ms
#        new_id = 14  # the new event id for a hit. If None, reference_id is used.
#        events_1, lag = define_target_events(events, reference_id, target_id,
#                                    sfreq, tmin, tmax, new_id)
#-----------------------------------------------------------



        print("Input: ", raw_fname_in)
        print("Output: ", eve_fname_out)

        mne.write_events(eve_fname_out, events_ints)
#        mne.write_events(eve_fname_out, events)

        if config.plot:
            # plot events
            # It would be good to have names on the figures, from which Run are
            # the events plotted
            figure = mne.viz.plot_events(events_ints, sfreq=raw.info['sfreq'],
                                         first_samp=raw.first_samp)
#            figure = mne.viz.plot_events(events, sfreq=raw.info['sfreq'],
#                                         first_samp=raw.first_samp)
            figure.show()
#--------------------------------------


parallel, run_func, _ = parallel_func(run_events, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)
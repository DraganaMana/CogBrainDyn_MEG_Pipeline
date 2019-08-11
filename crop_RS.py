# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:32:29 2019

@author: Dragana
"""

import os.path as op

import mne
import numpy as np

#import config

subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 
                 'ch180036', 'ms180425', 'cg190026', 'ih190084', 'cr170417', 'll180197', 
                 'tr180110', 'ep190335', 'gl180335', 'lr190095', 'ad190325', 'ag170045', 
                 'pl170230', 'ma190185'] 

#subjects_list = ['hm070076']

RSs = ['RS01', 'RS02']

study_name = 'ScaledTime'

# Directory where the .fif files are
meg_dir = 'D:/ScaledTime/MEGdata/MEG/'

stim_channel = 'STI101' 
min_event_duration = 0.0001
shortest_event = 0
freq = 2000

for subject in subjects_list:
    print("Subject: ", subject)
    for RS in RSs:
        print("Run:", RS)
        # read events
        meg_subject_dir = op.join(meg_dir, subject)
        
        # Read the raw file
        raw_fname_in = op.join(meg_subject_dir, RS + '.fif')
        print(raw_fname_in)
        raw = mne.io.read_raw_fif(raw_fname_in,
                                  allow_maxshield=True,
                                  preload=True, verbose='error')
#        raw.plot(n_channels=50, butterfly=False, group_by='original')

        
        # Find the events
        events = mne.find_events(raw, stim_channel=stim_channel,
                                 consecutive=True,
                                 min_duration=min_event_duration,
                                 shortest_event=shortest_event)
        
#        figure = mne.viz.plot_events(events, sfreq=raw.info['sfreq'],
#                                         first_samp=raw.first_samp)
#        figure.show()
        
        # I tried the code w/downsampled data so the events were with a slighly different length.
        # But this should be fine with the Multifracs data which is not resampled. 
        
        # Keep only the triggers with value 1.        
        events = events[events[:, 2] == 1]

        
        # Crop the data between the two triggers - at the beginning of the 5min interval, 
        # and at the end.
        row, col = events.shape
        
        # EXCEPTION for subject 'at140305' and similar cases
        event_time = events[0][0]/freq
        raw_length = raw.n_times/freq
        if raw_length < event_time:
            print("WARNING: The length of the raw is shorter than the event timestamp.")
            tmax = raw_length - 1 # minus 1 sec to compensate for rounding up
            tmin = raw_length - 301
            RS_crop = mne.io.Raw.crop(mne.io.Raw.copy(raw), 
                                      tmin=tmin, 
                                      tmax=tmax)
        # For all other subjects
        elif raw_length > event_time:
            if row == 1: # If only one event is found, set the crop values +/- 300sec 
                         # from that trigger. 
                print("WARNING: Only one trigger is found.")
                event_time = events[0][0]/freq
                if event_time >= 300:
                    tmin = event_time - 300
                    tmax = event_time
                elif event_time < 300:
                    tmin = event_time
                    tmax = event_time + 300
                RS_crop = mne.io.Raw.crop(mne.io.Raw.copy(raw), 
                                          tmin=tmin, 
                                          tmax=tmax)
            elif row == 2:
                RS_crop = mne.io.Raw.crop(mne.io.Raw.copy(raw), 
                                          tmin=events[0][0]/freq, 
                                          tmax=(events[1][0]/freq))
            
        RS_fname_out = op.join(meg_subject_dir, RS + '_cropped.fif')
        RS_crop.save(RS_fname_out, overwrite=True)

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:32:29 2019

@author: Dragana
"""

import os.path as op

import mne

#import config

subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 
                 'ch180036', 'ms180425', 'cg190026', 'ih190084', 'cr170417', 'll180197', 
                 'tr180110', 'ep190335', 'gl180335', 'lr190095', 'ad190325', 'ag170045', 
                 'pl170230', 'ma190185'] 

RSs = ['RS01', 'RS02']

study_name = 'ScaledTime'

# Directory where the .fif files are
meg_dir = '...'

stim_channel = 'STI101' 
min_event_duration = 0.005
shortest_event = 1
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
        
        # Crop the data between the two triggers - at the beginning of the 5min interval, 
        # and at the end.
        RS_crop = mne.io.Raw.crop(mne.io.Raw.copy(raw), 
                                  tmin=events[0][0]/freq, 
                                  tmax=(events[1][0]/freq))
        RS_fname_out = op.join(meg_subject_dir, RS + '_cropped.fif')
        RS_crop.save(RS_fname_out, overwrite=True)

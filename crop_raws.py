#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:40:38 2019

@author: dm258725
"""
import os.path as op

import mne
import numpy as np

#import config

subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 
                 'ch180036', 'ms180425', 'cg190026', 'ih190084', 'cr170417', 'll180197', 
                 'tr180110', 'ep190335', 'gl180335', 'lr190095', 'ad190325', 'ag170045', 
                 'pl170230', 'ma190185'] 

runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']


study_name = 'ScaledTime'
name_ext = 'MF-block'
base_fname = '{subject}_' + study_name + '_{extension}.fif'

# Directory where the .fif files are
meg_dir = '....'


for subject in subjects_list:
    print("Subject: ", subject)
    for run in runs:
        print("Run:", run)
        
        meg_subject_dir = op.join(meg_dir, subject)

        # Read the raw file
        extension = run + '_raw'
        raw_fname_in = op.join(meg_subject_dir, base_fname.format(**locals()))
        raw = mne.io.read_raw_fif(raw_fname_in,
                                  allow_maxshield=True,
                                  preload=True, verbose='error')
        
        eve_fname = op.join(meg_subject_dir, subject+'_ScaledTime_' + run + '_' + name_ext + '_sss_raw-eve.fif')
        events = mne.read_events(eve_fname)
        
#        freq = raw.info['sfreq'] # Acquizition frequency
        freq=2000

        
        eves = np.array(np.zeros((12,3)), np.int64)
        i = 0
        k = 0
        for nrows in range(len(events)):
            if (events[nrows][2]==1):
                eves[i][0] = events[nrows][0]
                eves[i][1] = events[nrows][1]
                eves[i][2] = events[nrows][2]
                i += 1
            if (events[nrows][2]==21):
                k += 1
                if k == 15:
                    eves[i][0] = events[nrows][0]
                    eves[i][1] = events[nrows][0]
                    eves[i][2] = 1
                    i += 1
                    k = 0
            if (events[nrows][2]==3):
                eves[i][0] = events[nrows][0]
                eves[i][1] = events[nrows][1]
                eves[i][2] = 2
                i += 1
            if (events[nrows][2]==41):
                k += 1
                if k == 15:
                    eves[i][0] = events[nrows][0]
                    eves[i][1] = events[nrows][0]
                    eves[i][2] = 2
                    i += 1
                    k=0
            if (events[nrows][2]==5):
                eves[i][0] = events[nrows][0]
                eves[i][1] = events[nrows][1]
                eves[i][2] = 3
                i += 1
            if (events[nrows][2]==61):
                k += 1
                if k == 15:
                    eves[i][0] = events[nrows][0]
                    eves[i][1] = events[nrows][0]
                    eves[i][2] = 3
                    i += 1
                    k = 0

        # Deletes the triggers for the Training start and keeps only the triggers for the Play and Replay
        eves = np.delete(eves, (8, 4, 0), axis=0) # 0, 4, 8
        
        # Crop the Plays and Replays of the 3 intervals   
        play1 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[0][0]/freq, tmax=eves[1][0]/freq)
        replay1 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[1][0]/freq, tmax=eves[2][0]/freq)
        
        play2 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[3][0]/freq, tmax=eves[4][0]/freq)
        replay2 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[4][0]/freq, tmax=eves[5][0]/freq)
        
        play3 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[6][0]/freq, tmax=eves[7][0]/freq)
        replay3 = mne.io.Raw.crop(mne.io.Raw.copy(raw), tmin=eves[7][0]/freq, tmax=eves[8][0]/freq)
#        
        # Save the Plays and Replays of the 3 intervals in .fif files
        play1_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Play_int1_raw.fif')
        play1.save(play1_fname_out)
        replay1_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Replay_int1_raw.fif')
        replay1.save(replay1_fname_out)

        play2_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Play_int2_raw.fif')
        play2.save(play2_fname_out)
        replay2_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Replay_int2_raw.fif')
        replay2.save(replay2_fname_out)
        
        play3_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Play_int3_raw.fif')
        play3.save(play3_fname_out)
        replay3_fname_out = op.join(meg_subject_dir, subject + '_ScaledTime_' + run + '_Replay_int3_raw.fif')
        replay3.save(replay3_fname_out)


"""

#interval = np.where(events.any()>0 & events.any()<=3)
#int1 = [] 
#col = interval[1]
#row = interval[0]            
#for i in range(len(col)):
#    if col[i] == 2:
#        int1.append(row[i])
#print(int1)
            
        
#        positions = np.where((events[2]==1) or (events[2]==3) or (events[2]==5))
#        events.index(1)
#        events.index(3)
#        events.index(5)


"""


        
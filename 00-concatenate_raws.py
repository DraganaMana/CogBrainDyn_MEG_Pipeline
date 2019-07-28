# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:27:30 2019

@author: Dragana
"""
import os.path as op

import mne
from mne.parallel import parallel_func
from warnings import warn

import config

subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 'ch180036', 'ms180425', 
                 'cg190026', 'ih190084', 'cr170417', 'll180197', 'tr180110', 'ep190335', 'gl180335',
                 'lr190095', 'ad190325', 'ag170045'] 
subject = subjects_list[0]
runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
r = '01'
run = runs[0]

meg_subject_dir = op.join(config.meg_dir, subject)

Run01 = subject + '_ScaledTime_' + run + '--1_raw.fif'
Run02 = subject + '_ScaledTime_' + run + '--2_raw.fif'
Run = subject + '_ScaledTime_' + run + '_raw.fif'

raw_fname_in1 = op.join(meg_subject_dir, Run01)
raw_fname_in2 = op.join(meg_subject_dir, Run02)


raw01 = mne.io.read_raw_fif(raw_fname_in1,
                                  preload=True, verbose='error', allow_maxshield=True)

raw02 = mne.io.read_raw_fif(raw_fname_in2,
                                  preload=True, verbose='error', allow_maxshield=True)

#raw_fname_out = op.join(meg_subject_dir, Run02)
extension = run + '_raw'
raw_fname_out = op.join(meg_subject_dir,
                                config.base_fname.format(**locals()))
Run_new = mne.concatenate_raws([raw01, raw02])

Run_new.save(raw_fname_out)

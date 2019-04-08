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

meg_subject_dir = op.join(config.meg_dir, config.subject_pilot)
Run02_1= 's190320_ScaledTime_Run02-1_raw.fif'
Run02_2= 's190320_ScaledTime_Run02-2_raw.fif'
Run02= 's190320_ScaledTime_Run02_raw.fif'
raw_fname_in1 = op.join(meg_subject_dir, Run02_1)
raw_fname_in2 = op.join(meg_subject_dir, Run02_2)


raw02_1 = mne.io.read_raw_fif(raw_fname_in1,
                                  preload=True, verbose='error', allow_maxshield=True)

raw02_2 = mne.io.read_raw_fif(raw_fname_in2,
                                  preload=True, verbose='error', allow_maxshield=True)

raw_fname_out = op.join(meg_subject_dir, Run02)
Run02_new = mne.concatenate_raws([raw02_1, raw02_2])

Run02_new.save(raw_fname_out)

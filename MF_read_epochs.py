# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:13:28 2019

@author: Dragana
"""

# Script to open the .fif epoch files

import os.path as op

import mne

# Study path where the .fif files are located
#study_path = 'C:/ScaledTime/MEGdata/'
study_path = '/neurospin/meg/meg_tmp/ScaledTime_Dragana_2019/Multifracs/MF_ad190325/Epochs (cleaned w ICA)/'

subjects_list = [ 'ad190325']
conditions = ['int58']

for subject in subjects_list:
    print("Processing subject: %s" %subject)
    for condition in conditions: 
        print("Processing condition: %s" %condition)
        
        # Name of the .fif file
        filename = subject + '_ScaledTime_MF-block-' + condition + '_cleaned-epo.fif'
        fif_file = op.join(study_path, filename)
        
        # Reads the .fif epochs file
        epochs = mne.read_epochs(fif_file, preload=True)
        
        # Plots the epochs 
        epochs.plot()
        epochs.plot_image(combine='gfp', group_by='type', sigma=2.,
                          cmap="YlGnBu_r")
        # Plots the PSD of the epochs 
        epochs.plot_psd(fmin=2., fmax=40.)

# To access a single epoch, write: epoch[i]. i is the number of the epoch. In the files there are
        # 5 to 6 epochs. 

import scipy.io as sio
mat_name = subject + '_ScaledTime_MF-block_' + condition + '_epoch-111' +  '_cleaned-epo.mat'
sio.savemat(mat_name, {'epoch': epochs[0][0]}, long_field_names=True)

#%%
import os.path as op

import mne
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

import config

subject = 'ag170045'
runs = ['Run05'] # 'Run06']
meg_subject_dir = op.join(config.meg_dir, subject)


for run in runs:
    extension = run + '_raw'
    raw_MEG = op.join(meg_subject_dir,
                               config.base_fname.format(**locals()))
    
    raw = mne.io.read_raw_fif(raw_MEG,
                                  allow_maxshield=config.allow_maxshield,
                                  preload=True, verbose='error')
    
    mat_name = subject + '_ScaledTime_MF-block_' + run +  '_cleaned-epo.mat'
#    ad190325_ScaledTime_MF-block_int145_cleaned-epo.mat
    data, times = raw[:]
    a = {}
    a['rawtimes']=times
    a['rawdata']=data
    sio.savemat(mat_name, a)

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:13:28 2019

@author: Dragana
"""

# Script to open the .fif epoch files

import os.path as op

import mne

# Study path where the .fif files are located
study_path = 'C:/ScaledTime/MEGdata/'

subjects_list = ['ep190335', 'ad190325']
conditions = ['int145', 'int29', 'int58']

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
        
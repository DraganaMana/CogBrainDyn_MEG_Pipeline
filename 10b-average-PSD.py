#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:08:40 2019

@author: dm258725
"""
import os.path as op

import mne
import numpy as np
import matplotlib.pyplot as plt

import config

PSD = np.zeros((len(config.subjects_list),3), dtype='object') # subjects * blocks* freq (alpha,beta)
for s,subj in enumerate(config.subjects_list): 
    meg_subject_dir = op.join(config.meg_dir, subj)
    fname_in = op.join(meg_subject_dir, subj + '_ScaledTime_-int-P-1-2-3_cleaned-epo.fif')
    epochs = mne.read_epochs(fname_in, preload=True)
    epochs.pick_types('mag')
        
    # Compute PSD
    psds, freqs = mne.time_frequency.psd_welch(epochs, fmin=3, fmax = 45, n_fft=450, n_jobs = 3) # to do colormap PSD
    
    psds = 10. * np.log10(psds)
    psds_mean = psds.mean(0).mean(0) # average over n_epochs and then over n_channels
    psds_std = psds.mean(0).std(0)  # average over n_epochs and then std over n_channels
    
    PSD[s,0] = psds_mean
    PSD[s,1] = psds_std
    PSD[s,2] = freqs


PSD_mean = PSD[:,0].mean()
PSD_std = PSD[:,1].mean()

f, ax = plt.subplots()
ax.plot(freqs, PSD_mean, color='k')
ax.fill_between(freqs, PSD_mean - PSD_std, PSD_mean + PSD_std,
                color='k', alpha=.5)
ax.set(title='Welch PSD (mag)', xlabel='Frequency',
       ylabel='Power Spectral Density (dB)')
plt.show()
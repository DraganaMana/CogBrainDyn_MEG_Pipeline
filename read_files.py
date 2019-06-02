# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 08:10:56 2019

@author: Dragana
"""

import os.path as op

import mne
import numpy as np
import matplotlib.pyplot as plt

import config

#subject = 'hm070076' #'at140305','hm070076', 'fr190151'
subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237'] 
#runs = ['Run01']
#runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06']
#meg_subject_dir = op.join(config.meg_dir, subject)

###############################################################################

# Read raw files from MEG room
""" 
for run in runs:
    extension = run + '_raw'
    raw_MEG = op.join(meg_subject_dir,
                               config.base_fname.format(**locals()))
    
    raw = mne.io.read_raw_fif(raw_MEG,
                                  allow_maxshield=config.allow_maxshield,
                                  preload=True, verbose='error')
#    raw.pick_types('grad')
    # plot raw data
    raw.plot(n_channels=50, butterfly=False, group_by='original')
    # plot power spectral densitiy
    raw.plot_psd(area_mode='range', tmin=10.0, tmax=100.0,
                         fmin=0.3, fmax=100., average=True)
    
# Read delay files
#raw_MEG = op.join('D:/ScaledTime/Delay_check/', 'ScaledTime_delayCheck_vis_pointCross2.fif')
raw_MEG = op.join('D:/ScaledTime/Delay_check/', 'ScaledTime_delayCheck_vis_pointPoint.fif')
raw = mne.io.read_raw_fif(raw_MEG, allow_maxshield=True, preload=True, verbose='error')
raw.plot(n_channels=50, butterfly=False, group_by='original')
   
# Read files after 01-import_and_filter.py - filtered files

for run in runs:
    extension = run + '_filt_raw'
    raw_filt = op.join(meg_subject_dir,
                            config.base_fname.format(**locals()))
    raw = mne.io.read_raw_fif(raw_filt, allow_maxshield=True)
    # plot raw data
    raw.plot(n_channels=50, butterfly=False, group_by='position')
    # plot power spectral densitiy
    raw.plot_psd(area_mode='range', tmin=10.0, tmax=100.0,
                 fmin=0., fmax=50., average=True)
    
# Read files after 02-apply_maxwell_filter.py

for run in runs:
    extension = run + '_sss_raw'
    raw_sss = op.join(meg_subject_dir,
                                config.base_fname.format(**locals()))
    raw = mne.io.read_raw_fif(raw_sss, allow_maxshield=True)
    #  plot maxfiltered data
    raw.plot(n_channels=50, butterfly=True, group_by='position')
    

    
# Read files (events) after 03-extract_events.py
for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '-eve.fif'
    events = mne.read_events(eve_fname)

figure = mne.viz.plot_events(events)
figure.show()
"""


## Read files after 04-make_epochs.py
#extension = '-int-P-1-2-3_cleaned-epo'
#fname_in = op.join(meg_subject_dir,
#               config.base_fname.format(**locals()))
#epochs = mne.read_epochs(fname_in, preload=True)
#epochs.plot_psd(fmin=2., fmax=40.)
#
#
## Read files from 10-TF
#for condition in config.time_frequency_conditions:
#    power_name = op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
#                    % (config.study_name, subject,
#                       condition.replace(op.sep, '')))
#    power = mne.time_frequency.read_tfrs(power_name)
#    power[0].plot_joint(baseline=(-1.5, -0.8), mode='mean', tmin=-1.5, tmax=1.25,
#                 timefreqs=[(.15, 10), (0.6, 20)])
#        

#%% Plot average PSD

PSD = np.zeros((len(config.subjects_list),3), dtype='object') # subjects * blocks* freq (alpha,beta)
for s,subj in enumerate(subjects_list): 
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


# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 21:13:19 2019

@author: Dragana
"""

import mne
import numpy as np
import matplotlib.pyplot as plt
import os.path as op
from pactools import raw_to_mask, Comodulogram

import config

#%%
#data_path = mne.datasets.sample.data_path()
#raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
#event_fname = data_path + ('/MEG/sample/sample_audvis_filt-0-40_raw-'
#                           'eve.fif')
"""
subject = 'ms180425'
study_path = 'D:/ScaledTime/MEGdata/MEG/'  #'H:/ScaledTime_Dragana_2019/'
meg_subject_dir = op.join(study_path, subject)

run = 'Run01'
extension = run + '_sss_raw'
raw_fname = op.join(meg_subject_dir, config.base_fname.format(**locals()))
raw = mne.io.read_raw_fif(raw_fname, preload=True)

extension = config.name_ext + '_cleaned-epo'
epochs_fname = op.join(meg_subject_dir, config.base_fname.format(**locals()))
epochs = mne.read_epochs(epochs_fname, preload=True)
epochs.subtract_evoked()

eve_fname = op.splitext(raw_fname)[0] + '_' + config.name_ext + '-eve.fif'
events = mne.read_events(eve_fname)


# select the time interval around the events
tmin, tmax = 0.5, 1. #-0.5, 1.25
# select the channels (phase_channel, amplitude_channel)
ixs = (1, 135) # (phase channel, amplitude channel)
#ixs = 10
low_fq_range = np.arange(3.5, 14.1, 0.2) # min 2.4cycles for the lowest freq
# staro za low_fq np.linspace(1, 10, 20)
low_fq_width = 2.0  # Hz
high_fq_range = np.arange(14, 160, 2) # array of frequency for amplitude signal
high_fq_width = 20.0  # Hz should be >= 2*driver freq


# create the input array for Comodulogram.fit
low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=tmin, tmax=tmax)

# create the instance of Comodulogram
estimator = Comodulogram(fs=500,
                         low_fq_range=low_fq_range, low_fq_width=low_fq_width,
                         high_fq_range=high_fq_range, high_fq_width=high_fq_width,
                         method='tort', progress_bar=True)
# compute the comodulogram
#estimator.fit(epochs[0])
estimator.fit(low_sig, high_sig, mask)

# plot the results
estimator.plot(tight_layout=False)
plt.show()
"""
#%% Similar code but to make it loop through subjects and channels
chan_mask = np.loadtxt('mask_significant_grads.txt', dtype=bool)
tmin, tmax = 0.5, 1. #-0.5, 1.25
comod_dir = config.meg_dir + '/Comodulograms/'

low_fq_range = np.arange(3.5, 14.1, 0.2) # min 2.4cycles for the lowest freq
# staro za low_fq np.linspace(1, 10, 20)
low_fq_width = 2.0  # Hz
high_fq_range = np.arange(14, 160, 2) # array of frequency for amplitude signal
high_fq_width = 20.0  # Hz should be >= 2*driver freq

for subject in config.subjects_list:
    print(subject)
    # Read the epochs
    meg_subject_dir = op.join(config.meg_dir, subject)
    extension = 'P-int123-scl_cleaned-epo'
    fname_in = op.join(meg_subject_dir,
                   config.base_fname.format(**locals()))
    epochs = mne.read_epochs(fname_in, preload=True)
    
    # Choose mag
    epochs.pick_types(meg = 'grad', eeg=False)
    channel_names = epochs.ch_names
    fs = epochs.info['sfreq']
    times = epochs.times
    
    sig = epochs.get_data() # gets the epoched data
    
    # temporal mask to considered only the interval of interest (applied after filtering)
    n_epochs, n_channels, n_points = sig.shape
    mask = np.zeros((n_epochs, n_points))
    mask[:,(times>tmin) & (times <tmax)] = 1
        
    for chan, signif_ch in enumerate(chan_mask):
        print(chan, signif_ch)
        if signif_ch == 1:
            
            channel_signal = sig[:, chan, :] # signal of the given channel
            
            estimator = Comodulogram(fs=500, # low_sig = channel_signal,
                     low_fq_range=low_fq_range, low_fq_width=low_fq_width,
                     high_fq_range=high_fq_range, high_fq_width=high_fq_width,
                     method='tort', progress_bar=True)
            
            estimator.fit(channel_signal, mask) # low_sig, high_sig = chan

            fig = estimator.plot(tight_layout=False)

            # save the figure
            save_name = '%s_%s_%s_%s' % (subject, config.study_name, config.name_ext, channel_names[chan])
            fig.savefig(comod_dir + save_name)
            dataname = comod_dir + save_name + '.npy'
            np.save(dataname, estimator)
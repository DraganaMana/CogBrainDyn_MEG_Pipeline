# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 17:20:05 2019

@author: DM258725
"""
import mne
import numpy as np
import matplotlib.pyplot as plt
import os.path as op
from pactools import raw_to_mask, Comodulogram

import config

#data_path = mne.datasets.sample.data_path()
#raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
#event_fname = data_path + ('/MEG/sample/sample_audvis_filt-0-40_raw-'
#                           'eve.fif')

subject = 'ms180425'
study_path = 'D:/ScaledTime/MEGdata/MEG/'  #'H:/ScaledTime_Dragana_2019/'
meg_subject_dir = op.join(study_path, subject)

run = 'Run01'
extension = run + '_sss_raw'
raw_fname = op.join(meg_subject_dir, config.base_fname.format(**locals()))
#raw = mne.io.read_raw_fif(raw_fname, preload=True)

extension = config.name_ext + '-epo'
epochs_fname = op.join(meg_subject_dir, config.base_fname.format(**locals()))
epochs = mne.read_epochs(epochs_fname, preload=True)
epochs.subtract_evoked()

eve_fname = op.splitext(raw_fname)[0] + '_' + config.name_ext + '-eve.fif'
events = mne.read_events(eve_fname)


# select the time interval around the events
tmin, tmax = -0.5, 1.25
# select the channels (phase_channel, amplitude_channel)
#ixs = (8, 10) (phase channel, amplitude channel)
ixs = (8, 10)

# create the input array for Comodulogram.fit
#low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=tmin, tmax=tmax)

# create the instance of Comodulogram
estimator = Comodulogram(fs=500,
                         low_fq_range=np.linspace(1, 10, 20), low_fq_width=2.,
                         method='duprelatour', progress_bar=True)
# compute the comodulogram
estimator.fit(epochs[0])
# plot the results
estimator.plot(tight_layout=False)
plt.show()

#%%
"""
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram, REFERENCES
from pactools import simulate_pac

#fs = 200.  # Hz
#high_fq = 50.0  # Hz
#low_fq = 5.0  # Hz
#low_fq_width = 1.0  # Hz
#
#n_points = 10000
#noise_level = 0.4
#
#signal = simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
#                      low_fq_width=low_fq_width, noise_level=noise_level,
#                      random_state=0)

# load epochs
filename = wdir + 'Laetitia/sensors/S03_' + binning + '_R1_onset_short_'+blocks+'-epo.fif'
loaded_epochs = mne.read_epochs(filename)
fs = loaded_epochs.info['sfreq']
loaded_epochs.pick_types('mag')
chosen_epochs = loaded_epochs.pick_types(meg = 'mag', eeg=False)
channel_names = chosen_epochs.ch_names  
times = chosen_epochs.times

low_fq_range = np.linspace(1, 10, 50)
methods = [
    'ozkurt', 'canolty', 'tort', 'penny', 'vanwijk', 'duprelatour', 'colgin',
    'sigl', 'bispectrum'
]

# Define the subplots where the comodulogram will be plotted
n_lines = 3
n_columns = int(np.ceil(len(methods) / float(n_lines)))
fig, axs = plt.subplots(
    n_lines, n_columns, figsize=(4 * n_columns, 3 * n_lines))
axs = axs.ravel()


# Compute the comodulograms and plot them
for ax, method in zip(axs, methods):
    print('%s... ' % (method, ))
    estimator = Comodulogram(fs=500, low_fq_range=low_fq_range,
                             low_fq_width=low_fq_width, method=method,
                             progress_bar=False)
    estimator.fit(signal)
    estimator.plot(titles=[REFERENCES[method]], axs=[ax])

plt.show()
"""
#%%
#############################################################################
############## CFC  ##############
#############################################################################
## Compute CFC with tort method for each magnetometer of a subject and save the 
## figures.


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import mne
from pactools.plot_comodulogram import plot_comodulograms
from pactools.comodulogram import comodulogram
from copy import deepcopy

import colormaps as cmaps
plt.register_cmap(name='viridis', cmap=cmaps.viridis)

################################# Functions ###################################

def subtractEvoked(epochs):
	"""
	Subtract evoked response to epochs
	Arguments
	------
	epochs: epoch object

	Return
	------
	epochs_induced: epoch object	
	"""
	evoked = epochs.average()
	epochs_induced = deepcopy(epochs)
	for i in range(len(epochs)):
		epochs_induced.get_data()[i,:,:] = epochs.get_data()[i,:,:] - evoked.data
	
	return epochs_induced

################################# Parameters ##################################

from config import (subjects, wdir, results_dir, method, low_fq_range, t_stim, 
                    low_fq_width, high_fq_range, high_fq_width,condition_list,
                    response_list, mask_subj, contrast_list, sensors_dir)

subjects = ['jm100109','dp150209','cd110147', 'cl120289', 'tc140215', 'la140083', 'ev070110', 'am150105','lb140113','cc150418','ag150338','rt150347','nd150350','vs150444','am090241','pj150414']
wdir         = "/neurospin/meg/meg_tmp/Rabbit_LaetitiaG_2015/" 
results_dir = op.join(wdir, 'results')
method = 'tort'
low_fq_range = np.arange(3.5, 14.1, 0.2) # min 2.4cycles for the lowest freq
low_fq_width = 2.0  # Hz
t_stim = {'LR':[272, 544], 'RL': [188, 376]} # onset of 2nd and 3rd flashes
high_fq_range = np.arange(14, 160, 2) # array of frequency for amplitude signal
high_fq_width = 20.0  # Hz should be >= 2*driver freq
condition_list = ['LR','RL']
response_list = ['TESTill', 'TESTcor', 'CTRL']
mask_subj = {   'LR': (np.array(subjects) != 'ev070110') & (np.array(subjects) != 'rt150347'),
                'RL': np.array(subjects) == np.array(subjects)}
contrast_list = [['TESTill', 'TESTcor'], ['TESTill', 'CTRL'],['CTRL', 'TESTcor']]
sensors_dir  = wdir + 'sensors/'
##############################################


comod_dir = results_dir + '/comodulogram/'

# Choose epochs locked on first stim or on button press
locked = '1stStim' # 'ButtonPress' '1stStim'
epname = {'ButtonPress': '_respLocked_', '1stStim': '_'}

# Define time window [tmin, tmax] following whether the evoked response is conserved
twin = 0.6

#################################### Main #####################################

# Loop across contrasts
for r, cont in enumerate(contrast_list):
    # Loop: RL and LR
    for condition in condition_list:
        
        # Define subjects list and onset of 3rd stim
        subjs = np.array(subjects)[mask_subj[condition]] 
        tmin = t_stim[condition][1]/1000. # in sec
        tmax = tmin + twin
        
        # Loop across subject
        for subject in subjects:
            print(condition + ' ' + str(cont) + ' ' + subject)
            # read epochs
            e1 = mne.read_epochs(sensors_dir + subject + '_filt160Hz' + epname[locked] + cont[0] + '_' + condition + '-epo.fif')
            e2 = mne.read_epochs(sensors_dir + subject + '_filt160Hz' + epname[locked] + cont[1] + '_' + condition + '-epo.fif')
            
            # equalize for the contrast
            mne.epochs.equalize_epoch_counts([e1,e2])
            fs = e1.info['sfreq']
            times = e1.times
            
            # concatenate epochs - link together in a 'list'
            e_all = mne.epochs.concatenate_epochs((e1,e2))
            
            # Loop across responses
            for ep_n, e in enumerate([e1, e2, e_all]):

                # Choose mag
                e.pick_types(meg = 'mag', eeg=False)
                channel_names = e.ch_names
                
                sig = e.get_data() # gets the epoched data
        
                # temporal mask to considered only the interval of interest (applied after filtering)
                n_epochs, n_channels, n_points = sig.shape
                mask = np.zeros((n_epochs, n_points))
                mask[:,(times>tmin) & (times <tmax)] = 1
        
                # Compute comodulogram for each channel
                for i_channel in range(n_channels):        
                    channel_signal = sig[:, i_channel, :]
                
                    # Compute CFC
                    comod = comodulogram(
                        low_sig= channel_signal, mask = mask, fs=fs, draw=False, method=method,
                        low_fq_range=low_fq_range, low_fq_width=low_fq_width,
                        high_fq_range=high_fq_range, high_fq_width=high_fq_width,
                        vmin=None, vmax=None)
                    
                    """
                    
                    # Locked on alpha phase
                    estimator = PeakLocking(fs=fs, low_fq = 10., low_fq_width = low_fq_width, t_plot = 0.3)
                    estimator.fit(channel_signal)
                    fig = estimator.plot(vmax=0.3, cmap='viridis')
                    
                    """
            
                    # plot the results
                    fig, axs = plt.subplots(1, 1, figsize=(6, 6))
                    plot_comodulograms(comod, fs, low_fq_range, high_fq_range, [channel_names[i_channel]],
                                           fig,[axs], plt.get_cmap('viridis'), None, None)
                
                    # save the figure
                    save_name = '%s_%s_%s' % (subject,method, channel_names[i_channel])
                    if ep_n <2:
                        fig.savefig(comod_dir + save_name + '_' + condition + '_' + str(cont)  + '_' + cont[ep_n])
                        dataname = comod_dir + save_name + '_' + condition + '_' + str(cont) + '_' + cont[ep_n] + '_comod.npy'
                    elif ep_n==2:
                        fig.savefig(comod_dir + save_name + '_' + condition + '_' + str(cont)  + '_all')
                        dataname = comod_dir + save_name + '_' + condition + '_' + str(cont) + '_all' + '_comod.npy'                        
                    np.save(dataname, comod)
                    plt.close('all')
        
    
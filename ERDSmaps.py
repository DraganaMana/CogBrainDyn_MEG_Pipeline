# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:53:52 2019

@author: Dragana
"""

# Authors: Clemens Brunner <clemens.brunner@gmail.com>
#
# License: BSD (3-clause)


import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
from mne.time_frequency import tfr_multitaper
from mne.stats import permutation_cluster_1samp_test as pcluster_test
from mne.viz.utils import center_cmap
import config
import os.path as op
from warnings import warn



# load and preprocess data ####################################################
#subject = 1  # use data from subject 1
#runs = [6, 10, 14]  # use only hand and feet motor imagery runs
#
#fnames = eegbci.load_data(subject, runs)
#raws = [read_raw_edf(f, preload=True, stim_channel='auto') for f in fnames]
#raw = concatenate_raws(raws)
#
#raw.rename_channels(lambda x: x.strip('.'))  # remove dots from channel names
#
#events = mne.find_events(raw, shortest_event=0, stim_channel='STI 014')
#
#picks = mne.pick_channels(raw.info["ch_names"], ["C3", "Cz", "C4"])

"""
So, we need: subject, runs, 
Probably these ones no, if we have the epochs loaded: raws(raw), events, picks?, 


"""
subject = 'hm070076'
runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06'] 
meg_subject_dir = op.join(config.meg_dir, subject)

## Read raw files from MEG room
#for run in runs:
#    extension = run + '_raw'
#    raw_MEG = op.join(meg_subject_dir,
#                               config.base_fname.format(**locals()))
#    raw = mne.io.read_raw_fif(raw_MEG,
#                                  allow_maxshield=config.allow_maxshield,
#                                  preload=True, verbose='error')
## Read files (events) after 03-extract_events.py
#for run in runs:
#    extension = run + '_sss_raw'
#    raw_fname_in = op.join(meg_subject_dir, config.base_fname.format(**locals()))
#    eve_fname = op.splitext(raw_fname_in)[0] + '_' + config.name_ext + '-eve.fif'
#    events = mne.read_events(eve_fname)





# epoch data ##################################################################
#tmin, tmax = -1, 4  # define epochs around events (in s)
#event_ids = dict(hands=2, feet=3)  # map event IDs to tasks
#
#epochs = mne.Epochs(raw, events, event_ids, tmin - 0.5, tmax + 0.5,
#                    picks=picks, baseline=None, preload=True)


tmin = config.tmin
tmax = config.tmax
baseline = config.baseline
event_ids = config.event_id

raw_list = list()
events_list = list()

for run in runs:
    extension = run + '_sss_raw'
    raw_fname_in = op.join(meg_subject_dir,
                           config.base_fname.format(**locals()))
    eve_fname = op.splitext(raw_fname_in)[0] + '_' + config.name_ext + '-eve.fif'
    print("Input: ", raw_fname_in, eve_fname)
    
    if not op.exists(raw_fname_in):
        warn('Run %s not found for subject %s ' %
             (raw_fname_in, subject))
        continue
    
    raw = mne.io.read_raw_fif(raw_fname_in, preload=True)
    
    events = mne.read_events(eve_fname)
    events_list.append(events)


    raw_list.append(raw)

print('  Concatenating runs')
raw, events = mne.concatenate_raws(raw_list, events_list=events_list)

if config.eeg:
    raw.set_eeg_reference(projection=True)

del raw_list

picks = mne.pick_channels(raw.info["ch_names"], ["MEG0433", "MEG0432", "MEG0431"])

# Epoch the data
print('  Epoching')
epochs = mne.Epochs(raw, events, config.event_id, config.tmin, config.tmax,
                    proj=True, picks=picks, baseline=config.baseline,
                    preload=False, decim=config.decim,
                    reject=config.reject)


# compute ERDS maps ###########################################################
freqs = np.arange(2, 36, 1)  # frequencies from 2-35Hz
n_cycles = freqs  # use constant t/f resolution
vmin, vmax = -0.5, 1.  # set min and max ERDS values in plot
baseline = [-0.3, -0.1]  # baseline interval (in s)
cmap = center_cmap(plt.cm.RdBu, vmin, vmax)  # zero maps to white
kwargs = dict(n_permutations=100, step_down_p=0.05, seed=1,
              buffer_size=None)  # for cluster test

for event in event_ids:
    print(event)
    tfr = tfr_multitaper(epochs[event], freqs=freqs, n_cycles=n_cycles,
                         use_fft=True, return_itc=False, average=False,
                         decim=2)
    tfr.crop(tmin, tmax)
    tfr.apply_baseline(baseline, mode="percent")

    fig, axes = plt.subplots(1, 4, figsize=(12, 4),
                             gridspec_kw={"width_ratios": [10, 10, 10, 1]})
    for ch, ax in enumerate(axes[:-1]):  # for each channel
        # positive clusters
        _, c1, p1, _ = pcluster_test(tfr.data[:, ch, ...], tail=1, **kwargs)
        # negative clusters
        _, c2, p2, _ = pcluster_test(tfr.data[:, ch, ...], tail=-1, **kwargs)

        # note that we keep clusters with p <= 0.05 from the combined clusters
        # of two independent tests; in this example, we do not correct for
        # these two comparisons
        c = np.stack(c1 + c2, axis=2)  # combined clusters
        p = np.concatenate((p1, p2))  # combined p-values
        mask = c[..., p <= 0.05].any(axis=-1)

        # plot TFR (ERDS map with masking)
        tfr.average().plot([ch], vmin=vmin, vmax=vmax, cmap=(cmap, False),
                           axes=ax, colorbar=False, show=False, mask=mask,
                           mask_style="mask")

        ax.set_title(epochs.ch_names[ch], fontsize=10)
        ax.axvline(0, linewidth=1, color="black", linestyle=":")  # event
        if not ax.is_first_col():
            ax.set_ylabel("")
            ax.set_yticklabels("")
    fig.colorbar(axes[0].images[-1], cax=axes[-1])
    fig.suptitle("ERDS ({})".format(event))
    fig.show()
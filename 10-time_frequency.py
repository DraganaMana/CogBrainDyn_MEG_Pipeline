"""
================================
09. Time-frequency decomposition
================================

The epoched data is transformed to time-frequency domain using morlet wavelets.
Faces and scrambled data sets are used and for both of them, the average power
and inter-trial coherence are computed and saved to disk. Only channel 'EEG070'
is used to save time.
"""

import os.path as op
import numpy as np
import matplotlib.pyplot as plt

import mne
from mne.parallel import parallel_func

import config

freqs = np.arange(10, 40)
n_cycles = freqs / 3.


def run_time_frequency(subject):
    print("processing subject: %s" % subject)
    meg_subject_dir = op.join(config.meg_dir, subject)
    extension = 'cleaned-epo'
    fname_in = op.join(meg_subject_dir,
                       config.base_fname.format(**locals()))
    print("Input: ", fname_in)

    epochs = mne.read_epochs(fname_in)

    for condition in config.time_frequency_conditions:
        this_epochs = epochs[condition]
        power, itc = mne.time_frequency.tfr_morlet(
            this_epochs, freqs=freqs, return_itc=True, n_cycles=n_cycles)

        power.save(
            op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
                    % (config.study_name, subject, 
                       condition.replace(op.sep, ''))), overwrite=True)
        itc.save(
            op.join(meg_subject_dir, '%s_%s_itc_%s-tfr.h5'
                    % (config.study_name, subject, 
                       condition.replace(op.sep, ''))), overwrite=True)

    if config.plot:
        fig, axis = plt.subplots(1, 2, figsize=(7, 4))
        figure1 = power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                   baseline=(-0.5, 0), mode='logratio', axes=axis[0],
                   title='Alpha', show=False)
        figure1 = power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                   baseline=(-0.5, 0), mode='logratio', axes=axis[1],
                   title='Beta', show=False)
        mne.viz.tight_layout()
        figure1.show()
        figure1.show()

parallel, run_func, _ = parallel_func(run_time_frequency, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)

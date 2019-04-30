"""
===============
06. Evoked data
===============

The evoked data sets are created by averaging different conditions.
"""

import os.path as op

import mne
from mne.parallel import parallel_func

import config


def run_evoked(subject):
    print("Processing subject: %s" % subject)
    meg_subject_dir = op.join(config.meg_dir, subject)

    extension = '_int123_cleaned-epo'
    
    fname_in = op.join(meg_subject_dir,
                       config.base_fname.format(**locals()))
    extension = '-int123-cleaned_epo-ave'
    fname_out = op.join(meg_subject_dir,
                        config.base_fname.format(**locals()))

    print("Input: ", fname_in)
    print("Output: ", fname_out)

    print('  Creating evoked datasets')
    epochs = mne.read_epochs(fname_in, preload=True)

    evokeds = []
    for condition in config.conditions:
        evokeds.append(epochs[condition].average())
    mne.evoked.write_evokeds(fname_out, evokeds)

    if config.plot:
        ts_args = dict(gfp=True, time_unit='s')

        topomap_args = dict(time_unit='s') # sensors=False, 

        for condition, evoked in zip(config.conditions, evokeds):
            evoked.plot_joint(title=condition, ts_args=ts_args,
                              topomap_args=topomap_args, times=[0., 0.1, .2, .3, .4, .5])

parallel, run_func, _ = parallel_func(run_evoked, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)

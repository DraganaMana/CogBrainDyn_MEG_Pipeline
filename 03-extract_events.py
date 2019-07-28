"""
============================================
03. Extract events from the stimulus channel
============================================

Here, all events present in the stimulus channel indicated in
config.stim_channel are extracted.
The events are saved to the subject's MEG directory.
This is done early in the pipeline to avoid distorting event-time,
for instance by resampling.
"""

import os.path as op

import mne
import numpy as np
from mne.parallel import parallel_func
#from mne.event import define_target_events

import numpy as np
from warnings import warn

import config


def run_events(subject):
    print("Processing subject: %s" % subject)
    MFmeg_subject_dir = op.join(config.MFmeg_dir, subject)

    for run in config.runs:
        extension = run + '_' + config.name_ext + '_sss_raw'
        raw_fname_in = op.join(MFmeg_subject_dir,
                               config.base_fname.format(**locals()))
        eve_fname_out = op.splitext(raw_fname_in)[0] + '-eve.fif'
        
        if not op.exists(raw_fname_in):
            warn('Run %s not found for subject %s ' %
                 (raw_fname_in, subject))
            continue

        raw = mne.io.read_raw_fif(raw_fname_in)
        
        events = mne.find_events(raw, stim_channel=config.stim_channel,
                                 consecutive=True,
                                 min_duration=config.min_event_duration,
                                 shortest_event=config.shortest_event)
        if config.trigger_time_shift:
            events = mne.event.shift_time_events(events,
                                                 np.unique(events[:, 2]),
                                                 config.trigger_time_shift,
                                                 raw.info['sfreq'])
        
        # XXX shift events by trigger
#        if config.trigger_offset:
#            events = mne.event.shift_time_events(
#                    events,
#                    np.unique(events[:,2]),
#                    config.trigger_offset,
#                    raw.info['sfreq'],
#                    )



        print("Input: ", raw_fname_in)
        print("Output: ", eve_fname_out)

        mne.write_events(eve_fname_out, events)

        if config.plot:
            # plot events
            # It would be good to have names on the figures, from which Run are
            # the events plotted
            figure = mne.viz.plot_events(events, sfreq=raw.info['sfreq'],
                                         first_samp=raw.first_samp)
            figure.show()


parallel, run_func, _ = parallel_func(run_events, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)

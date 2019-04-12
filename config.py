"""
===========
Config file
===========
Configuration parameters for the study. This should be in a folder called
``library/`` inside the ``processing/`` directory.
"""

import os
import numpy as np


# let the scripts generate plots or not
# execute %matplotlib qt in your command line once to show the figures in
# separate windows

plot = True

# execute %matplotlib qt 
# in the command line to get the plots in extra windows
###############################################################################
# DIRECTORIES
# -----------
# Let's set the `study path`` where the data is stored on your system
# study_path = '../MNE-sample-data/'

study_path = 'C:/Users/Dragana/Documents/MEG/MEG_pilot/Test_01/'


# The ``subjects_dir`` and ``meg_dir`` for reading anatomical and MEG files.
subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

###############################################################################
# SUBJECTS / RUNS
# ---------------
#
# The MEG-data need to be stored in a folder
# named my_study_path/MEG/my_subject/

# This is the name of your experimnet

study_name = 'ScaledTime'


# To define the list of participants, we use a list with all the anonymized participant names. Even if 
# you plan on analyzing a single participant, it needs to be set up as a list with a single element,
# as in the 'example'

subjects_list = ['s190320']
subject_pilot = 's190320'

# subjects_list = ['subject_01', 'subject_02', 'subject_03', 'subject_05',
#                  'subject_06', 'subject_08', 'subject_09', 'subject_10',
#                  'subject_11', 'subject_12', 'subject_14']

# ``bad subjects`` that should not be excluded from the above
# [Good Practice / Advice] keep track of the criteria leading you to exclude a participant (e.g. too many movements, 
# missing blocks, aborted experiment, did not understand the instructions, etc, ...) 
exclude_subjects = []  # ['subject_01']

# Define the names of your ``runs``

# [Good Practice / Advice] The naming should be consistent across participants.
# List the number of runs you ideally expect to have per participant. The scripts will issue a warning 
# if there are less runs than is expected. If there is only just one file, leave empty!
#runs = ['Run02', 'Run03']
runs = ['Run02', 'Run03', 'Run04']


# does the data have EEG?
eeg = False # True

# This generates the name for all files
# with the names specified above
# normally you should not have to touch this

base_fname = '{subject}_' + study_name + '_{extension}.fif'
#base_fname = '{runs}' + '.fif'

###############################################################################
# BAD CHANNELS
# ------------
#
# ``bad channels``, bad channels are noisy sensors that *must* to be listed *before* maxfilter is applied
# [Good Practice / Advice] during the acquisition of your MEG / EEG data, systematically list and keep track of the noisy sensors.
# Here, put the number of runs you ideally expect to have per participant.
# Use the simple dict if you don't have runs or if the same sensors are noisy across all runs

#bads = dict(subject_190301=['MEG 1512', 'MEG 0131', 'MEG 0341', 'MEG 0213', 'MEG 0133'])
# bads = dict(sample=['MISC 001', 'MISC 002'])
# Use the dict(dict) if you have many runs or if noisy sensors are changing across runs 
# bads = dict(SB01=dict(run01=['MEG 2443', 'EEG 053'],

#bads = dict(s190320=dict(Run04=['MEG1732', 'MEG1723', 'MEG1722', 'MEG0213', 'MEG0541', 'MEG1921']))
bads = dict(s190320=dict(Run02=['MEG1732', 'MEG1723', 'MEG1722', 'MEG0213', 'MEG0541', 'MEG1921'],
                         Run03=['MEG1732', 'MEG1723', 'MEG1722', 'MEG0213', 'MEG0541', 'MEG1921'],
                         Run04=['MEG1732', 'MEG1723', 'MEG1722', 'MEG0213', 'MEG0541', 'MEG1921']))

###############################################################################
# DEFINE ADDITIONAL CHANNELS
# --------------------------
#
# Here you name or replace  extra channels that were recorded, for instance EOG, ECG
# ``set_channel_types`` defines types of channels
# example :
# set_channel_types = {'EEG061': 'eog', 'EEG062': 'eog', 'EEG063': 'ecg', 'EEG064': 'misc'}
set_channel_types = {'EOG061': 'eog', 'EOG062': 'eog', 'ECG063': 'ecg', 
                     'MISC201': 'misc', 'MISC202': 'misc', 'MISC203': 'misc',
                     'MISC204': 'misc', 'MISC205': 'misc', 'MISC206': 'misc',
                     'MISC301': 'misc', 'MISC302': 'misc', 'MISC303': 'misc',
                     'MISC304': 'misc', 'MISC305': 'misc', 'MISC306': 'misc'}

# ``rename_channels`` rename channels
#
# example :
# rename_channels = {'EEG061': 'EOG061', 'EEG062': 'EOG062', 'EEG063': 'ECG063'}
rename_channels = None

###############################################################################
# FREQUENCY FILTERING
# -------------------
#
# [Good Practice / Advice]
# It is typically better to set your filtering properties on the raw data so as to avoid
# what we call border effects 
#
# If you use this pipeline for evoked responses, a default filtering would be 
# a high-pass filter cut-off of l_freq = 1 Hz
# a low-pass filter cut-off of h_freq = 40 Hz
# so you would preserve only the power in the 1Hz to 40 Hz band
#
# If you use this pipeline for time-frequency analysis, a default filtering would be 
# a high-pass filter cut-off of l_freq = 1 Hz
# a low-pass filter cut-off of h_freq = 120 Hz
# so you would preserve only the power in the 1Hz to 120 Hz band
#
# If you use are interested in the lowest frequencies, do not use a high-pass filter cut-off of l_freq = None
# If you need more fancy analysis, you are already likely past this kinD of tips! :)

# ``l_freq``  : the low-frequency cut-off in the highpass filtering step.
# Keep it None if no highpass filtering should be applied.
l_freq = None # should be none

# ``h_freq``  : the high-frequency cut-off in the lowpass filtering step.
# Keep it None if no lowpass filtering should be applied.
h_freq = 120.


###############################################################################
# MAXFILTER PARAMETERS
# -------------------
#

# Download the ``cross talk`` and ``calibration`` files. Warning: these are site and machine specific files
# that provide information about the environmental noise.
# For practical purposes, place them in your study folder.
# At NeuroSpin: ct_sparse and sss_call are on the meg_tmp server
# You can also download them from osf.io/m9nwz/ 'ct_sparse_nspn.fif' & 'sss_cal_nspn.dat')
mf_ctc_fname = os.path.join(study_path, 'system_calibration_files', 'ct_sparse_nsp_2017.fif')
mf_cal_fname = os.path.join(study_path, 'system_calibration_files', 'sss_cal_nsp_2017.dat')

# [Good Practice / Advice]
# Despite all possible care to avoid movements in the MEG, the participant will likely
# slowly drift down from the Dewar or slightly shift the head around in the course of the 
# recording session. Hence, to take this into account, we are realigning all data to a single
# position. For this, you need to define a reference run (typically the one in the middle of 
# the recording session). 
mf_reference_run = 0  # here, take 1st run as reference for head position

# Set the origin for the head position
mf_head_origin = 'auto'

# [Good Practice / Advice]
# There are two kinds of maxfiltering: sss and tsss 
# [sss = signal space separation ; tsss = temporal signal space separation]
# (Taulu et al, 2004): http://cds.cern.ch/record/709081/files/0401166.pdf
# If you are interested in low frequency activity (<0.1Hz), avoid using tsss and set mf_st_duration = None
# If you are interested in low frequency above 0.1 Hz, you can use the default mf_st_duration = 10 s
# Elekta default = 10s, meaning it acts like a 0.1 Hz highpass filter
# ``mf_st_duration `` : if None, no temporal-spatial filtering is applied during MaxFilter,
# otherwise, put a float that speficifies the buffer duration in seconds
mf_st_duration = None

###############################################################################
# RESAMPLING
# ----------
# 
# [Good Practice / Advice]
# If you have acquired data with a very high sampling frequency (e.g. 2 kHz)
# you will likely want to downsample to lighten up the size of the files you are working with (pragmatics)
# If you are interested in typical analysis (up to 120 Hz) you can typically resample your data down to 500 Hz 
# without preventing reliable time-frequency exploration of your data 
#
# ``resample_sfreq``  : a float that specifies at which sampling frequency
# the data should be resampled. If None then no resampling will be done.

resample_sfreq =  1000. # None


# ``decim`` : integer that says how much to decimate data at the epochs level.
# It is typically an alternative to the `resample_sfreq` parameter that
# can be used for resampling raw data. 1 means no decimation.
decim = 1

###############################################################################
# AUTOMATIC REJECTION OF ARTIFACTS
# --------------------------------
#
# [Good Practice / Advice]
# Have a look at your raw data and train yourself to detect a blink, a heart beat and an eye movement.
# You can do a quick average of blink data and check what the amplitude looks like.
#
#  ``reject`` : the default rejection limits to make some epochs as bads.
# This allows to remove strong transient artifacts.
# If you want to reject and retrieve blinks later, e.g. with ICA, don't specify

# a value for the eog channel (see examples below).
# Make sure to include values for eeg if you have eeg data


# **Note**: these numbers tend to vary between subjects.
# Examples: 
# reject = {'grad': 4000e-13, 'mag': 4e-12, 'eog': 150e-6}
# reject = {'grad': 4000e-13, 'mag': 4e-12, 'eeg': 200e-6}
# reject = None
"""  reject = dict(grad=4000e-13, # T / m (gradiometers)
                        mag=4e-12, # T (magnetometers)
                        eeg=40e-6, # V (EEG channels)
                        eog=250e-6 # V (EOG channels)
                        ) """


reject = {'grad': 4000e-13, 'mag': 4e-12}

###############################################################################
# EPOCHING
# --------
#
# ``tmin``: float that gives the start time before event of an epoch.
tmin = -1

#  ``tmax`` : float that gives the end time after event of an epochs.
tmax = 1.25 # I get 7 epochs, 3 from Play, 3 from Replay

# float specifying the offset for the trigger and the stimulus (in seconds)
# you need to measure this value for your specific experiment/setup
#trigger_offset = -0.0416
# XXX forward/delay all triggers by this value

# ``baseline`` : tuple that specifies how to baseline the epochs; if None,
# no baseline is applied

baseline = (-1, -0.5)

# stimulus channel, which contains the events
#stim_channel = ['STI001', 'STI002', 'STI003', 'STI004']  # 'STI014'# 'STI101'
stim_channel = 'STI101'

# minimal duration of the events you want to extract
min_event_duration = 0.003

#  `event_id`` : python dictionary that maps events (trigger/marker values)
# to conditions. E.g. `event_id = {'Auditory/Left': 1, 'Auditory/Right': 2}`
#event_id = {'Interval1': 9, 'Interval2': 10,
#            'Interval3': 12}
#conditions = ['Interval1', 'Interval2', 'Interval3']
#
#event_id = {'WhiteCross': 9, 'Int02': 10, 'Int03': 12}
event_id = {'ButtonPress': 5}
#conditions = ['Int01', 'Int02', 'Int03']
conditions = ['ButtonPress']

###############################################################################
# ICA PARAMETERS
# --------------
# ``runica`` : boolean that says if ICA should be used or not.
runica = True

rejcomps_man = dict(s190320=dict(meg=[],
                                eeg=[]))

###############################################################################
# DECODING
# --------------
#
# decoding_conditions should be a list of conditions to be classified.
# For example 'Auditory' vs. 'Visual' as well as
# 'Auditory/Left' vs 'Auditory/Right'
decoding_conditions = ['ButtonPress']
decoding_metric = 'roc_auc'
decoding_n_splits = 2

###############################################################################
# TIME-FREQUENCY
# --------------
#
#time_frequency_conditions = ['Int01','Int02','Int03']
time_frequency_conditions = ['ButtonPress']
###############################################################################
# SOURCE SPACE PARAMETERS
# -----------------------
#

spacing = 'oct6'
mindist = 5
smooth = 10

fsaverage_vertices = [np.arange(10242), np.arange(10242)]

if not os.path.isdir(study_path):
    os.mkdir(study_path)

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)

###############################################################################
# ADVANCED
# --------
#
# ``l_trans_bandwidth`` : float that specifies the transition bandwidth of the
# highpass filter. By default it's `'auto'` and uses default mne parameters.
l_trans_bandwidth = 'auto'

#  ``h_trans_bandwidth`` : float that specifies the transition bandwidth of the
# lowpass filter. By default it's `'auto'` and uses default mne parameters.
h_trans_bandwidth = 'auto'

#  ``N_JOBS`` : an integer that specifies how many subjects you want to run in parallel.
N_JOBS = 1

random_state = 42

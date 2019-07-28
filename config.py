"""
===========
Config file
===========
Configuration parameters for the study. This should be in a folder called
``library/`` inside the ``processing/`` directory.


https://mne-tools.github.io/0.17/auto_tutorials/plot_metadata_epochs.html?highlight=pandas%20querying%20metadata%20epochs%20objects
"""

import os
from collections import defaultdict
import numpy as np


# ``plot``  : boolean
#   If True, the scripts will generate plots.
#   If running the scripts from a notebook or spyder
#   run %matplotlib qt in the command line to get the plots in extra windows

plot = True
#plot = False
#
###############################################################################
# DIRECTORIES
# -----------
#
# ``study_path`` : str
#    Set the `study path`` where the data is stored on your system.
#
# Example
# ~~~~~~~
# study_path = '../MNE-sample-data/'

#study_path = '/neurospin/meg/meg_tmp/ScaledTime_Dragana_2019/'

# 'C:/Users/Dragana/Documents/MEG/MEG_pilot/Test_01/'

#study_path = '/media/dm258725/VERBATIM/ScaledTime/MEGdata/' 
#study_path = 'D:/ScaledTime/MEGdata/'
#study_path = 'H:/ScaledTime_Dragana_2019/'
study_path = '/home/dm258725/Desktop/Link to ScaledTime_Dragana_2019/'

# ``subjects_dir`` : str
#   The ``subjects_dir`` contains the MRI files for all subjects.

subjects_dir = os.path.join(study_path, 'subjects')

# ``meg_dir`` : str
#   The ``meg_dir`` contains the MEG data in subfolders
#   named my_study_path/MEG/my_subject/

meg_dir = os.path.join(study_path, 'MEG')
MFmeg_dir = os.path.join(study_path, 'Multifracs')


###############################################################################
# SUBJECTS / RUNS
# ---------------
#
# ``study_name`` : str
#   This is the name of your experiment.
study_name = 'ScaledTime'

name_ext = 'MF-PR' # 'P-int123-scl', 'R-int123-scl', 'P-ints'

# ``subjects_list`` : list of str
#   To define the list of participants, we use a list with all the anonymized
#   participant names. Even if you plan on analyzing a single participant, it
#   needs to be set up as a list with a single element, as in the 'example'
#   subjects_list = ['SB01']

# To use all subjects use
#subjects_list = ['ep190335'] 
#subjects_list = ['ad190325']
#subjects_list = ['ep190335', 'ad190325'] 
subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 
                 'ch180036', 'ms180425', 'cg190026', 'ih190084', 'cr170417', 'll180197', 
                 'tr180110', 'gl180335', 'lr190095', 'ag170045', 'pl170230', 'ma190185'] 

#subjects_list = ['ll180197', 
#                 'tr180110', 'ep190335', 'gl180335', 'lr190095', 'ad190325', 'ag170045'] 
#subjects_list2 = ['lr190095', 'ad190325', 'ag170045']
#subjects_list3 = ['tr180110', 'ep190335', 'gl180335']
#subjects_list = ['ih190084', 'cr170417', 'll180197', 'tr180110', 'ep190335', 'gl180335']
# 
#                 
# ALL PAX: 'fm180074', lk160274, empty_room, 
# final pax
# 'hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237', 'ld190260', 'ms180425', 'ch180036',
# 'cg190026', 'ih190084', 'cr170417', 'll180197', 'tr180110', 'lr190095', 'ep190335', 'gl180335', 
# 'ad190325'

#cur_subj = 'lk160274'
#subject_pilot = 's190320'
# else for speed and fast test you can use:

#subjects_list = ['SB01']

# ``exclude_subjects`` : list of str
#   Now you can specify subjects to exclude from the group study:
#
# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# Keep track of the criteria leading you to exclude
# a participant (e.g. too many movements, missing blocks, aborted experiment,
# did not understand the instructions, etc, ...)

exclude_subjects = []

# ``runs`` : list of str
#   Define the names of your ``runs``
#
# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# The naming should be consistent across participants. 
# List the number of runs you ideally expect to have per participant. 
# The scripts will issue a warning
# if there are less runs than is expected. If there is only just one file,
# leave empty!

runs = ['Run01', 'Run02', 'Run03', 'Run04', 'Run05', 'Run06'] #
#runs = ['Run03']

PR = ['Play', 'Replay']

# ``eeg``  : bool
#    If true use the EEG channels

eeg = False  # True

# ``base_fname`` : str
#    This automatically generates the name for all files
#    with the variables specified above.
#    Normally you should not have to touch this

base_fname = '{subject}_' + study_name + '_{extension}.fif'


###############################################################################
# BAD CHANNELS
# ------------
# for 01-import_and_filter.py

# ``bads`` : dict of list | dict of dict
#    Bad channels are noisy sensors that *must* to be listed
#    *before* maxfilter is applied. You can use the dict of list structure
#    if you have bad channels that are the same for all runs.
#
# Example
# ~~~~~~~
#
# Define dict(list): 
# >>> bads = defaultdict(list)
#
#   and to populate this, do:
#
# >>> bads['SB01'] = ['MEG1723', 'MEG1722']
#

#bads = defaultdict(list)
#bads['SB01'] = ['MEG1723', 'MEG1722']
#bads['SB04'] = ['MEG0543', 'MEG2333']
#bads['SB06'] = ['MEG2632', 'MEG2033']

#
#    Use the dict(dict) if you have many runs or if noisy sensors are changing
#    across runs.
#
# Example
# ~~~~~~~
#
# Define dict(dict):
# 
# >>> def default_bads():
# >>>     return dict(run01=[], run02=[])
# >>>
# >>> bads = defaultdict(default_bads)
#
#   and to populate this, do:
#
# >>> bads['subject01'] = dict(run01=[12], run02=[7])
#
# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# During the acquisition of your MEG / EEG data, systematically list and keep
# track of the noisy sensors. Here, put the number of runs you ideally expect
# to have per participant. Use the simple dict if you don't have runs or if
# the same sensors are noisy across all runs.


#def default_bads():
#     return dict(Run01=[], Run02=[], Run03=[], Run04=[], Run05=[])

def default_bads():
    return dict(Run01=[], Run02=[], Run03=[], Run04=[], Run05=[], Run06=[])

bads = defaultdict(default_bads)
#bads['s190320'] = ['MEG1732', 'MEG1723', 'MEG1722', 'MEG0213', 'MEG0541', 'MEG1921']
#bads = dict(fm180074 = ['MEG1732', 'MEG1722', 'MEG0213', 'MEG1512'])
#bads['fm180074'] = ['MEG1732', 'MEG1722', 'MEG0213', 'MEG1512']

"""
bads['lk160274'] = dict(Run01=['MEG1411', 'MEG0111','MEG0213', 'MEG0133', 'MEG2441', 'MEG1831', 'MEG2031', 'MEG2231', 'MEG2311', 'MEG2341', 'MEG2011', 'MEG2111', 'MEG2021', 'MEG2241', 'MEG1133', 'MEG2321', 'MEG0311', 'MEG1111', 'MEG1141', 'MEG0731', 'MEG1341', 'MEG2141', 'MEG2211', 'MEG2511', 'MEG2541', 'MEG0511', 'MEG2321', 'MEG2041'], 
    Run02=['MEG1411', 'MEG0111','MEG0213', 'MEG0133', 'MEG2031', 'MEG2441', 'MEG2311', 'MEG2021', 'MEG2231', 'MEG2241', 'MEG2111', 'MEG2221', 'MEG1831', 'MEG2211', 'MEG2341', 'MEG2321', 'MEG2331', 'MEG2041', 'MEG2431', 'MEG0521', 'MEG0731', 'MEG2521', 'MEG2541', 'MEG2511', 'MEG2532', 'MEG2131', 'MEG2121', 'MEG1921', 'MEG2411', 'MEG0311', 'MEG1133', 'MEG2631'], 
    Run03=['MEG1411', 'MEG0111','MEG0213', 'MEG0133', 'MEG1911', 'MEG1631', 'MEG1841', 'MEG2011', 'MEG2041', 'MEG1811', 'MEG1831', 'MEG2241', 'MEG1921', 'MEG2021', 'MEG0911', 'MEG1941', 'MEG1821', 'MEG2141', 'MEG1711', 'MEG0921', 'MEG0311', 'MEG2021', 'MEG2031', 'MEG2311', 'MEG2321', 'MEG1741', 'MEG2121', 'MEG1641', 'MEG0741', 'MEG1931', 'MEG2111', 'MEG1221'], 
    Run04=['MEG1411', 'MEG0111','MEG0213', 'MEG0133', 'MEG2041', 'MEG1911', 'MEG2011', 'MEG1741', 'MEG1831', 'MEG0311', 'MEG1841', 'MEG1921', 'MEG2111', 'MEG1931', 'MEG1941', 'MEG1933', 'MEG1631', 'MEG1821', 'MEG2121', 'MEG2031', 'MEG2311', 'MEG0642', 'MEG2231', 'MEG2241', 'MEG2341', 'MEG2321', 'MEG2241'], 
    Run05=['MEG1411', 'MEG0111','MEG0213', 'MEG2041', 'MEG1911', 'MEG1631', 'MEG2011', 'MEG0311', 'MEG1841', 'MEG1921', 'MEG1941', 'MEG1811', 'MEG0642', 'MEG2121', 'MEG1731', 'MEG2021', 'MEG2031', 'MEG2111',  'MEG1931', 'MEG1831', 'MEG2231', 'MEG1933', 'MEG2241', 'MEG2311', 'MEG2321', 'MEG2441', 'MEG2211', 'MEG2221', 'MEG2341', 'MEG2531', 'MEG2411', 'MEG2431', 'MEG2631', 'MEG2131'])

bads['fm180074'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'])
"""


#bads['hm070076'] = dict(Run01=[213, 1732, 1722, 1933, 633, 2522, 311, 613],
#    Run02=[213, 1732, 1722, 1933, 633, 2522],
#    Run03=[213, 1732, 1722, 1933, 633, 2522],
#    Run04=[213, 1732, 1722, 1933, 633],
#    Run05=[213, 1732, 1722, 1933],
#    Run06=[213, 1732, 1722, 1933])
#
#bads['fr190151'] = dict(Run01=[213, 1732, 1722, 1723, 1933, 633, 321, 613],
#    Run02=[213, 1732, 1722, 1723, 1933, 633, 321, 613],
#    Run03=[213, 1732, 1722, 1723, 1933, 633, 321, 613],
#    Run04=[213, 1732, 1722, 1723, 1933, 633, 321, 613],
#    Run05=[213, 1732, 1722, 1723, 1933, 633, 321, 613],
#    Run06=[213, 1732, 1722, 1723, 1933, 633, 321, 613])
#
#bads['at140305'] = dict(Run01=[213, 1732, 1722,1723, 1933, 633],
#    Run02=[213, 1732, 1722, 1723, 1933, 633, 342],
#    Run03=[213, 1732, 1722, 1723, 1933, 633, 2512],
#    Run04=[213, 1732, 1722, 1723, 1933, 633, 2512, 311, 1111, 1112, 1113],
#    Run05=[213, 1732, 1722, 1723, 1933, 633, 2512, 613])
#
#bads['cc150418'] = dict(Run01=[213, 1732, 1722, 1723, 1933, 2123],
#    Run02=[213, 1732, 1722, 1723, 1933, 633, 2123],
#    Run04=[213, 1732, 1722, 1723, 1933, 633, 2432],
#    Run05=[213, 1732, 1722, 1723, 1933, 633, 2632])
#
#bads['eb180237'] = dict(Run01=[213, 1732, 1722,1723, 1933, 633, 613, 623, 2511],
#    Run02=[213, 1732, 1722,1723, 1933, 633, 613, 623, 2511],
#    Run03=[213, 1732, 1722,1723, 1933, 633, 613, 623, 2511, 1512],
#    Run04=[213, 1732, 1722,1723, 1933, 633, 613, 623, 2511],
#    Run05=[213, 1732, 1722,1723, 1933, 633, 613, 623, 2542])

######################################################
# Pax 1
bads['hm070076'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG2522', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0511', 'MEG0541', 'MEG1723', 'MEG2531', 'MEG1811', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG2522', 'MEG0311', 'MEG1243', 'MEG1723', 'MEG0623', 'MEG0613', 'MEG0523', 'MEG0522', 'MEG0813', 'MEG0511'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG2522', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0523', 'MEG0522', 'MEG0813', 'MEG1243', 'MEG1723', 'MEG0511'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG1723', 'MEG0813', 'MEG0523', 'MEG0522', 'MEG0511', 'MEG1243'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG1723', 'MEG0813', 'MEG0523', 'MEG0522', 'MEG0511', 'MEG1243'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0311', 'MEG0623', 'MEG0613', 'MEG0523', 'MEG0522', 'MEG0813', 'MEG1243', 'MEG1723', 'MEG0511'])

bads['fr190151'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511', 'MEG0422'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511', 'MEG0422'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0321', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0813', 'MEG1243', 'MEG0523', 'MEG0522', 'MEG2133', 'MEG0511', 'MEG0422'])

bads['at140305'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0522', 'MEG1721'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0342', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0522', 'MEG1721'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG1721'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG1721'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2512', 'MEG0613', 'MEG0311', 'MEG0623', 'MEG1721'])

bads['cc150418'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2123', 'MEG0311',  'MEG2432', 'MEG0613', 'MEG0623'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2123', 'MEG0311',  'MEG2332', 'MEG0623'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2432', 'MEG0311',  'MEG0623'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG2632', 'MEG0311'])

# Pax 5
bads['eb180237'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0613', 'MEG0623', 'MEG2511', 'MEG1512', 'MEG0311', 'MEG0813', 'MEG0523', 'MEG0522'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0613', 'MEG0623', 'MEG2511', 'MEG1441', 'MEG0311', 'MEG0813', 'MEG0523', 'MEG0522', 'MEG1512'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0613', 'MEG0623', 'MEG2542', 'MEG0311', 'MEG0721', 'MEG2511'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG1243'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723','MEG1933', 'MEG0633', 'MEG0613', 'MEG0623', 'MEG0311',  'MEG0523', 'MEG0522', 'MEG0813'])

# 0131, 0132, 0133
bads['ld190260'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0311', 'MEG0331', 'MEG0633', 'MEG0522'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1441', 'MEG0311', 'MEG0331', 'MEG0633', 'MEG0522'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633','MEG0522', 'MEG0311', 'MEG0331', 'MEG0343', 'MEG0342', 'MEG0131', 'MEG1511', 'MEG0522', 'MEG0813'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633','MEG0311', 'MEG0331', 'MEG0343', 'MEG0342', 'MEG0131', 'MEG1511', 'MEG0522', 'MEG0813'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633','MEG0311', 'MEG2432', 'MEG0331', 'MEG0343', 'MEG0342', 'MEG0131', 'MEG1511', 'MEG0522', 'MEG0813', 'MEG2432'])

bads['ms180425'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG0422', 'MEG2432', 'MEG0311', 'MEG2432', 'MEG0741'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG0422', 'MEG2432', 'MEG0741', 'MEG0311', 'MEG0741'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG0422', 'MEG2432', 'MEG0522', 'MEG0311', 'MEG2432'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG0422', 'MEG2432', 'MEG0311', 'MEG2432'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG0422', 'MEG2432', 'MEG0311', 'MEG2432'])

bads['ch180036'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG0623', 'MEG0311', 'MEG0613'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG0311', 'MEG0613', 'MEG0623'])

bads['cg190026'] = dict(Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0633'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0711', 'MEG0633'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0633'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0633'])

# Pax 10
bads['ih190084'] = dict(Run02=['MEG0213', 'MEG1732', 'MEG1923', 'MEG0633', 'MEG0131', 'MEG1933', 'MEG1722', 'MEG1723', 'MEG0913'],
    Run03=['MEG0213', 'MEG1732', 'MEG1923', 'MEG0633', 'MEG1921', 'MEG1933', 'MEG1722', 'MEG1723', 'MEG0913'],
    Run04=['MEG0213', 'MEG1732', 'MEG1923', 'MEG0633', 'MEG1933', 'MEG1722', 'MEG1723', 'MEG0913'],
    Run05=['MEG0213', 'MEG1732', 'MEG1923', 'MEG0633', 'MEG1933', 'MEG1722', 'MEG1723'],
    Run06=['MEG0213', 'MEG1732', 'MEG1923', 'MEG0633', 'MEG1933', 'MEG1722', 'MEG1723'])

bads['cr170417'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG1721', 'MEG1723', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0341', 'MEG0542', 'MEG0943'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG0341', 'MEG1723', 'MEG0613', 'MEG0623', 'MEG0311', 'MEG0542'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG0613', 'MEG0522', 'MEG0523', 'MEG0542', 'MEG1723', 'MEG0623', 'MEG0311', 'MEG0542'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG0732', 'MEG1723', 'MEG0623', 'MEG0311', 'MEG0613', 'MEG0732', 'MEG0943'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1933', 'MEG0633', 'MEG0732', 'MEG0613', 'MEG0943', 'MEG1723', 'MEG0623', 'MEG0311', 'MEG0943', 'MEG0523', 'MEG0522', 'MEG0732'])

bads['ll180197'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0613', 'MEG0633', 'MEG0311', 'MEG0623', 'MEG1942'])

bads['tr180110 '] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0633'])

bads['lr190095'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0633', 'MEG0623', 'MEG1043', 'MEG1323', 'MEG0311', 'MEG0613',  'MEG2343'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0633', 'MEG0211', 'MEG1043', 'MEG1323', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG2111', 'MEG2343', 'MEG2431'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0633', 'MEG0623', 'MEG1043', 'MEG1323', 'MEG0613', 'MEG0311'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0633', 'MEG0623', 'MEG1043', 'MEG1323', 'MEG0311', 'MEG0613'])

# Pax 15
bads['ep190335'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1833', 'MEG1842', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG0311', 'MEG0613', 'MEG0623', 'MEG0341'])

################

bads['gl180335'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG0541', 'MEG0623', 'MEG0922', 'MEG2341', 'MEG0311', 'MEG1422', 'MEG1423'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG2511', 'MEG2341', 'MEG0922', 'MEG0311', 'MEG1422', 'MEG1423', 'MEG1831'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG0922', 'MEG0311', 'MEG1422', 'MEG1423', 'MEG1831', 'MEG2511'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG0541', 'MEG0311', 'MEG1422', 'MEG1423', 'MEG1831'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG0311', 'MEG1422', 'MEG1423', 'MEG1831', 'MEG2411'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG1412', 'MEG0311', 'MEG1422', 'MEG1423', 'MEG1831'])

bads['ad190325'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633', 'MEG1121'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG1512', 'MEG0613', 'MEG0623', 'MEG0111', 'MEG0311', 'MEG0633'])

bads['ag170045'] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG0311', 'MEG0111', 'MEG2041'],
    Run02=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG0311', 'MEG0111', 'MEG2041'],
    Run03=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG2041', 'MEG0311', 'MEG0111'],
    Run04=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG2041', 'MEG0311', 'MEG0111'],
    Run05=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG0311', 'MEG0111'],
    Run06=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613', 'MEG0633', 'MEG1512', 'MEG1043', 'MEG0311', 'MEG0111'])

bads['ma190185'] = dict(Run01=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132', 'MEG1121'],
    Run02=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132', 'MEG1121'],
    Run03=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132', 'MEG0522', 'MEG1141'],
    Run04=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132'],
    Run05=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132', 'MEG0522', 'MEG1021'],
    Run06=['MEG0213', 'MEG0311', 'MEG1323', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0633', 'MEG2132', 'MEG1011'])

bads['pl170230'] = dict(Run01=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132', 'MEG1523', 'MEG1921'],
    Run02=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132'],
    Run03=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132', 'MEG1741'],
    Run04=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132'],
    Run05=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132', 'MEG1121'],
    Run06=['MEG0213', 'MEG0311', 'MEG1512', 'MEG1513', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0633', 'MEG2132', 'MEG1121', 'MEG1921', 'MEG0522'])



"""
bads[''] = dict(Run01=['MEG0213', 'MEG1732', 'MEG1722', 'MEG1723', 'MEG1933', 'MEG0623', 'MEG0613'],
    Run02=[],
    Run03=[],
    Run04=[],
    Run05=[],
    Run06=[])
"""


###############################################################################
# DEFINE ADDITIONAL CHANNELS
# --------------------------

# for 01-import_and_filter.py

# ``rename_channels`` : dict rename channels
#    Here you name or replace extra channels that were recorded, for instance
#    EOG, ECG.
#
# Example
# ~~~~~~~
# >>> rename_channels = {'EEG061': 'EOG061', 'EEG062': 'EOG062',
#                        'EEG063': 'ECG063'}

rename_channels = None

# ``set_channel_types``: dict
#   Here you defines types of channels to pick later.
#
# Example
# ~~~~~~~
# >>> set_channel_types = {'EEG061': 'eog', 'EEG062': 'eog',
#                          'EEG063': 'ecg', 'EEG064': 'misc'}

set_channel_types = {'EOG061': 'eog', 'EOG062': 'eog', 'ECG063': 'ecg', 
                     'MISC201': 'misc', 'MISC202': 'misc', 'MISC203': 'misc',
                     'MISC204': 'misc', 'MISC205': 'misc', 'MISC206': 'misc',
                     'MISC301': 'misc', 'MISC302': 'misc', 'MISC303': 'misc',
                     'MISC304': 'misc', 'MISC305': 'misc', 'MISC306': 'misc'}

###############################################################################
# FREQUENCY FILTERING
# -------------------
# for 01-import_and_filter.py

# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# It is typically better to set your filtering properties on the raw data so
# as to avoid what we call border effects
#
# If you use this pipeline for evoked responses, a default filtering would be
# a high-pass filter cut-off of l_freq = 1 Hz
# a low-pass filter cut-off of h_freq = 40 Hz
# so you would preserve only the power in the 1Hz to 40 Hz band
#
# If you use this pipeline for time-frequency analysis, a default filtering
# would be a high-pass filter cut-off of l_freq = 1 Hz
# a low-pass filter cut-off of h_freq = 120 Hz
# so you would preserve only the power in the 1Hz to 120 Hz band
#
# If you use are interested in the lowest frequencies, do not use a high-pass
# filter cut-off of l_freq = None
# If you need more fancy analysis, you are already likely past this kind
# of tips! :)

BPfilter = False

# ``l_freq`` : the low-frequency cut-off in the highpass filtering step.
#   Keep it None if no highpass filtering should be applied.

l_freq = None

# ``h_freq`` : the high-frequency cut-off in the lowpass filtering step.
#   Keep it None if no lowpass filtering should be applied.

h_freq = None

notch = False
###############################################################################
# MAXFILTER PARAMETERS
# --------------------
# for 02_apply_maxfilter.py

# Download the ``cross talk`` and ``calibration`` files. 
# (They are on OSF for the example data.)
# Warning: these are site and machine specific files that provide information 
# about the environmental noise.
# For practical purposes, place them in your study folder.
# At NeuroSpin: ct_sparse and sss_call are on the meg_tmp server

# ``cal_files_path``  : str
#   path to the folder where the calibration files are
#   if you placed it right, you don't have to edit this
cal_files_path = os.path.join(study_path, 'system_calibration_files')

# ``mf_ctc_fname``  : str
#    Path to the FIF file with cross-talk correction information. 
mf_ctc_fname = os.path.join(cal_files_path, 'ct_sparse_nsp_2017.fif')

# ``mf_cal_fname``  : str
#   Path to the '.dat' file with fine calibration coefficients. 
mf_cal_fname = os.path.join(cal_files_path, 'sss_cal_nsp_2017.dat')



# ``mf_reference_run``  : integer
#   Which run to take as the reference for adjusting the head position of all
#   runs.

mf_reference_run = 0

# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# Despite all possible care to avoid movements in the MEG, the participant
# will likely slowly drift down from the Dewar or slightly shift the head
# around in the course of the recording session. Hence, to take this into
# account, we are realigning all data to a single position. For this, you need
# to define a reference run (typically the one in the middle of
# the recording session).


# ``mf_head_origin``  : str or array with 3 inputs
#   defines the origin for the head position 
#   if 'auto', position is fitted from the digitized points

mf_head_origin = 'auto'


# ``mf_st_duration `` : if None, no temporal-spatial filtering is applied
# during MaxFilter, otherwise, put a float that speficifies the buffer
# duration in seconds.
# ``mf_st_duration `` : None or float
#   Elekta default = 10s, meaning it acts like a 0.1 Hz highpass filter

mf_st_duration = None

# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# There are two kinds of maxfiltering: sss and tsss
# [sss = signal space separation ; tsss = temporal signal space separation]
# (Taulu et al, 2004): http://cds.cern.ch/record/709081/files/0401166.pdf
# If you are interested in low frequency activity (<0.1Hz), avoid using tsss
# and set mf_st_duration = None
# If you are interested in low frequency above 0.1 Hz, you can use the
# default mf_st_duration = 10 s
# Elekta default = 10s, meaning it acts like a 0.1 Hz highpass filter

mf_st_duration = None # 10 for the noisy data


###############################################################################
# RESAMPLING
# ----------
# for 01-import_and_filter.py
#
# [Good Practice / Advice]
# If you have acquired data with a very high sampling frequency (e.g. 2 kHz)
# you will likely want to downsample to lighten up the size of the files you
# are working with (pragmatics)
# If you are interested in typical analysis ('MEG0213', 'MEG1732', 'MEG1722', 'MEG1512'up to 120 Hz) you can typically
# resample your data down to 500 Hz without preventing reliable time-frequency
# exploration of your data

#
# ``resample_sfreq``  : a float that specifies at which sampling frequency
# the data should be resampled. If None then no resampling will be done.

resample_sfreq = None   # None

# ``decim`` : integer that says how much to decimate data at the epochs level.
# It is typically an alternative to the `resample_sfreq` parameter that
# can be used for resampling raw data. 1 means no decimation.
#   Decimation is applied in 04-make_epochs.py

decim = 1


# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# If you have acquired data with a very high sampling frequency (e.g. 2 kHz)
# you will likely want to downsample to reduce the size of the files you
# are working with (pragmatics)
# Make sure to resample to a frequency that is more than two times 
# the higher cut off of the frequency band you used for the low-pass filter
# (i.e. the Nyquist freuquency)
# If you are interested in typical analysis (up to 120 Hz) you can typically
# resample your data down to 500 Hz without preventing reliable time-frequency
# exploration of your data


###############################################################################
# AUTOMATIC REJECTION OF ARTIFACTS
# --------------------------------
# for 04-make_epochs.py
# 

#  ``reject`` : dict | None
#    The rejection limits to make some epochs as bads.
#    This allows to remove strong transient artifacts.
#    If you want to reject and retrieve blinks later, e.g. with ICA,
#    don't specify a value for the eog channel (see examples below).
#    Make sure to include values for eeg if you have EEG data

#reject = {'grad': 4000e-13, 'mag': 4e-12}

# Note
# ~~~~
# These numbers tend to vary between subjects.. You might want to consider
# using the autoreject method by Jas et al. 2018.
# See https://autoreject.github.io
#
# Examples
# ~~~~~~~~
# >>> reject = {'grad': 4000e-13, 'mag': 4e-12, 'eog': 150e-6}
# >>> reject = {'grad': 4000e-13, 'mag': 4e-12, 'eeg': 200e-6}
# >>> reject = None

"""  reject = dict(grad=4000e-13, # T / m (gradiometers)
                        mag=4e-12, # T (magnetometers)
                        eeg=40e-6, # V (EEG channels)
                        eog=250e-6 # V (EOG channels)
                        ) """

reject = {'grad': 56000e-13, 'mag': 56e-12}
#reject = None
# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# Have a look at your raw data and train yourself to detect a blink, a heart
# beat and an eye movement.
# You can do a quick average of blink data and check what the amplitude looks
# like.

###############################################################################
# EPOCHING
# --------
# for 04-make_epochs.py
#
# ``tmin``: float
#    A float in seconds that gives the start time before event of an epoch.

tmin = -0.5

# ``tmax``: float
#    A float in seconds that gives the end time before event of an epoch.

tmax = 110
# tmax epochs
# EP: 1.45 - 71s; 2.9 - 92s; 5.8 - 122s
# AD: 1.45 - 71s; 2.9 - 92s; 5.8 - 122s

# ``trigger_time_shift`` : float | None
#    If float it specifies the offset for the trigger and the stimulus
#    (in seconds). You need to measure this value for your specific
#    experiment/setup.

#trigger_time_shift = -0.0416
trigger_time_shift = -0.05

# ``baseline`` : tuple
#    It specifies how to baseline the epochs; if None, no baseline is applied.

baseline = (-0.3, -0.1) # (None, 0.)

# ``stim_channel`` : str
#    The name of the stimulus channel, which contains the events.

stim_channel = 'STI101'  # 'STI014'# None

# ``min_event_duration`` : float
#     The minimal duration of the events you want to extract (in seconds).
#     Chose a value that is larger than the expected trigger duration  


min_event_duration = 0.005

#  `event_id`` : dict
#     Dictionary that maps events (trigger/marker values)
#     to conditions.
#     Use the dash to divise sub-conditions, as in the example above.
#     This allows to analyse all 'Auditory' events regardless of left/right. 
#
# Example
# ~~~~~~~
# >>> event_id = {'Auditory/Left': 1, 'Auditory/Right': 2}`
# or
# >>> event_id = {'Onset': 4} with conditions = ['Onset']

#event_id = {'incoherent/1': 33, 'incoherent/2': 35,ih190084
#            'coherent/down': 37, 'coherent/up': 39}
#conditions = ['incoherent', 'coherent']

## For all intervals together
#event_id = {'BPint123': 5}
#conditions = ['BPint123']

## For the 3 different intervals in Play
#event_id = {'BPint01': 1, 'BPint02': 2, 'BPint03':3} # BP-ButtonPress
#conditions = ['BPint01', 'BPint02', 'BPint03']

## For the 3 different intervals in Replay
#event_id = {'BPRint01': 4, 'BPRint02': 5, 'BPRint03':6} # BP-ButtonPress
#conditions = ['BPRint01', 'BPRint02', 'BPRint03']


## PLAY: For all 3 ints, and short-correct-long
#event_id = {'BPint01s': 13, 'BPint01c': 15, 'BPint01l': 17, 
#            'BPint02s': 23, 'BPint02c': 25, 'BPint02l': 27,
#            'BPint03s': 33, 'BPint03c': 35, 'BPint03l': 37}
##event_id = {'BPint01c': 15}
#conditions = ['BPint01s', 'BPint01c', 'BPint01l',
#              'BPint02s', 'BPint02c', 'BPint02l',
#              'BPint03s', 'BPint03c', 'BPint03l']

# REPLAY: For all 3 ints, and short-correct-long
#event_id = {'BPRint01s': 14, 'BPRint01c': 16, 'BPRint01l': 18, 
#            'BPRint02s': 24, 'BPRint02c': 26, 'BPRint02l': 28,
#            'BPRint03s': 34, 'BPRint03c': 36, 'BPRint03l': 38}
##event_id = {'BPint01c': 15}
#conditions = ['BPRint01s', 'BPRint01c', 'BPRint01l',
#              'BPRint02s', 'BPRint02c', 'BPRint02l',
#              'BPRint03s', 'BPRint03c', 'BPRint03l']


#event_id = {'int145': 1}
#conditions = ['int145']
cond = 'int58'
#event_id = {'int29': 2}
#conditions = ['int29']
event_id = {'int58': 3}
conditions = ['int58']


# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# Carefully think about which event/ trigger you want to time-lock to.
# choose a time window that includes the time range needed to test your hypotheses.
# If you plan to apply a time-frequency transformation, chose your window larger
# than what you want to look at, to avoid edge artifacts in the time window of 
# interest.

# Note on the example data
# ~~~~~~~~~~~~~~~~~~~~~~~~
# In the example data, we time-lock to the onset of a coherent movement.
# The actual stimulus onset is 0.5 s before that. 
# Therefore, we take a pre-stimulus baseline= (-.6, -.5). 
# Note that in the NeuroSpin hard ware we have very short ghost triggers,
# lasting ~1 ms. Setting min_event_duration larger than that allows to 
# get rid of them. 


###############################################################################
# ARTIFACT REMOVAL
# ----------------
# 05a-run_ICA.py, 06a-apply_ICA.py // 05b-run_SSP.py, 06b-apply_SSP.py
#
# You can choose between ICA and SSP to remove eye and heart artifacts.
# SSP: https://mne-tools.github.io/stable/auto_tutorials/plot_artifacts_correction_ssp.html?highlight=ssp # noqa
# ICA: https://mne-tools.github.io/stable/auto_tutorials/plot_artifacts_correction_ica.html?highlight=ica # noqa
# if you choose ICA, run scripts 5a and 6a
# if you choose SSP, run scripts 5b and 6b
# if you running both, your cleaned epochs will be the ones cleaned with the
# methods you run last (they overwrite each other)
# Scripts 06a-apply_ICA.py or 06b-apply_SSP.py run an automated rejection
# procedure to detect eye and heart artifacts as described in the examples 
# above. 
#
#

# ICA parameters
# ~~~~~~~~~~~~~~
# ``runica`` : bool
#    If True ICA should be used or not.

runica = True

# ``ica_decim`` : int
#    The decimation parameter to compute ICA. If 5 it means
#    that 1 every 5 sample is used by ICA solver. The higher the faster
#    it is to run but the less data you have to compute a good ICA.

ica_decim = 11


# ``default_reject_comps`` : dict
#   A dictionary that contains ICA components to be rejected from either MEG
#   or EEG data. Use this to add components manually, for instance if they were
#   not found by the automatic rejection procedure, or represent other artifacts
#   than eye / heart activity that you wish to remove. 

#   For example you can use:
#    rejcomps_man['subject01'] = dict(eeg=[12], meg=[7])

def default_reject_comps():
    return dict(meg=[], eeg=[])

rejcomps_man = defaultdict(default_reject_comps)

# ``ica_ctps_ecg_threshold``: float
#    The threshold parameter passed to `find_bads_ecg` method.
#   If you find that artifact components are not rejected, set it lower. 

ica_ctps_ecg_threshold = 0.1

# Good Practice / Advice
# ~~~~~~~~~~~~~~~~~~~~~~
# If you go for ICA, inspect the html report created in the subject's folder
# after running 05a-run_ICA.py, to identify components you would like to be rejected.
# 06a-apply_ICA.py runs an automated rejection
# procedure to detect eye and heart artifacts as described in the examples 
# above and also generates a html report. 

# SSP parameters
# ~~~~~~~~~~~~~~
# XXX
# define parameters for SSP
# give minimal description


###############################################################################
# DECODING
# --------
# 09-sliding_estimator.py
#
# XXX needs more documentation
#
# ``decoding_conditions`` : list
#    List of conditions to be classified.
#
# Example
# ~~~~~~~
#
# >>> decoding_conditions = [('Auditory', 'Visual'), ('Left', 'Right')]

#decoding_conditions = [('incoherent', 'coherent')]
# Play
decoding_conditions = [('BPint01', 'BPint02')]
# Replay
#decoding_conditions = ['BPRint01', 'BPRint02', 'BPRint03']
# Play s-c-l division
#decoding_conditions = ['BPint01s', 'BPint01c', 'BPint01l',
#              'BPint02s', 'BPint02c', 'BPint02l',
#              'BPint03s', 'BPint03c', 'BPint03l']


# ``decoding_metric`` : str
#    The metric to use for cross-validation. It can be 'roc_auc' or 'accuracy'
#    or any metric supported by scikit-learn.

decoding_metric = 'roc_auc'

# ``decoding_n_splits`` : int
#    The number of folds (a.k.a. splits) to use in the cross-validation.

decoding_n_splits = 5

###############################################################################
# TIME-FREQUENCY
# --------------
# 10-time_frequency_conditions.py
#
# ``time_frequency_conditions`` : list
#    The conditions to compute time-frequency decomposition on.

#time_frequency_conditions = ['BPint123']
#time_frequency_conditions = ['BPint01', 'BPint02', 'BPint03']
#time_frequency_conditions = ['BPRint01', 'BPRint02', 'BPRint03']
# Play s-c-l division
time_frequency_conditions = ['BPint01s', 'BPint01c', 'BPint01l',
                             'BPint02s', 'BPint02c', 'BPint02l',
                             'BPint03s', 'BPint03c', 'BPint03l']


# Replay s-c-l
#time_frequency_conditions = ['BPRint01s', 'BPRint01c', 'BPRint01l',
#                             'BPRint02s', 'BPRint02c', 'BPRint02l',
#                             'BPRint03s', 'BPRint03c', 'BPRint03l']


###############################################################################
# SOURCE SPACE PARAMETERS
# -----------------------
#

# ``spacing`` : str
#    The spacing to use. Can be ``'ico#'`` for a recursively subdivided
#    icosahedron, ``'oct#'`` for a recursively subdivided octahedron,
#    ``'all'`` for all points, or an integer to use appoximate
#    distance-based spacing (in mm).

spacing = 'oct6'

# ``mindist`` : float
#    Exclude points closer than this distance (mm) to the bounding surface.

mindist = 5

# ``loose`` : float in [0, 1] | 'auto'
#    Value that weights the source variances of the dipole components
#    that are parallel (tangential) to the cortical surface. If loose
#    is 0 then the solution is computed with fixed orientation,
#    and fixed must be True or "auto".
#    If loose is 1, it corresponds to free orientations.
#    The default value ('auto') is set to 0.2 for surface-oriented source
#    space and set to 1.0 for volumetric, discrete, or mixed source spaces,
#    unless ``fixed is True`` in which case the value 0. is used.

loose = 0.2

# ``depth`` : None | float | dict
#    If float (default 0.8), it acts as the depth weighting exponent (``exp``)
#    to use (must be between 0 and 1). None is equivalent to 0, meaning no
#    depth weighting is performed. Can also be a `dict` containing additional
#    keyword arguments to pass to :func:`mne.forward.compute_depth_prior`
#    (see docstring for details and defaults).

depth = 0.8

# method : "MNE" | "dSPM" | "sLORETA" | "eLORETA"
#    Use minimum norm, dSPM (default), sLORETA, or eLORETA.

method = 'dSPM'

# smooth : int | None
#    Number of iterations for the smoothing of the surface data.
#    If None, smooth is automatically defined to fill the surface
#    with non-zero values. The default is spacing=None.

smooth = 10

# base_fname_trans = '{subject}_' + study_name + '_raw-trans.fif'
base_fname_trans = '{subject}-trans.fif'

#   XXX – do we really have to hard-code this?
fsaverage_vertices = [np.arange(10242), np.arange(10242)]

if not os.path.isdir(study_path):
    os.mkdir(study_path)

if not os.path.isdir(subjects_dir):
    os.mkdir(subjects_dir)

###############################################################################
# ADVANCED
# --------
#
# ``l_trans_bandwidth`` : float | 'auto'
#    A float that specifies the transition bandwidth of the
#    highpass filter. By default it's `'auto'` and uses default mne
#    parameters.

l_trans_bandwidth = 'auto'

#  ``h_trans_bandwidth`` : float | 'auto'
#    A float that specifies the transition bandwidth of the
#    lowpass filter. By default it's `'auto'` and uses default mne
#    parameters.

h_trans_bandwidth = 'auto'

#  ``N_JOBS`` : int
#    An integer that specifies how many subjects you want to run in parallel.

N_JOBS = 1

# ``random_state`` : None | int | np.random.RandomState
#    To specify the random generator state. This allows to have
#    the results more reproducible between machines and systems.
#    Some methods like ICA need random values for initialisation.

random_state = 42

# ``shortest_event`` : int
#    Minimum number of samples an event must last. If the
#    duration is less than this an exception will be raised.

shortest_event = 1

# ``allow_maxshield``  : bool
#    To import data that was recorded with Maxshield on before running
#    maxfilter set this to True.

allow_maxshield = True

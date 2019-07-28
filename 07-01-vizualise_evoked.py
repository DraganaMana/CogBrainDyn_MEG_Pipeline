# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:10:37 2019

@author: Dragana
"""

import os.path as op
import numpy as np
import matplotlib.pyplot as plt
import config
import mne

data_path = 'C:/Users/Dragana/Documents/MEG/MEG_pilot/Test_01/'
fname = op.join(data_path, 'MEG', 's190320', 's190320_ScaledTime_-int123-cleaned_epo-ave.fif')
evoked = mne.read_evokeds(fname, baseline=(None, 0), proj=True)
print(evoked)
##########################
# Pick evoked. In this case there is one condition so one evoked. 
evoked_w_cross = evoked[0]
#==========PLOTS=======
# Plot the evoked
fig = evoked_w_cross.plot(exclude=(), time_unit='s')
# Fansier plot w/ colours
picks = mne.pick_types(evoked_w_cross.info, meg=True, eeg=False, eog=False)
evoked_w_cross.plot(spatial_colors=True, gfp=True, picks=picks, time_unit='s')
#=========TOPOMAPS======
# Plot the topomaps with default times
evoked_w_cross.plot_topomap(times=(-1.5, -0.5, 0, 0.5, 0.75, 1, 1.25), time_unit='s')
# Plot the topomaps with predetermined times
times = np.arange(0.05, 0.151, 0.05)
evoked_w_cross.plot_topomap(times=times, ch_type='mag', time_unit='s')


###
mne.viz.plot_compare_evokeds(evoked, picks=None)
#
evoked_w_cross.plot_joint(title='All intervals, time locked - 1st button press', times=[0, .1, .2, .3, .35, .4, .45, 0.5, 0.75])





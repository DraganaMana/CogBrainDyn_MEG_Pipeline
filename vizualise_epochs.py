# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:10:37 2019

@author: Dragana
"""

import os.path as op
import numpy as np
import matplotlib.pyplot as plt

import mne

data_path = 'C:/Users/Dragana/Documents/MEG/MEG_pilot/Test_01/'
fname = op.join(data_path, 'MEG', 's190320', 's190320_ScaledTime_-ave.fif')
evoked = mne.read_evokeds(fname, baseline=(None, 0), proj=True)
print(evoked)

evoked_l_aud = evoked[0]

fig = evoked_l_aud.plot(exclude=(), time_unit='s')
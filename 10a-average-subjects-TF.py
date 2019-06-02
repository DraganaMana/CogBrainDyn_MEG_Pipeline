#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:02:05 2019

@author: dm258725
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os.path as op

import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, read_tfrs , write_tfrs, AverageTFR
from mne.baseline import rescale
from mne.stats import _bootstrap_ci

from mne.stats import (spatio_temporal_cluster_test, f_threshold_mway_rm,
                       f_mway_rm)
from mne.channels import read_ch_connectivity

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

from functools import partial
import config
#%% get nips
subjects_list = ['hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237'] 
nips = subjects_list # ['hm_070076','cc_150418']
print(nips)

conditions = config.time_frequency_conditions

ch_type = 'mag' # mag/grad/eeg


tmin = config.tmin
tmax = config.tmax

    
# load TFS  
for pp, nip in enumerate(nips):
    print(nip) 
    
    for c,condition in enumerate(conditions):
         
        meg_subject_dir = op.join(config.meg_dir, nip)
        
        # Calculate the TFs w/o a baseline
        power = mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
                                                     % (config.study_name, nip,
                                                        condition.replace(op.sep, ''))))

        power = power.pop()
        power.apply_baseline(mode='percent',baseline=(-0.3,-0.1))
            
        power = power.crop(tmin=tmin,tmax=tmax)    
       
        
        if ch_type == 'mag':
            power.pick_types(meg='mag')
        elif ch_type == 'grad':
            power.pick_types(meg='grad')
        elif ch_type == 'eeg':
            power.pick_types(eeg=True,meg = False)
        
        
        # plot single subject
#        power.plot_topo(baseline=None) # , vmin = -50,vmax = 50
     
        # initiate matrices on first need
        if pp == 0 and c == 0:
            POW = np.zeros((len(nips), len(conditions), len(power.ch_names), len(power.freqs),len(power.times)))         
            ITC = np.zeros((len(nips), len(conditions), len(power.ch_names), len(power.freqs),len(power.times)))         
           
        POW[pp,c]=power.data

        
        itc =  mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_itc_%s-tfr.h5'
                                                    % (config.study_name, nip,
                                                       condition.replace(op.sep, ''))))
        itc = itc.pop()
        itc = itc.crop(tmin=tmin,tmax=tmax)
        
        if ch_type == 'mag':
           itc.pick_types(meg='mag')
        elif ch_type == 'grad':
            itc.pick_types(meg='grad')
        elif ch_type == 'eeg':
            itc.pick_types(eeg=True,meg = False)
        
        ITC[pp,c]=itc.data

    if pp == 0:
        pow_dummy = power
        itc_dummy = itc
        
        #%% compute condition differences per FP and visualize    
         
plot_tmin = tmin
plot_tmax = tmax  
subj = 'subj1-'+ str(len(subjects_list))       
            
for c, condition in enumerate(conditions):          
    # loop over FP
   
#        c = 3
#        condition = conditions[c]
#         
    P = np.mean(POW[:,c], 0) # avg over sbs
    AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
      
#    AVGPOW.plot_topo(baseline=None, tmin = plot_tmin, tmax = plot_tmax,
#                title=('POW ' + condition )) # vmin = -50,vmax = 50
    AVGPOW.plot_joint(baseline=None, tmin=-0.5, tmax=1.25, vmin = -1.2, vmax = 1.2,
                             timefreqs=[(.15, 10), (0.6, 20)], title=('POW '+ ch_type + ' ' + condition))
    
    plt.savefig('%s_%s_%s_%s_%s.png' %(config.study_name, subj, 
                                       condition, 'averageTF', ch_type))
 

# Choose either the first or the second
#POW_P = POW
#POW_R = POW
    
# plot condition difference
P = np.mean(POW_P[:,2] - (POW_R[:,2]), 0) # avg over sbs
AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
      
#AVGPOW.plot_topo(baseline=None, tmin = plot_tmin, tmax = plot_tmax,
#                title=('POW ' + 'difference' ),
#                vmin = -.30,vmax = .30) # , axes=axis[c]
AVGPOW.plot_joint(baseline=None, tmin=-0.5, tmax=1.25,
                             timefreqs=[(.15, 10), (0.6, 20)], title=('POW diff Pint3-Rint3'))
    
plt.savefig('%s_%s_%s_%s.png' %(config.study_name, subj, 'diff_P3-R3', ch_type))
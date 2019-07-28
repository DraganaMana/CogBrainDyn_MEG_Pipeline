#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:02:05 2019

@author: dm258725
"""


import numpy as np
from numpy import append
import matplotlib.pyplot as plt
import os.path as op

import mne

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

import config
#% get nips
subjects_list = config.subjects_list
nips = subjects_list # ['hm_070076','cc_150418']
print(nips)

conditions = config.time_frequency_conditions

ch_type = 'grad' # mag/grad/eeg


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
            power.pick_types(eeg=True, meg = False)
        
        
        # plot single subject
#        power.plot_topo(baseline=None) # , vmin = -50,vmax = 50
     
        # initiate matrices on first need
        if pp == 0 and c == 0:
            POW = np.zeros((len(nips), len(conditions), len(power.ch_names), len(power.freqs),len(power.times)))         
            ITC = np.zeros((len(nips), len(conditions), len(power.ch_names), len(power.freqs),len(power.times)))         
           
        POW[pp,c]=power.data

################################# ITC
#        itc =  mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_itc_%s-tfr.h5'
#                                                    % (config.study_name, nip,
#                                                       condition.replace(op.sep, ''))))
#        itc = itc.pop()
#        itc = itc.crop(tmin=tmin,tmax=tmax)
        
#        if ch_type == 'mag':
#           itc.pick_types(meg='mag')
#        elif ch_type == 'grad':
#            itc.pick_types(meg='grad')
#        elif ch_type == 'eeg':
#            itc.pick_types(eeg=True,meg = False)
#        
#        ITC[pp,c]=itc.data
#################################
    if pp == 0:
        pow_dummy = power
#        itc_dummy = itc
        
#%% 1. Compute condition averages per channel type and visualize    
         
plot_tmin = tmin
plot_tmax = tmax  
subj = 'subj1-'+ str(len(subjects_list))  
topomap_args = dict(vmin=-1.8, vmax=1.8) # fix the colormap values
vvmin = -0.9 # -1.2 for mag and 1.2
vvmax = 0.9           

for c, condition in enumerate(conditions):          
#        c = 3
#        condition = conditions[c]
    P = np.mean(POW[:,c], 0) # avg over sbs
    AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info, P ,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
    
#    AVGPOW.save(op.join(config.study_path, '%s_%s_%s_AVGpower_%s-tfr.h5'
#                    % (config.study_name, 'all-subj', ch_type,
#                       condition.replace(op.sep, ''))), overwrite=True)  
    
    AVGPOW.plot(baseline=None, tmin=-0.5, tmax=1., vmin = vvmin, vmax = vvmax,
                             title=('POW '+ ch_type + ' ' + condition))
#    fig = plt.figure()
#    fig.set_figheight(3)
#    fig.set_figwidth(4)
    
    AVGPOW.plot_topomap(baseline=None, tmin=0.5, tmax=1., fmin=15, fmax=40,
#                              vmin = vvmin, vmax = vvmax, 
                              colorbar=True,
                              title=('Beta power (15-40Hz) of gradiometers (fT/cm), t=0.5-1sec'))
    
#    AVGPOW.plot_joint(baseline=None, tmin=-0.5, tmax=1., 
#                              topomap_args=topomap_args, 
#                              vmin = vvmin, vmax = vvmax, 
#                              timefreqs=[(.15, 10), (0.6, 20)], 
#                              title=('POW '+ ch_type + ' ' + condition))
#    plt.savefig('%s_%s_%s_%s_%s.png' %(config.study_name, subj, condition, 'averageTF_1sec', ch_type),
#                dpi=96)
 
    
#%% 2. Compute condition average differences per channel type and visualize    

# Choose either the first or the second
POW_P = POW
#POW_R = POW

# cond1 - cond2
cond1 = 3
cond2 = 1
    
# Plot condition difference
P = np.mean(POW_P[:,(cond1-1)] - (POW_P[:,(cond2-1)]), 0) # avg over sbs
AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info, P ,pow_dummy.times,pow_dummy.freqs,nave=len(nips))    
#AVGPOW.plot_topo(baseline=None, tmin = plot_tmin, tmax = plot_tmax,
#                title=('POW ' + 'difference' ),
#                vmin = -.30,vmax = .30) # , axes=axis[c]
AVGPOW.plot_joint(baseline=None, tmin=-0.5, tmax=1.25,
                             timefreqs=[(.15, 10), (0.6, 20)], 
                             title=('POW '+ ch_type +' diff Pint' 
                                        + str(cond1) + ' - Pint' + str(cond2)))
    
plt.savefig('%s_%s_%s_%s.png' %(config.study_name, subj, ('diff_P' + str(cond1) + '-P' + str(cond2)), 
                                ch_type))

#%% Compute average beta power 0.5-1 sec for all pax together

# idk if this is correct, because there are negative values and they cancel each other
# check how to make them mean but w/ absolute values

pow_beta = []
pow_beta_sd = []
for c, cond in enumerate(conditions):
    P = np.mean(POW[:,c], 0) # avg over sbs
    AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info, P ,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
    AVGPOW = AVGPOW.crop(0.5,1)
    AVGPOW1 = AVGPOW.data  
    
    AVGPOW_beta = np.zeros((len(AVGPOW1[:,0,0]), 28, 251))
# also I need to check which are the significant channels from the clusters, and
    # only pick them like I picked the freq and times
    for i, chan in enumerate(AVGPOW1[:,0,0]):
        for k, time in enumerate(AVGPOW1[i,0,:]):
            m=0
            for j, freq in enumerate(AVGPOW1[i,:,k]):
                if j > 9 and j <= 37: # j<=37
                    AVGPOW_beta[i,m,k] = freq
                    m += 1

            
    pow_beta.append(np.mean(AVGPOW_beta)) # average over times and frequencies and channels 
    pow_beta_sd.append(np.std(AVGPOW_beta, axis=(0,1,2)))
    
ints = ['1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
plt.plot(ints, pow_beta, 'bo-')
#plt.errorbar(ints, pow_beta, yerr=pow_beta_sd, linestyle='None', marker='^')

# Check
#count = 0
#if AVGPOW_beta.any() != 0:
#    count = count+1
    
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 16:57:42 2019

@author: Dragana
"""

import numpy as np
from numpy import append
import matplotlib.pyplot as plt
import os.path as op

import mne

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from warnings import warn


import config
#% get nips
subjects_list = config.subjects_list
nips = subjects_list # ['hm_070076','cc_150418']
print(nips)

conditions = config.time_frequency_conditions

ch_type = 'grad' # mag/grad/eeg


tmin = config.tmin
tmax = config.tmax

 
pow_beta = []
pow_beta_sd = []
# power_beta = (channels, frequencies, time points) 251 time points is between 0.5 and 1sec
if ch_type == 'mag':
    power_beta = np.zeros((102, 28, 251))
elif ch_type == 'grad':
    power_beta = np.zeros((204, 28, 251))
    
    
#%%
import pandas as pd
import numpy as np

# Build the df which need to be filled in iteratively
subjects= ('hm070076', 'fr190151', 'at140305', 'cc150418', 'eb180237',
           'ld190260', 'ms180425', 'ch180036', 'cg190026', 'ih190084', 
           'cr170417', 'll180197', 'tr180110', 'lr190095', 'ep190335', 
           'gl180335', 'ad190335', 'ag170045', 'pl170230', 'ma190185')
   

time_frequency_conditions = ['BPRint01s', 'BPRint01c', 'BPRint01l',
                             'BPRint02s', 'BPRint02c', 'BPRint02l',
                             'BPRint03s', 'BPRint03c', 'BPRint03l']

TF_epochs = ['TF1', 'TF2', 'TF3', 'TF4', 'TF5', 'TF6', 'TF7', 'TF8', 'TF9', 'TF10',
             'TF11', 'TF12', 'TF13', 'TF14', 'TF15', 'TF16', 'TF17', 'TF18', 'TF19', 'TF20',
             'TF21', 'TF22', 'TF23', 'TF24', 'TF25', 'TF26', 'TF27', 'TF28', 'TF29', 'TF30']

# Create the strings with the names of the columns
cols = []
for cond in time_frequency_conditions:
    for TF_epo in TF_epochs:
        print(cond+'_'+TF_epo)
        cols.append(cond+'_'+TF_epo)
        
df_pow = pd.DataFrame(np.nan, index=subjects, columns=cols)

#%% 


for c,condition in enumerate(conditions):
    print(condition)
    for pp, nip in enumerate(nips):
        print(nip)
         
        meg_subject_dir = op.join(config.meg_dir, nip)
        
        # Itarate through the single TFs in a condition
        for i in range(1,31): 
            # Calculate the TFs w/o a baseline
            
           TF_filename = op.join(meg_subject_dir, '%s_%s_power_%s_epoch-TF%s-tfr.h5'
                                                     % (config.study_name, nip,
                                                        condition.replace(op.sep, ''), str(i)))            
           if not op.exists(TF_filename):
               warn('TF %s not found for subject %s ' % (TF_filename, nip))
               continue
            
           power = mne.time_frequency.read_tfrs(TF_filename)
           
           power = power.pop()
           power.apply_baseline(mode='percent',baseline=(-0.3,-0.1))
            
           power = power.crop(tmin=tmin,tmax=tmax) 
        
           if ch_type == 'mag':
               power.pick_types(meg='mag')
           elif ch_type == 'grad':
               power.pick_types(meg='grad')
           elif ch_type == 'eeg':
               power.pick_types(eeg=True, meg = False)
            
#        picks = mne.pick_channels(raw.info["ch_names"], ["C3", "Cz", "C4"])
            
#        itc =  mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_itc_%s-tfr.h5'
#                                                    % (config.study_name, nip,
#                                                       condition.replace(op.sep, ''))))
#        itc = itc.pop()
#        itc = itc.crop(tmin=tmin,tmax=tmax)
#        
#        if ch_type == 'mag':
#           itc.pick_types(meg='mag')
#        elif ch_type == 'grad':
#            itc.pick_types(meg='grad')
#        elif ch_type == 'eeg':
#            itc.pick_types(eeg=True,meg = False)
            
        ##################
           power1 = power.crop(0.5,1)
           power1 = power1.data
                # also I need to check which are the significant channels from the clusters, and
                # only pick them like I picked the freq and times
           for i, channels in enumerate(power1[:,0,0]):
               for k, time in enumerate(power1[i,0,:]):
                   m=0
                   for j, freq in enumerate(power1[i,:,k]):
                       if j > 10 and j <= 37: # j<=37 10 --> 13Hz; 37 --> 40 Hz
                           power_beta[i,m,k] = freq
                           m += 1
                            
#           # In this case, I need to append it to a matrix/df that knows which condition and pax we are talking about
#           pow_beta.append(np.mean(power_beta)) # average over times and frequencies and channels 
#           pow_beta_sd.append(np.std(power_beta))
                           
           mean_pow_beta = np.mean(power_beta)
           
           row_name = condition + '_TF' + i
           df_pow.loc[nip, condition] = mean_pow_beta

            
           
           
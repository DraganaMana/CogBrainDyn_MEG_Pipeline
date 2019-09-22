# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 12:17:05 2019

@author: Dragana
"""
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
cols = []
for cond in time_frequency_conditions:
    for TF_epo in TF_epochs:
        print(cond+'_'+TF_epo)
        cols.append(cond+'_'+TF_epo)
        
df_pow = pd.DataFrame(np.nan, index=subjects, columns=cols)


cond = 'BPRint01s_TF1'
subj = 'hm070076'
df_pow.loc[subj, cond] = 10
        


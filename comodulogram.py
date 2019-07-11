# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:14:05 2019

@author: DM258725
"""

import os.path as op
from itertools import chain
import mne
from mne.parallel import parallel_func
from mne.minimum_norm import apply_inverse_epochs, read_inverse_operator

import config
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram

snr = 1.0  # use lower SNR for single epochs
lambda2 = 1.0 / snr ** 2
method='dSPM'

labels = mne.read_labels_from_annot('fsaverage','HCPMMP1_combined', 'lh', subjects_dir=config.subjects_dir)
aud_label=[label for label in labels if label.name == 'Early Auditory Cortex-lh'][0]
vis_label=[label for label in labels if label.name == 'MT+ Complex and Neighboring Visual Areas-lh'][0]
#aud_label=[label for label in labels if label.name == 'L_LBelt_ROI-lh'][0]

roi = [aud_label,vis_label]
cfc_method='duprelatour'
cfc_method='tort'
cfc_method='canolty'

conditions = ['PAa','TAa']
aud_label_ts_a=[]
for condition in conditions:  
    print("processing condition: %s"%condition)
    for sub,subject  in enumerate(config.subjects_list_source):    
        print("Processing subject: %s" % subject)
        meg_subject_dir = op.join(config.meg_dir, subject)
        extension = 'cleaned-epo'
        fname_in = op.join(meg_subject_dir,config.analysis,
                        config.base_fname.format(**locals()))
        epochs = mne.read_epochs(fname_in, preload=True)
        epochs.subtract_evoked()
        extension='oct6-inv'
        fname_inv = op.join(meg_subject_dir,config.analysis,config.base_fname.format(**locals()))
        inverse_operator = read_inverse_operator(fname_inv)
        
        src = inverse_operator['src']
        
        stcs = apply_inverse_epochs(epochs[condition], inverse_operator, lambda2, method,
                                        pick_ori="normal", return_generator=False)
        
        this_aud_label_ts = mne.extract_label_time_course(stcs, aud_label, src, mode='max', 
                                            return_generator=False)
    
        aud_label_ts_a.append(np.concatenate(this_aud_label_ts,1))
        
        estimator = Comodulogram(fs=500,high_fq_range=np.linspace(30,120,80),
                                    low_fq_range=np.linspace(1, 7, 20), low_fq_width=2.,
                                    method=cfc_method, progress_bar=True)
t=aud_label_ts_a.pop()
estimator.fit(t)
estimator.plot()


del this_aud_label_ts


conditions = ['PAb','TAb']
aud_label_ts_b=[]
for condition in conditions:  
    print("processing condition: %s"%condition)
    for sub,subject  in enumerate(config.subjects_list_source):    
        print("Processing subject: %s" % subject)
        meg_subject_dir = op.join(config.meg_dir, subject)
        extension = 'cleaned-epo'
        fname_in = op.join(meg_subject_dir,config.analysis,
                        config.base_fname.format(**locals()))
        epochs = mne.read_epochs(fname_in, preload=True)
        epochs.subtract_evoked()
        extension='oct6-inv'
        fname_inv = op.join(meg_subject_dir,config.analysis,config.base_fname.format(**locals()))
        inverse_operator = read_inverse_operator(fname_inv)
        
        src = inverse_operator['src']
        
        stcs = apply_inverse_epochs(epochs[condition], inverse_operator, lambda2, method,
                                        pick_ori="normal", return_generator=False)
        
        this_aud_label_ts = mne.extract_label_time_course(stcs, aud_label, src, mode='max',
                                            return_generator=False)
        # vis_label_ts = mne.extract_label_time_course(stcs, vis_label, src, mode='mean_flip',
        #                                 return_generator=False)
        
        # select the channels (phase_channel, amplitude_channel)
        #ixs = (8, 10)
        
        # create the input array for Comodulogram.fit
        #low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=config.tmin,
        #                                      tmax=config.tmax)
        # create the instance of Comodulogram
        aud_label_ts_b.append(this_aud_label_ts.pop())
        estimator = Comodulogram(fs=500,high_fq_range=np.linspace(20,120,80),
                                    low_fq_range=np.linspace(1, 4, 20), low_fq_width=2 .,
                                    method=cfc_method, progress_bar=True)
# compute the comodulogram

estimator.fit(aud_label_ts_b.pop())
#  
##
#p_value=0.001
#estimator.plot(contour_method='comod_max', contour_level=p_value,
#               titles=['With a p-value on the distribution of maxima'])
del this_aud_label_ts

conditions = ['PAc','TAc']
aud_label_ts_c=[]
for condition in conditions:  
    print("processing condition: %s"%condition)
    for sub,subject  in enumerate(config.subjects_list_source):    
        print("Processing subject: %s" % subject)
        meg_subject_dir = op.join(config.meg_dir, subject)
        extension = 'cleaned-epo'
        fname_in = op.join(meg_subject_dir,config.analysis,
                        config.base_fname.format(**locals()))
        epochs = mne.read_epochs(fname_in, preload=True)
        epochs.subtract_evoked()
        extension='oct6-inv'
        fname_inv = op.join(meg_subject_dir,config.analysis,config.base_fname.format(**locals()))
        inverse_operator = read_inverse_operator(fname_inv)
        
        src = inverse_operator['src']
        
        stcs = apply_inverse_epochs(epochs[condition], inverse_operator, lambda2, method,
                                        pick_ori="normal", return_generator=False)
        
        this_aud_label_ts = mne.extract_label_time_course(stcs, aud_label, src, mode='max',
                                            return_generator=False)
        # vis_label_ts = mne.extract_label_time_course(stcs, vis_label, src, mode='mean_flip',
        #                                 return_generator=False)
        
        # select the channels (phase_channel, amplitude_channel)
        #ixs = (8, 10)
        
        # create the input array for Comodulogram.fit
        #low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=config.tmin,
        #                                      tmax=config.tmax)
        # create the instance of Comodulogram
        aud_label_ts_c.append(this_aud_label_ts.pop())
        estimator = Comodulogram(fs=500,high_fq_range=np.linspace(20,120,80),
                                    low_fq_range=np.linspace(4, 7, 20), low_fq_width=2.,
                                    method=cfc_method, progress_bar=True,n_surrogates=100)
# compute the comodulogram

#estimator.fit(np.concatenate(aud_label_ts_v1,1))
  
#estimator.plot()
#
#p_value=0.001
#estimator.plot(contour_method='comod_max', contour_level=p_value,
#               titles=['With a p-value on the distribution of maxima'])
del this_aud_label_ts

conditions = ['PAd','TAd']
aud_label_ts_d=[]
for condition in conditions:  
    print("processing condition: %s"%condition)
    for sub,subject  in enumerate(config.subjects_list_source):    
        print("Processing subject: %s" % subject)
        meg_subject_dir = op.join(config.meg_dir, subject)
        extension = 'cleaned-epo'
        fname_in = op.join(meg_subject_dir,config.analysis,
                        config.base_fname.format(**locals()))
        epochs = mne.read_epochs(fname_in, preload=True)
        epochs.subtract_evoked()
        extension='oct6-inv'
        fname_inv = op.join(meg_subject_dir,config.analysis,config.base_fname.format(**locals()))
        inverse_operator = read_inverse_operator(fname_inv)
        
        src = inverse_operator['src']
        
        stcs = apply_inverse_epochs(epochs[condition], inverse_operator, lambda2, method,
                                        pick_ori="normal", return_generator=False)
        
        this_aud_label_ts = mne.extract_label_time_course(stcs, aud_label, src, mode='max',
                                            return_generator=False)
        # vis_label_ts = mne.extract_label_time_course(stcs, vis_label, src, mode='mean_flip',
        #                                 return_generator=False)
        
        # select the channels (phase_channel, amplitude_channel)
        #ixs = (8, 10)
        
        # create the input array for Comodulogram.fit
        #low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=config.tmin,
        #                                      tmax=config.tmax)
        # create the instance of Comodulogram
        aud_label_ts_d.append(this_aud_label_ts.pop())
        estimator = Comodulogram(fs=500,high_fq_range=np.linspace(20,120,80),
                                    low_fq_range=np.linspace(4, 7, 20), low_fq_width=2.,
                                    method=cfc_method, progress_bar=True,n_surrogates=100)

estimator.fit(np.concatenate(aud_label_ts_a,1))
#  
##estimator.plot()
##
p_value=0.001
estimator.plot(contour_method='comod_max', contour_level=p_value,
               titles=['With a p-value on the distribution of maxima'])



#%%
import os.path as op
from itertools import chain
import mne
from mne.parallel import parallel_func
from mne.minimum_norm import apply_inverse_epochs, read_inverse_operator

import config
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram

snr = 1.0  # use lower SNR for single epochs
lambda2 = 1.0 / snr ** 2
method='dSPM'

labels = mne.read_labels_from_annot('fsaverage','HCPMMP1_combined', 'lh', subjects_dir=config.subjects_dir)
aud_label=[label for label in labels if label.name == 'Early Auditory Cortex-lh'][0]
vis_label=[label for label in labels if label.name == 'MT+ Complex and Neighboring Visual Areas-lh'][0]
#aud_label=[label for label in labels if label.name == 'L_LBelt_ROI-lh'][0]

roi = [aud_label,vis_label]
cfc_method='duprelatour'
cfc_method='tort'
cfc_method='canolty'

conditions = ['PAa','TAa']
aud_label_ts_a=[]

for condition in config.conditions:  
    print("processing condition: %s"%condition)
    aud_label_ts_a=[]

    for sub,subject  in enumerate(config.subjects_list_source):    
        print("Processing subject: %s" % subject)
        meg_subject_dir = op.join(config.meg_dir, subject)
        extension = 'cleaned-epo'
        fname_in = op.join(meg_subject_dir,config.analysis,
                        config.base_fname.format(**locals()))
        epochs = mne.read_epochs(fname_in, preload=True)
        epochs.subtract_evoked()
        extension='oct6-inv'
        fname_inv = op.join(meg_subject_dir,config.analysis,config.base_fname.format(**locals()))
        inverse_operator = read_inverse_operator(fname_inv)
        
        src = inverse_operator['src']
        
        stcs = apply_inverse_epochs(epochs[condition], inverse_operator, lambda2, method,
                                        pick_ori="normal", return_generator=False)
        
        this_aud_label_ts = mne.extract_label_time_course(stcs, aud_label, src, mode='max', 
                                            return_generator=False)
    
        aud_label_ts_a.append(np.concatenate(this_aud_label_ts,1))
        
        estimator = Comodulogram(fs=500,high_fq_range=np.linspace(30,80,80),
                                    low_fq_range=np.linspace(1, 7, 20), low_fq_width=2.,
                                    method=cfc_method, progress_bar=True)
    t=np.concatenate(aud_label_ts_a,1)

    np.save(op.join(config.meg_dir,'n14',config.analysis,'CFC', '%s_%sdSPM_%s-%s_-cfc'
                    % ('n14',config.study_name,aud_label.name,
                        condition.replace(op.sep, ''))), t)
    del aud_label_ts_a
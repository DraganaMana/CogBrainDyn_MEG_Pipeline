import os.path as op

import mne
from mne.stats.regression import linear_regression
from mne.viz import plot_evoked_topo, plot_topomap, plot_compare_evokeds

import config
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mne.time_frequency import read_tfrs, read_csd


import matplotlib.style
import matplotlib as mpl

from mne.stats import spatio_temporal_cluster_1samp_test 
import statsmodels.formula.api as smf
from scipy import stats
from mne.stats import fdr_correction
from mne.channels import read_ch_connectivity
from mne.channels import find_layout, find_ch_connectivity
from mne.viz import plot_topomap
from functools import partial

from mne.channels import read_ch_connectivity
connectivity, ch_names = read_ch_connectivity('neuromag306mag') #  neuromag306planar


subject = config.subjects_list[0] #take the first subject
meg_subject_dir = op.join(config.meg_dir, subject)
extension = '-ave'
fname_in = op.join(meg_subject_dir,config.analysis,
                            config.base_fname.format(**locals()))
evokeds = mne.read_evokeds(fname_in)
dum_evo = evokeds[0]
times = len(dum_evo.times)
n_channels = len(mne.pick_types(dum_evo.info, 'mag'))

bands = {'theta':(4,7),'alpha':(8,12),
        'beta1':(12,20),'beta2':(20,30),
        'gamma':(30,60),'hgamma':(60,120)}

conditions = ['PAa']

power=[list() for _ in range(len(conditions))]
itc=[list() for _ in range(len(conditions))]
all_freq=np.zeros((len(bands),len(config.subjects_list),n_channels,times))
this_freq=np.zeros((len(config.subjects_list),n_channels,times))

p_threshold = 0.01
n_samples = len(config.subjects_list)-len(config.exclude_subjects) # *len(conditions)
threshold = - stats.distributions.t.ppf(p_threshold / 2., n_samples - 1)
threshold_tfce = dict(start=0., step = 0.2)
p_accept = .01# 0.15
n_perm = 1000

sigma = 1e-3

stat_fun_hat = partial(mne.stats.ttest_1samp_no_p, sigma = sigma)

for con,condition in enumerate(conditions):
        print("processing condition: %s" % condition)
        for z,(band,freq) in enumerate(bands.items()):
                print("processing band: %s" % band)      
                for i,subject in enumerate(config.subjects_list):
                        print("processing subject: %s" % subject) 
                        meg_subject_dir = op.join(config.meg_dir, subject)
                        fname_in=op.join(config.meg_dir,subject,config.analysis)
                        extension = '-tfr'
                        power[con] = read_tfrs(
                                op.join(meg_subject_dir,config.analysis, '%s_%s_power_%s-tfr.h5'
                                        % (config.study_name, subject, 
                                        condition.replace(op.sep, ''))))
                # itc[con] = read_tfrs(
                #         op.join(meg_subject_dir,config.analysis, '%s_%s_itc_%s-tfr.h5'
                #                 % (config.study_name, subject, 
                #                 condition.replace(op.sep, ''))))
                             
                        this_freq[i,:,:]=power[con][0].data[204::,freq[0]:freq[1],:].mean(axis=1)
                all_freq[z,:,:,:]=this_freq[:,:,:]

#transpose the dimensions according to spatiotemporal stat function
all_freq = np.transpose(all_freq, (0,1,3,2)) 


cluster_stats  = spatio_temporal_cluster_1samp_test(
        all_freq[0,:,:,:], connectivity=connectivity,stat_fun=stat_fun_hat, threshold=threshold,
        n_permutations=n_perm, buffer_size=None, out_type='indices') 

T_obs, clusters, p_values, H0 = cluster_stats
good_cluster_inds = np.where(p_values < p_accept)[0]
print('found ' + str(len(good_cluster_inds)) + ' significant clusters')

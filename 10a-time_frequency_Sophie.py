#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:31:08 2018

@author: sh252228
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
#%% import from config file
import config


#%% get nips
subjects_list = ['hm_070076','cc_150418','sf_180213','eb_180237','og_170145',
                'ga_180461','fr_190151','tr_180110','ld_190260','cg_190026']

nips = subjects_list # ['hm_070076','cc_150418']
print(nips)

#oneP = [6] #range(11,len(nips)) # [3]
#nips = [nips[pp] for pp in oneP]
#print(nips) 
# nips = nips[14:19]
#%% get parameters from config file
#epochs = mne.read_epochs(fname_in)
#EpochInfo = epochs.info
#tasks = EpochInfo['task_names']
conditions = ['1_interval','3_intervals']
cond_colors = ['b','g']

#%% LOAD ALL EPOCHS

#run_tf = 0 # run it or load saved 


ch_type = 'mag' # mag/grad/eeg


tmin = -.1
tmax = 4.2

    
# load TFS  
for pp, nip in enumerate(nips):
    print(nip) 
    
    for c,condition in enumerate(conditions):
        cond_name = condition.replace("/","_")
         
        meg_subject_dir = op.join(config.meg_dir, nip)
        
        power = mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
                                                     % (config.study_name, nip,
                                                        condition.replace(op.sep, ''))))

        power = power.pop()
        power.apply_baseline(mode='percent',baseline=(-0.1,0))
            
        power = power.crop(tmin=tmin,tmax=tmax)    
       
        
        if ch_type == 'mag':
            power.pick_types(meg='mag')
        elif ch_type == 'grad':
            power.pick_types(meg='grad')
        elif ch_type == 'eeg':
            power.pick_types(eeg=True,meg = False)
        
        
        # plot single subject
        power.plot_topo(baseline=None) # , vmin = -50,vmax = 50
     
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
            
for c, condition in enumerate(conditions):          
    # loop over FP
   
#        c = 3
#        condition = conditions[c]
#         
    P = np.mean(POW[:,c], 0) # avg over sbs
    AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
      
    AVGPOW.plot_topo(baseline=None, tmin = plot_tmin, tmax = plot_tmax,
                title=('POW ' + condition ),
                ) # vmin = -50,vmax = 50
 

# plot condition difference
P = np.mean(POW[:,1] - (POW[:,0]), 0) # avg over sbs
AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
      
AVGPOW.plot_topo(baseline=None, tmin = plot_tmin, tmax = plot_tmax,
                title=('POW ' + 'difference' ),
                vmin = -.30,vmax = .30) # , axes=axis[c]


#%%    visualize condition differences at selected frequency bands

plot_tmin = 1.
plot_tmax = 1.5 

vmax_pow = .1
vmin_pow = -vmax_pow
vmax_itc = .02
vmin_itc = -vmax_itc

fmin = 15
fmax = 30

P = np.mean(POW[:,1] - (POW[:,0]), 0) # avg over sbs
AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
AVGPOW.plot_topomap(ch_type=ch_type, tmin=plot_tmin, tmax=plot_tmax, fmin=fmin, fmax=fmax,
               baseline=None,
               title=('POW difference:' + str(fmin) + '-'+ str(fmax) + ' Hz '
                      + str(plot_tmin) + '-' + str(plot_tmax) + ' s'),  
               show=False, vmin = vmin_pow, vmax = vmax_pow)


#%% plot per COND and FP, at 1 selected channel
    
mne.viz.plot_sensors(pow_dummy.info,ch_type='mag')
plotchan = pow_dummy.ch_names.index('MEG2241')      # MEG1632    EEG012      
plot_tmin = tmin
plot_tmax = tmax   

for c, condition in enumerate(conditions):          
    # loop over FP
   
#        c = 3
#        condition = conditions[c]
#         
    P = np.mean(POW[:,c], 0) # avg over sbs
    AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
      
    AVGPOW.plot([plotchan], baseline=None, tmin = plot_tmin, tmax = plot_tmax,
                title=('POW ' + condition + AVGPOW.ch_names[plotchan])) # , axes=axis[c]
    
     
P = np.mean(POW[:,1] - (POW[:,0]), 0) # avg over sbs
AVGPOW = mne.time_frequency.AverageTFR(pow_dummy.info,P,pow_dummy.times,pow_dummy.freqs,nave=len(nips))
       
AVGPOW.plot([plotchan], baseline=None, tmin = plot_tmin, tmax = plot_tmax,
                title=('POW ' + 'difference' + AVGPOW.ch_names[plotchan])) # , axes=axis[c]
#%% CLUSTER T-TESTS between single conditions
            
# POW or ITC ? 
testwhat = 'pow'
do_tfce = 0
# conds are pitch_np, pitch_p,time_np,time_p

tmin_test = -.5
tmax_test = 0.

# need to avg over freqs
# test_freqs = [15,20]
# test_freqs = [20,25]
test_freqs = [4,7]

diffname = 'pitch_p-np'
test_conds = [1, 0]

#diffname = 'pitch_p-pitch_np'
#test_conds = [1, 0]

#diffname = 'pitch_np-pitch_p'
#test_conds = [0, 1]

#diffname = 'time_np-pitch_np'
#test_conds = [2, 0]

#diffname = 'time_p-time_np'
#test_conds = [3, 2]

#diffname = 'time_np-pitch_np'
#test_conds = [3, 0]

#diffname = 'time_np-pitch_p'
#test_conds = [2, 1]

tail = 0  # f-test, so tail > 0
n_permutations = 1000  # Save some time (the test won't be too sensitive ...)

n_conditions = len(conditions)
n_replications = len(nips)

if do_tfce == 1: 
    threshold = dict(start=0., step = 0.2)
else:   
    p_threshold = 0.05
    n_samples = len(nips) # *len(conditions)
    from scipy import stats
    threshold = - stats.distributions.t.ppf(p_threshold / 2., n_samples - 1)

def find_nearest(a,a0):
    "Element in nd array 'a' closest to the scalar value a0"
    idx = np.abs(a - a0).argmin()
    return a.flat[idx]

tp1 = find_nearest(itc_dummy.times,tmin_test)
tp1 = np.asscalar(np.where(itc_dummy.times == tp1)[0])

tp2 = find_nearest(itc_dummy.times,tmax_test)
tp2 = np.asscalar(np.where(itc_dummy.times == tp2)[0])
n_times = len(np.arange(tp1,tp2,1))

f1 = find_nearest(itc_dummy.freqs,test_freqs[0])
f1 = np.asscalar(np.where(itc_dummy.freqs == f1)[0])

f2 = find_nearest(itc_dummy.freqs,test_freqs[1])
f2 = np.asscalar(np.where(itc_dummy.freqs == f2)[0])

n_chans = len(pow_dummy.ch_names)

# prepare data
allconds_power = list()
allconds_itc = list()
for c, condition in enumerate(conditions):          
    
    # avg over FP
    Ptmp = POW[:,c]
    Ptmp = Ptmp[:,:,:,f1:f2,tp1:tp2]
    P = np.mean(Ptmp, 1) # avg over FP
    P = np.mean(P, 2) # avg over FREQS
    P = P.reshape(n_replications, n_times, n_chans) 
    allconds_power.append(P)
    
    Itmp = ITC[:,c]
    Itmp = Itmp[:,:,:,f1:f2,tp1:tp2]
    I = np.mean(Itmp, 1) # avg over FP
    I = np.mean(I, 2) # avg over FREQS
    I = I.reshape(n_replications, n_times, n_chans)   
    allconds_itc.append(I)


freqs = pow_dummy.freqs
times = itc_dummy.times[np.arange(tp1,tp2,1)]

# set up for the clustering
connectivity, _ = read_ch_connectivity('neuromag306mag') # neuromag306mag neuromag306planar
#from mne.channels import find_ch_connectivity
#connectivity, _ = find_ch_connectivity(pow_dummy.info, ch_type='eeg')

Ttestdata = list()
if testwhat == 'pow':
    Ttestdata.append(allconds_power[test_conds[0]])
    Ttestdata.append(allconds_power[test_conds[1]])
elif testwhat == 'itc':
    Ttestdata.append(allconds_itc[test_conds[0]])
    Ttestdata.append(allconds_itc[test_conds[1]])

print('Clustering..')  
T_obs, clusters, cluster_p_values, h0 = mne.stats.spatio_temporal_cluster_test(
        Ttestdata, connectivity=connectivity,stat_fun=None, threshold=threshold, tail=tail, 
        n_permutations=n_permutations, buffer_size=None, out_type = 'mask')
# stat_fun=f_mway_rm

#sigma = 1e-3
#stat_fun_hat = partial(mne.stats.ttest_1samp_no_p, sigma = sigma)
#t_tfce_hat, clusters, p_tfce_hat, h0 = mne.stats.spatio_temporal_cluster_test(
#        Ttestdata, connectivity=connectivity,stat_fun=stat_fun_hat, threshold=threshold, tail=tail, 
#        n_permutations=n_permutations, buffer_size=None)


#%%
good_clusters = np.where(cluster_p_values < .08)[0]
print('min (p): ' + str(np.min(cluster_p_values)))

TestDat = Ttestdata[0] - Ttestdata[1]
TestDat_avg =  np.mean(TestDat,0)
# visualise tfce result
if do_tfce == 0:
    for i_cluster, good_cluster in enumerate(good_clusters):
          
                masky = np.invert(clusters[np.squeeze(good_cluster)])
    #                plt.imshow(np.swapaxes(clusters[np.squeeze(good_cluster)]*1,1,0),vmin=0, vmax=1)
    #                plt.colorbar()
    #                # Initialize figure
    
                T_masked = np.ma.masked_array(T_obs, masky) # masks the TRUE values (but has been inverted before)
                
                fig, ax = plt.subplots(1)    
                ax1 = plt.subplot2grid((1, 2), (0, 0))
                
                # plot topo 
                topodat = np.mean(T_masked,0)               
                topodat = topodat.reshape(102,1,1)
                TOPO = AverageTFR(pow_dummy.info,topodat,[0],[1],nave=len(nips))
                TOPO.plot_topomap(ch_type=ch_type, tmin=0, tmax=0, fmin=1, fmax=1,
                       baseline=None,
                       title=(diffname +  "\n" +
                          " cluster-level corrected (p <= " + str(p_threshold)),  
                          axes = ax1, show=True)
                
                
                # collapse mask over timepoints 
                # to get all channels that are significant at any time
                mask_chan = clusters[np.squeeze(good_cluster)].any(axis = 1)
                mask_chan_mat = np.tile(mask_chan, (1,n_chans))
                
                time_inds = np.ma.masked_array(times,np.invert(clusters[np.squeeze(good_cluster)].any(axis = 1)))
                
                TestDat_diff = Ttestdata[0] - Ttestdata[1]
                
                TestDat0_masked = np.ma.masked_array(np.mean(Ttestdata[0],0), np.invert(mask_chan_mat))
                TestDat1_masked = np.ma.masked_array(np.mean(Ttestdata[1],0), np.invert(mask_chan_mat))
                
                TestDat_diff_masked = np.ma.masked_array(np.mean(TestDat_diff,0), mask_chan_mat)
                
                plotdat0 = TestDat0_masked.mean(axis = 1)
                plotdat1 = TestDat1_masked.mean(axis = 1)
                
                ax1 = plt.subplot2grid((1, 2), (0, 1))
                plt.plot(times, plotdat0)
                plt.plot(times, plotdat1)            
                plt.title(diffname)
             
                plt.fill_betweenx((0.15, .2), time_inds.min(), time_inds.max(),
                                 color='grey', alpha=0.3)
                     
else:
    
    # visualise tfce result
    significant_points = cluster_p_values.reshape(T_obs.shape).T < .15
    print('found ' + str(significant_points.sum()) + " points selected by TFCE ...")
       
    
    AVGITC_allFP_Pitch_P_NP.plot_image(mask=significant_points, time_unit='s',
                                    )
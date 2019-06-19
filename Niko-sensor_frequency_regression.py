"""
This script is a mix of two, so not really correct(?):
    https://martinos.org/mne/stable/auto_tutorials/stats-source-space/
                plot_stats_cluster_spatio_temporal.html#sphx-glr-auto-tutorials-
                stats-source-space-plot-stats-cluster-spatio-temporal-py
    https://mne-tools.github.io/0.17/auto_tutorials/
                plot_stats_spatio_temporal_cluster_sensors.html?highlight=make_axes_locatable

"""


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
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mne.channels import read_ch_connectivity


connectivity, ch_names = read_ch_connectivity('neuromag306planar') #  neuromag306mag
chan_pick = 'grad'


subject = config.subjects_list[0] #take the first subject
meg_subject_dir = op.join(config.meg_dir, subject)
extension = config.name_ext + '_cleaned-epo-ave'
fname_in = op.join(meg_subject_dir,
                            config.base_fname.format(**locals()))
evokeds = mne.read_evokeds(fname_in)
dum_evo = evokeds[0]
times = len(dum_evo.times)
n_channels = len(mne.pick_types(dum_evo.info, chan_pick))

#bands = {'theta':(4,7),'alpha':(8,12),
#        'beta1':(12,20),'beta2':(20,30),
#        'gamma':(30,60),'hgamma':(60,120)}

#bands = {'alpha':(8,12), 'beta1':(12,20), 'beta2':(20,40), 'beta':(15,40)}
bands = {'beta': (15,40)}


#event_id = {'BPint01s': 13, 'BPint01c': 15, 'BPint01l': 17, 
#            'BPint02s': 23, 'BPint02c': 25, 'BPint02l': 27,
#            'BPint03s': 33, 'BPint03c': 35, 'BPint03l': 37}
event_id = {'BPint123': 5}
conditions = ['BPint123']
#conditions = ['BPint01s', 'BPint01c', 'BPint01l',
#              'BPint02s', 'BPint02c', 'BPint02l',
#              'BPint03s', 'BPint03c', 'BPint03l']
power=[list() for _ in range(len(conditions))]
itc=[list() for _ in range(len(conditions))]
all_freq=np.zeros((len(bands),len(config.subjects_list),n_channels,times))
this_freq=np.zeros((len(config.subjects_list),n_channels,times))

p_threshold = 0.00001
n_samples = len(config.subjects_list)-len(config.exclude_subjects) # *len(conditions)
threshold = - stats.distributions.t.ppf(p_threshold / 2., n_samples - 1)
threshold_tfce = dict(start=0., step = 0.2)
p_accept = 0.01# 0.15
n_perm = 1000

sigma = 1e-3

stat_fun_hat = partial(mne.stats.ttest_1samp_no_p, sigma = sigma)

for con,condition in enumerate(conditions): # currently it iterates through all of them, but if I want to save them
    # I need to either create a list of all_freq per condition, or add another dimension 5th in the all_freq matrix
        print("processing condition: %s" % condition)
        for z,(band,freq) in enumerate(bands.items()):
                print("processing band: %s" % band)      
                for i, subject in enumerate(config.subjects_list):
                        print("processing subject: %s" % subject) 
                        meg_subject_dir = op.join(config.meg_dir, subject)
                        fname_in=op.join(config.meg_dir,subject)
                        extension = '-tfr'
                        power[con] = read_tfrs(
                                op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
                                        % (config.study_name, subject, 
                                        condition.replace(op.sep, ''))))
                        
                        power[con] = power[con][-1]
                        power[con].apply_baseline(mode='percent',baseline=(-0.3,-0.1))
                        
                        power[con].pick_types(meg=chan_pick)
                # itc[con] = read_tfrs(
                #         op.join(meg_subject_dir,config.analysis, '%s_%s_itc_%s-tfr.h5'
                #                 % (config.study_name, subject, 
                #                 condition.replace(op.sep, ''))))
                             
                        this_freq[i,:,:]=power[con].data[:,freq[0]:freq[1],:].mean(axis=1)
                all_freq[z,:,:,:]=this_freq[:,:,:]

#transpose the dimensions according to spatiotemporal stat function
all_freq = np.transpose(all_freq, (0,1,3,2)) 


cluster_stats  = spatio_temporal_cluster_1samp_test(
        all_freq[0,:,:,:], connectivity=connectivity,stat_fun=stat_fun_hat, threshold=threshold,
        n_permutations=n_perm, buffer_size=None, out_type='indices') 

T_obs, clusters, p_values, H0 = cluster_stats
good_cluster_inds = np.where(p_values < 0.05)[0]
print('found ' + str(len(good_cluster_inds)) + ' significant clusters')

#%% 

# Read the epochs
for subject in config.subjects_list:
    meg_subject_dir = op.join(config.meg_dir, subject)
    extension = config.name_ext + '_cleaned-epo'
    fname_in = op.join(meg_subject_dir,
                   config.base_fname.format(**locals()))
    epochs = mne.read_epochs(fname_in, preload=True)
    epochs.pick_types(meg=chan_pick)
#%% Visualise clusters
    
# configure variables for visualization
colors = {"BPint123": "crimson"}
linestyles = {"BPint123": '-'}

# get sensor positions via layout
pos = mne.find_layout(epochs.info).pos

# organize data for plotting

evokeds = {cond: epochs[cond].average() for cond in event_id}

# loop over clusters
for i_clu, clu_idx in enumerate(good_cluster_inds):
    # unpack cluster information, get unique indices
    time_inds, space_inds = np.squeeze(clusters[clu_idx])
    ch_inds = np.unique(space_inds)
    time_inds = np.unique(time_inds)

    # get topography for F stat
    f_map = T_obs[time_inds, ...].mean(axis=0)

    # get signals at the sensors contributing to the cluster
    sig_times = epochs.times[time_inds]

    # create spatial mask
    mask = np.zeros((f_map.shape[0], 1), dtype=bool)
    mask[ch_inds, :] = True

    # initialize figure
    fig, ax_topo = plt.subplots(1, 1, figsize=(10, 3))

    # plot average test statistic and mark significant sensors
    image, _ = plot_topomap(f_map, pos, mask=mask, axes=ax_topo, cmap='Reds',
                            vmin=np.min, vmax=np.max, show=False)

    # create additional axes (for ERF and colorbar)
    divider = make_axes_locatable(ax_topo)

    # add axes for colorbar
    ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(image, cax=ax_colorbar)
    ax_topo.set_xlabel(
        'Averaged F-map ({:0.3f} - {:0.3f} s)'.format(*sig_times[[0, -1]]))

    # add new axis for time courses and plot time courses
    ax_signals = divider.append_axes('right', size='300%', pad=1.2)
    title = 'Cluster #{0}, {1} sensor'.format(i_clu + 1, len(ch_inds))
    if len(ch_inds) > 1:
        title += "s (mean)"
    plot_compare_evokeds(evokeds, title=title, picks=ch_inds, axes=ax_signals,
                         colors=colors, linestyles=linestyles, show=False,
                         split_legend=True, truncate_yaxis='max_ticks')

    # plot temporal cluster extent
    ymin, ymax = ax_signals.get_ylim()
    ax_signals.fill_betweenx((ymin, ymax), sig_times[0], sig_times[-1],
                             color='orange', alpha=0.3)

    # clean up viz
    mne.viz.tight_layout(fig=fig)
    fig.subplots_adjust(bottom=.05)
    plt.show()
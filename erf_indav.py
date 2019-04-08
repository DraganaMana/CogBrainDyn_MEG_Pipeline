# to RUN separately for A trigger onsets and V trigger onsets

######################## SETUP ENV #######################
import os
from copy import deepcopy

import mne
from mne import fiff
from mne.minimum_norm import apply_inverse, make_inverse_operator, read_inverse_operator, source_induced_power
from mne.event import merge_events
from mne.stats import permutation_t_test

import numpy as np
import pylab as pl
import scipy.io as io

################### PATHS DEFINITION ###################
# if on external drive
#SUBJECTS_DIR = '/media/My Passport/MEG_DATA/2012_Natstats_Diana/meg_data-and-scripts/Freesurfer segmentation/'
# if on server
SUBJECTS_DIR = '/neurospin/meg/meg_tmp/2012_Natstats_Diana/meg_data-and-scripts/Freesurfer_segmentation/'

os.environ['SUBJECTS_DIR']=SUBJECTS_DIR

# if on external drive
#base_path 		= '/media/My Passport/MEG_DATA/2012_Natstats_Diana/'
# if on server
base_path 		= '/neurospin/meg/meg_tmp/2012_Natstats_Diana/'
data_path      = base_path + 'meg_data-and-scripts/'
fif_indav_path = base_path + '201312_vvw_analysis/ERF_analysis/indav_fif/'
stc_indav_path = base_path + '201312_vvw_analysis/ERF_analysis/indav_stc/'

################### SUBJECT VARIABLES TO EDIT ################
'''# ALL participants
sid     = ['s01', 's02','s03','s04','s05', \
           's06','s07','s08','s09','s10', \
           's11','s12','s13','s14','s15', \
           's16','s17','s18','s19']
sid_nip = ['jm100109', 'cd110379', 'jm100042', 'nc110174_landmark', 'vr100551_landmark', \
           'ns110383', 'cg120234', 'vd110117', 'cb100118', 'pj100477', \
           'vm080111', 'cj100142', 'bd090157', 'ib100049', 'md120159', \
           'cd100449', 'kr080082_landmark', 'mn080208', 'rk09001']
'''
# only clean subjects, N=16
sid     = ['s01', 's02','s03','s04','s05', \
           's06','s07','s08','s09','s10', \
           's11','s12','s13','s14', \
           's17','s18']
sid_nip = ['jm100109', 'cd110379', 'jm100042', 'nc110174_landmark', 'vr100551_landmark', \
           'ns110383', 'cg120234', 'vd110117', 'cb100118', 'pj100477', \
           'vm080111', 'cj100142', 'bd090157', 'ib100049', \
           'kr080082_landmark', 'mn080208']

runs  = ['r1', 'r2','r3','r4','r5','r6']

#######
#######
# A = 0 / V = 1
TRIGcond = 1
#######
#######

if TRIGcond == 0:
    conds = ['TAa','TAb','TAc','TAd','PAa','PAb','PAc','PAd']
elif TRIGcond == 1:
    conds = ['vTAa','vTAb','vTAc','vTAd','vPAa','vPAb','vPAc','vPAd']

###################### STUDY DEFINITION  #################
Adelay_samples = ([140, 0, 0])
Vdelay_samples = ([62, 0, 0])
trigs = dict()

################### AUDIO trigger #########################
Atmin = dict()
Atmax = dict()

Atmin[0],Atmax[0] = -0.6, 1.4
Atmin[1],Atmax[1] = -0.8, 1.2
Atmin[2],Atmax[2] = -1.2, 0.8
Atmin[3],Atmax[3] = -1.4, 0.6

tmin = dict()
tmax = dict()

trigs['TAa'],tmin['TAa'],tmax['TAa'] = 1, Atmin[0], Atmax[0]
trigs['TAb'],tmin['TAb'],tmax['TAb'] = 2, Atmin[1], Atmax[1]
trigs['TAc'],tmin['TAc'],tmax['TAc'] = 3, Atmin[2], Atmax[2]
trigs['TAd'],tmin['TAd'],tmax['TAd'] = 4, Atmin[3], Atmax[3]

trigs['PAa'],tmin['PAa'],tmax['PAa'] = 5, Atmin[0], Atmax[0]
trigs['PAb'],tmin['PAb'],tmax['PAb'] = 6, Atmin[1], Atmax[1]
trigs['PAc'],tmin['PAc'],tmax['PAc'] = 7, Atmin[2], Atmax[2]
trigs['PAd'],tmin['PAd'],tmax['PAd'] = 8, Atmin[3], Atmax[3]

######################## VISUAL trigger ####################
Vtmin,Vtmax = -0.2, 1.8

trigs['vTAa'], tmin['vTAa'], tmax['vTAa'] = 12, Vtmin, Vtmax
trigs['vTAb'], tmin['vTAb'], tmax['vTAb'] = 13, Vtmin, Vtmax
trigs['vTAc'], tmin['vTAc'], tmax['vTAc'] = 14, Vtmin, Vtmax
trigs['vTAd'], tmin['vTAd'], tmax['vTAd'] = 15, Vtmin, Vtmax

trigs['vPAa'], tmin['vPAa'], tmax['vPAa'] = 16, Vtmin, Vtmax
trigs['vPAb'], tmin['vPAb'], tmax['vPAb'] = 17, Vtmin, Vtmax
trigs['vPAc'], tmin['vPAc'], tmax['vPAc'] = 18, Vtmin, Vtmax
trigs['vPAd'], tmin['vPAd'], tmax['vPAd'] = 19, Vtmin, Vtmax

# pick list
include = []
exclude = []
reject = dict(grad=4000e-13, mag=4e-12, eog=600e-6)

##################  EVENTS DEFINITION ################
raws     = dict()
evts_tmp = dict()
evts     = dict()

# parameters for inverse solution
snr         = 3.0
lambda2     = 1.0 / snr ** 2
method      = "dSPM"
pick_ori    ="normal"


for s, subj in enumerate(sid):

    idata_path = data_path + '%s/' % subj
    sss_path = data_path + '%s/' %subj
    inverse_operator= read_inverse_operator(sss_path + subj + '-inv-oct6.fif')   
    
    print(s)

    for run in range(1, 7):
        k = 'r%d' % run
        raws[k]     = mne.io.Raw(idata_path + '%s_run%d_trans_sss_filt40_raw.fif' % (subj, run))
        evts[k] = mne.find_events(raws[k], stim_channel=['STI101'], min_duration=0.002)        
        tmp = evts[k]

        if TRIGcond == 0:      
            evts[k] = evts[k] + Adelay_samples  
        elif TRIGcond == 1:
            evts[k] = evts[k] + Vdelay_samples  

    ###################### EPOCHS + AVE ##########################
    epochs = dict()
    evoked = dict()
    istc = dict()
    all_evoked = dict()

    for cond in conds:

        bsln_min = tmin[cond]
        bsln_max = tmin[cond] + 0.2

        for run in runs:
            picks = mne.fiff.pick_types(raws[run].info, meg=True, eeg=False, stim=False,eog=True,
                                        include=include, exclude=exclude)
            epochs[run] = mne.Epochs(raws[run], evts[run], trigs[cond], tmin[cond], tmax[cond],
                                     picks=picks, baseline=(bsln_min, bsln_max), reject=reject)
            evoked[run] = epochs[run].average()

        all_evoked[cond] = evoked['r1'] + evoked['r2'] + evoked['r3'] + evoked['r4'] + evoked['r5'] + evoked['r6']
        all_evoked[cond].comment = cond

        #istc = apply_inverse(all_evoked[cond], inverse_operator, lambda2, method, pick_ori)
        #istc.save(stc_indav_path + subj +'_dSPM_inv_%s' %cond)

        #istc_fsaverage = mne.morph_data(sid_nip[s], 'fsaverage', istc, n_jobs=4)
        #istc_fsaverage.save(stc_indav_path + subj +'_dSPM_inv_%s_fs' %cond)
    
    if TRIGcond == 0:      
        mne.io.write_evokeds(fif_indav_path + subj + '-ave.fif', [e for e in all_evoked.values()])
    elif  TRIGcond == 1:      
        mne.io.write_evokeds(fif_indav_path + subj + '_Von-ave.fif', [e for e in all_evoked.values()])
  
    print "Done."

    
    ########## butterfly plot ERF ##########
    #mne.viz.plot_evoked(all_evoked['TAa'])


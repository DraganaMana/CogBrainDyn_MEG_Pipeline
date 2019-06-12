"""
=================================
17. Group average on sensor Time-Frequency
=================================

"""

import os.path as op
import numpy as np

import mne
from mne.parallel import parallel_func
from mne.time_frequency import read_tfrs, read_csd
import config

all_power = np.zeros((len(config.subjects_list),306,config.df,600)) # what is config.df
all_itc = np.zeros((len(config.subjects_list),306,config.df,600))

#power[0].data.shape
#Out[50]: (306, 30, 1376)


subject=config.subjects_list_source[1]
condition=config.conditions[0]
meg_subject_dir = op.join(config.meg_dir, subject)

extension = '-ave'
fname_in = op.join(meg_subject_dir,config.analysis,
                    config.base_fname.format(**locals()))

#load a random evoked for extracting the .info
evokeds = mne.read_evokeds(fname_in)
evokeds[0].resample(config.resample_sfreq)
info=evokeds[0].info
times=evokeds[0].times

power=[list() for _ in range(len(config.conditions1))]
itc=[list() for _ in range(len(config.conditions1))]

for con,condition in enumerate(config.conditions1):
        print("processing condition: %s" % condition)
        for i,subject in enumerate(config.subjects_list):
                if subject in config.exclude_subjects:
                        print("ignoring subject: %s" % subject)
                        continue
                else:
                        print("processing subject: %s" % subject)
                meg_subject_dir = op.join(config.meg_dir, subject)
                fname_in=op.join(config.meg_dir,subject,config.analysis)
                extension = '-tfr'
                power[con] = read_tfrs(
                        op.join(meg_subject_dir,config.analysis, '%s_%s_power_%s-tfr.h5'
                                % (config.study_name, subject, 
                                condition.replace(op.sep, ''))))
                itc[con] = read_tfrs(
                        op.join(meg_subject_dir,config.analysis, '%s_%s_itc_%s-tfr.h5'
                                % (config.study_name, subject, 
                                condition.replace(op.sep, ''))))
        
                all_power[i,:,:,:]=power[con][0].data
                all_itc[i,:,:,:]=itc[con][0].data

        gapow = all_power.mean(axis=0)
        gaitc = all_power.mean(axis=0)

        gapow_tfr = mne.time_frequency.AverageTFR(info,gapow,times,config.freqs,nave=len(config.subjects_list))
        gaitc_tfr = mne.time_frequency.AverageTFR(info,gaitc,times,config.freqs,nave=len(config.subjects_list))
        
        gapow_tfr.save(
            op.join(config.meg_dir,'n16',config.analysis,'sensor_time_frequency', '%s_power_%s-tfr.h5'
                    % ('n16', 
                       condition.replace(op.sep, ''))), overwrite=True)
        gaitc_tfr.save(
            op.join(config.meg_dir,'n16',config.analysis,'sensor_time_frequency', '%s_itc_%s-tfr.h5'
                    % ('n16', 
                       condition.replace(op.sep, ''))), overwrite=True)
        
##############################################################################################       
# Find the difference between the two Replay and Play average power and itc
        
# Read files from 10-TF
for condition in config.time_frequency_conditions:
    power_name = op.join(config.meg_dir, 'some folder in case', '%s_power_%s-tfr.h5'
                    % ('n16', condition.replace(op.sep, ''))), overwrite=True)
    power = mne.time_frequency.read_tfrs(power_name)
    power[0].plot_joint(baseline=(-1.5, -0.8), mode='mean', tmin=-1.5, tmax=1.25,
                 timefreqs=[(.15, 10), (0.6, 20)])
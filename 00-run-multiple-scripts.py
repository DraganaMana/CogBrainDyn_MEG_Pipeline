# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:16:06 2019

@author: Dragana
"""

#exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/config.py").read())
#exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/01-import_and_filter.py").read())
#exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/02-apply_maxwell_filter.py").read())
#
#exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/03-extract_events.py").read())
exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/03a-events-Pscl.py").read())

exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/04-make_epochs.py").read())
exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/05a-run_ica.py").read())
exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/06a-apply_ica.py").read())

exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/07-make_evoked.py").read())

exec(open("/home/dm258725/CogBrainDyn_MEG_Pipeline/10-time-frequency.py").read())


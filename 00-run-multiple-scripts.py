# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:16:06 2019

@author: Dragana
"""
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline\config.py").read())
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline\config01-import_and_filter.py").read())
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/02-apply_maxwell_filter.py").read())

exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/03-extract_events.py").read())
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/03a-events-Pscl.py").read())

exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/04-make_epochs.py").read())
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/05a-run_ica.py").read())
exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/06a-apply_ica.py").read())

exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/07-make_evoked.py").read())

exec(open("C:\Users/Dragana/Repositories/CogBrainDyn_MEG_Pipeline/10-time-frequency.py").read())

""" For a .bat file
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\config.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\01-import_and_filter.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\02-apply_maxwell_filter.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\03-extract_events.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\03a-events-Pscl.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\04-make_epochs.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\05a-run_ica.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\06a-apply_ica.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\07-make_evoked.py"
"C:\Users\Dragana\Anaconda3\envs\mne\python.exe" "C:\Users\Dragana\Repositories\CogBrainDyn_MEG_Pipeline\10-time_frequency.py"
pause
"""
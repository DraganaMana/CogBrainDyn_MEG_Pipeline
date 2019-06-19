# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:45:55 2019

@author: Dragana
"""
import numpy as np
from numpy import append
import matplotlib.pyplot as plt
import os.path as op

import mne

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

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


for c,condition in enumerate(conditions):
    print(condition)
    for pp, nip in enumerate(nips):
        print(nip)
         
        meg_subject_dir = op.join(config.meg_dir, nip)
        
        # Calculate the TFs w/o a baseline
        power = mne.time_frequency.read_tfrs(op.join(meg_subject_dir, '%s_%s_power_%s-tfr.h5'
                                                     % (config.study_name, nip,
                                                        condition.replace(op.sep, ''))))

        power = power.pop()
        power.apply_baseline(mode='percent',baseline=(-0.3,-0.1))
            
        power = power.crop(tmin=tmin,tmax=tmax) 
        
        if ch_type == 'mag':
            power.pick_types(meg='mag')
        elif ch_type == 'grad':
            power.pick_types(meg='grad')
        elif ch_type == 'eeg':
            power.pick_types(eeg=True,meg = False)
            
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
        power = power.crop(0.5,1)
        power = power.data
            # also I need to check which are the significant channels from the clusters, and
            # only pick them like I picked the freq and times
        for i, channels in enumerate(power[:,0,0]):
            for k, time in enumerate(power[i,0,:]):
                m=0
                for j, freq in enumerate(power[i,:,k]):
                    if j > 10 and j <= 37: # j<=37 10 --> 13Hz; 37 --> 40 Hz
                        power_beta[i,m,k] = freq
                        m += 1
                        
        pow_beta.append(np.mean(power_beta)) # average over times and frequencies and channels 
        pow_beta_sd.append(np.std(power_beta))

#%% plot, transform, check
ints = ['1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
for p in range(0,len(ints)):
    for r in range(p*18,(p+1)*18):   
        plt.plot(ints[p], pow_beta[r], 'bo-')

# I want to make the ints list as long as pow_beta in order to do the linear regression
ints_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
ints_long = []   
for i in range(0, len(ints_num)):  
    for p in range(0,18):
        ints_long.append(ints_num[i])
#
#for i, val in enumerate(pow_beta):
#    if val > 1:
#        print(i,val)
#        
#for p in range(0,len(ints)):
#    print(p)
    
    
    
#%% Linear regression
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#cvss = []
#cvss.extend(cvs1)
#cvss.extend(cvs2)
#cvss.extend(cvs3)
#erss = []
#erss.extend(ers1)
#erss.extend(ers2)
#erss.extend(ers3)

x = np.array(ints_long).reshape((-1, 1))
y = np.array(pow_beta)

model = LinearRegression().fit(x, y)

#  the coefficient of determination (𝑅²) with .score() called on model
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)

y_pred = model.predict(x)
print('predicted response:', y_pred, sep='\n')

# Plot outputs
plt.scatter(x, y,  color='black')
plt.plot(x, y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()

#%% New plot
"""
import pandas as pd
import seaborn as sns
import itertools
#%matplotlib qt

xl      = np.ndarray.tolist(x) # x from the linear regress is an array, and we get list of lists
yl      = np.ndarray.tolist(y)
yl_pred = np.ndarray.tolist(y_pred)
xll = list(itertools.chain.from_iterable(xl)) # we have list of lists, and we need a flat list

df1 = pd.DataFrame({'Int123scl': xll, 'betaPow': y})
df2 = pd.DataFrame({'X': xll, 'y_pred': y_pred})

sns.set_style("whitegrid")
#plt.figure()
# 1
#ints = ['why', '1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
#spl = sns.scatterplot(x="Int123scl", y="betaPow", data=df1, s=60, #marker="s", 
#                      color="indianred", label="Beta power")
#spl = sns.lineplot(x="X", y="y_pred", data=df2, color="black", label="Linear regression")
# 2
#ints = ['1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
#spl = sns.boxplot(x="Int123scl", y="betaPow", data=df1, color="indianred")
# 3
spl = sns.regplot(x="Int123scl", y="betaPow", data=df1, x_jitter=.1, color="indianred",
                  label="Beta power")
ints = ['why','1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
plt.title("Beta power over P123 scl, per pax")
plt.xlabel("P 123 scl", fontsize=12) 
plt.ylabel("Average beta power per pax", fontsize=12)    
spl.legend(loc='upper left', frameon=True)
spl.set_xticklabels(ints)
#plt.figure(frameon=True)
plt.show()


#

#spl.figure.savefig("betaPower_perInt123scl_perPax.svg")
#plt.show()
"""
#%% Box plot
import pandas as pd
import seaborn as sns
import itertools
import matplotlib.style as style
#%matplotlib qt

xl      = np.ndarray.tolist(x) # x from the linear regress is an array, and we get list of lists
yl      = np.ndarray.tolist(y)
yl_pred = np.ndarray.tolist(y_pred)
xll = list(itertools.chain.from_iterable(xl)) # we have list of lists, and we need a flat list

df1 = pd.DataFrame({'Int123scl': xll, 'betaPow': y})
#df2 = pd.DataFrame({'X': xll, 'y_pred': y_pred})
#with sns.color_palette("YlOrRd", 6):
sns.set_style("whitegrid")
style.use('seaborn-poster')
# Draw a pointplot to show pulse as a function of three categorical factors
spl = sns.catplot(x="Int123scl", y="betaPow", # alpha=1.5, # hue="kind", col="diet",
                capsize=.2, palette=sns.color_palette("Reds", 9), # height=6, aspect=.75,
                kind="point", data=df1)
ints = ['1.45s','1.45c','1.45l','2.9s','2.9c','2.9l','5.8s','5.8c','5.8l']
plt.title("Average beta power per condition")
plt.xlabel("Conditions (s-short, c-correct, l-long) per interval") 
plt.ylabel("Beta power") 
plt.ylim(0.05, 0.35)   
spl.set_xticklabels(ints)
sns.despine() 
plt.show()




#%% Plot the CV-ER dots + the linear regression
"""
import pygal

xl = np.ndarray.tolist(x) # x from the linear regress is an array, and we get list of lists
import itertools
xll = list(itertools.chain.from_iterable(xl)) # we have list of lists, and we need a flat list
tups = list(zip(xll, y_pred)) # we need a list of tuples for plotting

from pygal.style import BlueStyle, CleanStyle

# MAKING MY OWN STYLE 
from pygal.style import Style
custom_style = Style(
  background='#ffffff',
  plot_background='#ffffff',
  foreground='#000000',
  foreground_strong='#000000',
  foreground_subtle='#000000',
  opacity='.6',
  opacity_hover='.9',
  transition='400ms ease-in',
  colors=('#08cc9e', '#4860db', '#10c6d3', '#0a2628'),
  title_font_size = 20,
  label_font_size = 15,
  legend_font_size = 15)

xy_chart = pygal.XY(stroke=False, style=custom_style, 
                    title=u'Beta power over P123 scl, per pax', 
                    x_title='P 123 scl',
                    y_title='Average beta power per pax',
                    legend_at_bottom=True,
                    dots_size = 5)

t = list(zip(ints_long,pow_beta))  # we need a list of tuples for plotting
#for i in range(len(ints_long)):
xy_chart.add('beta power per pax', [t[i] for i in range(len(ints_long))])

xy_chart.add('Linear regression', [min(tups), max(tups)], stroke=True, stroke_style={'width': 3})
xy_chart.render()
xy_chart.render_to_file('beta-power_P123scl_perPax.svg')
"""
#%% Pearson correlation coefficient and p-value for testing non-correlation.

#https://www.texasgateway.org/resource/124-testing-significance-correlation-coefficient-optional
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

#import scipy 
from scipy import stats

r, p = stats.pearsonr(ints_long, pow_beta)
print(r,p)
# mag:
    # w/ outlier 0.14153083219897472 0.0724152918454892
    # w/o outlier 0.18636512107579575 0.017572062204390407
# mag:
    # w/ outlier 0.12760538683080672 0.10562015665252471
    # w/o outlier 0.17544942770317948 0.02553800749221432
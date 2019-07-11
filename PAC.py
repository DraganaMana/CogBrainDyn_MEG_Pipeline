# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:17:04 2019

@author: DM258725
"""

import matplotlib.pyplot as plt

from pactools import PeakLocking
from pactools import simulate_pac

fs = 200.  # Hz
high_fq = 50.0  # Hz
low_fq = 3.0  # Hz
low_fq_width = 2.0  # Hz

n_points = 10000
noise_level = 0.4
t_plot = 2.0  # sec

signal = simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
                      low_fq_width=low_fq_width, noise_level=noise_level,
                      random_state=0)

estimator = PeakLocking(fs=fs, low_fq=low_fq, low_fq_width=2.0, t_plot=t_plot)
estimator.fit(signal)
estimator.plot()

estimator = PeakLocking(fs=fs, low_fq=low_fq, low_fq_width=0.5, t_plot=t_plot)
estimator.fit(signal)
estimator.plot()

plt.show()

#%%
import mne
import numpy as np
import matplotlib.pyplot as plt

from pactools import raw_to_mask, Comodulogram

#data_path = mne.datasets.sample.data_path()
#raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
#event_fname = data_path + ('/MEG/sample/sample_audvis_filt-0-40_raw-'
#                           'eve.fif')
study_path = 'H:/ScaledTime_Dragana_2019/'
raw_fname = 
event_fname = 

raw = mne.io.read_raw_fif(raw_fname, preload=True)
events = mne.read_events(event_fname)

# select the time interval around the events
tmin, tmax = -5, 15
# select the channels (phase_channel, amplitude_channel)
ixs = (8, 10)

# create the input array for Comodulogram.fit
low_sig, high_sig, mask = raw_to_mask(raw, ixs=ixs, events=events, tmin=tmin,
                                      tmax=tmax)
# create the instance of Comodulogram
estimator = Comodulogram(fs=raw.info['sfreq'],
                         low_fq_range=np.linspace(1, 10, 20), low_fq_width=2.,
                         method='tort', progress_bar=True)
# compute the comodulogram
estimator.fit(low_sig, high_sig, mask)
# plot the results
estimator.plot(tight_layout=False)
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram, REFERENCES
from pactools import simulate_pac

fs = 200.  # Hz
high_fq = 50.0  # Hz
low_fq = 5.0  # Hz
low_fq_width = 1.0  # Hz

n_points = 10000
noise_level = 0.4

signal = simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
                      low_fq_width=low_fq_width, noise_level=noise_level,
                      random_state=0)

low_fq_range = np.linspace(1, 10, 50)
methods = [
    'ozkurt', 'canolty', 'tort', 'penny', 'vanwijk', 'duprelatour', 'colgin',
    'sigl', 'bispectrum'
]

# Define the subplots where the comodulogram will be plotted
n_lines = 3
n_columns = int(np.ceil(len(methods) / float(n_lines)))
fig, axs = plt.subplots(
    n_lines, n_columns, figsize=(4 * n_columns, 3 * n_lines))
axs = axs.ravel()


# Compute the comodulograms and plot them
for ax, method in zip(axs, methods):
    print('%s... ' % (method, ))
    estimator = Comodulogram(fs=fs, low_fq_range=low_fq_range,
                             low_fq_width=low_fq_width, method=method,
                             progress_bar=False)
    estimator.fit(signal)
    estimator.plot(titles=[REFERENCES[method]], axs=[ax])

plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram
from pactools import simulate_pac

fs = 200.  # Hz
high_fq = 50.0  # Hz
low_fq = 5.0  # Hz
low_fq_width = 1.0  # Hz

n_points = 1000
noise_level = 0.4

signal = simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
                      low_fq_width=low_fq_width, noise_level=noise_level,
                      random_state=0)

low_fq_range = np.linspace(1, 10, 50)
method = 'duprelatour'  # or 'tort', 'ozkurt', 'penny', 'colgin', ...

n_surrogates = 200

n_jobs = 4

estimator = Comodulogram(fs=fs, low_fq_range=low_fq_range,
                         low_fq_width=low_fq_width, method=method,
                         n_surrogates=n_surrogates, progress_bar=True,
                         n_jobs=n_jobs)
estimator.fit(signal)

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

z_score = 4.
estimator.plot(contour_method='z_score', contour_level=z_score,
               titles=['With a z-score on each couple of frequency'],
               axs=[axs[0]])

p_value = 0.05
estimator.plot(contour_method='comod_max', contour_level=p_value,
               titles=['With a p-value on the distribution of maxima'],
               axs=[axs[1]])

plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt

from pactools import Comodulogram
from pactools import simulate_pac
from pactools.dar_model import DAR, extract_driver

fs = 200.  # Hz
high_fq = 50.0  # Hz
low_fq = 5.0  # Hz
low_fq_width = 1.0  # Hz

n_points = 10000
noise_level = 0.4

signal = simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
                      low_fq_width=low_fq_width, noise_level=noise_level,
                      random_state=0)

# Prepare the plot for the two figures
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs = axs.ravel()

# Extract a low frequency band
sigdriv, sigin, sigdriv_imag = extract_driver(
    sigs=signal, fs=fs, low_fq=low_fq, bandwidth=low_fq_width,
    extract_complex=True, random_state=0, fill=2)

# Create a DAR model
# Here we use BIC selection to get optimal hyperparameters (ordar, ordriv)
dar = DAR(ordar=20, ordriv=2, criterion='bic')
# Fit the DAR model
dar.fit(sigin=sigin, sigdriv=sigdriv, sigdriv_imag=sigdriv_imag, fs=fs)

# Plot the BIC selection
bic_array = dar.model_selection_criterions_['bic']
lines = axs[0].plot(bic_array)
axs[0].legend(lines, ['ordriv=%d' % d for d in [0, 1, 2]])
axs[0].set_xlabel('ordar')
axs[0].set_ylabel('BIC / T')
axs[0].set_title('BIC order selection')
axs[0].plot(dar.ordar_, bic_array[dar.ordar_, dar.ordriv_], 'ro')

# Plot the modulation extracted by the optimal model
dar.plot(ax=axs[1])
axs[1].set_title(dar.get_title(name=True))

# Here we do not give the default set of parameter. Note that the BIC selection
# will be performed independantly for each model (i.e. at each low frequency).
dar = DAR(ordar=20, ordriv=2, criterion='bic')
low_fq_range = np.linspace(1, 10, 50)
estimator = Comodulogram(fs=fs, low_fq_range=low_fq_range,
                         low_fq_width=low_fq_width, method=dar,
                         progress_bar=False, random_state=0)
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
estimator.fit(signal)
estimator.plot(axs=[ax])
ax.set_title('Comodulogram')

plt.show()

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline

from pactools import simulate_pac
from pactools.grid_search import ExtractDriver, AddDriverDelay
from pactools.grid_search import DARSklearn, MultipleArray
from pactools.grid_search import GridSearchCVProgressBar

fs = 200.  # Hz
high_fq = 50.0  # Hz
low_fq = 5.0  # Hz
low_fq_width = 1.0  # Hz

n_epochs = 3
n_points = 10000
noise_level = 0.4

low_sig = np.array([
    simulate_pac(n_points=n_points, fs=fs, high_fq=high_fq, low_fq=low_fq,
                 low_fq_width=low_fq_width, noise_level=noise_level,
                 random_state=i) for i in range(n_epochs)
])
    
model = Pipeline(steps=[
    ('driver', ExtractDriver(fs=fs, low_fq=4., max_low_fq=7.,
                             low_fq_width=low_fq_width, random_state=0)),
    ('add', AddDriverDelay()),
    ('dar', DARSklearn(fs=fs, max_ordar=100)),
])

# grid of parameter on which we will loop
param_grid = {
    'dar__ordar': np.arange(0, 110, 30),
    'dar__ordriv': [0, 1, 2],
    'add__delay': [0],
    'driver__low_fq': [3., 4., 5., 6., 7.],
    'driver__low_fq_width': [0.25, 0.5, 1.],
}

# Plug the model and the parameter grid into a GridSearchCV estimator
# (GridSearchCVProgressBar is identical to GridSearchCV, but it adds a nice
# progress bar to monitor progress.)
gscv = GridSearchCVProgressBar(model, param_grid=param_grid,
                               return_train_score=False, verbose=1)

# Fit the grid-search. We use `MultipleArray` to put together low_sig and
# high_sig. If high_sig is None, we use low_sig for both the driver and the
# modeled signal.
X = MultipleArray(low_sig, None)
gscv.fit(X)

print("\nBest parameters set found over cross-validation:\n")
print(gscv.best_params_)

#
def plot_results(index='dar__ordar', columns='dar__ordriv'):
    """Select two hyperparameters from which we plot the fluctuations"""
    index = 'param_' + index
    columns = 'param_' + columns

    # prepare the results into a pandas.DataFrame
    df = pd.DataFrame(gscv.cv_results_)

    # Remove the other by selecting their best values (from gscv.best_params_)
    other = [c for c in df.columns if c[:6] == 'param_']
    other.remove(index)
    other.remove(columns)
    for col in other:
        df = df[df[col] == gscv.best_params_[col[6:]]]

    # Create pivot tables for easy plotting
    table_mean = df.pivot_table(index=index, columns=columns,
                                values=['mean_test_score'])
    table_std = df.pivot_table(index=index, columns=columns,
                               values=['std_test_score'])

    # plot the pivot tables
    plt.figure()
    ax = plt.gca()
    for col_mean, col_std in zip(table_mean.columns, table_std.columns):
        table_mean[col_mean].plot(ax=ax, yerr=table_std[col_std], marker='o',
                                  label=col_mean)
    plt.title('Grid-search results (higher is better)')
    plt.ylabel('log-likelihood compared to an AR(0)')
    plt.legend(title=table_mean.columns.names)
    plt.show()


plot_results(index='dar__ordar', columns='dar__ordriv')
plot_results(index='driver__low_fq', columns='driver__low_fq_width')

#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

from pactools import Comodulogram, REFERENCES
from pactools.utils.pink_noise import pink_noise
from pactools.utils.validation import check_random_state


def simulate_spurious_pac(n_points, fs, spike_amp=1.5, spike_fwhm=0.01,
                          spike_fq=10., spike_interval_jitter=0.2,
                          random_state=None):
    """Simulate some spurious phase-amplitude coupling (PAC) with spikes

    References
    ----------
    Gerber, E. M., Sadeh, B., Ward, A., Knight, R. T., & Deouell, L. Y. (2016).
    Non-sinusoidal activity can produce cross-frequency coupling in cortical
    signals in the absence of functional interaction between neural sources.
    PloS one, 11(12), e0167351
    """
    n_points = int(n_points)
    fs = float(fs)
    rng = check_random_state(random_state)

    # draw the position of the spikes
    interval_min = 1. / float(spike_fq) * (1. - spike_interval_jitter)
    interval_max = 1. / float(spike_fq) * (1. + spike_interval_jitter)
    n_spikes_max = np.int(n_points / fs / interval_min)
    spike_intervals = rng.uniform(low=interval_min, high=interval_max,
                                  size=n_spikes_max)
    spike_positions = np.cumsum(np.int_(spike_intervals * fs))
    spike_positions = spike_positions[spike_positions < n_points]

    # build the spike time series, using a convolution
    spikes = np.zeros(n_points)
    spikes[spike_positions] = spike_amp
    # full width at half maximum to standard deviation convertion
    spike_std = spike_fwhm / (2 * np.sqrt(2 * np.log(2)))
    spike_shape = scipy.signal.gaussian(M=np.int(spike_std * fs * 10),
                                        std=spike_std * fs)
    spikes = scipy.signal.fftconvolve(spikes, spike_shape, mode='same')

    noise = pink_noise(n_points, slope=1.)

    return spikes + noise, spikes

fs = 1000.  # Hz
n_points = 60000
spike_amp = 1.5
random_state = 0

# generate the signal
signal, spikes = simulate_spurious_pac(
    n_points=n_points, fs=fs, random_state=random_state, spike_amp=spike_amp)

# plot the signal and the spikes
n_points_plot = np.int(1. * fs)
time = np.arange(n_points_plot) / fs
fig, axs = plt.subplots(nrows=2, figsize=(10, 6), sharex=True)
axs[0].plot(time, signal[:n_points_plot], color='C0')
axs[0].set(title='spikes + pink noise')
axs[1].plot(time, spikes[:n_points_plot], color='C1')
axs[1].set(xlabel='Time (sec)', title='spikes')
plt.show()

methods = ['ozkurt', 'penny', 'tort', 'duprelatour']
low_fq_range = np.linspace(1., 20., 60)
high_fq_range = np.linspace(low_fq_range[-1], 100., 60)
low_fq_width = 4.  # Hz

# A good rule of thumb is n_surrogates = 10 / p_value. Example: 10 / 0.05 = 200
# Here we use 10 to be fast
n_surrogates = 10
p_value = 0.05
n_jobs = 11

# prepare the plot axes
n_lines = 2
n_columns = int(np.ceil(len(methods) / float(n_lines)))
figsize = (4 * n_columns, 3 * n_lines)
fig, axs = plt.subplots(nrows=n_lines, ncols=n_columns, figsize=figsize)
axs = axs.ravel()

for ax, method in zip(axs, methods):
    # compute the comodulograms
    estimator = Comodulogram(fs=fs, low_fq_range=low_fq_range,
                             high_fq_range=high_fq_range,
                             low_fq_width=low_fq_width, method=method,
                             n_surrogates=n_surrogates, n_jobs=n_jobs)
    estimator.fit(signal)

    # plot the comodulogram with contour levels
    estimator.plot(contour_method='comod_max', contour_level=p_value, axs=[ax],
                   titles=[REFERENCES[method]])

fig.tight_layout()
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt

from pactools.dar_model import DAR
from pactools.utils import peak_finder
from pactools.utils.viz import phase_string, SEABORN_PALETTES, set_style
from pactools.delay_estimator import DelayEstimator

plt.close('all')
set_style(font_scale=1.4)
blue, green, red, purple, yellow, cyan = SEABORN_PALETTES['deep']

fs = 500.  # Hz
high_fq = 80.0  # Hz
low_fq = 3.0  # Hz
low_fq_mod_fq = 0.5  # Hz
plot_fq_range = [40., 120.]  # Hz

bandwidth = 2.0  # Hz

high_fq_amp = 0.5
low_fq_mod_amp = 3.0

ratio = 1. / 6.
phi_0 = -2 * np.pi * ratio
delay = -1. / low_fq * ratio
offset = -1.
sharpness = 5.
noise_level = 0.1

n_points = 30000
t_plot = 1.  # sec


def sigmoid(array, sharpness):
    return 1. / (1. + np.exp(-sharpness * array))


def clean_peak_finder(sig):
    """Remove first peak if it is at t=0"""
    peak_inds, _ = peak_finder(sig, thresh=None, extrema=1)
    if peak_inds[0] == 0:
        peak_inds = peak_inds[1:]
    return peak_inds


def simulate_and_plot(phi_0, delay, ax, rng):
    """Simulate oscillations with frequency modulation"""
    # create the slow oscillations
    time = np.arange(n_points) / fs
    phase = time * 2 * np.pi * low_fq + np.pi / 2
    # add frequency modulation
    phase += low_fq_mod_amp * np.sin(time * 2 * np.pi * low_fq_mod_fq)
    theta = np.cos(phase)

    # add the fast oscillations
    gamma = np.cos(time * 2 * np.pi * high_fq)
    modulation = sigmoid(offset + np.cos(phase - phi_0),
                         sharpness) * high_fq_amp
    gamma *= modulation

    # add a delay
    delay_point = int(delay * fs)
    gamma = np.roll(gamma, delay_point)
    modulation = np.roll(modulation, delay_point)

    # plot the beginning of the signal
    sel = slice(int(t_plot * fs) + 1)
    lines_theta = ax.plot(time[sel], theta[sel])
    ax.plot(time[sel], gamma[sel])
    lines_modulation = ax.plot(time[sel], modulation[sel])

    # plot the horizontal line of phi_0
    if delay == 0 and False:
        ax.hlines(
            np.cos(-phi_0), time[sel][0], time[sel][-1], color='k',
            linestyle='--')

    gamma_peak_inds = clean_peak_finder(modulation[sel])
    theta_peak_inds = clean_peak_finder(theta[sel])
    cosph_peak_inds = clean_peak_finder(np.cos(phase - phi_0)[sel])

    # plot the vertical lines of the maximum amplitude
    ax.vlines(time[sel][gamma_peak_inds], -1, 1, color='k', linestyle='--')

    # fill vertical intervals between start_idx and stop_idx
    start_idx = gamma_peak_inds
    stop_idx = cosph_peak_inds
    fill_zone = np.zeros_like(time[sel])
    fill_zone[np.minimum(np.maximum(start_idx, 0), sel.stop - 1)] += 1
    fill_zone[np.minimum(np.maximum(stop_idx, 0), sel.stop - 1)] += -1
    ax.fill_between(time[sel], -1, 1, where=np.cumsum(fill_zone) != 0,
                    color=cyan, alpha=0.5)

    # add annotations
    if delay != 0:
        for start, stop in zip(start_idx, stop_idx):
            middle = 0.7 * time[sel][start] + 0.3 * time[sel][stop]
            ax.annotate(r"$\tau_0$", (middle, -1), xycoords='data')
    if phi_0 != 0:
        # ax.annotate(r"$\cos(\phi_0)$", (0, np.cos(phi_0)), xycoords='data')
        ticks = [-1, 0, np.cos(phi_0), 1]
        ticklabels = ['-1', '0', r'$\cos(\phi_0)$', '1']
        ax.set_yticks(ticks)
        ax.set_yticklabels(ticklabels)

    # fill the horizontal interval between cos(phi_0) and 1
    ax.fill_between(time[sel], np.cos(phi_0), 1, color=cyan, alpha=0.5)
    # plot the squares of the theta peaks
    ax.plot(time[sel][theta_peak_inds], theta[sel][theta_peak_inds], 's',
            color=lines_theta[0].get_color())
    # plot the circles of maximum gamma amplitude
    ax.plot(time[sel][gamma_peak_inds], modulation[sel][gamma_peak_inds], 'o',
            color=lines_modulation[0].get_color())

    ax.set_xlim([0, t_plot])
    ax.set_xlabel('Time (s)')
    ax.text(0.99, 0.22, r'$\phi_0 = %s$' % (phase_string(phi_0), ),
            horizontalalignment='right', transform=ax.transAxes)
    ax.text(0.99, 0.08, r'$\tau_0 = %.0f \;\mathrm{ms}$' % (delay * 1000, ),
            horizontalalignment='right', transform=ax.transAxes)

    return theta + gamma + noise_level * rng.randn(*gamma.shape)


def fit_dar_and_plot(sig, ax_logl, ax_phase, phi_0, random_state=None):
    dar_model = DAR(ordar=10, ordriv=2)
    est = DelayEstimator(fs, dar_model=dar_model, low_fq=low_fq,
                         low_fq_width=bandwidth,
                         random_state=random_state)
    est.fit(sig)
    est.plot(ax=ax_logl)

    # plot the modulation of the best model
    est.best_model_.plot(ax=ax_phase, mode='c', frange=plot_fq_range)

    ax_phase.set_title('')
    ticks = [-np.pi, phi_0, np.pi]
    ax_phase.set_xticks(ticks)
    ax_phase.set_xticklabels([r'$%s$' % phase_string(d) for d in ticks])
    ax_phase.grid('on')
    ax_phase.grid(color=(0.5, 0.5, 0.5))


# initialize the plots
rng = np.random.RandomState(3)
fig, axs = plt.subplots(4, 3, figsize=(18, 12),
                        gridspec_kw={'width_ratios': [3, 1, 1]})

# loop over the four conditions
for phi_0_, delay_, axs_ in zip([0, phi_0, 0, phi_0], [0, 0, delay, delay],
                                axs):
    sig = simulate_and_plot(phi_0=phi_0_, delay=delay_, ax=axs_[0], rng=rng)
    fit_dar_and_plot(sig, axs_[1], axs_[2], phi_0=phi_0_, random_state=rng)

plt.tight_layout()
plt.show()s
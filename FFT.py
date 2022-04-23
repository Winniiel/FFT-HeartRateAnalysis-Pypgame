# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 21:44:13 2022

@author: winni
"""

import numpy as np
from scipy import fftpack, signal
from matplotlib import pyplot as plt
import pandas as pd
from scipy.io import wavfile
import pandas as pd
import sys, os, os.path


time_step=1/44100
noise_amplitude=0.25
noise_amplitude2=0.5



freq1=400 #1Hz
period1 = 1/freq1
time_vec = np.arange(0, 1, time_step)
sig1 = 1000*(np.sin(2 * np.pi / period1 * time_vec))


freq2=600 #1Hz
period2 = 1/freq2
time_vec = np.arange(0, 1, time_step)
sig2 = noise_amplitude*1000*(np.sin(2 * np.pi / period2 * time_vec))



freq3=800 #1Hz
period3 = 1/freq3
time_vec = np.arange(0, 1, time_step)
sig3 = noise_amplitude2*1000*(np.sin(2 * np.pi / period3 * time_vec))

#combine three signals
sig = sig1 + sig2 + sig3
plt.figure(figsize=(60,30))
plt.title('Combined Signals (410Hz, 654Hz, 759Hz)', fontsize=80)
plt.ylabel('Amplitude', fontsize=60)
plt.xlabel('Time (s)', fontsize=60)
plt.xticks(fontsize=55)
plt.yticks(fontsize=55)
plt.xlim(0,1)
plt.plot(time_vec, sig)
plt.savefig('Combined_Signal')


# turn combined signal into .wav file
wavfile.write('1.wav', 44100, sig.astype(np.int16))

# fft and power to signal
sig_fft = fftpack.fft(sig)
power = np.abs(sig_fft)**2
sample_freq = fftpack.fftfreq(sig.size, d=time_step)
plt.figure(figsize=(60, 30))
plt.title('Signal in Frequency Domain', fontsize=80)
plt.ylabel('Power', fontsize=60)
plt.xlabel('Frequency (Hz)', fontsize=60)
plt.xticks(fontsize=55)
plt.yticks(fontsize=55)
plt.xlim(-1000,1000)
plt.plot(sample_freq, power)
plt.savefig('FFT_Unfiltered')

# finding peak frequency
pos_mask = np.where(sample_freq > 0)
freqs = sample_freq[pos_mask]
peak_freq = freqs[power[pos_mask].argmax()]

# filter out high frequencies
high_freq_fft = sig_fft.copy()
high_freq_fft[np.abs(sample_freq) > peak_freq] = 0
filtered_sig = fftpack.ifft(high_freq_fft)

# turn filtered signal into .wav file
wavfile.write('2.wav', 44100, filtered_sig.astype(np.int16))

# FFT graph
plt.figure(figsize=(60,30))
plt.title('Original and Filtered Time Domain Signals', fontsize=80)
plt.plot(time_vec, sig, label='Original signal')
plt.plot(time_vec, filtered_sig, linewidth=5, label='Filtered signal')
plt.xlabel('Time (s)', fontsize=60)
plt.ylabel('Amplitude', fontsize=60)
plt.xticks(fontsize=55)
plt.yticks(fontsize=55)
plt.xlim(0,.01)
plt.legend(loc='best')
plt.savefig('Original_and_Filtered_Time_Domain')

# filter signal FFT confirmation
sig_fft1 = fftpack.fft(filtered_sig)
power = np.abs(sig_fft1)**2
sample_freq = fftpack.fftfreq(filtered_sig.size, d=time_step)

#filtered FFT
plt.figure(figsize=(60, 30))
plt.title('Filtered Signal in Frequency Domain', fontsize=80)
plt.ylabel('Power', fontsize=60)
plt.xlabel('Frequency (Hz)', fontsize=60)
plt.xticks(fontsize=55)
plt.yticks(fontsize=55)
plt.xlim(-1500,1500)
plt.plot(sample_freq, power)
plt.savefig('FFT_Filtered')
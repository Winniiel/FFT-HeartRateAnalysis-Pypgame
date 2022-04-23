# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 22:03:52 2022

@author: winni
"""

import matplotlib.pyplot as plt
import heartpy as hp

sample_rate=300
data = hp.get_data ('HEARTBEAT.csv')
plt.figure(figsize=(30,4))
plt.plot(data)
plt.show()

Peak, Heart= hp.process(data, sample_rate)

plt.figure(figsize=(30,4))
hp.plotter(Peak, Heart)

#display computed measures
for measure in Heart.keys():
    print('%s: %f' %(measure,Heart[measure]))
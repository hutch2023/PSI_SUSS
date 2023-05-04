#!/bin/usr/python3
# Generating Stacked Bar Charts

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

title = "PSI Communication Cost as Sender Size Varies"
subtitle = "Receiver Set Size: 100; BF False Positive Rate: $2^{-40}$"

xs = ['$2^7$', '$2^8$', '$2^9$', '$2^{10}$']
ys_bf = [932, 1855, 3702, 7395]
ys_nobf = [4100, 8196, 16388, 32772]

fname = "varying_ksize.png"
xaxis = "Sender Set Size (n)"
yaxis = "Set K Size (bytes)"

r = np.arange(4)
width = 0.25

plt.bar(r,ys_bf,color='g',width=width,label='Bloom Filter')
plt.bar(r+width,ys_nobf,color='r',width=width,label='No Bloom Filter')
plt.xlabel(xaxis)
plt.ylabel(yaxis)
plt.suptitle(title, fontsize=14)
plt.title(subtitle, fontsize=10)
plt.legend(loc='upper left')
plt.xticks(r + width/2,xs)
plt.tight_layout()
plt.savefig("pngs/" + fname)

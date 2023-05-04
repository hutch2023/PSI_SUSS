#!/bin/usr/python3
# Generating Stacked Bar Charts

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

title = "Comparing Computational Costs of Streaming to Not Streaming"
subtitle = "Receiver Set Size: 100; BF False Positive Rate: $2^{-40}$"

xs = ['$2^7$', '$2^8$', '$2^9$', '$2^{10}$']
streaming = np.array([1.3867, 2.6915, 4.7816, 10.5686])
not_streaming = np.array([1.4014, 2.7675, 5.6601, 10.7445])

fname = "comp_streaming.png"
xaxis = "Sender Set Size (n)"
yaxis = "Total Online Time (s)"

r = np.arange(4)
width = 0.25

def barplot(ys_bf, ys_nobf):
    plt.bar(r,ys_bf,width=width,color="gold",label="Streaming")
    plt.bar(r+width+0.05,ys_nobf,width=width,color="navy",label="Not Streaming")

barplot(streaming, not_streaming)

plt.xlabel(xaxis)
plt.ylabel(yaxis)
plt.suptitle(title, fontsize=14)
plt.title(subtitle, fontsize=10)
plt.xticks(r + width/2 + 0.025,xs)
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("pngs/" + fname)

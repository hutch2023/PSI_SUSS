#!/bin/usr/python3
# Generating Stacked Bar Charts

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

title = "PSI Computational Costs as Sender Size Varies"
subtitle = "Receiver Set Size: 100; BF False Positive Rate: $2^{-40}$"

xs = ['$2^7$', '$2^8$', '$2^9$', '$2^{10}$']
mgs_bf      = np.array([0.0176, 0.018, 0.0349, 0.0098])
mgs_nobf    = np.array([0.0098, 0.0168, 0.0096, 0.0098])

his_bf      = np.array([0.000, 0.0001, 0.0003, 0.0006])
his_nobf    = np.array([0.0001, 0.0001, 0.0003, 0.0007])

gks_bf      = np.array([1.0921, 2.1344, 4.3208, 8.6117])
gks_nobf    = np.array([1.0822, 2.1026, 4.1503, 8.0982])

gsr_bf      = np.array([1.8251, 1.4713, 1.7619, 1.6284])
gsr_nobf    = np.array([1.5867, 1.6314, 1.8488, 1.7584])

itr_bf      = np.array([0.0454, 0.0451, 0.0473, 0.0445])
itr_nobf    = np.array([0.0453, 0.0443, 0.0451, 0.045])

gmr_bf      = np.array([0.8011, 0.8159, 0.7904, 0.7606])
gmr_nobf    = np.array([0.7978, 0.8117, 0.9456, 0.7788])

ckr_bf      = np.array([0.0032, 0.0026, 0.0029, 0.0016])
ckr_nobf    = np.array([0.0001, 0.0001, 0.0001, 0.0001])

fname = "times_500s.png"
xaxis = "Sender Set Size (n)\nLeft Column: Our Protocol; Right Column: The RT Protocol"
yaxis = "Time (s)"

r = np.arange(4)
width = 0.25
bottom_bf = np.array([0,0,0,0])
bottom_nobf = np.array([0,0,0,0])

def barplot(ys_bf, ys_nobf, label, color, bf_bottom, nobf_bottom):
    plt.bar(r,ys_bf,width=width,label=label,bottom=bf_bottom,color=color)
    plt.bar(r+width+0.05,ys_nobf,width=width,bottom=nobf_bottom,color=color)
    return bf_bottom + ys_bf, nobf_bottom + ys_nobf

bottom_bf, bottom_nobf = barplot(mgs_bf, mgs_nobf, "Message Generation", "red", bottom_bf, bottom_nobf)
bottom_bf, bottom_nobf = barplot(his_bf, his_nobf, "Sender Hash Items", "purple", bottom_bf, bottom_nobf)
bottom_bf, bottom_nobf = barplot(gks_bf, gks_nobf, 'Generate K', "navy", bottom_bf, bottom_nobf)

bottom_bf, bottom_nobf = barplot(gsr_bf, gsr_nobf, "Generate Secrets", "gold", bottom_bf, bottom_nobf)
bottom_bf, bottom_nobf = barplot(itr_bf, itr_nobf, "Interpolate", "green", bottom_bf, bottom_nobf)
bottom_bf, bottom_nobf = barplot(gmr_bf, gmr_nobf, 'Generate Matches', "silver", bottom_bf, bottom_nobf)
bottom_bf, bottom_nobf = barplot(ckr_bf, ckr_nobf, "Check K", "orange", bottom_bf, bottom_nobf)

plt.xlabel(xaxis)
plt.ylabel(yaxis)
plt.suptitle(title, fontsize=14)
plt.title(subtitle, fontsize=10)
plt.legend(loc='upper left')
plt.xticks(r + width/2 + 0.025,xs)
plt.tight_layout()
plt.savefig("pngs/" + fname)

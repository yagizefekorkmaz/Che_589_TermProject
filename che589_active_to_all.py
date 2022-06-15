# -*- coding: utf-8 -*-
"""Che589_Active_to_All.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LyZGtAdkC1SQHEDahLUfosD-OHtZDyp7
"""

import numpy as np
import math
import pandas as pd
import MDAnalysis as mda

#-------MDAnalysis Part---

u = mda.Universe("sarscov2.pdb","all_traj.dcd")
alpha = u.select_atoms('name CA')

#-----Distances of One Active Site alpha-C to every alpha-C-----------

start_frame = 0
end_frame = 100000
active_carbon = 268
atom_number = 320
dist = np.zeros([1,atom_number])
dist_to_write = np.zeros([atom_number,1])
frame = 1
dist_list = []

for ts in u.trajectory[start_frame:end_frame:1] :
  for i in range(0,atom_number):
    dist[0,i] = math.dist(alpha.positions[active_carbon],alpha.positions[i])
    dist = np.reshape(dist,(1,320))
  dist_list.append(dist)
  dist = np.zeros([1,atom_number])
  frame = frame+1

#--------Calculating the Changes in Distances------

dist_list_pd = pd.array(dist_list)
atom_number = 320
delta = np.zeros([320,np.size(dist_list_pd)-1])
bin_delta = np.zeros([320,np.size(dist_list_pd)-1])


for j in range(0,int(np.size(dist_list_pd))-1) :
  for i in range(0,atom_number-1) :
    delta[i,j] = dist_list_pd[j][0,i] - dist_list_pd[j+1][0,i]
    if delta[i,j]>0.9:
      bin_delta[i,j] = +1
    if delta[i,j]<-0.9:
      bin_delta[i,j] = -1
    if delta[i,j]<0.9 and delta[i,j]>-0.9:
      bin_delta[i,j] = 0

#--------Writing the bin_delta's into a txt file------

f = open('bin_delta_cutoff_0.9.txt', 'w')
np.savetxt(f,bin_delta,fmt='%+1d' ,delimiter=" ")
f.close()

#------Read dX_1_2.txt------

delta_x = pd.read_csv('bin_delta_cutoff_0.9.txt', sep=" ", header=None)

#-------Sum of All Rows-----

sum_of_rows = np.zeros([np.shape(delta_x)[0],1])

for j in range(0,np.shape(delta_x)[0]) :
  for i in range(0,np.shape(delta_x)[1]) :
    sum_of_rows[j,0] = sum_of_rows[j,0] + delta_x.iloc[j,i]

f = open('sum_of_rows_cutoff_0.9.txt', 'w')
np.savetxt(f,sum_of_rows,fmt='%+1d' ,delimiter=" ")
f.close()
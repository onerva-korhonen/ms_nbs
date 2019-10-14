#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:45:22 2019

@author: onerva

Parameters used for the NBS analysis of the MS patients
"""
# File paths

subjects = [] # TODO: this should be a list of subject folders
tsFileName = '' # TODO: this should be the name of the time series NIFTI file

ROIMaskPath = 'atlases/brainnetome/BNA_MPM_rois_2mm.nii'

# NBS
thres = 2 # This is the test statistic threshold for NBS
k = 1000 # This is the number of permutations used in NBS
tail = 'both' # I'll use the two-tailed t-test where the alternative hypothesis is "x and y are not equal"
betweenPaired = False # To compare groups I'll use the population (2-sample) t-test as the observations are not paired
withinPaired = True # To compare time windows of a subject I'll use the paired (1-sample) t-test as the observations are paired 
verbose = True


# visualization
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:45:22 2019

@author: onerva

Parameters used for the NBS analysis of the MS patients
"""
# Experimental set-up

tasks = ['Mental','Physique']
conditions = ['mild','middle','strong']

# File paths

subjectsMentalFirst = [] # TODO: this should be a list of subject folders
subjectsPhysicalFirst = []
subjects = subjectsMentalFirst + subjectsPhysicalFirst

# NOTE: start paths with '/'; this will help combining later on
inputPathsMild = [[]] # TODO: this will be a list of lists, each sublist containing the names of files belonging to the same block of task 1
inputPathsMiddle = [[]]
inputPathsStrong = [[]]
inputPaths = [inputPathsMild,inputPathsMiddle,inputPathsStrong]

outputPathsMild = ['combined-timeseries-mild-press-block' + str(n) + '.nii' for n in len(inputPathsMild)] # names of the combined time series NIFTI files
outputPathsMiddle = ['combined-timeseries-middle-press-block' + str(n) + '.nii' for n in len(inputPathsMiddle)]
outputPathsStrong = ['combined-timeseries-strong-press-block' + str(n) + '.nii' for n in len(inputPathsStrong)]
outputPaths = [outputPathsMild,outputPathsMiddle,outputPathsStrong]

ROIMaskPath = 'atlases/brainnetome/BNA_MPM_rois_2mm.nii'

nbsOutputPath = '/home/onerva/projects/nbs/output/nbs-results-'

# NBS
primaryThres = 4 # This is the test statistic threshold for NBS
pThresh = 0.001 # This is the final threshold of significance for components
k = 1000 # This is the number of permutations used in NBS
tail = 'both' # I'll use the two-tailed t-test where the alternative hypothesis is "x and y are not equal"
betweenPaired = False # To compare groups I'll use the population (2-sample) t-test as the observations are not paired
withinPaired = True # To compare time windows of a subject I'll use the paired (1-sample) t-test as the observations are paired 
verbose = True


# visualization

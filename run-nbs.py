#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:03:32 2019

@author: onerva

A frontend script for running the NBS analysis
"""
import numpy as np

import ROIplay

import parameters as params
import functions

subjects = params.subjects
ROIMaskPath = params.ROIMaskPath

# Downloading data and calculating adjacency matrices
for subject in subjects:
    dataPath = subject + params.tsFileName
    ROIMaps,ROITs = ROIplay.pickROITs(dataPath,ROIMaskPath)
    adjacencyMatrix = np.corrcoef(ROITs)
# TODO: next: from adjacency  matrices construct input for nbs
# run nbs
# visualize results???



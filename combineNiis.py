#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:20:52 2020

@author: onerva

A script for transforming the MS data to a form suitable for further analysis.
The data has been saved as single slices, and this script combines them into
time series.
"""
import nibabel as nib

import parameters as params
import functions

tasks = params.tasks
conditions = params.conditions

subjectsMentalFirst = params.subjectsMentalFirst
subjectsPhysicalFirst = params.subjectsPhysicalFirst
subjects = subjectsMentalFirst+subjectsPhysicalFirst
prefixes = params.prefixes
inputPaths = params.inputPaths
individualMaskPaths = params.allIndividualMaskPaths
outputPaths = params.outputPaths

# The following loops are over all possible combinations of task and condition (see params for details)

for task,subjectPrefixes, maskPaths in zip(tasks,prefixes,individualMaskPaths):
    for condition,inputs,outputs in zip(conditions,inputPaths,outputPaths):
        nBlocks = len(inputs)
        for subject, subjectPrefix, maskPath in zip(subjects, subjectPrefixes, maskPaths):
            print subject
            mask = nib.load(maskPath)
            maskImg = mask.get_fdata()
            for block, output in zip(inputs, outputs):
                block = [subject + '/' + task + '/' + subjectPrefix + fName for fName in block]
                output = subject + '/' + task + '/' + output
                functions.combineNiis(block,output,mask=maskImg)

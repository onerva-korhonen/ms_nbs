#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:44:16 2020

@author: onerva

A script for additional preprocessing of the MS data before NBS analysis. This
script includes options for resampling the data and for registering it to the
MNI standard space as well as for constructing and saving a group-level brain
mask.

NOTE: parts of this script make use of the FSL software (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki).
Ensure that you have it installed before running the script.
"""
import numpy as np
import cPickle as pickle
from bct import nbs
import nibabel as nib
import os

import parameters as params

import pdb; pdb.set_trace()

tasks = params.tasks
conditions = params.conditions

subjectsMentalFirst = params.subjectsMentalFirst
subjectsPhysicalFirst = params.subjectsPhysicalFirst
subjects = subjectsMentalFirst+subjectsPhysicalFirst
prefixes = params.prefixes
inputPaths = params.inputPaths
anatomicalInputPaths = params.anatomicalInputPaths
individualMaskPaths = params.allIndividualMaskPaths
outputPaths = params.outputPaths
resampledPaths = params.resampledPaths
ROIMaskPath = params.ROIMaskPath
nbsOutputPath = params.nbsOutputPath
groupMaskSaveName = params.groupMaskSaveName

regMatrixStruc2StdPaths = params.regMatrixStruc2StdPaths
regMatrixFunc2StrucPaths = params.regMatrixFunc2StrucPaths
regMatrixFunc2StdPaths = params.regMatrixFunc2StdPaths
anatomicalStandardSpacePaths = params.anatomicalStandardSpacePaths
standardSpacePaths = params.standardSpacePaths

resampleResolution = params.resampleResolution
MNITemplate = params.MNITemplate

# Edit the following variables to pick the steps to be performed

resampleNiis = True
useNonResampled = False # set to True to use original, non-resampled data
registerToMNI = True
constructGroupMask = True

# The following loops are over all possible combinations of task and condition (see params for details)

for i,task,subjectPrefixes,maskPaths in enumerate(zip(tasks,prefixes,individualMaskPaths)):
    for j,condition,inputs,outputs in enumerate(zip(conditions,inputPaths,outputPaths)):
        nBlocks = len(inputs)
        
        if resampleNiis:
        # Case for resampling the data to a given resolution, for example to match an atlas template
            resampled = resampledPaths[j]
            for subject in subjects:
                for output, resampledPath in zip(outputs,resampled):
                    niiToResample = subject + '/' + task + '/' + output
                    resampledOutputPath = subject + '/' + task + '/' + resampledPath
                    os.system('flirt -applyisoxfm ' + str(resampleResolution) + ' -in ' + niiToResample + ' -ref ' + MNITemplate  + ' -out ' + resampledOutputPath + ' -interp nearestneighbour')
                    
        elif useNonResampled:
        # If the data will not be resampled, let's just ensure that the paths are defined correctly for further steps
            resampled = outputs
            resampledPaths = outputPaths
            
        if registerToMNI:
        # Case for registering the data to the MNI standard space
            anatomicalInputs = anatomicalInputPaths[i][j]
            regMatricesStruc2Std = regMatrixStruc2StdPaths[j]
            regMatricesFunc2Struc = regMatrixFunc2StrucPaths[j]
            regMatricesFunc2Std = regMatrixFunc2StdPaths[j]
            anatomicalStandardSpaces = anatomicalStandardSpacePaths[j]
            standardSpaces = standardSpacePaths[j]
            for subject in subjects:
                for anatomicalInput,regMatrixStruc2Std,regMatrixFunc2Struc,regMatrixFunc2Std,anatomicalStandardSpace,standardSpace,resampledPath in zip(anatomicalInputs,regMatricesStruc2Std,regMatricesFunc2Struc,regMatricesFunc2Std,anatomicalStandardSpaces,standardSpaces,resampled):
                    regMatrixStruc2StdPath = subject + '/' + task + '/' + regMatrixStruc2Std
                    regMatrixFunc2StrucPath = subject + '/' + task + '/' + regMatrixFunc2Struc
                    regMatrixFunc2StdPath = subject + '/' + task + '/' + regMatrixFunc2Std
                    anatomicalStandardSpacePath = subject + '/' + task + '/' + anatomicalStandardSpace
                    standardSpacePath = subject + '/' + task + '/' + standardSpace
                    niiToRegister = subject + '/' + task + '/' + resampledPath
                    # First, let's register the anatomical image to the standard space
                    os.system('flirt -i ' + anatomicalInput + ' -ref ' + MNITemplate + ' -omat ' + regMatrixStruc2StdPath + ' -bins 256 -cost corratio -searchrx -120 120 -searchy -120 120 -searchz -120 120 -dof 12')
                    os.system('flirt -in ' + anatomicalInput + ' -applyxfm -init ' + regMatrixStruc2StdPath + ' -out ' + anatomicalStandardSpacePath + ' -paddingsize 0.0 -interp trilinear -ref ' + MNITemplate)
                    # Next, let's register the functional image to the anatomical image
                    os.system('flirt -in ' + niiToRegister + ' -ref ' + anatomicalInput + ' -omat ' + regMatrixFunc2StrucPath + ' -bins 256 -cost corratio -searchrx -120 120 -searchry -120 120 -searchrz -120 120 -dof 9')
                    # Next, let's concatenate the registration matrices to get the registration matrix to the standard space for the functional image
                    os.system('convert_xfm -concat ' + regMatrixStruc2StdPath + ' -omat ' + regMatrixFunc2StdPath + regMatrixFunc2StrucPath)
                    # Finally, let's register the functional image to the standard space
                    os.system('flirt -in ' + niiToRegister + ' -applyxfm -init ' + regMatrixFunc2StdPath + ' -out ' + standardSpacePath + ' -paddingsize 0.0 -interp trilinear -ref' + MNITemplate)
        
        if construcGroupMask:
        # Case for multiplying the individual brain masks to construct a group-level mask
            for k, subject in enumerate(subjects):
        # Data has already been combined to time series in nii format. Let's greate a group gray matter mask
                print subject
                for l, block in enumerate(resampled):
                    dataPath = subject + '/' + task + '/' + block
                    data = ROIplay.readNii(dataPath)
                    if k == l == 0:
                        groupMask = np.ones(data.shape[0:3])
                    groupMask[np.where(np.prod(data,axis=3)==0)] = 0
            groupMaskSavePath = os.path.split(os.path.split(subjects[0])[0])[0] + '/' + groupMaskSaveName
            outputImg = nib.Nifti1Image(groupMask,affine=None)     
            nib.save(outputImg,groupMaskSavePath)

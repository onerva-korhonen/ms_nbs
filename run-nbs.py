#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:03:32 2019

@author: onerva

A frontend script for running the NBS analysis
"""
import numpy as np
import cPickle as pickle
from bct import nbs
import nibabel as nib
import os
import system

import ROIplay

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
resampledPaths = params.resampledPaths
ROIMaskPath = params.ROIMaskPath
nbsOutputPath = params.nbsOutputPath
groupMaskSaveName = params.groupMaskSaveName

resampleResolution = params.resampleResolution
resampleTemplate = params.resampleTemplate

primaryThres = params.primaryThres
pThres = params.pThresh
k = params.k
tail = params.tail
betweenPaired = params.betweenPaired
withinPaired = params.withinPaired
verbose = params.verbose

# Edit the following variables to pick the comparisons to be performed

concatenateNiis = False
resampleNiis = True


compareGroups = True
compareFirstLast = False
compareConsequtive = False
compareConditions = False

# The following loops are over all possible combinations of task and condition (see params for details)

for task,subjectPrefixes, maskPaths in zip(tasks,prefixes,individualMaskPaths):
    for condition,inputs,outputs,resampled in zip(conditions,inputPaths,outputPaths,resampledPaths):
        nBlocks = len(inputs)
        
        if concatenateNiis:
        
        # Data has been saved as single slides. Let's combine them into time series

            for subject, subjectPrefix, maskPath in zip(subjects, subjectPrefixes, maskPaths):
                print subject
                mask = nib.load(maskPath)
                maskImg = mask.get_fdata()
                for block, output in zip(inputs, outputs):
                    block = [subject + '/' + task + '/' + subjectPrefix + fName for fName in block]
                    output = subject + '/' + task + '/' + output
                    functions.combineNiis(block,output,mask=maskImg)
                    
        if resampleNiis:
            
        # Case for resampling the data to a given resolution, for example to match an atlas template
        # NOTE: resampling is done by FSL FLIRT (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki) that need to be installed
            for subject in subjects:
                for output, resampledPath in zip(outputs,resampledPaths):
                    niiToResample = subject + '/' + task + '/' + output
                    system('flirt -applyisoxfm ' + resampleResolution + ' -in ' + niiToResample + ' -ref ' + resampleTemplate  + ' -out ' + resampledPath + ' -interp nearestneighbour')
            
        for i, subject in enumerate(subjects):
        # Data has already been combined to time series in nii format. Let's greate a group gray matter mask
            print subject
            for j, block in enumerate(resampled):
                dataPath = subject + '/' + task + '/' + block
                data = ROIplay.readNii(dataPath)
                if i == j == 0:
                    groupMask = np.ones(data.shape[0:3])
                groupMask = np.prod(data,axis=3)*groupMask
        groupMask[np.where(np.abs(groupMask)>0)] = 1
        groupMaskSavePath = os.path.split(os.path.split(subjects[0])[0])[0] + groupMaskSaveName
        outputImg = nib.Nifti1Image(groupMask,affine=None)     
        nib.save(outputImg,groupMaskSavePath)
                    
        # Case 1: comparison between groups
        if compareGroups:
        # Downloading data and calculating adjacency matrices (read all blocks, average adjacency matrices across groups)
            mentalFirstMatrices = []
            physicalFirstMatrices = []
            for subject in subjectsMentalFirst:
                adjacencyMatrices = []
                for dataPath in outputs:
                    dataPath = subject + '/' + task + '/' + dataPath
                    ROIMaps,ROITs = ROIplay.pickROITs(dataPath,ROIMaskPath,grayMaskPath=groupMaskSavePath)
                    adjacencyMatrices.append(functions.fisherTransform(np.corrcoef(ROITs)))
                mentalFirstMatrices.append(np.sum(adjacencyMatrices,axis=0)/nBlocks)
            mentalFirstMatrices = np.stack(mentalFirstMatrices,axis=2)
                
            for subject in subjectsPhysicalFirst:
                adjacencyMatrices = []
                for dataPath in outputs:
                    dataPath = subject + dataPath
                    ROIMaps,ROITs = ROIplay.pickROITs(dataPath,ROIMaskPath)
                    adjacencyMatrices.append(functions.fisherTransform(np.corrcoef(ROITs)))
                physicalFirstMatrices.append(np.sum(adjacencyMatrices,axis=0)/nBlocks)
            physicalFirstMatrices = np.stack(physicalFirstMatrices,axis=2)
            
            # Running NBS
            pval, adj, null = nbs(mentalFirstMatrices,physicalFirstMatrices,primaryThres,k,tail,betweenPaired,verbose)
            nSignificant = len(np.where(pval<pThres))
            print('Task: ' + task + ', condition: ' + condition + ', between groups: ' + str(nSignificant) + ' significantly different components found')
    
            # Saving results
            savePath = nbsOutputPath + 'between-groups_' + task + '_' + condition + '.pkl'
            data = {'condition':condition,'task':task,'pval':pval,'adj':adj,'null':null}
            with open(savePath, 'wb') as f:
                pickle.dump(data, f, -1)
                
            # TODO: add visualization here?
            
        # Case 2: Inside groups between the first and last task blocks
        if compareFirstLast:
        # Downloading data and calculating adjacency matrices (for first and last blocks, separately for both groups)
            firstMatricesMental = []
            lastMatricesMental = []
            firstMatricesPhysical = []
            lastMatricesPhysical = []
            
            for subject in subjectsMentalFirst:
                _,firstROITs = ROIplay.pickROITs(subject + outputs[0],ROIMaskPath)
                firstMatricesMental.append(functions.fisherTransform(np.corrcoef(firstROITs)))
                _,lastROITs = ROIplay.pickROITs(subject + outputs[-1],ROIMaskPath)
                lastMatricesMental.append(functions.fisherTransform(np.corrcoef(lastROITs)))
            firstMatricesMental = np.stack(firstMatricesMental,axis=2)
            lastMatricesMental = np.stack(lastMatricesMental,axis=2)
            
            for subject in subjectsPhysicalFirst:
                _,firstROITs = ROIplay.pickROITs(subject + outputs[0],ROIMaskPath)
                firstMatricesPhysical.append(functions.fisherTransform(np.corrcoef(firstROITs)))
                _,lastROITs = ROIplay.pickROITs(subject + outputs[-1],ROIMaskPath)
                lastMatricesPhysical.append(functions.fisherTransform(np.corrcoef(lastROITs)))
            firstMatricesPhysical = np.stack(firstMatricesMental,axis=2)
            lastMatricesPhysical = np.stack(lastMatricesMental,axis=2)
            
            # Running NBS
            pval, adj, null = nbs(firstMatricesMental,lastMatricesMental,primaryThres,k,tail,withinPaired,verbose)
            nSignificant = len(np.where(pval<pThres))
            print('Task: ' + task + ', condition: ' + condition + ', mental first vs last: ' + str(nSignificant) + ' significantly different components found')
            
            # Saving results
            savePath = nbsOutputPath + 'mental-first-vs-last_' + task + '_' + condition + '.pkl'
            data = {'condition':condition,'task':task,'pval':pval,'adj':adj,'null':null}
            with open(savePath, 'wb') as f:
                pickle.dump(data, f, -1)
                
            # TODO: add visualization here?
                
            # Running NBS
            pval, adj, null = nbs(firstMatricesPhysical,lastMatricesPhysical,primaryThres,k,tail,withinPaired,verbose)
            nSignificant = len(np.where(pval<pThres))
            print('Task: ' + task + ', condition: ' + condition + ', physical first vs last: ' + str(nSignificant) + ' significantly different components found')
            
            # Saving results
            savePath = nbsOutputPath + 'physical-first-vs-last_' + task + '_' + condition + '.pkl'
            data = {'condition':condition,'task':task,'pval':pval,'adj':adj,'null':null}
            with open(savePath, 'wb') as f:
                pickle.dump(data, f, -1)
                
            # TODO: add visualization here?
                
        # Case 3: Inside groups between consequtive blocks
        if compareConsequtive:
            firstMatricesMental = []
            # First, let's calculate adjacency matrix for the first block
            for subject in subjectsMentalFirst:
                _,firstROITs = ROIplay.pickROITs(subject + outputs[0],ROIMaskPath)
                firstMatricesMental.append(functions.fisherTransform(np.corrcoef(firstROITs)))
            firstMatricesMental = np.stack(firstMatricesMental,axis=2)
            # Looping over blocks, let's calculate the next adjacency matrix, run NBS, and save results
            for i in range(nBlocks-1):
                lastMatricesMental = []
                for subject in subjectsMentalFirst:
                    _,lastROITs = ROIplay.pickROITs(subject + outputs[i+1],ROIMaskPath)
                    lastMatricesMental.append(functions.fisherTransform(np.corrcoef(lastROITs)))
                lastMatricesMental = np.stack(lastMatricesMental,axis=2)
                pval, adj, null = nbs(firstMatricesMental,lastMatricesMental,primaryThres,k,tail,withinPaired,verbose)
                nSignificant = len(np.where(pval<pThres))
                print('Task: ' + task + ', condition: ' + condition + ', mental ' + str(i) + ' vs ' + str(i+1) + ': ' + str(nSignificant) + ' significantly different components found')
                savePath = nbsOutputPath + 'mental-' + str(i) + '-vs-' + str(i+1) + '_' + task + '_' + condition + '.pkl'
                data = {'condition':condition,'task':task,'pval':pval,'adj':adj,'null':null}
                with open(savePath, 'wb') as f:
                    pickle.dump(data, f, -1)
                firstMatricesMental = lastMatricesMental.copy()
             
            firstMatricesPhysical = []
            # First, let's calculate adjacency matrix for the first block
            for subject in subjectsPhysicalFirst:
                _,firstROITs = ROIplay.pickROITs(subject + outputs[0],ROIMaskPath)
                firstMatricesPhysical.append(functions.fisherTransform(np.corrcoef(firstROITs)))
            firstMatricesPhysical = np.stack(firstMatricesPhysical,axis=2)
            # Looping over blocks, let's calculate the next adjacency matrix, run NBS, and save results
            for i in range(nBlocks-1):
                lastMatricesPhysical = []
                for subject in subjectsPhysicalFirst:
                    _,lastROITs = ROIplay.pickROITs(subject + outputs[i+1],ROIMaskPath)
                    lastMatricesPhysical.append(functions.fisherTransform(np.corrcoef(lastROITs)))
                lastMatricesPhysical = np.stack(lastMatricesPhysical,axis=2)
                pval, adj, null = nbs(firstMatricesPhysical,lastMatricesPhysical,primaryThres,k,tail,withinPaired,verbose)
                nSignificant = len(np.where(pval<pThres))
                print('Task: ' + task + ', condition: ' + condition + ', physical ' + str(i) + ' vs ' + str(i+1) + ': ' + str(nSignificant) + ' significantly different components found')
                savePath = nbsOutputPath + 'physical-' + str(i) + '-vs-' + str(i+1) + '_' + task + '_' + condition + '.pkl'
                data = {'condition':condition,'task':task,'pval':pval,'adj':adj,'null':null}
                with open(savePath, 'wb') as f:
                    pickle.dump(data, f, -1)
                firstMatricesPhysical = lastMatricesPhysical.copy()
            
    # Case 4: inside groups between conditions (Note: this is inside the task loop but not inside the condition loop)
    if compareConditions: 
        conditionMatrices = [[] for condition in conditions]
        for i, (conditions, inputs, outputs) in enumerate(zip(conditions,inputPaths,outputPaths)):
            for subject in subjectsMentalFirst:
                adjacencyMatrices = []
                for dataPath in outputs:
                    dataPath = subject + dataPath
                    _,ROITs = ROIplay.pickROITs(dataPath,ROIMaskPath)
                    adjacencyMatrices.append(functions.fisherTransform(np.corrcoef(ROITs)))
                conditionMatrices[i].append(np.sum(adjacencyMatrices,axis=0)/nBlocks)
        conditionMatrices = [np.stack(conditionMatrix,axis=2) for conditionMatrix in conditionMatrices]
        
        for i in range(len(conditions)):
            for j in range(i,len(conditions)):
                pval, adj, null = nbs(conditionMatrices[i],conditionMatrices[j],primaryThres,k,tail,withinPaired,verbose)
                nSignificant = len(np.where(pval<pThres))
                print('Task: ' + task + ', mental ' + conditions[i] + ' vs ' + conditions[j] + ': ' + str(nSignificant) + ' significantly different components found')
                savePath = nbsOutputPath + 'mental-' +  conditions[i] + '-vs-' + conditions[j] + '_' + task + '.pkl'
                data = {'condition':conditions[i] + ' vs ' + conditions[j],'task':task,'pval':pval,'adj':adj,'null':null}
                with open(savePath, 'wb') as f:
                    pickle.dump(data, f, -1)
                    
        for i, (conditions, inputs, outputs) in enumerate(zip(conditions,inputPaths,outputPaths)):
            for subject in subjectsPhysicalFirst:
                adjacencyMatrices = []
                for dataPath in outputs:
                    dataPath = subject + dataPath
                    _,ROITs = ROIplay.pickROITs(dataPath,ROIMaskPath)
                    adjacencyMatrices.append(functions.fisherTransform(np.corrcoef(ROITs)))
                conditionMatrices[i].append(np.sum(adjacencyMatrices,axis=0)/nBlocks)
        conditionMatrices = [np.stack(conditionMatrix,axis=2) for conditionMatrix in conditionMatrices]
        
        for i in range(len(conditions)):
            for j in range(i,len(conditions)):
                pval, adj, null = nbs(conditionMatrices[i],conditionMatrices[j],primaryThres,k,tail,withinPaired,verbose)
                nSignificant = len(np.where(pval<pThres))
                print('Task: ' + task + ', physical ' + conditions[i] + ' vs ' + conditions[j] + ': ' + str(nSignificant) + ' significantly different components found')
                savePath = nbsOutputPath + 'physical-' +  conditions[i] + '-vs-' + conditions[j] + '_' + task + '.pkl'
                data = {'condition':conditions[i] + ' vs ' + conditions[j],'task':task,'pval':pval,'adj':adj,'null':null}
                with open(savePath, 'wb') as f:
                    pickle.dump(data, f, -1)





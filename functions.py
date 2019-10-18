#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:51:49 2019

@author: onerva

This file contains all the functions used in the NBS analysis of MS patients
"""
import numpy as np
import networkx as nx
import nibabel as nib
import bct 

import ROIplay

import parameters as params

def combineNiis(inputPaths, outputPath):
    """
    Combines several NIFTI files at paths to a single file. The data of this new file
    consists of the data of the onput files stacked horizontally. The affine of the
    new file is the affine of the first of the input files.
    
    Parameters:
    -----------
    inputPaths: list of strs, paths to the input NIFTI files
    outputPath: str, path to which save the new NIFTI file
    
    Returns:
    --------
    no direct output, saves the new NIFTI file
    """
    outputData = []
    for i, path in enumerate(inputPaths):
        img = nib.load(path)
        outputData.append(img.get_fdata())
        if i == 0:
            affine = img.affine
        #else:
            #outputData = np.concatenate((outputData,img.get_fdata()),axis=)
    outputData = np.stack(outputData,axis=3)
    outputImg = nib.Nifti1Image(outputData,affine)     
    nib.save(outputImg,outputPath)
    
def fisherTransform(data):
    """
    Performs the Fisher Z transform.
    
    Parameters:
    -----------
    data: scalar or np.array
    
    Returns:
    --------
    z: scalar or np.array, Fisher Z-transformed version of data
    """
    z = 0.5*np.log((1+data)/(1-data))
    return z

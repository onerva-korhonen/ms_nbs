#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:45:22 2019

@author: onerva

Parameters used for the NBS analysis of the MS patients
"""
# Experimental set-up

tasks = ['Mental','Physique']
conditions = ['all']#['mild','middle','strong']

# File paths

subjectsMentalFirst = ['/m/cs/scratch/networks/aokorhon/nbs/data/mental_first/' + subject for subject in ['P01_DS','P2_CA','P03_CR','P3_HE','P6_CS','P8_TM','P10_BT','P12_SG','P14_OA','P16_CA','P18_CM','P20_BC','P24_HJ','P26_PC','P28_YM','P30_RD','P33_SL','P37_GS','P39_PR']]
subjectsPhysicalFirst = ['/m/cs/scratch/networks/aokorhon/nbs/data/physical_first/' + subject for subject in ['P00_MM','P1_DE','P4_OF','P7_PE','P9_AM','P11_DA','P13_VM','P15_HD','P17_CL','P19_LM','P23_ZS','P25_LK','P27_MN','P29_MF','P31_CC','P32_ME','P34_FA','P36_LC']]
subjects = subjectsMentalFirst + subjectsPhysicalFirst
# prefixes is a task x subjects 2D list, mentalFirst and physicalFirst subjects combined inside tasks
# NOTE: the order must be the same as in the subjects list
# TODO: add the remaining mentalFirst subjects
prefixes = [['swrasP01-0006-','swrasP2-0003-','swrasP03-0005-','swrasHEP3-0003-','swrasCSP6-0004-','swrasTMP8-0003-','swrasBTP10-0003-','swrasSGP12-0003-','swrasOAP14-0003-','swrasCAP16-0005-','swrasCMP18-0004-','swrasBCP20-0003-','swrasHJP24-0006-','swrasPCP26-0004-','swrasP28-0003-','swrasP30-0003-','swrasP32SL-0003-','swrasP37GS-0003-','swrasP39PR-0003-','swrasP0-0003-','swrasP1-0005-','swrasOFP4-0004-','swrasPEP7-0005-','swrasAMP9-0007-','swrasDAP11-0003-','swrasVMP13-0006-','swrasHDP15-0005-','swrasCLP17-0006-','swrasLMP19-0008-','swrasSZP23-0005-','swrasLKP25-0006-','swrasMNP27-0006-','swrasMFP29-0003-','swrasCCP31-0004-','swrasP31ME-0006-','swrasP33FA-0010-','swrasP36LC-0004-'],
            ['swrasP01-0004-','swrasP2-0006-','swrasP03-0003-','swrasHEP3-0003-','swrasCSP6-0006-','swrasTMP8-0003-','swrasBTP10-0007-','swrasSGP12-0005-','swrasOAP14-0005-','swrasCAP16-0008-','swrasCMP18-0006-','swrasBCP20-0005-','swrasHJP24-0008-','swrasPCP26-0006-','swrasP28-0005-','swrasP30-0005-','swrasP32SL-0005-','swrasP37GS-0004-','swrasP39PR-0005-','swrasP0-0006-','swrasP1-0003-','swrasOFP4-0006-','swrasPEP7-0003-','swrasAMP9-0003-','swrasDAP11-0003-','swrasVMP13-0003-','swrasHDP15-0003-','swrasCLP17-0004-','swrasLMP19-0004-','swrasSZP23-0003-','swrasLKP25-0004-','swrasMNP27-0004-','swrasMFP29-0003-','swrasCCP31-0003-','swrasP31ME-0003-','swrasP33FA-0008-','swrasP36LC-0003-']]

inputPathsMild = [[]] # TODO: this will be a list of lists, each sublist containing the names of files belonging to the same block of task 1
inputPathsMiddle = [[]]
inputPathsStrong = [[]]
inputPathsAll = [['00001-001144-01.nii','00001-001188-01.nii','00001-001232-01.nii','00001-001276-01.nii','00001-001320-01.nii','00001-001364-01.nii','00001-001408-01.nii','00001-001452-01.nii','00001-001496-01.nii',
                  '00001-001540-01.nii','00001-001584-01.nii','00001-001628-01.nii','00001-001672-01.nii','00001-001716-01.nii','00001-001760-01.nii','00001-001804-01.nii','00001-001848-01.nii','00001-001892-01.nii',
                  '00001-001936-01.nii','00001-001980-01.nii','00001-002024-01.nii','00001-002068-01.nii','00001-002112-01.nii','00001-002156-01.nii'],
                 ['00001-004488-01.nii','00001-004532-01.nii','00001-004576-01.nii','00001-004620-01.nii','00001-004664-01.nii','00001-004708-01.nii','00001-004752-01.nii','00001-004796-01.nii',
                  '00001-004840-01.nii','00001-004884-01.nii','00001-004928-01.nii','00001-004972-01.nii','00001-005016-01.nii','00001-005060-01.nii','00001-005104-01.nii','00001-005148-01.nii','00001-005192-01.nii',
                  '00001-005236-01.nii','00001-005280-01.nii','00001-005324-01.nii','00001-005368-01.nii','00001-005412-01.nii','00001-005456-01.nii','00001-005500-01.nii'],
                 ['00001-007788-01.nii','00001-007832-01.nii','00001-007876-01.nii','00001-007920-01.nii','00001-007964-01.nii','00001-008008-01.nii','00001-008052-01.nii','00001-008096-01.nii','00001-008140-01.nii',
                  '00001-008184-01.nii','00001-008228-01.nii','00001-008272-01.nii','00001-008316-01.nii','00001-008360-01.nii','00001-008404-01.nii','00001-008448-01.nii','00001-008492-01.nii','00001-008536-01.nii',
                  '00001-008580-01.nii','00001-008624-01.nii','00001-008668-01.nii','00001-008712-01.nii','00001-008756-01.nii','00001-008800-01.nii'],
                 ['00001-011132-01.nii','00001-011176-01.nii','00001-011220-01.nii','00001-011264-01.nii','00001-011308-01.nii','00001-011352-01.nii','00001-011396-01.nii','00001-011440-01.nii',
                  '00001-011484-01.nii','00001-011528-01.nii','00001-011572-01.nii','00001-011616-01.nii','00001-011660-01.nii','00001-011704-01.nii','00001-011748-01.nii','00001-011792-01.nii','00001-011836-01.nii',
                  '00001-011880-01.nii','00001-011924-01.nii','00001-011968-01.nii','00001-012012-01.nii','00001-012056-01.nii','00001-012100-01.nii','00001-012144-01.nii']]
inputPaths = [inputPathsAll]#[inputPathsMild,inputPathsMiddle,inputPathsStrong]

# these will be tasks x subjects lists
individualMaskPathsMentalFirst = [['/m/cs/scratch/networks/aokorhon/nbs/data/masks_mental_first/' + subject + '/mask_M.nii' for subject in ['P01_DS','P2_CA','P03_CR','P3_HE','P6_CS','P8_TM','P10_BT','P12_SG','P14_OA','P16_CA','P18_CM','P20_BC','P24_HJ','P26_PC','P28_YM','P30_RD','P33_SL','P37_GS','P39_PR']],
                                  ['/m/cs/scratch/networks/aokorhon/nbs/data/masks_mental_first/' + subject + '/mask_P.nii' for subject in ['P01_DS','P2_CA','P03_CR','P3_HE','P6_CS','P8_TM','P10_BT','P12_SG','P14_OA','P16_CA','P18_CM','P20_BC','P24_HJ','P26_PC','P28_YM','P30_RD','P33_SL','P37_GS','P39_PR']]]
individualMaskPathsPhysicalFirst = [['/m/cs/scratch/networks/aokorhon/nbs/data/masks_physical_first/' + subject + '/mask_M.nii' for subject in ['P00_MM','P1_DE','P4_OF','P7_PE','P9_AM','P11_DA','P13_VM','P15_HD','P17_CL','P19_LM','P23_ZS','P25_LK','P27_MN','P29_MF','P31_CC','P32_ME','P34_FA','P36_LC']],
                                    ['/m/cs/scratch/networks/aokorhon/nbs/data/masks_physical_first/' + subject + '/mask_P.nii' for subject in ['P00_MM','P1_DE','P4_OF','P7_PE','P9_AM','P11_DA','P13_VM','P15_HD','P17_CL','P19_LM','P23_ZS','P25_LK','P27_MN','P29_MF','P31_CC','P32_ME','P34_FA','P36_LC']]]
allIndividualMaskPaths = [individualMaskPathsMentalFirst[0] + individualMaskPathsPhysicalFirst[0], individualMaskPathsMentalFirst[1] + individualMaskPathsPhysicalFirst[1]]

outputPathsMild = ['combined-timeseries-mild-press-block' + str(n) + '.nii' for n in range(len(inputPathsMild))] # names of the combined time series NIFTI files
outputPathsMiddle = ['combined-timeseries-middle-press-block' + str(n) + '.nii' for n in range(len(inputPathsMiddle))]
outputPathsStrong = ['combined-timeseries-strong-press-block' + str(n) + '.nii' for n in range(len(inputPathsStrong))]
outputPathsAll = ['combined-timeseries-allTasks-block' + str(n) + '.nii' for n in range(len(inputPathsAll))] 
outputPaths = [outputPathsAll]#[outputPathsMild,outputPathsMiddle,outputPathsStrong]

resampledPaths = [['combined-timeseries-allTasks-block' + str(n) + '_resampled.nii.gz' for n in range(len(inputPathsAll))]]

ROIMaskPath = 'atlases/brainnetome/BNA_MPM_rois_2mm.nii'

nbsOutputPath = '/home/onerva/projects/nbs/output/nbs-results-'

resampleResolution = 4
resampleTemplate = '/m/cs/scratch/networks/aokorhon/nbs/ms_nbs/atlases/MNI152_T1_4mm_brain.nii'

groupMaskSaveName = 'group-gray-matter-mask.nii'

# NBS
primaryThres = 4 # This is the test statistic threshold for NBS
pThresh = 0.001 # This is the final threshold of significance for components
k = 1000 # This is the number of permutations used in NBS
tail = 'both' # I'll use the two-tailed t-test where the alternative hypothesis is "x and y are not equal"
betweenPaired = False # To compare groups I'll use the population (2-sample) t-test as the observations are not paired
withinPaired = True # To compare time windows of a subject I'll use the paired (1-sample) t-test as the observations are paired 
verbose = True


# visualization

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:02:35 2020

@author: nicholebouffard
"""

#%% import packages
import numpy as np
import pandas as pd
import os, sys, random
import itertools as it

# Read in the sceneface image names and the object image names
#sceneInfo gives the names of the scene/face blocks (sceneface = starts with scene, facescene= starts with face)
sceneInfo = pd.read_csv('sceneNames.csv')
objInfo = pd.read_csv('objNames.csv')
colorInfo = pd.read_csv('colorNames.csv')

numTrials = 16
numBlocks = [1,2] # change for actual experiment


### SCENE BLOCKS ###

# Loop through to create two sceneblock trial lists
for s in np.arange(len(numBlocks)):
# create sceneface blocks. Repeat each image in sceneInfo 8 times 
    sceneConds = sceneInfo.iloc[np.repeat(np.arange(len(sceneInfo)), 8)] # 8 is length of an event
    sceneConds.reset_index(drop=True, inplace=True)

# create a list of randomly ordered object images from objectInfo
#Since I'm only using 16 stim for 32 trials right now, create random samples size 16 twice then concat
    chosen_idx1 = np.random.choice(numTrials, replace = False, size = numTrials) # change for actual experiment with full list of stim
    randObj1 = objInfo.objects.iloc[chosen_idx1] # use objects column because has path directly to image, diff for color blocks
    chosen_idx2 = np.random.choice(numTrials, replace = False, size = numTrials) # change for actual experiment with full list of stim
    randObj2 = objInfo.objects.iloc[chosen_idx2] 

    randObj = pd.concat([randObj1,randObj2], ignore_index = True)

# Select one of the counterbalance orders from sceneConds and bind with object list
# put together in dataframe, where each row is a trial
    sceneCondDFforJoin = pd.DataFrame(sceneConds.iloc[:,s]) #df.join won't join a series with a df
    sceneblockTrialList = sceneCondDFforJoin.join(randObj)     
#write out the trial list for each block (for this project there are only two scene blocks, maybe different in actual experiment)
    sceneblockTrialList.to_csv(str(s+1) + 'SceneBlockTrialList.csv', index=False)


### COLOR BLOCKS ###
    
# create two object blocks. Same design as sceneface but red/blue objects + constant scene (block1) then constant face(block2)
for s in np.arange(len(numBlocks)):
# create redblue blocks. Repeat each image in colorInfo 8 times 
    colorConds = colorInfo.iloc[np.repeat(np.arange(len(colorInfo)), 8)] # 8 is length of an event
    colorConds.reset_index(drop=True, inplace=True)

# create a list of randomly ordered object images from objectInfo
#Since I'm only using 16 stim for 32 trials right now, create random samples size 16 twice then concat
    chosen_idxA = np.random.choice(numTrials, replace = False, size = numTrials) # change for actual experiment with full list of stim
    randObjA = objInfo.objectName.iloc[chosen_idxA] #use column objectName here because it has diff path than sceneface blocks
    chosen_idxB = np.random.choice(numTrials, replace = False, size = numTrials) # change for actual experiment with full list of stim
    randObjB = objInfo.objectName.iloc[chosen_idxB] 

    randObj2 = pd.concat([randObjA,randObjB], ignore_index = True)

# Select one of the counterbalance orders from colorConds and bind with object list
# put together in dataframe, where each row is a trial
    colorCondDFforJoin = colorConds.iloc[:,s] #df.join won't join a series with a df
# Bind the color cond path names with the object names
    joinedColor = pd.DataFrame(colorCondDFforJoin.str.cat(randObj2, sep = ''))
# Bind this with a column of a randomly selected repeating scene (block1) or face (block2)
    sceneOrface=sceneInfo.iloc[s,0]
    repSceneOrFace = pd.DataFrame(np.repeat(sceneOrface,32))
    colorblockTrialList = repSceneOrFace.join(joinedColor)     
#write out the trial list for each block (for this project there are only two color blocks, maybe different in actual experiment)
    colorblockTrialList.to_csv(str(s+1) + 'ColorBlockTrialList.csv', index=False)


### Scene and Color block counterbalancce ###
# Write out a csv with the counterbalance for altenrating scene and color blocks 
# Latin square design

conds = ['1SceneBlockTrialList.csv','1ColorBlockTrialList.csv','2SceneBlockTrialList.csv','2ColorBlockTrialList.csv'] # set the conditions for the two different types of blocks
condOrders=[] # initialize empty variable for the counter balanace order
for c in np.arange(len(conds)): # Run this loop which creates the four possible counterbalance orders
    condOrders.append(conds)
    conds = conds[-1:] + conds[:-1]

# save out each order in four different files that will be used in the experiment 
for s in np.arange(len(condOrders)):
    df = pd.DataFrame(condOrders[s], columns=['blockList'])
    df.to_csv(str(s+1) + 'PickBlocks.csv', index=False)
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final python experiment (for Retrieval Boundary Project)
@author: nrbouffard
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os, sys
import random as rand
from psychopy import visual, core, event, gui, logging


# global shutdown key for debugging!
event.globalKeys.add(key='q',func=core.quit)

# create a gui object
subgui = gui.Dlg()
subgui.addField("Subject ID:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]

#%% prepare output

outputFileName = 'data' + os.sep + 'sub' + subjID + '.csv'
if os.path.isfile(outputFileName) :
    sys.exit("data for this session already exists")

outVars = ['subj', 'blockCounterBalance','trialCounterBalance', 'block', 'trial', 'object', 'sceneFace','sfImage', 'color', 'rating','val', 'rt','trialStart','scaleStart', 'trialEnd']    
out = pd.DataFrame(columns=outVars)

# create output file now, to append to as the experiment progresses
out['subj'] = subjID
out.to_csv(outputFileName,index = False)

# instruction file
instFile = 'instructions.jpeg'

# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', units='height') 

# initialize clocks
trialClock = core.Clock() 
expClock = core.Clock() 
stimClock = core.Clock()
fbClock = core.Clock()

# randomly select a num 1-4 to determine block order csv
r=rand.randrange(4)
#select block order
blockInfo = pd.read_csv(str(r+1) + 'PickBlocks.csv',)

# initialize rating scale
### had to move this stuff within the trial loop because the scale text wasn't showing up on the red/blue background
### can change back for actual experiment
#myScale = visual.RatingScale(win, low=1, high=7, marker='triangle',
 #   tickMarks=[1,2,3,4,5,6,7],markerStart=None,markerColor='black',pos = (0,-.6),singleClick = True, textColor = 'black', lineColor = 'black'   )

# feedback
#bigFeedback = visual.TextStim(win, text='Very Vivid', pos=(0,0), height=.05, color = 'black')
#smallFeedback = visual.TextStim(win, text='Not Vivid', pos=(0,0), height=.05,color = 'black')
#neutFeedback = visual.TextStim(win, text='Kind of Vivid', pos=(0,0), height=.05,color = 'black')
#naFeedback = visual.TextStim(win, text='No response recorded', pos=(0,0), height=.05,color = 'black')


# set stimulus times in seconds
isiDur = 1
stimDur = 5
fbDur = 1.5

# set number of blocks
nBlocks = len(blockInfo)

# prepare image for display
instr = visual.ImageStim(win, image="instructions.jpg", size = .9)

# draw image to window buffer
instr.draw()
# flip window to reveal image
event.clearEvents() # this clears any prior button presses
win.flip()

# don't do anything until a key is pressed
event.waitKeys()

# Start block loop

for b in np.arange(len(blockInfo)):

# select trial order
    trialFile = blockInfo.blockList[b+1]
    trialInfo = pd.read_csv(trialFile)
# set number of trials
    nTrials = len(trialInfo)


# make your loop
    for t in np.arange(0,nTrials) :
    
        trialClock.reset()
        
     # Get get file names
        fnameOb = trialInfo.iloc[t,1]
        fnameObSep=fnameOb.split('/')
        fnameFS = trialInfo.iloc[t,0]
        fnameFSSep=fnameFS.split('/')
        
        if len(fnameObSep) < 3:
            obj=fnameObSep[1]
            sceneface=fnameFSSep[0]
            sf=fnameFSSep[1]
            col= 'orig'
        elif len(fnameObSep) == 3:
            obj = fnameObSep[2]
            sceneface = fnameFSSep[0]
            sf=fnameFSSep[1]
            col=fnameObSep[1]
            if col == 'red':
                win = visual.Window(fullscr=True, allowGUI=False, color= 'red', units='height')
            elif col == 'blue':
                win = visual.Window(fullscr=True, allowGUI=False, color= 'blue', units='height')

        objectLeft = visual.ImageStim(win, image =trialInfo.iloc[t,1] , pos= (-0.4,0)) #object, column2
        faceRight = visual.ImageStim(win, image = trialInfo.iloc[t,0],pos= (0.4,0)) #face/scene, column1
        myText = visual.TextStim(win, text = 'imagine', pos = (0,-.35), color = 'black', height = .10)
#        vivText = visual.TextStim(win, text = 'not vivid              very vivid', pos = (0,0), color = 'black', height = .10) 

        # initialize rating scale
        myScale = visual.RatingScale(win, low=1, high=7, marker='triangle',
        tickMarks=[1,2,3,4,5,6,7],markerStart=None,pos = (0,0), size = 1.5,
        singleClick = True, textColor = 'black', acceptPreText='vividness', acceptText='vividness', lineColor = None)

        # feedback
        bigFeedback = visual.TextStim(win, text='Very Vivid', pos=(0,0), height=.05, color = 'black')
        smallFeedback = visual.TextStim(win, text='Not Vivid', pos=(0,0), height=.05,color = 'black')
        neutFeedback = visual.TextStim(win, text='Kind of Vivid', pos=(0,0), height=.05,color = 'black')
        naFeedback = visual.TextStim(win, text='No response recorded', pos=(0,0), height=.05,color = 'black')


        # then draw all stimuli
        #objectLeft.draw() 
        #faceRight.draw()
        #myScale.draw()
        #myText.draw()
            
        # record trial prarameters
        out.loc[t,'subj'] = subjID
        #out.loc[t,'object'] = trialInfo.iloc[t,1]
        out.loc[t,'object'] = obj
        out.loc[t,'blockCounterBalance'] = r+1
        out.loc[t,'trialCounterBalance'] = trialFile
        #out.loc[t,'sceneFace'] = trialInfo.iloc[t,0]
        out.loc[t,'sceneFace'] = sceneface
        out.loc[t,'sfImage'] = sf
        out.loc[t,'color'] = col
        out.loc[t,'trial'] = t + 1
        out.loc[t,'block'] = b + 1
        
        # do nothing while isi is still occuring
        while trialClock.getTime() < isiDur:
            core.wait(.001)

        # then flip your window
        win.flip()
        stimClock.reset()
        # record when stimulus was prsented 
        out.loc[t, 'trialStart'] = expClock.getTime()

    
        #myScale.reset()  #reset rating scale right before drawing for RT
        while stimClock.getTime()<stimDur:
            faceRight.draw()
            objectLeft.draw()
            myText.draw()
            win.flip()
    
        stimClock.reset()
        # record when stimulus was prsented 
        out.loc[t, 'scaleStart'] = expClock.getTime()
        
        myScale.reset()  #reset rating scale right before drawing for RT
        event.clearEvents() # this clears any prior button presses
        while myScale.noResponse and stimClock.getTime()<stimDur:
            myScale.draw()
 #           vivText.draw()
            win.flip()
    
        trialResp = myScale.getRating()
        trialRT = myScale.getRT()
    
         # record when stimulus removed
        if myScale.noResponse == False: 
            out.loc[t,'trialEnd'] = expClock.getTime()
            if trialResp < 4:
                smallFeedback.draw()
                out.loc[t,'val'] = 'notVivid'
            elif trialResp > 4:
                bigFeedback.draw()
                out.loc[t,'val'] = 'Vivid'
            else:
                neutFeedback.draw()
                out.loc[t,'val'] = 'Neutral'
                
            win.flip()
            fbClock.reset()
            while fbClock.getTime() < fbDur:
                core.wait(.001)
    
        elif myScale.noResponse == True: 
            naFeedback.draw()
            out.loc[t,'val'] = 'NA'
            
            win.flip()
            fbClock.reset()
            while fbClock.getTime() < fbDur:
                core.wait(.001)
    
    # save responses       
        if myScale.noResponse == False: #if response was made
            out.loc[t, 'rating'] = trialResp
            out.loc[t, 'rt'] = trialRT
        elif myScale.noResponse == True:
            out.loc[t, 'rating'] = 'NA'
            out.loc[t, 'rt'] = 'NA'
            
        out.loc[[t]].to_csv(outputFileName, mode = 'a', header = False, index = False)
      
        # finish experiment
    win.flip() 
    core.wait(1)
 
    endofblock = visual.TextStim(win, text="""END OF BLOCK                         
    Please wait for next block""", height=.05, color = 'black')  
    endofblock.draw()
    win.flip()
    core.wait(5)

# finish experiment
win.flip() 
core.wait(1)
 
goodby = visual.TextStim(win, text="""Thank you for participating
                         
Please get the experimenter""", height=.05, color = 'black')  
goodby.draw()
win.flip()

#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly


core.wait(4)
win.close()
core.quit()

from __future__ import division  # important
from psychopy import visual, event, core, data, gui, monitors
import numpy, random, sys, math
from psychopy.visual.windowwarp import Warper

from U6io import U6io
labjack = U6io()

import csv

# Dr. Tristan G. Heintz 2017

timewave  = []
timex     = []
# --------------------------------------------Setting Up LabJack ------------------------------------------------------- #

#setup labjack U6

labjack.setOutputVoltageFIO(0,0) # channel for opto
labjack.setOutputVoltageFIO(1,0) # channel for 2P trigger (on during all experiment)
labjack.setOutputVoltageFIO(2,0) # channel for pupil camera (1 pulse per frame)
labjack.setOutputVoltageFIO(3,0) # channel for timewave (on when stim on)

#length is 5780 frames
# ------------------------------------------ Stimulus Parameters ------------------------------------------------------#

info = {}


orientations         =  [315]   #,180,90,270,45,225,135,315] # [0,45,90,135] and [180,225,270,315]
info['ORI']          = len(orientations)                           # make sure it runs at 120Hz
info['trialN']       = 10
info['RefreshRate']  = 120                           # Refresh rate of the monitor, in Hz

info['PreStim']    = info['RefreshRate'] * 10
info['StimLength'] = info['RefreshRate'] * 10
info['ISI']        = info['RefreshRate'] * 20
 
info['Orientation']     = 0
info['SF']              = 0.04                         # cycles per degree
info['TF']              = 1                          # in Hz (1 cycles per seconds = 1Hz = 1/60)
info['Contrast']        = 1
info['SD_grating']      = 3                            # the "SD" of the mask 'gauss'. The default value is 3*SD
info['Position']        = [47.5106513, 2.88901593] #[-13.93,27.95] #[0,0] #[-32.6,22.4]  [-12.45,-1.36]# [-12.45,-1.36]#[0,0] # [0.45,-15.39]# [0,0] ##[7.67581736 , 5.647961660] #[-16.09,13.23] #[6.1797,-12.68] #[4.59,3.61]

sizeGrating = [20, 20] #[10,20,30,40,60,90]#[5,10,15,20,30,40] #  [10,20,30,40,60,90]
info['size'] = len(sizeGrating)

mon = monitors.Monitor('StimMonitor')
win = visual.Window(fullscr=True, monitor=mon, screen = 1, waitBlanking=False, useFBO = True)   #waitBlanking=False if you want 120Hz 
grating = visual.GratingStim(win, units='deg', mask='circle', sf = info['SF'], tex='sin', pos = info['Position'])    # maskParams = {'sd':3} for mask 'gauss' and maskParams = {'fringeWidth':0.2} for 'raisedCos'
warper = Warper(win, warp='spherical', warpfile="", warpGridsize  = 128, eyepoint = [0.5,0.5], flipHorizontal = False, flipVertical = False)

# Calculate length Experiment:
lengthPreStim = info['PreStim']/info['RefreshRate']
nbOfTrials = info['trialN']
#nbOfRepeatsSF = info['SF'] 
nbOfRepeatsSize = info['size'] 
nbOfRepeatsORI = info['ORI']
lengthStimISI = (1*(info['StimLength']/info['RefreshRate'])) + (info['ISI']/info['RefreshRate'])

lengthEXP = lengthPreStim + nbOfTrials*nbOfRepeatsORI*lengthStimISI*nbOfRepeatsSize
print "Experiment Duration = ", lengthEXP, "seconds"
print "At 5 Hz: ", lengthEXP*6.07, "frames"



# --------------------------------------------- Routine ------------------------------------------------------#

labjack.setOutputVoltageFIO(1,1)

clock = core.Clock()

for frameN in range(info['PreStim']):                                   # Create a prestim
    labjack.setOutputVoltageFIO(2,0)
    win.flip()
    labjack.setOutputVoltageFIO(2,1)
    labjack.setOutputVoltageFIO(3,0)
    timewave.append(0)
    
for thisTrial in range(info['trialN']): 
    print '  '
    print 'Trial number', thisTrial+1
    
    oriN = 0
    for thisOri in range(info['ORI']):
        print '    Orientation is ', orientations[oriN], 'degree'
        SizeN = 0
        
        for thisSize in range(info['size']):                               # Nb of stim per trial
            labjack.setOutputVoltageFIO(3,0)
            print '        Size is: ', sizeGrating[SizeN], 'degree'
            grating.phase = 0.5
            timex.append(clock.getTime()) 
            labjack.setOutputVoltageFIO(0,0)
           # if (thisTrial == 1 or thisTrial == 3 or thisTrial == 5 or thisTrial == 7 or thisTrial == 9):
           #     labjack.setOutputVoltageFIO(0,1)
            
            #for frameN in range(info['StimLength']):
            #    grating.setSize(sizeGrating[SizeN])
            #    grating.setPhase(info['TF']/info['RefreshRate'], '+')           # To get the TF in Hz, divide TF by the refresh rate       # set like this for TF fction of speed:  grating.setPhase(mouse_dX/100,'+')
            #    grating.ori = orientations[oriN]
                #grating.draw()
            #    win.flip()
            #    labjack.setOutputVoltageFIO(3,1)
            #    timewave.append(2)
            #if (thisTrial == 1 or thisTrial == 3 or thisTrial == 5 or thisTrial == 7 or thisTrial == 9):
            #    labjack.setOutputVoltageFIO(0,1)
            
#            for frameN in range(info['StimLength']):
#                grating.setSize(sizeGrating[SizeN])
#                grating.setPhase(info['TF']/info['RefreshRate'], '+')           # To get the TF in Hz, divide TF by the refresh rate       # set like this for TF fction of speed:  grating.setPhase(mouse_dX/100,'+')
#                grating.ori = orientations[oriN]
#                grating.setContrast(info['Contrast'])
#                grating.draw()
#                win.flip()
#                labjack.setOutputVoltageFIO(3,1)
#                timewave.append(sizeGrating[SizeN])
            #labjack.setOutputVoltageFIO(0,1)
            
            if (thisSize == 1 or thisSize == 3 or thisSize == 5 or thisSize == 7 or thisSize == 9):
                labjack.setOutputVoltageFIO(0,1)
            #labjack.setOutputVoltageFIO(0,1)
            
            for frameN in range(info['StimLength']):
                grating.setSize(sizeGrating[SizeN])
                grating.setPhase(info['TF']/info['RefreshRate'], '+')           # To get the TF in Hz, divide TF by the refresh rate       # set like this for TF fction of speed:  grating.setPhase(mouse_dX/100,'+')
                grating.ori = orientations[oriN]
                grating.setContrast(info['Contrast'])
                grating.draw()
                labjack.setOutputVoltageFIO(2,0) 
                win.flip()
                labjack.setOutputVoltageFIO(2,1) 
                labjack.setOutputVoltageFIO(3,1)
                timewave.append(sizeGrating[SizeN])
            labjack.setOutputVoltageFIO(0,0)
            timex.append(clock.getTime())
            for frameN in range(info['ISI']):                               # add an ISI or post stim interval
                labjack.setOutputVoltageFIO(2,0)
                win.flip()
                labjack.setOutputVoltageFIO(2,1)
                labjack.setOutputVoltageFIO(3,0)
                timewave.append(0)
                
            SizeN+=1                                                         # move to the next ori
        oriN += 1    

labjack.setOutputVoltageFIO(2,0) 

with open("Timewave_ContrastAdapt10sec.csv", "wb") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in timewave:
        writer.writerow([val])  
        
with open("Timex_ContrastAdapt10sec.csv", "wb") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in timex:
        writer.writerow([val])  
        
        
labjack.setOutputVoltageFIO(1,0)
labjack.setOutputVoltageFIO(3,0)
    
from __future__ import division  # important
from psychopy import visual, event, core, data, gui, monitors
import numpy, random, sys, math
from psychopy.visual.windowwarp import Warper
import serial

#eventually remove labjack from system
#for that we connect via serial to the ESP32
#import serial

from U6io import U6io

labjack = U6io()

import csv


timewave = []
timex = []
# --------------------------------------------Setting Up LabJack ------------------------------------------------------- #

# setup labjack U6 --> could this be made into variables or a little function for reading easiness?
# something like:
optoChannel = 0
twoPtrigger = 1
pupilCamera = 2
timeWave = 3

# then everytime the setOutputVoltageFIO is called, one could call by the names instead of numbers
labjack.setOutputVoltageFIO(optoChannel, 0)  # channel for opto  
labjack.setOutputVoltageFIO(twoPtrigger, 0)  # channel for 2P trigger (on during all experiment)  
labjack.setOutputVoltageFIO(pupilCamera, 0)  # channel for pupil camera (1 pulse per frame)  
labjack.setOutputVoltageFIO(timeWave, 0)  # channel for timewave (on when stim on)  

# labjack.setOutputVoltageFIO(0,0) # channel for opto
# labjack.setOutputVoltageFIO(1),0) # channel for 2P trigger (on during all experiment)
# labjack.setOutputVoltageFIO(2,0) # channel for pupil camera (1 pulse per frame)
# labjack.setOutputVoltageFIO(3,0) # channel for timewave (on when stim on)


# ------------------------------------------ Stimulus Parameters ------------------------------------------------------#

info = {}

info["trialN"] = 5
info["RefreshRate"] = 120  # Refresh rate of the monitor, in Hz
info["PreStim"] = info["RefreshRate"] * 2
info["StimLength"] = info["RefreshRate"] * 2
info["ISI"] = info["RefreshRate"] * 2

info["Orientation"] = 315  # ,180,90,270,45,225,135,315,0 = vertical right
info["SF"] = 0.04  # cycles per degree
info["TF"] = 1  # in Hz (1 cycles per seconds = 1Hz = 1/60)
info["Contrast"] = 1
info["SD_grating"] = 3  # the "SD" of the mask 'gauss'. The default value is 3*SD
info["Position"] = [47.5106513, 2.88901593]

sizeGrating = 20

info["size"] = sizeGrating

mon = monitors.Monitor("StimMonitor")

win = visual.Window(
    fullscr=True, monitor=mon, screen=1, waitBlanking=False, useFBO=True
)  # waitBlanking=False if you want 120Hz
grating = visual.GratingStim(
    win, units="deg", mask="circle", sf=info["SF"], tex="sin", pos=info["Position"]
)  # maskParams = {'sd':3} for mask 'gauss' and maskParams = {'fringeWidth':0.2} for 'raisedCos'
grating.phase = 0.5
warper = Warper(
    win,
    warp="spherical",
    warpfile="",
    warpGridsize=128,
    eyepoint=[0.5, 0.5],
    flipHorizontal=False,
    flipVertical=False,
)

win2 = visual.Window(
    fullscr=True, monitor=mon, screen=2, waitBlanking=False, useFBO=True
)  # waitBlanking=False if you want 120Hz
grating2 = visual.GratingStim(
    win2, units="deg", mask="circle", sf=info["SF"], tex="sin", pos=info["Position"]
)  # maskParams = {'sd':3} for mask 'gauss' and maskParams = {'fringeWidth':0.2} for 'raisedCos'
grating2.phase = 0.5
warper2 = Warper(
    win2,
    warp="spherical",
    warpfile="",
    warpGridsize=128,
    eyepoint=[0.5, 0.5],
    flipHorizontal=False,
    flipVertical=False,
)

# Calculate length Experiment:

lengthPreStim = info["PreStim"] / info["RefreshRate"]
nbOfTrials = info["trialN"]
lengthStimISI = (1 * (info["StimLength"] / info["RefreshRate"])) + (
    info["ISI"] / info["RefreshRate"]
)

lengthEXP = lengthPreStim + nbOfTrials * lengthStimISI
print ("Experiment Duration = ", str(lengthEXP), "seconds")
print ("At 5 Hz: ", str(lengthEXP * 6.07), "frames")


# setup a serial connection with the ESP - this will be used when LabJack is removed from the setup
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used


#add info here to make sure the connection is made
#ser.write(b'hello')     # write a string


# --------------------------------------------- Routine ------------------------------------------------------#


labjack.setOutputVoltageFIO(twoPtrigger, 1)

clock = core.Clock()

for frameN in range(info["PreStim"]):  # Create a prestim
    labjack.setOutputVoltageFIO(pupilCamera, 0)
    win.flip()
    win2.flip()
    labjack.setOutputVoltageFIO(pupilCamera, 1)
    labjack.setOutputVoltageFIO(timeWave, 0)
    timewave.append(0)

for thisTrial in range(info["trialN"]):
    #ADD SUBROUTINE THAT WILL WAIT FOR SERIAL COMMAND FROM ESP32
    while ser.available() == 0:
        print("waiting for ESP")
    monitorSide = ser.readline()
    print("monitor: " + str(monitorSide))
    # Random screen chosen in each trial
    ran = [[win, grating], [win2, grating2]]
    #ranchoice = random.choice(ran)
    ranchoice = ran[monitorSide]

    winran = ranchoice[0]
    gratingran = ranchoice[1]

    print "test  "
    print "Trial number", thisTrial + 1
    #labjack.setOutputVoltageFIO(timeWave, 0)
    print "        Size is: ", sizeGrating, "degree"
    timex.append(clock.getTime())
    labjack.setOutputVoltageFIO(optoChannel, 0)

    for frameN in range(info["StimLength"]):
        gratingran.setSize(sizeGrating)
        gratingran.setPhase(
            info["TF"] / info["RefreshRate"], "+"
        )  # To get the TF in Hz, divide TF by the refresh rate       # set like this for TF fction of speed:  grating.setPhase(mouse_dX/100,'+')
        gratingran.ori = info["Orientation"]
        gratingran.setContrast(info["Contrast"])
        gratingran.draw()
        labjack.setOutputVoltageFIO(pupilCamera, 0)
        winran.flip()
        labjack.setOutputVoltageFIO(pupilCamera, 1)
        #labjack.setOutputVoltageFIO(timeWave, 1)
        timewave.append(sizeGrating)
    ser.write("d")
    labjack.setOutputVoltageFIO(optoChannel, 0)
    timex.append(clock.getTime())


    for frameN in range(info["ISI"]):  # add an ISI or post stim interval
        labjack.setOutputVoltageFIO(pupilCamera, 0)
        winran.flip()
        labjack.setOutputVoltageFIO(pupilCamera, 1)
        #labjack.setOutputVoltageFIO(timeWave, 0)
        timewave.append(0)

labjack.setOutputVoltageFIO(pupilCamera, 0)
labjack.setOutputVoltageFIO(optoChannel, 0)
#labjack.setOutputVoltageFIO(timeWave, 0)


#close serial connection with ESP
#ser.close()             # close port
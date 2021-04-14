import utime
from machine import Pin

class task1:
    def __init__(self):
        #ports
        self.lickSensor1 = 1
        self.lickSensor2 = 2
        self.actuator1 = 3
        self.actuator2 = 4
        self.solenoid1 = 5
        self.solenoid2 = 6
        self.stimTrigger = 7
        self.monitor1 = 8
        self.monitor2 = 9

        #set the "direction" of the ports
        self.lickSensor1Pin = Pin(self.lickSensor1, Pin.IN,Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(self.lickSensor2, Pin.IN,Pin.PULL_DOWN)
        self.actuator1Pin = Pin(self.actuator1, Pin.OUT)
        self.actuator2Pin = Pin(self.actuator2, Pin.OUT)
        self.solenoid1Pin = Pin(self.solenoid1, Pin.OUT)
        self.solenoid2Pin = Pin(self.solenoid2, Pin.OUT)
        self.stimTriggerPin = Pin(self.stimTrigger, Pin.OUT)
        self.monitor1Pin = Pin(self.monitor1,Pin.OUT)
        self.monitor2Pin = Pin(self.monitor2,Pin.OUT)

        #set a seed for a random number generator (fixing the seed will allow for )

        #time/interval variables
        self.iti = 5000 #inter trial interval in ms
        self.baseline = 10000 # time to wait at the beginning of session to record baseline
        self.stimDuration = 5000 # stimulus presentation duration
        self.responseWindowDuration = 2000 #time window to respond after stim presentation
        
        self.rewardDuration = 1000 # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.numberOfTrials = 100 #the number of trials that will be presented to the animals
        self.trial = 1 #the current trial


    def task(self):
        while self.trial<=self.numberOfTrials:
            #if it is the first trial, then wait for the baseline activity measurement
            if self.trial ==1:
                self.time_intervals(interval_ms = self.baseline)
        
        #send a trigger out to start stimulation (in case we are timing things with the ESP)
        self.stimTriggerPin(1)
        self.time_intervals(interval_ms=self.stimDuration)
        self.stimTriggerPin(0)

        #receive a trigger while stimulation is running
        #this is still rudimentary as depending on timing/synching this loop could still be problematic
        #stimStatus = self.strimTriggerPin.value()
        #while stimStatus == 1:
        #    self.time_intervals(interval_ms=5)
        #    stimStatus = self.strimTriggerPin.value()
        
        #once stimulation is done, start the actuators
        self.actuator1Pin(1)
        lick1status = self.lickSensor1Pin.value()
        lick2status = self.lickSensor2Pin.value()

        #after trial is done, start iti
        self.time_intervals(intervals_ms = self.iti)
        trial = trial+1    


    def time_intervals(self,interval_ms=100):
        time1 = utime.ticks_ms()
        time2 = utime.ticks_ms()
        while time2-time1<interval_ms:
            time2 = utime.ticks_ms()
    
            
    
- At the start there is a 10 sec interval without a stimulus to record baseline activity. 
Then the mouse sees a stimulus (always the same drifting grating) which appears randomly either on the left or the right screen.
 after 5 sec. of stimulus presentation the actuator moves the lick sensors in front of the mouse for two sec. 
 - in which the mouse has to report on which side the stimulus is present, hence lick left or right. 
   -If the answer is correct a reward is given (solenoid valves).
   -If the answer is incorrect no reward is given.
- The actuator retracts the lick sensors after 2 sec. either way. 
- Then there is an inter trial interval for 5+ sec before the next stimulus will be presented. 
If the mouse was incorrect the stimulus will be presented on the same side as the trial before until the mouse makes the correct decision (to avoid bias).I might want to change the timeframes for the different stages depending on how the training goes.

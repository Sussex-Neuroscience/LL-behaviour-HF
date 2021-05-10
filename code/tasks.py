import utime
from machine import Pin
from machine import UART

class task1:
    def __init__(self):
        # ports
        self.lickSensor1 = 1
        self.lickSensor2 = 3
        self.actuator1Foward = 2
        self.actuator1Backward = 15
        self.solenoid1 = 16
        self.solenoid2 = 19
        self.stimTrigger = 7
        self.monitor1 = 8
        self.monitor2 = 9

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(self.lickSensor1, Pin.IN, Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(self.lickSensor2, Pin.IN, Pin.PULL_DOWN)
        self.actuator1ForwardPin = Pin(self.actuator1Forward, Pin.OUT)
        self.actuator1BackwardPin = Pin(self.actuator2Backward, Pin.OUT)
        self.solenoid1Pin = Pin(self.solenoid1, Pin.OUT)
        self.solenoid2Pin = Pin(self.solenoid2, Pin.OUT)
        self.stimTriggerPin = Pin(self.stimTrigger, Pin.OUT)
        self.monitor1Pin = Pin(self.monitor1, Pin.OUT)
        self.monitor2Pin = Pin(self.monitor2, Pin.OUT)


        #turn everything off at the beginning
        self.actuator1ForwardPin.off()
        self.actuator1BackwardPin.off()
        self.solenoid1Pin.off()
        self.solenoid2Pin.off()
        self.stimTriggerPin.off()
        self.monitor1Pin.off()
        self.monitor2Pin.off

        # set a seed for a random number generator (fixing the seed will allow for )
        # or make a list with the order of presentation in the monitors
        # time/interval variables
        self.iti = 5000  # inter trial interval in ms
        self.baseline = (
            10000  # time to wait at the beginning of session to record baseline
        )
        self.stimDuration = 5000  # stimulus presentation duration
        self.responseWindowDuration = (
            2000  # time window to respond after stim presentation
        )

        self.rewardDuration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.numberOfTrials = (
            100  # the number of trials that will be presented to the animals
        )
        self.trial = 1  # the current trial

        #initialize serial port 1 for communication with host pc
        self.uart = UART(1, 9600)                         # init with 9600 baudrate


    def run_task(self):
        while self.trial <= self.numberOfTrials:
            # if it is the first trial, then wait for the baseline activity measurement
            if self.trial == 1:
                self.time_intervals(interval_ms=self.baseline)

        # send a trigger out to indicate stimulation is ongoing (so this can be registered by the scan system)
        
        self.stimTriggerPin(1)
        self.time_intervals(interval_ms=self.stimDuration)
        self.stimTriggerPin(0)
        
        #need to send a serial signal so that the stimulation PC turns on the monitors

        # receive a trigger while stimulation is running
        # this is still rudimentary as depending on timing/synching this loop could still be problematic
        # stimStatus = self.strimTriggerPin.value()
        # while stimStatus == 1:
        #    self.time_intervals(interval_ms=5)
        #    stimStatus = self.strimTriggerPin.value()

        # once stimulation is done, start the actuators
        self.actuator1ForwardPin.on()
        #wait for actuator to move spouts forward
        self.time_intervals(interval_ms=100)

        self.actuator1ForwardPin.off()

        timeWindow = utime.ticks_ms()
        while timeWindow<self.responseWindowDuration:
            lick1status = self.lickSensor1Pin.value()
            lick2status = self.lickSensor2Pin.value()
            if lick1status == 1 or lick2status==1:
                if lick1Status == 1 and monitor1Pin.value()==1:
                    correct = 1
                self.actuator1BackwardPin.on()
                
                #wait for actuator to move spouts backward
                self.time_intervals(interval_ms=100)
                
                self.actuator1BackwardPin.off()
                
                break
            timeWindow = utime.ticks_ms()
            
        
        
        # after trial is done, start iti
        self.time_intervals(interval_ms=self.iti)
        self.trial = self.trial + 1

    def time_intervals(self, interval_ms=100):
        time1 = utime.ticks_ms()
        time2 = utime.ticks_ms()
        while time2 - time1 < interval_ms:
            time2 = utime.ticks_ms()


#
# - At the start there is a 10 sec interval without a stimulus to record baseline activity.
# Then the mouse sees a stimulus (always the same drifting grating) which appears randomly either on the left or the right screen.
# after 5 sec. of stimulus presentation the actuator moves the lick sensors in front of the mouse for two sec.
# - in which the mouse has to report on which side the stimulus is present, hence lick left or right.
#   -If the answer is correct a reward is given (solenoid valves).
#   -If the answer is incorrect no reward is given.
# - The actuator retracts the lick sensors after 2 sec. either way.
# - Then there is an inter trial interval for 5+ sec before the next stimulus will be presented.
# If the mouse was incorrect the stimulus will be presented on the same side as the trial before until the mouse makes the correct decision (to avoid bias).I might want to change the timeframes for the different stages depending on how the training goes.
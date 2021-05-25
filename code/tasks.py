import utime
from machine import Pin
from machine import UART
from machine import I2C


import urandom

class task1:
    def __init__(self):
        # ports
        self.lickSensor1 = 0
        self.lickSensor2 = 4
        self.actuator1Forward = 2
        self.actuator1Backward = 15
        self.solenoid1 = 16
        self.solenoid2 = 19
        self.stimTrigger = 7
        #self.stimIndValue = 0.1
        self.lickSensor1Ind = 0.1
        self.lickSensor2Ind = 0.2
        self.solenoid1Ind = 0.4
        self.solenoid2Ind = 0.8
        
        #self.monitor1 = 8
        #self.monitor2 = 9
        #i2c initialization
        self.i2c=I2C(0, scl = Pin(14), sda = Pin(15),  freq=400000)
        self.i2cAdd = self.i2c.scan()

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(self.lickSensor1, Pin.IN, Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(self.lickSensor2, Pin.IN, Pin.PULL_DOWN)
        self.actuator1ForwardPin = Pin(self.actuator1Forward, Pin.OUT)
        self.actuator1BackwardPin = Pin(self.actuator1Backward, Pin.OUT)
        self.solenoid1Pin = Pin(self.solenoid1, Pin.OUT)
        self.solenoid2Pin = Pin(self.solenoid2, Pin.OUT)
        self.stimTriggerPin = Pin(self.stimTrigger, Pin.OUT)
        #self.monitor1Pin = Pin(self.monitor1, Pin.OUT)
        #self.monitor2Pin = Pin(self.monitor2, Pin.OUT)


        #turn everything off at the beginning
        self.actuator1ForwardPin.off()
        self.actuator1BackwardPin.off()
        self.solenoid1Pin.off()
        self.solenoid2Pin.off()
        #self.stimTriggerPin.off()
        #self.monitor1Pin.off()
        #self.monitor2Pin.off()

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

        #create array with indication on which monitor should be on.
        #this should be a pseudorandom way
        #set a seed so that all the time the random order is the same 
        urandom.seed(42)
        self.monitorOrder = list()
        for i in range(self.numberOfTrials):
            self.monitorOrder.append(urandom.randint(0,1))
        

            
        
        #initialize serial port 1 for communication with host pc
        self.uart = UART(0, 9600)                         # init with 9600 baudrate


    def run_task1(self):
        while self.trial <= self.numberOfTrials:
            # if it is the first trial, then wait for the baseline activity measurement
            #ANALOG OUT = 0
            if self.trial == 1:
                self.time_intervals(interval_ms=self.baseline)

            #####ANALOG OUT = STIMULATION ON
        
            #need to send a serial signal so that the stimulation PC turns on the monitors
            #start stimulation
            monitor = self.monitorOrder[self.trial]
            self.uart.write(monitor)
            self.stimTriggerPin.on()
            timeWindow = utime.ticks_ms()
            stimOn = self.uart.any()
            while stimOn == 0:
                #stimulus still running
                stimOn = self.uart.any()
            read = self.uart.read()
            self.stimTriggerPin.off()
            
            
            #while timeWindow<self.stimDuration:
            #    self.time_intervals(interval_ms=5)
                

            ##### ANALOG OUT = STIMULATION OFF


            # once stimulation is done, start the actuators
            self.actuator1ForwardPin.on()
            #wait for actuator to move spouts forward
            self.time_intervals(interval_ms=100)

            self.actuator1ForwardPin.off()

            timeWindow = utime.ticks_ms()
            
            correct = 0
            solenoid1 = 0
            solenoid2 = 0

            while timeWindow<self.responseWindowDuration:
                lick1Status = self.lickSensor1Pin.value()
                lick2Status = self.lickSensor2Pin.value()
                if lick1Status == 1 and monitor == 0:
                    correct = 1
                    solenoid1 = 1
                    break
                elif lick2Status == 1 and monitor == 1:
                    correct = 1
                    solenoid2 = 1
                    break
                else:
                    correct = 0
                    solenoid1 = 0
                    solenoid2 = 0
                    
                self.actuator1BackwardPin.on()
                
                #wait for actuator to move spouts backward
                self.time_intervals(interval_ms=100)
                
                self.actuator1BackwardPin.off()
                timeWindow = utime.ticks_ms()
                #break
                
            
            if correct == 1:
                if solenoid1 == 1:
                    self.solenoid1Pin.on()
                    self.time_intervals(interval_ms=100)
                    self.solenoid1Pin.off()
                if solenoid2 == 1:
                    self.solenoid2Pin.on()
                    self.time_intervals(interval_ms=100)
                    self.solenoid2Pin.off()

                
        
        
            # after trial is done, start iti
            self.time_intervals(interval_ms=self.iti)
            self.trial = self.trial + 1

    def time_intervals(self, interval_ms=100):
        time1 = utime.ticks_ms()
        time2 = utime.ticks_ms()
        while time2 - time1 < interval_ms:
            time2 = utime.ticks_ms()

    def writeToDac(self,value):
        buf=bytearray(2)
        buf[0]=(value >> 8) & 0xFF
        buf[1]=value & 0xFF
        self.i2c.writeto(self.i2cAdd,buf)
    #example DAC
    #self.writeToDac(2048)

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

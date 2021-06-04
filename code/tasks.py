import utime
from machine import Pin
#from machine import UART
#from machine import I2C
from machine import Pin
#from machine import I2C
from machine import SoftI2C

import urandom

class Task1:
    def __init__(self):

        self.stimIndValue = 0.1
        self.stimIndValue = self.volt2Int(volt = self.stimIndValue)
        self.lickSensor1Ind = 0.2
        self.lickSensor1Ind = self.volt2Int(volt = self.lickSensor1Ind)
        self.solenoid1Ind = 0.4
        self.solenoid1Ind = self.volt2Int(volt = self.solenoid1Ind)
        self.lickSensor2Ind = 0.8
        self.lickSensor2Ind = self.volt2Int(volt = self.lickSensor2Ind)
        self.solenoid2Ind = 1.6
        self.solenoid2Ind = self.volt2Int(volt = self.solenoid2Ind)
        
        #self.monitor1 = 998
        #self.monitor2 = 999
        self.i2c = SoftI2C(scl=Pin(12), sda=Pin(13), freq=100000)

        #self.i2c=SoftI2C(scl=Pin(9), sda=Pin(10))
        self.i2cAdd = self.i2c.scan()

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(5, Pin.IN, Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(18, Pin.IN, Pin.PULL_DOWN)
        self.actuator1ForwardPin = Pin(2, Pin.OUT)
        self.actuator1BackwardPin = Pin(15, Pin.OUT)
        self.solenoid1Pin = Pin(16, Pin.OUT)
        self.solenoid11Pin = Pin(17, Pin.OUT)
        self.solenoid2Pin = Pin(19, Pin.OUT)
        self.solenoid22Pin = Pin(21, Pin.OUT)
        self.stimTriggerPin = Pin(23, Pin.OUT)
        self.monitorSidePin = Pin(22,Pin.OUT)
        self.twopPin = Pin(14, Pin.OUT)
        
        
        ##self.monitor1Pin = Pin(self.monitor1, Pin.OUT)
        ##self.monitor2Pin = Pin(self.monitor2, Pin.OUT)


        #turn everything off at the beginning
        self.actuator1ForwardPin.value(0)
        self.actuator1BackwardPin.value(0)
        self.solenoid1Pin.value(0)
        self.solenoid11Pin.value(0)
        self.solenoid2Pin.value(0)
        self.solenoid22Pin.value(0)
        self.stimTriggerPin.value(0)


        

        self.twopPin.value(0)
        self.monitorSidePin.value(0)
        ##self.monitor1Pin.off()
        ##self.monitor2Pin.off()

        
        # time/interval variables
        self.iti = 5000  # inter trial interval in ms
        self.baseline = 10000  # time to wait at the beginning of session to record baseline
        self.stimDuration = 5000  # stimulus presentation duration
        self.responseWindowDuration = 2000  # time window to respond after stim presentation
        self.actuatorForwardDuration = 500 #how much time the actuator spends moving forward
        self.actuatorBackwardDuration = 500 #how much time the actuator spends moving forward
        self.reward1Duration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.reward2Duration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.numberOfTrials = 100  # the number of trials that will be presented to the animals
        
        self.trial = 1  # the current trial

        #create array with indication on which monitor should be on.
        #this should be a pseudorandom way
        #set a seed so that all the time the random order is the same 
        urandom.seed(42)

        self.monitorOrder = [0]*self.numberOfTrials

        for i in range(self.numberOfTrials):
            self.monitorOrder[i]=self.monitorOrder[i]+urandom.randint(0,1)
        
        #print("monitor order")
        #print(self.monitorOrder)

    def run_task1(self):
        #self.stimTriggerPin.value(1)
        #self.time_intervals( interval_ms=1000)
        #self.stimTriggerPin.value(0)
        self.twopPin.value(1)

        while self.trial <= self.numberOfTrials:
            # if it is the first trial, then wait for the baseline activity measurement
            #ANALOG OUT = 0
            self.writeToDac(value = 0)
            if self.trial == 1:
                self.time_intervals(interval_ms=self.baseline)

            #####ANALOG OUT = STIMULATION ON
            value = self.volt2Int(volt = self.stimIndValue)
            #print("value: "+str(value[0]))
            self.writeToDac(value = value)
            
            #start stimulation
            monitor = self.monitorOrder[self.trial]
            print("monitor: " + str(monitor) )
            self.monitorSidePin.value(monitor)
            self.stimTriggerPin.value(1) 
            print("stim on")
            
            #timeWindow = utime.ticks_ms()
            #stimOn = self.uart.any()
            #while stimOn == 0:
                #stimulus still running
            #    stimOn = self.uart.any()
            #read = self.uart.read()

            
            self.time_intervals(interval_ms=self.stimDuration)
            
            #while timeWindow<self.stimDuration:
            #    self.time_intervals(interval_ms=10)
            #    print("counting stim time")
            
            self.stimTriggerPin.value(0)    

            ##### ANALOG OUT = STIMULATION OFF
            value = self.volt2Int(volt = 0)
            self.writeToDac(value = value)

            # once stimulation is done, start the actuators
            self.actuator1ForwardPin.value(1)
            
            #wait for actuator to move spouts forward
            self.time_intervals(interval_ms=500)

            self.actuator1ForwardPin.value(0)
            
            timeWindow1 = utime.ticks_ms()
            timeWindow2 = utime.ticks_ms()
            correct = 0
            solenoid1 = 0
            solenoid2 = 0
            value = 0

            while timeWindow2-timeWindow1<self.responseWindowDuration:
                lick1Status = self.lickSensor1Pin.value()
                print(str(lick1Status))
                lick2Status = self.lickSensor2Pin.value()
                if lick1Status == 1 and monitor == 0:
                    
                    correct = 1
                    solenoid1 = 1
                    value = value + self.lickSensor1Ind
                    self.writeToDac(value = value)
                    break
                elif lick2Status == 1 and monitor == 1:
                    value = self.volt2Int(volt = self.lickSensor2Ind)
                    #self.writeToDac(value = value)
                    correct = 1
                    solenoid2 = 1
                    value = value + self.lickSensor2Ind
                    self.writeToDac(value = value)
                    break
                else:
                    correct = 0
                    solenoid1 = 0
                    solenoid2 = 0
                timeWindow2 = utime.ticks_ms()  

            



            if correct == 1:
                if solenoid1 == 1:
                    print("solenoid1")
                    self.solenoid1Pin.value(1)
                    value = self.solenoid1Ind
                    self.writeToDac(value)
                    self.time_intervals(interval_ms=self.reward1Duration)
                    self.solenoid1Pin.value(0)
                    self.writeToDac(0)
                if solenoid2 == 1:
                    print("solenoid2")
                    self.solenoid2Pin.value(1)
                    value = self.solenoid2Ind
                    self.writeToDac(value)
                    self.time_intervals(interval_ms=self.reward2Duration)
                    self.solenoid2Pin.value(0)
                    self.writeToDac(0)

                self.actuator1BackwardPin.value(1)
                
                #wait for actuator to move spouts backward
                self.time_intervals(interval_ms=self.actuatorBackwardDuration)
                
                self.actuator1BackwardPin.value(0)
                #timeWindow = utime.ticks_ms()
                #break
                self.writeToDac(0)
            

                
        
        
            # after trial is done, start iti
            self.time_intervals(interval_ms=self.iti)
            self.trial = self.trial + 1
            print("next trial " + str(self.trial))

    def time_intervals(self, interval_ms=100):
        time1 = utime.ticks_ms()
        time2 = utime.ticks_ms()
        while time2 - time1 < interval_ms:
            time2 = utime.ticks_ms()

    def writeToDac(self,value):
        buf=bytearray(2)
        buf[0]=(value >> 8) & 0xFF
        buf[1]=value & 0xFF
        self.i2c.writeto(self.i2cAdd[0],buf)
    
    def volt2Int(self, volt=0, minI = 0, maxI=4095, minV=0, maxV=5):
        deltaI = maxI - minI
        deltaV = maxV - minV
        value = (deltaI * (volt - minI) / deltaV) + minV 
        value = round(value)
        return value

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

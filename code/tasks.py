import utime
from machine import Pin
from machine import PWM
#from machine import UART
#from machine import I2C
#
#from machine import RTC
#from machine import I2C
from machine import SoftI2C

import urandom

class Task1:
    def __init__(self):
        #set different analog voltage out for monitoring what was on/when
        self.stimIndValue = 3.5
        self.stimIndValue = self.volt2Int(volt = self.stimIndValue)
        self.lickSensor1Ind = 0.5
        self.lickSensor1Ind = self.volt2Int(volt = self.lickSensor1Ind)
        self.solenoid1Ind = 1.0
        self.solenoid1Ind = self.volt2Int(volt = self.solenoid1Ind)
        self.lickSensor2Ind = 2
        self.lickSensor2Ind = self.volt2Int(volt = self.lickSensor2Ind)
        self.solenoid2Ind = 2.5
        self.solenoid2Ind = self.volt2Int(volt = self.solenoid2Ind)
        
        #self.monitor1 = 998
        #self.monitor2 = 999
        self.i2c = SoftI2C(scl=Pin(12), sda=Pin(13), freq=100000)

        #self.i2c=SoftI2C(scl=Pin(9), sda=Pin(10))
        self.i2cAdd = self.i2c.scan()
        self.writeToDac(value=0x60)
        #write 0 volts to the DAC
        self.writeToDac(value=0)

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(5, Pin.IN, Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(18, Pin.IN, Pin.PULL_DOWN)
        
        self.servo1Pin = PWM(Pin(2), freq=50)
        self.servo2Pin = PWM(Pin(15), freq=50)
        self.servoMax = 50
        self.servoMin = 0
        
        #self.servo1ForwardPin = Pin(15, Pin.OUT)
        #self.servo1BackwardPin = Pin(2, Pin.OUT)
        
        
        
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
        #self.actuator1ForwardPin.value(0)
        #self.actuator1BackwardPin.value(0)
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
        self.actuatorForwardDuration = 400 #how much time the actuator spends moving forward
        self.actuatorBackwardDuration = 400 #how much time the actuator spends moving forward
        self.reward1Duration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.reward2Duration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
        self.moveBackDelay = 300
        self.numberOfTrials = 100  # the number of trials that will be presented to the animals
        
        self.trial = 1  # the current trial

        #create array with indication on which monitor should be on.
        #this should be a pseudorandom way
        #set a seed so that all the time the random order is the same 
        #urandom.seed(42)

        self.monitorOrder = [0]*self.numberOfTrials

        for i in range(self.numberOfTrials):
            self.monitorOrder[i]=self.monitorOrder[i]+urandom.randint(0,1)
        
        #print("monitor order")
        #print(self.monitorOrder)

    def run_task1(self):
        self.trial = 1
        self.twopPin.value(1)
        self.writeToDac(0)
        
        while self.trial <= self.numberOfTrials:
            # if it is the first trial, then wait for the baseline activity measurement
            #ANALOG OUT = 0

            if self.trial == 1:
                self.time_intervals(interval_ms=self.baseline)
                monitor = self.monitorOrder[self.trial]
                print("monitor: " + str(monitor) )
                self.monitorSidePin.value(monitor)
                self.time_intervals(interval_ms=10)

                #variables to monitor animal performance over time
                self.correctLick1Counter = 0
                self.correctLick2Counter = 0
                self.noLickCounter = 0
                self.incorrectLick1Counter = 0
                self.incorrectLick2Counter = 0

            #####ANALOG OUT = STIMULATION ON
            #value = self.volt2Int(volt = self.stimIndValue)
            #print("value: "+str(value))
            self.writeToDac(value = self.stimIndValue)
            
            #start stimulation
 
            self.stimTriggerPin.value(1) 
            

            #self.writeToDac(value = 0)
            print("stim on")

            
            self.time_intervals(interval_ms=self.stimDuration-self.actuatorForwardDuration)
            print("moving servos")
            # once stimulation is close to being done, start the actuator
            self. move_servos_forward()       
            
            
            
            #pause so that there is no false triggering of the lick sensors.
            self.time_intervals(interval_ms=200)
            
            #once the actuator is out, we can end the stimulation trigger
            self.stimTriggerPin.value(0) 
   

            ##### ANALOG OUT = STIMULATION OFF
            #value = self.volt2Int(volt = 0)
            self.writeToDac(value = 0)

            #start response window
            timeWindow1 = utime.ticks_ms()
            timeWindow2 = utime.ticks_ms()
            responseStatus = 0
            #solenoid1 = 0
            #solenoid2 = 0
            

            while timeWindow2-timeWindow1<self.responseWindowDuration:
                lick1Status = self.lickSensor1Pin.value()
                #print(str(lick1Status))
                lick2Status = self.lickSensor2Pin.value()
                if lick1Status == 1 and monitor == 0:
                    self.writeToDac(self.lickSensor1Ind)
                    self.time_intervals(interval_ms=5)                    
                    self.writeToDac(0)
                    responseStatus = 1
                    #solenoid1 = 1
                    #value = self.volt2Int(volt = self.lickSensor1Ind)
                    self.writeToDac(value = self.lickSensor1Ind)
                    #print("lick1"+ str(value))
                    break

                elif lick1Status == 1 and monitor == 1:
                    self.writeToDac(self.lickSensor1Ind)
                    self.time_intervals(interval_ms=5)                    
                    self.writeToDac(0)
                    responseStatus = 3
                    break
                    
                elif lick2Status == 1 and monitor == 1:
                    self.writeToDac(self.lickSensor2Ind)
                    self.time_intervals(interval_ms=5)                    
                    self.writeToDac(0)
                    #value = self.volt2Int(volt = self.lickSensor2Ind)
                    self.writeToDac(value = self.lickSensor2Ind)
                    responseStatus = 2
                    #solenoid2 = 1
                    
                    
                    break
                
                elif lick2Status == 1 and monitor == 0:
                    self.writeToDac(self.lickSensor2Ind)
                    self.time_intervals(interval_ms=5)                    
                    self.writeToDac(0)
                    responseStatus = 4
                    break
                else:
                    responseStatus = 0
                    #solenoid1 = 0
                    #solenoid2 = 0
                timeWindow2 = utime.ticks_ms()  

            
            if responseStatus == 0:
                self.noLickCounter = self.noLickCounter+1
                print("no licks")

            if responseStatus == 1:
                print("solenoid1")
                self.solenoid1Pin.value(1)
                #value = value+self.solenoid1Ind
                self.writeToDac(self.solenoid1Ind)
                self.time_intervals(interval_ms=self.reward1Duration)
                self.solenoid1Pin.value(0)
                self.writeToDac(0)
                self.correctLick1Counter = self.correctLick1Counter + 1
                
            
            if responseStatus == 2:
                print("solenoid2")
                self.solenoid2Pin.value(1)
                #value = value+self.solenoid2Ind
                self.writeToDac(self.solenoid2Ind)
                self.time_intervals(interval_ms=self.reward2Duration)
                self.solenoid2Pin.value(0)
                self.writeToDac(0)
                self.correctLick2Counter = self.correctLick2Counter + 1
          
            if responseStatus == 3:
                print("lick spout 1 error") 
                self.incorrectLick1Counter = self.incorrectLick1Counter + 1
            if responseStatus == 4:
                print("lick spout 2 error") 
                self.incorrectLick2Counter = self.incorrectLick2Counter + 1
            
            responseStatus = 0
            correctTrials = self.correctLick1Counter+self.correctLick2Counter
            incorrectTrials = self.incorrectLick1Counter+self.incorrectLick2Counter
            print("trials = " + str(self.trial))
            print("no lick = " + str(self.noLickCounter))
            print("correct trials = " + str(correctTrials))
            print("incorrect trials = " + str(incorrectTrials)+"\n")
            
            print("lick spout 1 correct = " + str(self.correctLick1Counter))
            print("lick spout 2 correct = " + str(self.correctLick2Counter)+"\n")
            
            print("lick spout 1 incorrect = " + str(self.incorrectLick1Counter))
            print("lick spout 2 incorrect = " + str(self.incorrectLick2Counter)+"\n")
                        
            self.time_intervals(interval_ms=self.moveBackDelay)

            self. move_servos_backward()

                
            #wait for actuator to move spouts backward
            #self.time_intervals(interval_ms=self.actuatorBackwardDuration)
                
            #self.actuator1BackwardPin.value(0)
            #timeWindow = utime.ticks_ms()
            #break
            #self.writeToDac(0)
            

                
        
        
            # after trial is done, start iti
            self.time_intervals(interval_ms=self.iti)
            
            self.trial = self.trial + 1
            
            print("next trial " + str(self.trial))
            
            monitor = self.monitorOrder[self.trial]
            
            print("monitor: " + str(monitor) )
            
            self.monitorSidePin.value(monitor)
            
            #except KeyboardInterrupt:
            #    self.writeToDac(0)
        
            
    def solenoid1(self):
        self.solenoid1Pin.value(1)
        self.time_intervals(interval_ms=self.reward1Duration)
        self.solenoid1Pin.value(0)
    
    def solenoid2(self):
        self.solenoid2Pin.value(1)
        self.time_intervals(interval_ms=self.reward2Duration)
        self.solenoid2Pin.value(0)


    def move_servos_forward(self):
        self.servo1Pin.duty(55)
        self.servo2Pin.duty(55)
        #step = 5
        #for i in range (0, 50, step):
        #    self.servo1Pin.duty(i)
        #    self.servo2Pin.duty(i)
        #    time.sleep (0.1)

    def move_servos_backward(self):
        self.servo1Pin.duty(25)
        self.servo2Pin.duty(25)
        #step = 5
        #for i in range (50, 0, -step):
        #    self.servo1Pin.duty(i)
        #    self.servo2Pin.duty(i)
        #    time.sleep (0.1)
            
    def actuator_forward(self):
        self.actuator1ForwardPin.value(1)
        #wait for actuator to move spouts forward
        self.time_intervals(interval_ms=self.actuatorForwardDuration)

        self.actuator1ForwardPin.value(0)
    
    def actuator_backward(self):
        self.actuator1BackwardPin.value(1)
        #wait for actuator to move spouts backward
        self.time_intervals(interval_ms=self.actuatorBackwardDuration)  
        self.actuator1BackwardPin.value(0)    
        
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

    def setDAC2start0(self):
        '''this function writes data to the EEPROM of the MCP4725 DAC board
        in this specific case we want to set the board to always output 0 when
        it is first starting, or in low power mode.
        - in principle this only needs to be run once
        - it is also possible to change this so that the DAC will output another 
        specified value different than 0 when first started and/or low power mode.
        '''
        buf = bytearray()
        buf.append(0x60)
        buf.append(1)
        buf.append(0)
        self.i2c.writeto(self.i2cAdd[0],buf)
        return
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

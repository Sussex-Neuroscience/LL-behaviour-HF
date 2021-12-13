import utime
from machine import Pin
from machine import PWM
#from machine import UART
#from machine import I2C
#
#from machine import RTC
#from machine import I2C
from machine import SoftI2C
from machine import UART


import urandom
import time

class Task1:
    def __init__(self,testing=0):
        #set different analog voltage out for monitoring what was on/when
        #fid=open("session_res.csv","w")
        #fid.close()
        #self.uart = UART(1, baudrate=9600, tx=1, rx=3)
        #self.uart.write('hello')  # write 5 bytes
        #print("hello")
        self.stimIndValue = 3.5
        self.stimIndValue = self.volt2Int(volt = self.stimIndValue)
        self.lickSensor1Ind = 1.0
        self.lickSensor1Ind = self.volt2Int(volt = self.lickSensor1Ind)
        self.solenoid1Ind = 0.5
        self.solenoid1Ind = self.volt2Int(volt = self.solenoid1Ind)
        self.lickSensor2Ind = 2.5
        self.lickSensor2Ind = self.volt2Int(volt = self.lickSensor2Ind)
        self.solenoid2Ind = 2.0
        self.solenoid2Ind = self.volt2Int(volt = self.solenoid2Ind)
        
        #self.monitor1 = 998
        #self.monitor2 = 999
        self.i2c = SoftI2C(scl=Pin(12), sda=Pin(13), freq=100000)

        #self.i2c=SoftI2C(scl=Pin(9), sda=Pin(10))
        self.i2cAdd = self.i2c.scan()
        #self.writeToDac(value=0x60)
        #write 0 volts to the DAC
        #self.writeToDac(value=0)

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(5, Pin.IN, Pin.PULL_DOWN)
        self.lickSensor2Pin = Pin(18, Pin.IN, Pin.PULL_DOWN)
        
        #self.actuator1ForwardPin = Pin(15, Pin.OUT)
        #self.actuator1BackwardPin = Pin(2, Pin.OUT)
        self.servo1Pin = PWM(Pin(2), freq=50)
        self.servo2Pin = PWM(Pin(15), freq=50)
        
        self.servoMax = 45
        self.servoMin = 25
        
        
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

        #store what the animal did
        #1 = correct lick spout 1
        #2 = correct lick spout 2
        #3 = incorrect lick spout 1
        #4 = incorrect lick spout 2
        #0 = no response
        self.responseStatus = 0
        

        self.twopPin.value(0)
        self.monitorSidePin.value(0)
        ##self.monitor1Pin.off()
        ##self.monitor2Pin.off()


        # time/interval variables
        self.iti = 10000  # inter trial interval in ms
        self.baseline = 10000  # time to wait at the beginning of session to record baseline
        self.stimDuration = 10000  # stimulus presentation duration
        self.responseWindowDuration = 2000  # time window to respond after stim presentation
        #self.actuatorForwardDuration = 300 #how much time the actuator spends moving forward
        #self.actuatorBackwardDuration = 300 #how much time the actuator spends moving forward
        self.reward1Duration = 100  # duration the solenoid valves will stay in open state, 
                                    #which ends up being the amount of water offered
        self.reward2Duration = 100  # duration the solenoid valves will stay in open state,
        ##                          #which ends up being the amount of water offered
        self.moveBackDelay = 700
        self.numberOfTrials = 100 # the number of trials that will be presented to the animals
        
        
        
        if testing==1:
            self.iti = 2500  # inter trial interval in ms
            self.baseline = 1000  # time to wait at the beginning of session to record baseline
            self.stimDuration = 2500  # stimulus presentation duration
            self.responseWindowDuration = 2000  # time window to respond after stim presentation
            #self.actuatorForwardDuration = 300 #how much time the actuator spends moving forward
            #self.actuatorBackwardDuration = 300 #how much time the actuator spends moving forward
            self.reward1Duration = 100  # duration the solenoid valves will stay in open state, 
            self.reward2Duration = 100  # duration the solenoid valves will stay in open state, 
            self.moveBackDelay = 0
            self.numberOfTrials = 30 # the number of trials that will be presented to the animals
        
        #self.trial = 0  # the current trial

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
        
        trial = 0
        self.twopPin.value(1)
        #self.writeToDac(0)
        #lick1Status = 0
        #lick2Status = 0
        
        while trial < self.numberOfTrials:
            # after trial is done, start iti
            #self.time_intervals(interval_ms=self.iti)
            
            #self.trial = self.trial + 1
            #print("status: "+str(self.responseStatus)+"\n")
            #print("trial " + str(trial+1),end='')
            #fid.write("trial " +str(trial+1)+"\n\r")
            if self.responseStatus == 3 or self.responseStatus == 4:
                monitor = self.bias_correction()
                #print("bias correction  ",end='')
                
            else:
                #print("no correction")
                monitor = self.monitorOrder[trial]
            
            self.monitorSidePin.value(monitor)
            self.time_intervals(interval_ms=10)
            
            #print("  monitor: " + str(monitor), end='' )
            #fid.write("monitor Side " +str(monitor)+"\n\r")
            
        #while self.trial <= self.numberOfTrials:
            # if it is the first trial, then wait for the baseline activity measurement
            #ANALOG OUT = 0
            #monitor = self.monitorOrder[trial]
            
            if trial == 0:
                self.time_intervals(interval_ms=self.baseline)
                #monitor = self.monitorOrder[trial]
                #print("monitor: " + str(monitor) )
                #self.monitorSidePin.value(monitor)
                #

                #variables to monitor animal performance over time
                self.correctLick1Counter = 0
                self.correctLick2Counter = 0
                self.noLickCounter = 0
                self.incorrectLick1Counter = 0
                self.incorrectLick2Counter = 0

            #####ANALOG OUT = STIMULATION ON
            #value = self.volt2Int(volt = self.stimIndValue)
            #print("value: "+str(value))
            #self.writeToDac(value = self.stimIndValue)
            
            #start stimulation
            #print("  stim on",end='')
            self.stimTriggerPin.value(1) 
            

            ##self.writeToDac(value = 0)
            

            #self.time_intervals(interval_ms=self.stimDuration)
            
            #end the stimulation trigger
            #self.stimTriggerPin.value(0) 
            
            self.time_intervals(interval_ms=self.stimDuration-550)
            #print("moving actuator\n")
            # once stimulation is close to being done, start the actuator
            self.move_servos_forward()
            #print("moving servos")
            # once stimulation is close to being done, start the actuator
              
            
            
            
            #once the actuator is out, we can end the stimulation trigger
            #self.stimTriggerPin.value(0) 
   
            #pause so that there is no false triggering of the lick sensors.
            self.time_intervals(interval_ms=200)
            ##### ANALOG OUT = STIMULATION OFF
            #value = self.volt2Int(volt = 0)
            #self.writeToDac(value = 0)

            #start response window
            timeWindow1 = utime.ticks_ms()
            timeWindow2 = utime.ticks_ms()

            #solenoid1 = 0
            #solenoid2 = 0
            

            while timeWindow2-timeWindow1<self.responseWindowDuration:
                self.stimTriggerPin.value(1)
                lick1Status = self.lickSensor1Pin.value()
                #print(str(lick1Status))
                lick2Status = self.lickSensor2Pin.value()
                
                if lick1Status == 1 and monitor == 0:
                    #self.writeToDac(self.lickSensor1Ind)
                    self.time_intervals(interval_ms=5)                    
                    #self.writeToDac(0)
                    self.responseStatus = 1
                    #solenoid1 = 1
                    #value = self.volt2Int(volt = self.lickSensor1Ind)
                    #self.writeToDac(value = self.lickSensor1Ind)
                    #print("lick1"+ str(value))
                    break

                elif lick1Status == 1 and monitor == 1:
                    #self.writeToDac(self.lickSensor1Ind)
                    self.time_intervals(interval_ms=5)                    
                    #self.writeToDac(0)
                    self.responseStatus = 3
                    break
                    
                elif lick2Status == 1 and monitor == 1:
                    #self.writeToDac(self.lickSensor2Ind)
                    self.time_intervals(interval_ms=5)                    
                    #self.writeToDac(0)
                    #value = self.volt2Int(volt = self.lickSensor2Ind)
                    #self.writeToDac(value = self.lickSensor2Ind)
                    self.responseStatus = 2
                    #solenoid2 = 1
                    
                    
                    break
                
                elif lick2Status == 1 and monitor == 0:
                    #self.writeToDac(self.lickSensor2Ind)
                    self.time_intervals(interval_ms=5)                    
                    #self.writeToDac(0)
                    self.responseStatus = 4
                    break
                
                elif lick1Status == 0 and lick2Status == 0:
                    self.responseStatus = 0
                    #solenoid1 = 0
                    #solenoid2 = 0
                
                timeWindow2 = utime.ticks_ms()  

            
            if self.responseStatus == 0:
                self.noLickCounter = self.noLickCounter+1
                
                #print("no licks")

            if self.responseStatus == 1:
                #print("solenoid1\n")
                self.solenoid1Pin.value(1)
                #value = value+self.solenoid1Ind
                #self.writeToDac(self.solenoid1Ind)
                self.time_intervals(interval_ms=self.reward1Duration)
                self.solenoid1Pin.value(0)
                #self.writeToDac(0)
                self.correctLick1Counter = self.correctLick1Counter + 1
                
            
            if self.responseStatus == 2:
                #print("solenoid2\n")
                self.solenoid2Pin.value(1)
                #value = value+self.solenoid2Ind
                #self.writeToDac(self.solenoid2Ind)
                self.time_intervals(interval_ms=self.reward2Duration)
                self.solenoid2Pin.value(0)
                #self.writeToDac(0)
                self.correctLick2Counter = self.correctLick2Counter + 1
            
            #self.writeToDac(self.stimIndValue)
            
            if self.responseStatus == 3:
                #print("lick spout 1 error\n") 
                self.incorrectLick1Counter = self.incorrectLick1Counter + 1
            if self.responseStatus == 4:
                #print("lick spout 2 error\n") 
                self.incorrectLick2Counter = self.incorrectLick2Counter + 1
            
            #self.responseStatus = 0
            correctTrials = self.correctLick1Counter+self.correctLick2Counter
            incorrectTrials = self.incorrectLick1Counter+self.incorrectLick2Counter
            
            print("trial, " + str(trial+1)+",", end=' ')
            print("monitor, "+ str(monitor)+",", end=' ')
            print("response Status, "+ str(self.responseStatus)+",", end=' ')
            print(" no lick, " + str(self.noLickCounter)+",", end=' ')
            print(" correct trials, " + str(correctTrials)+",", end=' ')
            print(" incorrect trials, " + str(incorrectTrials)+",",end=' ')
            
            print(" spout 1 correct, " + str(self.correctLick1Counter)+",", end=' ')
            print(" spout 2 correct, " + str(self.correctLick2Counter)+",", end=' ')
            
            print(" spout 1 incorrect, " + str(self.incorrectLick1Counter)+",", end=' ')
            print(" spout 2 incorrect, " + str(self.incorrectLick2Counter)+",", end='\n')
                        
            self.time_intervals(interval_ms=self.moveBackDelay)
            
            self.move_servos_backward()
            
            #once the servos have been moved back, we can end the stimulation trigger
            #fid=open("session_res.csv","a")
            #fid.write("trial, " +str(trial+1)+",")
            #fid.write("monitor, " +str(monitor)+",")
            #fid.write("response status, " +str(self.responseStatus)+",")
            #fid.write("monitor, " +str(monitor)+",")
            #fid.close()
            #fid.write("bias corrected, " +str(trial+1)+"\n\r")
            
            
            
            
            #self.writeToDac(0)
            self.stimTriggerPin.value(0) 
            
            
            
            #self.actuator1BackwardPin.value(1)
                
            #wait for actuator to move spouts backward
            #self.time_intervals(interval_ms=self.actuatorBackwardDuration)
                
            #self.actuator1BackwardPin.value(0)
            #timeWindow = utime.ticks_ms()
            #break
            ##self.writeToDac(0)
            

                
        
        
            # after trial is done, start iti
            self.time_intervals(interval_ms=self.iti)
            if self.responseStatus == 3 or self.responseStatus==4:
                trial=trial
            else:
                trial = trial+1
        
        fid.close()
        
            #self.trial = self.trial + 1
            
            #print("next trial " + str(trial+1))
            
            #monitor = self.monitorOrder[trial]
            
            #print("monitor: " + str(monitor) )
            
            #self.monitorSidePin.value(monitor)
            
            #except KeyboardInterrupt:
            #    #self.writeToDac(0)

    def move_servos_forward(self):
        
        #self.servo1Pin.duty(self.servoMax)
        #self.servo2Pin.duty(self.servoMax)
        #self.time_intervals(interval_ms=200)
        step = 5
        for i in range (self.servoMin, self.servoMax+5, step):
            self.servo1Pin.duty(i)
            self.servo2Pin.duty(i)
            time.sleep (0.1)

    def move_servos_backward(self):
        #self.servo1Pin.duty(self.servoMin)
        #self.servo2Pin.duty(self.servoMin)
        step = 5 
        for i in range (self.servoMax, self.servoMin-5, -step):
            self.servo1Pin.duty(i)
            self.servo2Pin.duty(i)
            time.sleep (0.1)            
            
    def bias_correction(self):#,trial=0):
        if self.responseStatus==3:
            monitor=1
        elif self.responseStatus==4:
            monitor=0
        return monitor#,trial
        
        
    def solenoid1(self):
        self.solenoid1Pin.value(1)
        self.time_intervals(interval_ms=self.reward1Duration)
        self.solenoid1Pin.value(0)
    
    def solenoid2(self):
        self.solenoid2Pin.value(1)
        self.time_intervals(interval_ms=self.reward2Duration)
        self.solenoid2Pin.value(0)


    #def actuator_forward(self):
    #    self.actuator1ForwardPin.value(1)
    #    #wait for actuator to move spouts forward
    #    self.time_intervals(interval_ms=self.actuatorForwardDuration)

    #    self.actuator1ForwardPin.value(0)
    
    #def actuator_backward(self):
    #    self.actuator1BackwardPin.value(1)
    #    #wait for actuator to move spouts backward
    #    self.time_intervals(interval_ms=self.actuatorBackwardDuration)
    #    self.actuator1BackwardPin.value(0)    
        
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
        #self.i2c.writeto(self.i2cAdd[0],buf)
        return
    #example DAC
    ##self.writeToDac(2048)




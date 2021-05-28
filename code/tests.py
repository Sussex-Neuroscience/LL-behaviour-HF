import utime
import urandom
from machine import Pin
#from machine import I2C
from machine import SoftI2C

class Tests:
    def __init__(self):

        self.stimIndValue = 0.1
        self.lickSensor1Ind = 0.1
        self.lickSensor2Ind = 0.2
        self.solenoid1Ind = 0.4
        self.solenoid2Ind = 0.8
        
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
        self.stimTriggerPin = Pin(22, Pin.OUT)
        
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
        
        ##self.monitor1Pin.off()
        ##self.monitor2Pin.off()

        # set a seed for a random number generator (fixing the seed will allow for )
        # or make a list with the order of presentation in the monitors
        # time/interval variables
        self.iti = 5000  # inter trial interval in ms
        self.baseline = 10000  # time to wait at the beginning of session to record baseline
        self.stimDuration = 5000  # stimulus presentation duration
        self.responseWindowDuration = 2000  # time window to respond after stim presentation
        self.rewardDuration = 1000  # duration the solenoid valves will stay in open state, which ends up being the amount of water offered
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
            
        
        #initialize serial port 1 for communication with host pc
        #self.uart = UART(0, 9600)                         # init with 9600 baudrate

    def peripherals(self):
        for i in range(10):
            print("trial "+ str(i))
            # once stimulation is done, start the actuators
            print("actuator move foward")
            self.actuator1ForwardPin.on()
            #wait for actuator to move spouts forward
            self.time_intervals(interval_ms=2000)#
            self.actuator1ForwardPin.off()

            time1 = utime.ticks_ms()
            time2 = utime.ticks_ms()
            lick1Status = 0
            lick2Status = 0
            intervalms = 10000
            while time2 - time1 < intervalms:
                print("lick window")
                
                time2 = utime.ticks_ms()
                lick1Status = self.lickSensor1Pin.value()
                print("lick1 status")
                print(lick1Status)

                lick2Status = self.lickSensor2Pin.value()
                print("lick2 status")
                print(lick2Status)

                if lick1Status == 1:
                    
                    self.solenoid1Pin.on()
                    self.time_intervals(interval_ms=2000)
                    self.solenoid1Pin.off()
                    lick1Status = 0

                if lick2Status == 1:
                    self.solenoid2Pin.on()
                    self.time_intervals(interval_ms=500)
                    self.solenoid2Pin.off()
                    lick2Status = 0
                
            print("actuator move backward")
            self.actuator1BackwardPin.on()
            #wait for actuator to move spouts forward
            self.time_intervals(interval_ms=2000)#
            self.actuator1BackwardPin.off()
            self.time_intervals(interval_ms=2000)
    
    def serial(self):
        pass
        #initialize serial port 1 for communication with host pc
        #self.uart = UART(0, 9600)                         # init with 9600 baudrate
        #for i in range(10):
        #    monitor = self.monitorOrder[i]
        #    self.uart.write(monitor)
        #    while self.uart.any():
        #        print("empty")
        #    
        #    read = self.uart.readline()

    def DAC(self,value=10):
        buf=bytearray(2)
        buf[0]=(value >> 8) & 0xFF
        buf[1]=value & 0xFF
        self.i2c.writeto(self.i2cAdd[0],buf)

    def time_intervals(self, interval_ms=100):
        time1 = utime.ticks_ms()
        time2 = utime.ticks_ms()
        while time2 - time1 < interval_ms:
            time2 = utime.ticks_ms()
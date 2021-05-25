import utime
import urandom
from machine import Pin
from machine import I2C

class Tests:
    def __init__(self):
        # ports
        self.lickSensor1 = 1
        self.lickSensor2 = 4
        self.actuator1Forward = 2
        self.actuator1Backward = 15 # see if this conflicts with i2c
        self.solenoid1 = 16
        self.solenoid2 = 19
        self.stimTrigger = 7
        self.stimIndValue = 0.1
        self.lickSensor1Ind = 0.1
        self.lickSensor2Ind = 0.2
        self.solenoid1Ind = 0.4
        self.solenoid2Ind = 0.8
        
        #self.monitor1 = 8
        #self.monitor2 = 9
        #self.i2c=I2C(0, scl=Pin(14), sda=Pin(15))
        #self.i2cAdd = self.i2c.scan()

        # set the "direction" of the ports
        self.lickSensor1Pin = Pin(self.lickSensor1, Pin.IN)#, Pin.PULL_DOWN)
        #self.lickSensor2Pin = Pin(self.lickSensor2, Pin.IN)#, Pin.PULL_DOWN)
        #self.actuator1ForwardPin = Pin(self.actuator1Forward, Pin.OUT)
        #self.actuator1BackwardPin = Pin(self.actuator1Backward, Pin.OUT)
        #self.solenoid1Pin = Pin(self.solenoid1, Pin.OUT)
        #self.solenoid2Pin = Pin(self.solenoid2, Pin.OUT)
        #self.stimTriggerPin = Pin(self.stimTrigger, Pin.OUT)
        #self.monitor1Pin = Pin(self.monitor1, Pin.OUT)
        #self.monitor2Pin = Pin(self.monitor2, Pin.OUT)


        #turn everything off at the beginning
        #self.actuator1ForwardPin.off()
        #self.actuator1BackwardPin.off()
        #self.solenoid1Pin.off()
        #self.solenoid2Pin.off()
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
        #for i in range(self.numberOfTrials):
        #    self.monitorOrder.append(urandom.randint(0,1))
        
        #print("monitor order")
        #print(self.monitorOrder)
            
        
        #initialize serial port 1 for communication with host pc
        #self.uart = UART(0, 9600)                         # init with 9600 baudrate

    #def tests_peripherals(self):
    #    for i in range(10):
    #        print("trial "+ str(i))
    #        # move spouts
    #        # once stimulation is done, start the actuators
    #        self.actuator1ForwardPin.on()
    #        #wait for actuator to move spouts forward
    #        self.time_intervals(interval_ms=100)#
    #
    #        self.actuator1ForwardPin.off()
    #        time1 = utime.ticks_ms()
    #        time2 = utime.ticks_ms()
    #        lick1Status = 0
    #        lick2Status = 0
    #        intervalms = 2000
    #        while time2 - time1 < intervalms:
    #            time2 = utime.ticks_ms()
    #            lick1Status = self.lickSensor1Pin.value()
    #            lick2Status = self.lickSensor2Pin.value()
    #            if lick1Status == 1:
    #                
    #                self.solenoid1Pin.on()
    #                self.time_intervals(interval_ms=100)
    #                self.solenoid1Pin.off()
    #            if lick2Status == 1:
    #                self.solenoid2Pin.on()
    #                self.time_intervals(interval_ms=100)
    #                self.solenoid2Pin.off()
    
    def test_serial(self):
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

    def test_DAC(self):
        pass
        #buf=bytearray(2)
        #buf[0]=(value >> 8) & 0xFF
        #buf[1]=value & 0xFF
        #self.i2c.writeto(self.i2cAdd,buf)

    
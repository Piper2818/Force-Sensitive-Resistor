"""A Program to measure force using the
Force-Sensitive Resistor (FSR): Interlink 402"""
"""A FSR is a variable resistor that changes its resistance
in proportion to the force applied. Interlink 402 is a cheap
FSR and not highly accurate"""


#import time
from time import sleep
#Import Serial Programmable Interface module from the Adafruit SPI library
import Adafruit_GPIO.SPI as SPI
#Import the MCP3008 module from the Adafruit library
import Adafruit_MCP3008
#Import GPIO library
import RPi.GPIO as io

#Define SPI Port and Device Identifiers
spiPort = 0
#SPI Device Identifier
spiDevice = 0
#Analog To Digital Object Global Variable
adc = 0
#Channel Number to which the FSR is connected
chnFSR = 0

"""A callback method to be called when the pushbutton is pressed
The callback method should measure the channel 0"""
def MeasureForce(channel):
    """Variable to store the dynamic resistance of FSR
        initialized to the upper limit value"""
    #print('\nbtn pressed') # just a print to test that my btn is working, don't need
    R1 = 0.0
    #Resistance in Series with FSR:
    R2 = 10000.0 # ohms
    #Valid Maximum Force Sensor Resistance
    MaxR1 = 30000.0
    #Force Variable
    Force = 0.0
    #Define the maximum decimal value that can be measured on Channel 0 of the ADC
    MaxRawValue = 1023
    """Define the reference value of the input voltage signal connected
        to Channel 0 of the ADC"""
    RefVolt = 3.3
    """Variables to store the raw and corresponding values of the voltage
        measured at Channel 0 of the ADC"""
    rawValue = 0 #Variable to store the raw value of the signal input to Channel 0
    VoltageSum = 0.0 #Variable to store the sum of twenty five analog samples
    AverageVoltage = 0.0 #Variable to store the average of twenty-five analog samples
    """Sampling twenty-five values over a period of 2.5 seconds
     and storing sum of the twenty five samples in the variable VoltageSum"""
    Samples = 25
    count = 0 # initialize count, just for testing
    for sample in range(Samples):
        """Read the raw value from the Channel 0 using the chnFSR variable
            and adc object, and store in variable rawValue"""
        #rawValue = adc.ReadChannel(chnFSR) # test line
        #print(rawValue) # don't need just a test to see what this value is
        rawValue = adc.read_adc(chnFSR)
        #print('Raw Value = {:4d}\tVoltage = {:.2f}'.format(rawValue,Voltage)) # don't need just a test
        #print(count) # just a test to make sure my loop is running 25 times, not asked for in assignment
        """Convert the rawValue to its corresponding analog Voltage using the
            RefValue and add it to the VoltageSum variable"""
        volts = rawValue*(RefVolt/MaxRawValue) # Volts
        #print('Volts: ' , volts) # just testing to see that my chip is reading values, don't need
        VoltageSum = VoltageSum + volts # Volts
        #print('VoltageSum:{:.5f} '.format(VoltageSum))
        #Sleep for appropriate time to perform 25 samples approximately in 2.5 seconds
        sleep(0.1)
        count = count + 1 # increment count, just for testing
    #Compute the average of the twenty-five samples and store in AverageVoltage
    AverageVoltage = VoltageSum / Samples # Volts
    print('Average Voltage: {:.2f} V '.format(AverageVoltage))
    """Compute the resistance R1 of the Force Sensor using the Voltage divider formulae,
        the RefVolt, Average Voltage and R2"""
    R1 = ( (RefVolt - AverageVoltage) * R2) / (AverageVoltage)      
    #Display the Force Sensing Resistor value matching the sample format
    print('Force Sensor Resistance: {:.3f} Ohms'.format(R1))
    """Compute the corresponding force using the straight line equations
        only if the measured resistance of the FSR is less than or equal to 30,000 ohms"""
    """You should first implement an if-else to check whether the measured resistance
        is less than 30kohms, and then inside the if condition implement
        three if conditions corresponding to the three line segements"""
    if R1 <= 30000: # ohms
        if R1 <= 30000 and R1 > 6000: # ohms
            Force = (R1 - 36000) / -300 # g
            print('Applied Force: {:.2f} g'.format(Force))
        elif R1 <= 6000 and R1 > 1000: # ohms
            Force = (R1 - 6555) / -5.556 # g
            print('Applied Force: {:2f} g'.format(Force))
        elif R1 <= 1000 and R1 > 150: # ohms
            Force = (R1 - 1094.4) / -0.0944 # g
            print('Applied Force: {:.2f} g'.format(Force))
    else:
        # If the Force Sensor Resitance is greater then 30,000 ohms then, less than 20g is being applied to sensor and we can't calculate
        # 20g of force = 30,000 g of force roughly
        print('The applied Force is less than 20g')
   
if __name__ == '__main__':
    # Initialize a variable to save the btn pin
    # btn is set for pull down (red line)
    btnMeasureForce = 26
    io.setmode(io.BCM)
    #Instantiate a ADC object using the global variable adc, spiPort, and spiDevice
    #ACD Object = object of type MCP3008 from Adafruit_MCP3008??
    adc = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(spiPort,spiDevice))
   
    """setup the push button using the variable btnMeasureForce
        connected to GPIO26"""
    io.setup(btnMeasureForce, io.IN, pull_up_down = io.PUD_DOWN)
    """setup the OS to detect an edge event at GPIO26 with the
        callback method MeaureForce"""
    io.add_event_detect(btnMeasureForce,io.RISING,callback = MeasureForce,bouncetime = 400)
   
   
    input('Press Pushbutton to start measuring Force\n or press any key to exit')
    print('Exiting the program')
    io.cleanup()
   

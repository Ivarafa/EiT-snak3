# This Python file uses the following encoding: utf-8

from __future__ import division
import numpy as np


# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).


# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)


# Configure min and max servo pulse lengths
FREQUENCY = 50
NUM_SERVOS = 6
servo_min = 205  # Min pulse length out of 4096
servo_max = 410  # Max pulse length out of 4096
# Helper function to make setting a servo pulse width simpler.
# Set frequency to 60hz, good for servos.


class MotorInterface:
    def __init__(self, freq = FREQUENCY, num_servos = NUM_SERVOS):
        self.freq = freq
        self.num_servos = num_servos
        print("frequency set to", self.freq)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.freq)

    def setAbsAngles(self, angles):
        relAngles = [0]*self.num_servos
        relAngles[0] = angles[0]
        for i in range(1, self.num_servos):
            relAngles[i] = angles[i] - angles[i-1]
        processedAngles = self.convertAngles(relAngles)
        print(processedAngles)
        for i in range(self.num_servos):
            if (processedAngles[i] > servo_min and processedAngles[i] < servo_max):
                self.pwm.set_pwm(i, 0, processedAngles[i])
            else:
                print("motor value error")

    def convertAngles(self, angles):
        return [self.convert(ang) for ang in angles]

    #TODO: This method may need updating based on output from main loop
    def convert(self, angle):
        return int(102/np.pi*2*angle + 307.5)

    def reset(self):
        """Sends a software reset (SWRST) command to all servo drivers on the bus."""
        # Setup I2C interface for device 0x00 to talk to all of them.
        import Adafruit_GPIO.I2C as I2C
        i2c = I2C
        device = i2c.get_i2c_device(0x00)
        device.writeRaw8(0x06)  # SWRST
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self.freq)
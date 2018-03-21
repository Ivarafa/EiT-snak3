# This Python file uses the following encoding: utf-8

import ASUS.GPIO as GPIO
import time

#Constants
#TODO: Fill inn the pin numbers used
pins = []        #write pins used here in order back to front of the snake
FREQUENCY = 50
INIT_ANGLE = 7.5


GPIO.setmode(GPIO.ASUS)
GPIO.setwarnings(False)
servos = []


def conncet(num):
    for i in range(num):
        myservo = getNextPin()
        GPIO.setup(myservo,GPIO.OUT)
        pwm = GPIO.PWM(myservo, FREQUENCY)
        pwm.start(INIT_ANGLE)
        servos.append(pwm)

def shutDown():
    GPIO.cleanup()

def getNextPin():
    global pins
    return pins.pop()

def setServos(angles):
    processedAngles = convertAngles(angles)
    for i in range(len(servos)):
        servos[i].ChangeDutyCycle(processedAngles[i])

def convertAngles(angles):
    return [convert(ang) for ang in angles]

#TODO: This method may need updating based on output from main loop
def convert(angle):
    return angle
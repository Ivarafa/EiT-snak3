# This Python file uses the following encoding: utf-8


class Sensor:

    #TODO: connection method
    def __init__(self):
        self.value = ""

    #TODO: method to read and store value of sensor
    def read(self):
        self.value = ""   #TODO: get the value from a sensor

    #method for returning value of the sensor
    def getValue(self):
        return self.formatted(self.value)

    #TODO: update or omit whether or not processing of the sensor value is needed
    def formatted(self,value):
        return value
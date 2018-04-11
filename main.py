# This Python file uses the following encoding: utf-8

import DecisionMaker
#import MotorInterface                  #Must be uncommented when shipped to TinkerBoard
import SensorReader
import ComInput
import sys

class RobotProgram:

    def __init__(self, num_of_links=7, *args):
        #Type fixing
        num_of_links = int(num_of_links)

        self.coms = self.setUpComs()
        self.sensors = self.setUpSensors()
        self.motors = self.setUpMotors()
        self.decision_maker = DecisionMaker.SimpleDecisionMaker()     #Replace with actual decision maker

        #The following variable is maybe better replaced by a list of joint angles
        self.snake = [0]*num_of_links       #init snake as fully stretched along x-axis

        self.knowledge = {}                 #dict of relevant info for the decsion_maker


    #TODO: should return a list of Connection objects from ComInput
    def setUpComs(self):
        return []

    #TODO: should return a list of Sensor objects from SensorReader
    def setUpSensors(self):
        return []

    #TODO: should make us of MotorInterface (which needs update due to hardware addition)
    def setUpMotors(self):
        return []

    #TODO: Should make use of threading!
    def run(self):
        try:
            while True:
                for i in range(len(self.sensors)):
                    self.knowledge['sen{0}'.format(i)] = self.sensors[i].getValue()
                for i in range(len(self.coms)):
                    self.knowledge['com{0}'.format(i)] = self.coms[i].getValue()       #may want to do this another way
                angles = self.decision_maker.getDecision(self.snake, **self.knowledge)
                print(angles)
                for i in range(len(self.motors)):
                    self.motors[i].setAngle(angles[i])              #This function is not supported in motorInterface
        except:
            self.shutDown()

    def shutDown(self):
        for sensor in self.sensors:
            sensor.shutDown()
        for com in self.coms:
            com.close()
        #The following loop must be updated acording to update of motorInterface
        for motor in self.motors:
            motor.shutDown()



if __name__ == '__main__':
    print(sys.argv[1:])
    program = RobotProgram(*sys.argv[1:])
    program.run()

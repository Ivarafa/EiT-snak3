# This Python file uses the following encoding: utf-8

import DecisionMaker
#import MotorInterface                  #Must be uncommented when shipped to TinkerBoard
import SensorReader
import ComInput
import sys
import threading

class RobotProgram:

    def __init__(self, num_of_links=7, *args):
        #Type fixing
        self.num_of_links = int(num_of_links)

        self.coms = self.setUpComs()
        self.sensors = self.setUpSensors()
        self.motors = self.setUpMotors()
        self.decision_maker = DecisionMaker.SimpleDecisionMaker()     #Replace with actual decision maker

        #The following variable is maybe better replaced by a list of joint angles
        self.snake = [0]*self.num_of_links       #init snake as fully stretched along x-axis

        self.knowledge = {}                 #dict of relevant info for the decsion_maker


    #TODO: should return a list of Connection objects from ComInput
    def setUpComs(self):
        return []

    def handle_message(self, message):
        key, val = message[0],message[1]
        if key == "start":
            self.running = True
        elif key == "stop":
            self.running = False
        elif key == "shutdown":
            self.shutDown()
        elif key == "reset":
            self.reset()
        else:
            print("Unrecognized command")

    def reset(self):
        self.running = False
        angles = [0]*self.num_of_links
        for i in range(len(self.motors)):
            self.motors[i].setAngle(angles[i])


    #TODO: should return a list of Sensor objects from SensorReader
    def setUpSensors(self):
        return []

    #TODO: should make us of MotorInterface (which needs update due to hardware addition)
    def setUpMotors(self):
        return []

    #TODO: Should make use of threading!
    def run(self, messages, lock):
        self.program = True
        self.reset()
        try:
            while self.program:
                lock.acquire()
                for i in range(len(messages)):
                    print("Handling coms message")
                    self.handle_message(messages.pop(0))
                lock.release()
                if self.running:
                    for i in range(len(self.sensors)):
                        self.knowledge['sen{0}'.format(i)] = self.sensors[i].getValue()
                    angles = self.decision_maker.getDecision(self.snake, **self.knowledge)
                    print(angles)
                    for i in range(len(self.motors)):
                        self.motors[i].setAngle(angles[i])              #This function is not supported in motorInterface
        except Exception as e:
            print(e)
            self.shutDown()

    def shutDown(self):
        print("Shutting down")
        for sensor in self.sensors:
            sensor.shutDown()
        #The following loop must be updated acording to update of motorInterface
        for motor in self.motors:
            motor.shutDown()
        self.program = False



if __name__ == '__main__':
    print(sys.argv[1:])
    messages = []
    lock = threading.Lock()
    server_thread = threading.Thread(target=ComInput.run, args=(messages,lock,))
    server_thread.start()
    program = RobotProgram(*sys.argv[1:])
    program_thread = threading.Thread(target=program.run, args=(messages,lock,))
    program_thread.start()
    program_thread.join()
    server_thread.join()


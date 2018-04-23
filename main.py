# This Python file uses the following encoding: utf-8
import numpy as np
import DecisionMaker
import MotorInterface                  #Must be uncommented when shipped to TinkerBoard
import SensorReader
import ComInput
import sys
import threading
import time

ctrl_freq = 0.5
ctrl_amplitude = np.pi/2
ctrl_phase = -1


class RobotProgram:

    def __init__(self, num_of_links=7, *args):
        #Type fixing
        self.num_of_links = int(num_of_links)

        self.coms = self.setUpComs()
        self.sensors = self.setUpSensors()
        self.motors = MotorInterface.MotorInterface(50, num_of_links-1)
        self.decision_maker = DecisionMaker.SimpleDecisionMaker(ctrl_freq, ctrl_amplitude, ctrl_phase, time.time())     #Replace with actual decision maker

        #The following variable is maybe better replaced by a list of joint angles
        self.snake = [0]*self.num_of_links       #init snake as fully stretched along x-axis

        self.knowledge = {}                 #dict of relevant info for the decsion_maker


    #TODO: should return a list of Connection objects from ComInput
    def setUpComs(self):
        return []

    def handle_message(self, message):
        key, val = message[0],message[1]
        if (key == "start" and self.state == "stop"):
            self.state = "init"
        elif (key == "straight" and self.state == "stop"):
                state = "straight"
        elif key == "stop":
            self.state = "stop"
        elif key == "shutdown":
            self.shutDown()
        elif key == "reset":
            self.reset()
        else:
            print("Unrecognized command")

    def reset(self):
        self.state = "stop"
        self.motors.reset()
        angles = [0]*(self.num_of_links-1)
        self.motors.setAbsAngles(angles)


    #TODO: should return a list of Sensor objects from SensorReader
    def setUpSensors(self):
        return []


    #TODO: Should make use of threading!
    def run(self, messages, lock):
        self.program = True
        self.reset()
        
        while self.program:
            try:
                lock.acquire()
                for i in range(len(messages)):
                    print("Handling coms message")
                    self.handle_message(messages.pop(0))
                lock.release()
                if self.state == "stop":
                    "empty state"
                if self.state == "straight":
                    angles = [0]*self.num_of_links
                    self.motors.setAbsAngles(angles)
                    self.state = "stop"
                if self.state == "init":
                    angles = [0]*self.num_of_links
                    for j in range(50):
                        for i in range(self.num_of_links-1):
                            angles[i] = j/50.0*ctrl_amplitude*np.cos(ctrl_phase*i)
                        time.sleep(0.1)
                        self.motors.setAbsAngles(angles)
                    time.sleep(1)
                    self.decision_maker.reset(time.time())
                    self.state = "running"
                if self.state == "running":
                    for i in range(len(self.sensors)):
                        self.knowledge['sen{0}'.format(i)] = self.sensors[i].getValue()
                    angles = self.decision_maker.getDecision(self.snake, **self.knowledge)
                    self.motors.setAbsAngles(angles)
            except OSError as e:
                print(e)
            except Exception as e:
                print(e)
                self.shutDown()
                break

    def shutDown(self):
        print("Shutting down")
        self.motors.reset()
        for sensor in self.sensors:
            sensor.shutDown()
        #The following loop must be updated acording to update of motorInterface
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


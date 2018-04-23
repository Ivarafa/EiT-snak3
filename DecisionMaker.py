# This Python file uses the following encoding: utf-8

import random
import numpy as np

import time
#this class is meant as an abstract superclass with it's methods overwritten
class DecisionMaker:
    #init should set relevant static info
    def __init__(self):
        ""

    #this function may be redundant (only need getDecsion)
    def updateKnowledge(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def getDecision(self, snake, **kwargs):
        raise NotImplementedError

class SimpleDecisionMaker(DecisionMaker):
    def __init__(self, freq, amp, phase, timeatstart):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.t0 = timeatstart

    def reset(self, timeatstart):
        self.t0 = timeatstart

    def getDecision(self, snake, **kwargs):
        return [self.amp*np.cos(self.freq*(time.time()-self.t0) + self.phase*i) for i in range(len(snake)-1)]

class RandomDecisionMaker(DecisionMaker):

    def getDecision(self, snake, **kwargs):
        return [(random.random()-.5)*np.pi/4 for x in range(len(snake)-1)]
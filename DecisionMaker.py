# This Python file uses the following encoding: utf-8

import random

#this class is meant as an abstract superclass with it's methods overwritten
class DecisionMaker:
    #init should set relevant static info
    def __init__(self):
        ""

    #this function may be redundant (only need getDecsion)
    def updateKnowledge(self):
        raise NotImplementedError

    def getDecision(self, snake, **kwargs):
        raise NotImplementedError

class SimpleDecisionMaker(DecisionMaker):

    def getDecision(self, snake, **kwargs):
        return [random.random()*10-5 for x in range(len(snake)-1)]


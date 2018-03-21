# This Python file uses the following encoding: utf-8

#this class is meant as an abstract superclass with it's methods overwritten
class DecisionMaker:
    #init should set relevant static info
    def __init__(self):
        ""

    def updateKnowledge(self):
        raise NotImplementedError

    def getDecision(self):
        raise NotImplementedError


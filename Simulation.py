__author__ = 'Ivar A. Fauske'
# This Python file uses the following encoding: utf-8
import random
import numpy as np
import time

servo_slew = 2
link_length = 40
link_mass = 5

def sat(low,x,high):
    if(x<low):
        return low
    elif(x>high):
        return high
    else:
        return x


class Link:
    def __init__(self, id, parent, child, length, mass, angle=0):
        self.id = id
        self.parent = parent
        self.child = child
        self.length = length
        self.mass = mass
        self.inertia = self.mass*self.length**2/3
        self.angle = angle
    def get_T_matrix(self):
        T_matrix = np.matrix([[np.cos(self.angle), -np.sin(self.angle), link_length*np.cos(self.angle)], [np.sin(self.angle), np.cos(self.angle), link_length*np.sin(self.angle)], [0, 0, 1]])
        return T_matrix
    def get_displacement(self):
        disp = np.matrix([[link_length*np.cos(self.angle)],[link_length*np.sin(self.angle)]])
        return disp
class Snake:
    def __init__(self, size, joints = [], links=[], linkmass=0.5,  pos=(0,0)):
        self.joints = joints
        self.size = size
        self.links = links
        self.speed = 0
        self.timeatstart = time.time()
        self.lastmovetime = time.time()
        self.pos = np.matrix(pos)
        self.linkmass = linkmass
        self.e = np.matrix([1 for i in range(size)]).T
        self.phi = 0
    def make(self,size):
        prev_link = Link(0,None,None, link_length, link_mass)
        self.links.append(prev_link)
        for i in range(1,size):
            link = Link(i,prev_link,None, link_length, link_mass)
            self.links.append(link)
            prev_link = link
        return self
    def get_size(self):
        return self.size
    def move(self):
        t = time.time()
        self.phi += (t - self.lastmovetime)*self.speed
        self.lastmovetime = t
        self.speed = (t-self.timeatstart)**(1/2)
        for i in range(0,self.size):
            print(self.speed)
            self.links[i].angle =  servo_slew/sat(servo_slew,self.speed,10)*np.cos(self.phi + i)
    def heading(self):
        return sum([x.angle for x in self.links])/len(self.links)
    def get_cm(self):
        cm = np.matrix([[0.0],[0.0]])
        link_start = np.matrix([[0.0],[0.0]])
        for i in range(0,self.size):
            cm += self.linkmass*(self.links[i].get_displacement()/2 + link_start)
            link_start += self.links[i].get_displacement()
        cm = cm/(self.linkmass*self.size)
        return cm
    def get_velocity(self):
        return np.matrix([np.cos(self.heading()),np.sin(self.heading())])*self.get_cm().T

__author__ = 'Ivar A. Fauske'
# This Python file uses the following encoding: utf-8
import random
import numpy as np
import time

servo_slew = 2
link_length = 40
link_mass = 5
f_fric = 0.1
c_fric = 5.0

def sat(low,x,high):
    if(x<low):
        return low
    elif(x>high):
        return high
    else:
        return x


class Link:
    def __init__(self, id, length, mass, angle=0, angle_dot = 0):
        self.id = id
        self.length = length
        self.mass = mass
        self.inertia = self.mass*self.length**2/3
        self.angle = angle
        self.angle_dot = 0
    def get_T_matrix(self):
        T_matrix = np.matrix([[np.cos(self.angle), -np.sin(self.angle), link_length*np.cos(self.angle)], [np.sin(self.angle), np.cos(self.angle), link_length*np.sin(self.angle)], [0, 0, 1]])
        return T_matrix
    def get_displacement(self):
        disp = np.matrix([[link_length*np.cos(self.angle)],[link_length*np.sin(self.angle)]])
        return disp
class Snake:
    def __init__(self, size, joints = [], links=[], linkmass=0.5,  pos=(0.0,300.0)):
        self.joints = joints
        self.size = size
        self.links = links
        self.velocity = np.matrix([[1.0],[0.0]])
        self.timeatstart = time.time()
        self.lastmovetime = time.time()
        self.pos = np.matrix(pos).T
        self.linkmass = linkmass
        self.e = np.matrix([1 for i in range(size)]).T
        self.phi = 0
        self.e = np.matrix([1 for i in range(size)]).T
        self.A = np.matrix([[1 if j==i or j==i+1 else 0 for j in range(size)]for i in range(size-1)])
        self.D = np.matrix([[1 if j==i else -1 if j==i+1 else 0 for j in range(size)]for i in range(size-1)])
        self.K = np.transpose(self.A)*np.linalg.inv(self.D*np.transpose(self.D))*self.D
    def make(self):
        for i in range(0 ,self.size):
            link = Link(i,link_length, link_mass)
            self.links.append(link)
        return self
    def get_size(self):
        return self.size
    def move(self):
        t = time.time()
        self.phi += (t - self.lastmovetime)*self.get_speed()
        ZF = 0
        for i in range(0,self.size):
            angle =  servo_slew/self.get_speed()*np.cos(self.phi + i)
            angle = sat(-1.57,angle,1.57)
            self.links[i].angle_dot = (angle - self.links[i].angle)/(t-self.lastmovetime)
            self.links[i].angle = angle
        XY_dot = self.big_XY_dot()
        self.velocity += (t-self.lastmovetime)*self.friction()/float(self.linkmass*self.size)
        self.pos += self.velocity*(t-self.lastmovetime)
        self.lastmovetime = t
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
    def get_pos(self):
        return self.pos
    def get_speed(self):
        return np.linalg.norm(self.velocity)**(1/2)
    def diag(self, mat):
        return np.matrix([[mat.item(i) if j==i else 0 for j in range(np.shape(mat)[1])] for i in range(np.shape(mat)[1])])
    def big_XY(self):
        theta = []
        stheta = []
        ctheta = []
        for i in range(0, self.size):
            th = self.links[i].angle
            theta.append(th)
            stheta.append(np.sin(th))
            ctheta.append(np.cos(th))
        theta = np.transpose(np.matrix(theta))
        stheta = np.transpose(np.matrix(stheta))
        ctheta = np.transpose(np.matrix(ctheta))
        X = -link_length/2*np.transpose(self.K)*ctheta + self.e*self.get_cm()[0]
        Y = -link_length/2*np.transpose(self.K)*stheta + self.e*self.get_cm()[1]
        return np.stack((np.transpose(X),np.transpose(Y)))
    def big_XY_dot(self):
        theta = []
        theta_dot = []
        stheta = []
        ctheta = []
        for i in range(0, self.size):
            th = self.links[i].angle
            theta.append(th)
            theta_dot.append(self.links[i].angle_dot)
            stheta.append(np.sin(th))
            ctheta.append(np.cos(th))
        theta = self.diag(np.matrix(theta))
        theta_dot = np.transpose(np.matrix(theta_dot))
        stheta = self.diag(np.matrix(stheta))
        ctheta = self.diag(np.matrix(ctheta))
        X = link_length/2*np.transpose(self.K)*stheta*theta_dot + self.e*self.velocity[0]
        Y = -link_length/2*np.transpose(self.K)*ctheta*theta_dot + self.e*self.velocity[1]
        return np.stack((np.transpose(X),np.transpose(Y)))
    def friction(self):
        ZF = np.matrix([[0.0],[0.0]])
        XY_dot = self.big_XY_dot()
        for i in range(self.size):
            cos = np.cos(self.links[i].angle)
            sin = np.sin(self.links[i].angle)
            f_der = cos*XY_dot[0,i] - sin*XY_dot[1,i]
            c_der = sin*XY_dot[0,i] + cos*XY_dot[1,i]
            #Coloumb friction
            ZF += np.matrix([[cos*f_fric*np.sign(f_der) + sin*c_fric*np.sign(c_der)],[- sin*f_fric*np.sign(f_der) + cos*c_fric*np.sign(c_der)]])
        return ZF


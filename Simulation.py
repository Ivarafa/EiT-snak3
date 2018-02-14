__author__ = 'Ivar A. Fauske'
# This Python file uses the following encoding: utf-8

import random
import numpy as np


class Link:

    def __init__(self, id, parent, child, length, mass, pos=(0,0), angle=0):
        self.id = id
        self.parent = parent
        self.child = child
        self.length = length
        self.mass = mass
        self.pos = np.matrix(pos)
        self.cm = np.matrix((pos[0]+length,pos[1]+length))
        self.inertia = self.mass*self.length**2/3
        self.angle = angle
        self.rotation_matrix = self.get_rotation_matrix()

    def get_rotation_matrix(self):
        return np.matrix([[np.cos(self.angle), -np.sin(self.angle)],[np.sin(self.angle),np.cos(self.angle)]])


class Joint:
    def __init__(self, id, left, right, pos=(0,0), angle=0):
        self.id = id
        self.left = left
        self.right = right
        self.angle = self.calc_angle()
        self.pos = np.matrix(pos)

    def calc_angle(self):
        self.angle = self.left.angle-self.right.angle


class Snake:
    def __init__(self, size, joints = [], links=[], mass=0):
        self.joints = joints
        self.size = size
        self.links = links
        self.cm = np.matrix((0,0)) #needs fix!
        self.mass = mass
        self.e = np.matrix([1 for i in range(size)]).T
        self.A = np.matrix([[1 if j==i or j==i+1 else 0 for j in range(size)]for i in range(size-1)])
        self.D = np.matrix([[1 if j==i else -1 if j==i+1 else 0 for j in range(size)]for i in range(size-1)])

    def make_random(self,size):
        prev_joint = Joint(0,None,None,(random.randint(0,500),random.randint(0,500)))
        self.joints.append(prev_joint)
        for i in range(1,size):
            joint = Joint(i,prev_joint,None,(16+prev_joint.pos[0],prev_joint.pos[1]))
            self.joints.append(joint)
            link = Link(i,prev_joint,joint,(prev_joint.pos[0]+13,prev_joint.pos[1]+5))
            self.links.append(link)
            prev_joint = joint
        return self

    def get_size(self):
        return len(self.joints)

    def move(self):
        self.joints[0].rotation += 0.02

    def heading(self):
        return sum([x.angle for x in self.links])/len(self.links)

    def get_cm(self):
        X = np.matrix([x.cm.item(0) for x in self.links])
        Y = np.matrix([x.cm.item(1) for x in self.links])
        self.cm[0,0] = X*self.e/self.size
        self.cm[0,1] = Y*self.e/self.size
        return self.cm

    def get_velocity(self):
        return np.matrix([np.cos(self.heading()),np.sin(self.heading())])*self.get_cm().T

    def sign(self, mat):
        return np.sign(mat)

    #takes in a 1 x N matrix returns N x N diagonal matrix
    def diag(self, mat):
        return np.matrix([[mat.item(i) if j==i else 0 for j in range(np.shape(mat)[1])] for i in range(np.shape(mat)[1])])

    def t_inverse(self):
        return np.matrix([self.D.T*(self.D*self.D.T).I,self.e])

    def update_X(self):
        ""

l = Link(0,None,None,5,10)
print(l)
s = Snake(4)
for i in range(4):
    s.links.append(Link(i,None,None,5,10,(10*i +5 ,0)))
print(s.heading(),s.get_velocity())
print(s.t_inverse())

'''
snake = Snake().make_random(3)

print([(x.id,x.pos) for x in snake.joints])
print([x.id for x in snake.links])
'''
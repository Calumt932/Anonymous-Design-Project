# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:51:31 2022

@author: bjorn
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import time
from scipy.fftpack import fft,rfft,fftfreq

# def implicitit_Euler():
#     y_i+f(x_i+1,y_i+1)dt-y_i+1 = 0

# Main class that contains all methodologies pertaining to solving FPUT problems numerically 
class FPUT():
    
    # Configure the variables needed for computing the solution
    def __init__(self,X=np.zeros(65),V=np.zeros(65),L=1,N=65,Time=120,k=0.1,p=400,alpha=0,time_step = 0.01):
        self.nodes = N
        self.length= L
        
        self.h = L/(N-1)
        self.m = self.h*p
        self.k = k/self.h

        self.alpha = alpha
        self.Time = int(Time/time_step)
        self.time_step = time_step
        self.node_positions = np.arange(0,L+L/(N-1),L/(N-1))

        # Generate a list of initial displacement & velocity if the initial profile input,X & V,is a function
        # Else if the X & V is a list of displacement, no function will be called. 

        self.init_x = X(self.node_positions) if callable(X) else X
      
        if len(self.init_x) != self.nodes:
            print("\nList of initial positions must equal number of Nodes.")
            return(None)
    
        
        self.init_v = V(self.node_positions) if callable(V) else V
        if len(self.init_v) != self.nodes:
            print("\nList of initial velocities must equal number of Nodes.")
            return(None)
        
        # Set the boundaries to 0, as per the boundary conditions
        self.init_x[[0,-1]] = 0
        self.init_v[[0,-1]] = 0
        
        
    # Solve for the accleration at each node as per the FPUT Differential Equation.
    def Acceleration(self, pos):
        # Generate list of displacement pairs, for easier computing. 
        pos_pairs = [pos[i:i+3] for i in range(len(pos)-2)]
        
        # Define the FPUT equation
        a = lambda x: (self.k/self.m)*(x[0]+x[2]-2*x[1])*(1+self.alpha*(x[2]-x[0]))

        acc = [a(x) for x in pos_pairs] # Generate list of acceleration at each node
        acc = np.concatenate([[0],acc,[0]]) # Our method truncates the list, so we append 0 to each end to compensate.
        
        return acc

    # Following section describes methods we used to solve the FPUT problem
    # They all take in a list of displacement and velocity and calculates values for the next time step.

    def Euler(self, pos, vel):
        
        acc = self.Acceleration(pos)

        pos = pos + self.time_step*vel
        vel = vel + self.time_step*acc

        return pos, vel

    def Euler_Mod(self, pos, vel):

        acc = self.Acceleration(pos)
        dpos = 0.5*acc*(self.time_step**2)
        pos += dpos + self.time_step * vel
        vel += self.time_step * acc

        return pos, vel
    
    def Implicitit_Euler(self,pos,vel):
        pass
    
    def RK(self, pos, vel):
        
        dt = self.time_step
        pos_0 = pos

        kv1 = self.Acceleration(pos_0)
        kp1 = vel
        vel_1 = vel + 0.5*dt*kv1

        #Implicit Euler
        pos_1 = pos + 0.5*dt*vel_1
        
        kv2 = self.Acceleration(pos_1)
        kp2 = vel_1
        vel_2 = vel + 0.5*dt*kv2
        pos_2 = pos + 0.5*dt*vel_2
        
        kv3 = self.Acceleration(pos_2)
        kp3 = vel_2
        vel_3 = vel + dt*kv3
        pos_3 = pos + dt*vel_3

        kv4 = self.Acceleration(pos_3) 
        kp4 = vel_3
        
        new_pos = pos + (dt/6)*(kp1+2*kp2+2*kp3+kp4)
        
        new_vel = vel + (dt/6)*(kv1+2*kv2+2*kv3+kv4)
        
        if any(y > 100000 for y in new_vel):
            print(new_vel)
            print("overflowed")
            return(None)
        
        return new_pos, new_vel
    


    # Main function that puts everything together
    # Solves FPUT problem iteratively with the chosen method
    # Argument, technique, is which method to use
    # returns a list of node displacements at each time step

    def GetData(self,technique = "Euler"):

        pos = []
        self.technique = technique
        if technique == "Euler":
            Method = self.Euler
        elif technique == "RK":
            Method = self.RK
        elif technique == "Euler_Mod":
            Method = self.Euler_Mod

        x = self.init_x
        v = self.init_v

        for i in range(self.Time):
            pos.append(x)
            x,v = Method(x,v)
        
        return pos


    # Returns a list of normalizedfourier coefficient amplitudes at each timestep 
    # and the corresponding frequencies.
    def FFT(self, data, nodes, length):
        
        freq = np.fft.fftfreq(nodes) * nodes * 1/length
        coef = np.array([2/nodes*np.abs(np.fft.rfft(i)) for i in data])
        
        # for index,i in enumerate(coef):
        #     coef[index] = coef[index]/sum(coef[index][:len(coef[index])//2])
        # for i in range(6):
        #     print(coef[i])
        #     print(coef[i].shape)

        return coef,freq





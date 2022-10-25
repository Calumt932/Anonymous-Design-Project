# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:51:31 2022

@author: bjorn
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from scipy.fftpack import fft

class FPUT():
    
    def __init__(self,X,V,L,N,Time,k,p,alpha, time_step = 0.01):
        self.nodes = N
        self.length= L
        
        self.h = L/(N-1)
        self.m = self.h*p
        self.k = k/self.h
        # predefining k/m instead of recomputing it every iteration saves 0.4s
        # Note 2: It doesnt matter, same speed
        # self.f = (self.k/self.m)

        self.alpha = alpha
        self.Time = int(Time/time_step)
        self.time_step = time_step
        self.node_positions = np.arange(0,L+L/(N-1),L/(N-1))
        
        self.init_x = X(self.node_positions) if callable(X) else X
      
        if len(self.init_x) != self.nodes:
            print("List of initial positions must equal number of Nodes.")
            return(None)
        
        self.init_v = V(self.node_positions) if callable(V) else V
        if len(self.init_v) != self.nodes:
            print("List of initial velocities must equal number of Nodes.")
            return(None)
        
        self.init_x[[0,-1]] = 0
        self.init_v[[0,-1]] = 0
        
        

    def Acceleration(self, pos):
        pos_pairs = [pos[i:i+3] for i in range(len(pos)-2)]
        
        a = lambda x: (self.k/self.m)*(x[0]+x[2]-2*x[1])*(1+self.alpha*(x[2]-x[0]))
        acc = [a(x) for x in pos_pairs]
        acc = np.concatenate([[0],acc,[0]])
        
        return acc

        
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
    

    def GetData(self,technique = "Euler"):
        pos = []
        
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

    def PlotInstance(self,df,target_time):
        index = int(target_time/self.time_step)
        x = self.node_positions
        y = df[index]
        plt.plot(x,y)
        plt.show()



    def Baseline(self, ratio = 1000):
        
        pos = self.init_x
        vel = self.init_v

        pos_list = []

        for i in range(self.Time*ratio):

            if i % ratio == 0:
                pos_list.append(pos)

            acc = self.Acceleration(pos)
        
            pos = pos + (self.time_step/ratio)*vel
            vel = vel + (self.time_step/ratio)*acc


        return pos_list


    def FFT(self, x):

        coef = [fft(i) for i in x]

        norm = lambda n,sum_n: n/sum_n

        coef = [norm(n,np.sum(n)) for n in coef] 






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
        self.m= self.h*p
        self.k = k/self.h
        self.alpha = alpha
        self.Time = Time
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
        
        print(self.k/self.m)
        

    def Acceleration(self, pos):
        pos_pairs = [pos[i:i+3] for i in range(len(pos)-2)]
        
        a = lambda x: (self.k/self.m)*(x[0]+x[2]-2*x[1])*(1+self.alpha*(x[2]-x[0]))
        acc = [a(x) for x in pos_pairs]
        # acc = np.array(list(map(a,pos_pairs)))
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





        
            
  
        
            
        
       





Node, Length, k, p, T = 65,1,0.1,400,12000

f = lambda x: np.sin(2*np.pi*x+np.pi)
FPUT = FPUT(f,np.zeros(Node),Length,Node,T,k,p,alpha=0.0)

def checkError():

    data = np.array(FPUT.GetData(technique="RK"))
    base = np.load("Baseline.npy")

    error = 0
    for i,j in zip(data,base):
        
        error += np.mean(abs(i[:]-j[:]))

    print(f"Mean Error: {error/T}")

def save_baseline():
    base = np.array(FPUT.Baseline(ratio=1000))
    np.save("Baseline.npy",base)


checkError()






def Plot():
    
    fig, ax = plt.subplots()
    
    x = Test1.node_positions

    def animate(i):
        
        ax.cla()
        ax.set_xlim(0,Test1.length)
        ax.set_ylim(-1.2,1.2)
        ax.plot(x,data[i])
        return ax
        
    ani = animation.FuncAnimation(fig, animate, frames=12000, interval=10, repeat=False)
    return ani
    

# ani = Plot()
# ani.save("RK_0.5.mp4")


def FFT(x):

        # coef = [fft(i) for i in x]
        coef = fft(x)
        coef = abs(coef)
        norm = lambda n,sum_n: n/sum_n
        plt.plot(x,coef)
        plt.xlim(-0.025,0.025)

        plt.show()

        coef = coef/np.sum(coef) 

        print(coef)


x = np.linspace(0,1,1000, endpoint=True)
y = [f(i) for i in x]

# FFT(y)

# plt.plot(x,y)
# plt.show()
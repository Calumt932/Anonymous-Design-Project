from FPUT import FPUT
import numpy as np

Node, Length, k, p, T = 65,1,0.1,400,120

f = lambda x: np.sin(2*np.pi*x+np.pi)
FPUT = FPUT(f,np.zeros(Node),Length,Node,T,k,p,alpha=0.25)





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

def Animate(self,data,ratio=4):
        start_time = time.time()
        def Plot():
        
            fig, ax = plt.subplots()
            
            x = self.node_positions

            def animate(i):
                ax.cla()
                ax.set_xlim(0,self.length)
                ax.set_ylim(-1.2,1.2)
                ax.plot(x,data[ratio*i])
                return ax
                
            ani = animation.FuncAnimation(fig, animate, frames=int(self.Time/ratio), interval=int(ratio*self.time_step*1000), repeat=False)
            return ani
        ani = Plot()
        ani.save(f"1.mp4")
        process_time = time.time() - start_time
        print(f"Animation function process time: {process_time} s")

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
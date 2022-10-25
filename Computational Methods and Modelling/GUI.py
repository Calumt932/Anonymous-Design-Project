import tkinter as tk
import numpy as np
import math
import time

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from FPUT import FPUT


class GUI():

    def __init__(self):
        pass

    def start(self):
        self.root = tk.Tk()

        self.root.title("FPUT Solver Graphical User Interface")

        screen_width=int(self.root.winfo_screenwidth())
        screen_height=int(self.root.winfo_screenheight())

        gui_width = int(0.9*screen_width)
        gui_height = int(0.9*screen_height)

        self.root.geometry(f"{gui_width}x{gui_height}")
        self.root.resizable(False, False)


        Entry_Node = tk.Frame()
        node_label=tk.Label(master=Entry_Node,text="Node",width=10)
        node_entry=tk.Entry(master=Entry_Node,width=6,bd=5)


        Entry_Node.grid(row=1,column=1)
        node_label.pack(side=tk.LEFT)
        node_entry.pack(side=tk.LEFT)

        Entry_Length = tk.Frame()
        l_label = tk.Label(master=Entry_Length,text="Length",width=10)
        l_entry = tk.Entry(master=Entry_Length, width=6,bd=5)

        Entry_Length.grid(row=2,column=1)
        l_label.pack(side=tk.LEFT)
        l_entry.pack(side=tk.LEFT)

        Entry_Time = tk.Frame()
        time_label = tk.Label(master=Entry_Time,text="Time",width=10)
        time_entry = tk.Entry(master=Entry_Time, width=6,bd=5)

        Entry_Time.grid(row=3,column=1)
        time_label.pack(side=tk.LEFT)
        time_entry.pack(side=tk.LEFT)

        Entry_dt = tk.Frame()
        dt_label = tk.Label(master=Entry_dt,text="dt",width=10)
        dt_entry = tk.Entry(master=Entry_dt, width=6,bd=5)

        Entry_dt.grid(row=4,column=1)
        dt_label.pack(side=tk.LEFT)
        dt_entry.pack(side=tk.LEFT)


        Entry_k = tk.Frame()
        k_label = tk.Label(master=Entry_k,text="k",width=10)
        k_entry = tk.Entry(master=Entry_k, width=6,bd=5)

        Entry_k.grid(row=1,column=2)
        k_label.pack(side=tk.LEFT)
        k_entry.pack(side=tk.LEFT)

        Entry_p = tk.Frame()
        p_label = tk.Label(master=Entry_p,text="p",width=10)
        p_entry = tk.Entry(master=Entry_p, width=6,bd=5)

        Entry_p.grid(row=2,column=2)
        p_label.pack(side=tk.LEFT)
        p_entry.pack(side=tk.LEFT)

        Entry_alpha = tk.Frame()
        alpha_label = tk.Label(master=Entry_alpha,text="alpha",width=10)
        alpha_entry = tk.Entry(master=Entry_alpha, width=6,bd=5)

        Entry_alpha.grid(row=3,column=2)
        alpha_label.pack(side=tk.LEFT)
        alpha_entry.pack(side=tk.LEFT)


        Select_X = tk.Frame()
        fx_label = tk.Label(master=Select_X,text="Initial position profile")

        init_x = tk.IntVar(master=Select_X,value=1)
        fx_sine  = tk.Radiobutton(master=Select_X,indicatoron=0,width=15,text="Full Sine Wave",variable=init_x,value=1)
        fx_half  = tk.Radiobutton(master=Select_X,indicatoron=0,width=15,text="Half Sine Wave",variable=init_x,value=2)
        fx_custom = tk.Radiobutton(master=Select_X,indicatoron=0,width=15,text="Custom Profile",variable=init_x,value=3)

        fx_factor_label=tk.Label(master=Select_X,text="Amplitude Scaler")
        fx_factor= tk.Entry(master=Select_X,width=6,bd=5)
        Select_X.place(x=20,y=150)
        fx_label.pack()
        fx_sine.pack(side=tk.TOP)
        fx_half.pack(side=tk.TOP)
        fx_custom.pack(side=tk.TOP)
        fx_factor_label.pack(side=tk.TOP)
        fx_factor.pack(side=tk.TOP)


        Custom_X = tk.Frame()
        customx_label = tk.Label(master=Custom_X,text="Custom Initial position")
        customx_footnote = tk.Label(master=Custom_X,text="use python syntax, math module allowed")
        customx_entry = tk.Entry(master=Custom_X, width=35,bd=5)

        Custom_X.place(x=20,y=330)
        customx_label.pack()
        # customx_footnote.pack()
        customx_entry.pack()

        Select_V = tk.Frame()
        fv_label = tk.Label(master=Select_V,text="Initial velocity profile")
        init_v   = tk.IntVar(master=Select_V,value=3)

        fv_sine  = tk.Radiobutton(master=Select_V,indicatoron=0,width=15,text="Full Sine Wave",variable=init_v,value=1)
        fv_half  = tk.Radiobutton(master=Select_V,indicatoron=0,width=15,text="Half Sine Wave",variable=init_v,value=2)
        fv_custom= tk.Radiobutton(master=Select_V,indicatoron=0,width=15,text="Custom Profile",variable=init_v,value=3)

        fv_factor_label=tk.Label(master=Select_V,text="Amplitude Scaler")
        fv_factor= tk.Entry(master=Select_V,width=6,bd=5)
        Select_V.place(x=185,y=150)
        fv_label.pack()
        fv_sine.pack(side=tk.TOP)
        fv_half.pack(side=tk.TOP)
        fv_custom.pack(side=tk.TOP)
        fv_factor_label.pack(side=tk.TOP)
        fv_factor.pack(side=tk.TOP)


        Custom_V = tk.Frame()
        customv_label = tk.Label(master=Custom_V,text="Custom Initial Profile")
        customv_footnote = tk.Label(master=Custom_V,text="use python syntax, math module allowed")
        customv_entry = tk.Entry(master=Custom_V, width=35,bd=5)

        Custom_V.place(x=20,y=390)
        customv_label.pack()
        # customv_footnote.pack()
        customv_entry.pack()


        Shell = tk.Frame()
        shell_label = tk.Label(master=Shell,text="", fg="Red", font=("Helvetica", 13), relief=tk.GROOVE,width=32,height=4)

        Shell.place(x=20,y=570)
        shell_label.pack()

        def CalculateSolution():
            try:
                N = float(node_entry.get())
                L = float(l_entry.get())
                T = float(time_entry.get())
                k = float(k_entry.get())
                p = float(p_entry.get())
                alpha = float(alpha_entry.get())
                dt = float(dt_entry.get())
            except:
                shell_label.configure(text="Error: Invalid Input")

            x = init_x.get()
            x_scale = float(fx_factor.get()) if fx_factor.get().isdigit() else 1
            if x == 1:
                f = lambda x: x_scale*np.sin(2*np.pi*x/L)
            elif x == 2:
                f = lambda x: x_scale*np.sin(np.pi*x/L)
            elif x == 3:
                f = lambda x: eval(customx_entry.get())\
                if "x" in customx_entry.get() else 0*x+eval(customx_entry.get())
         

            v = init_v.get()
            v_scale = float(fv_factor.get()) if fv_factor.get().isdigit() else 1
            if v == 1:
                g = lambda x: v_scale*np.sin(2*np.pi*x/L)
            elif v == 2:
                g = lambda x: v_scale*np.sin(np.pi*x/L)
            elif v == 3:
                g = lambda x: eval(customv_entry.get())\
                if "x" in customv_entry.get() else 0*x+eval(customv_entry.get())
         


            self.fput = FPUT(f,g,L,N,T,k,p,alpha,dt)
            self.df = self.fput.GetData(technique="RK")
            shell_label.configure(text="Done!")



        Solve = tk.Frame()
        solve_button= tk.Button(master=Solve,text="Calculate!",font=("Helvetica",15),height=2,width=11,\
         bd=5, command=CalculateSolution)

        Solve.place(x=20,y=480)
        solve_button.pack()


        def Visualize():

            try:
                target = round(float(target_entry.get()),2)
                target = int(target/self.fput.time_step)
                fig = Figure(figsize=(8,8))
                a = fig.add_subplot(111)
                a.plot(self.fput.node_positions,self.df[target])

                a.set_title ("FPUT Problem", fontsize=16)
                a.set_ylabel("Displacement", fontsize=14)
                a.set_xlabel("Node Position", fontsize=14)
                a.set_ylim(ymin=-2,ymax=2)

                canvas = FigureCanvasTkAgg(fig, master=self.root)
                canvas.get_tk_widget().place(x=450, y=20)
                canvas.draw()

                # This function also plots, but it retains previous plots
                # self.fput.PlotInstance(self.df,target)

                shell_label.configure(text="Note: Remember to re-calculate\nif the inputs have changed\n(Excluding Target Time)")

            except:
                shell_label.configure(text="Error: Target Time Out Of Range")







        Target = tk.Frame()
        target_value = tk.DoubleVar(master=Target)
        target_label = tk.Label(master=Target,text="Target Time")
        target_entry = tk.Entry(master=Target, width=6, bd=5)

        target_scale = tk.Scale(master=Target,from_=0,to=1,orient=tk.HORIZONTAL,\
            resolution=0.01,length=140,sliderlength=15,variable=target_value)
        target_button= tk.Button(master=Target,text="Visualize",command=Visualize)

        Target.place(x=170,y=480)
        target_label.grid(row=1,column=1)
        target_entry.grid(row=2,column=1)
        # target_scale.grid(row=3,column=1)
        target_button.grid(row=2,column=2)


        self.root.mainloop()


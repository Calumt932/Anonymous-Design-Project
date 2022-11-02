# Anonymous-Design-Project

## Update 02/11
# Added Modal Analysis Functionality

```python
  # Returns a list of normalized fourier coefficient amplitudes
  # and a list of appropriate frequencies, as instrcuted per the numpy documentation.
  def FFT(self, data, nodes, length):
      freq = np.fft.fftfreq(nodes) * nodes * 1/length  
      coef = np.array([2/nodes*np.abs(np.fft.rfft(i)) for i in data])
      return coef,freq
```
Loops through the dataframe containing node displacements and compute the magnitude of fourier coefficient at each time step
Also produces a list of frequencies for which we can use to plot these coefficients.

## Taks
# Antreas - Research the relation between time step and the numerical method used to solve te problem, find out what limitations should be put on the the time step to avoid divergence.

# Nadia - Research different values of alpha and its effect on result, 

## Download the "Computational Methods And Modelling" Folder, Do Not Modify The Content.
To start the GUI, run main.py. 
Make sure you have the packages needed installed.

## Graphical User Interface Guide 

![alt text](https://github.com/B-Harakat/Anonymous-Design-Project/blob/main/gui.PNG?raw=true)

### Input of Characteristics of FPUT Problem
Everything should be self explanatory, do note that *Time* and *dt* has unit seconds.

### Initial Profiles for Node Positions and Velocities
Some pre-defined profiles can be selected, *Amplitude Scaler* scales the initial profiles by the input (defaults = 1 i.e. no scaling), can be negative. The *Custom Profile* allows for custom functions and should be a function of "*x*". The input expression will converted to a lambda function using *eval()* so *numpy* and *math* methods can be used when writing the custom profile. It can also be used to create uniform initial profiles i.e. simply input *0* in the fields if you want the initial profile to be at rest.

### Calculate And Visualize
Once the inputs and profiles has been selected, press *Calculate* to numerically solve the FPUT problem. Once finished, the solution at sepcified time can be visualized. *Note: If the inputs have been changed, you need generate a new sets of solution by pressing "Calculate", otherwise you'll be only visualizing the old solution.*

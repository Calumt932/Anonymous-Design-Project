# Anonymous-Design-Project

## Graphical User Interface Guide 

![alt text](https://github.com/B-Harakat/Anonymous-Design-Project/blob/main/gui.PNG?raw=true)

### Input of Characteristics of FPUT Problem
Everything should be self explanatory, do note that *Time* and *dt* has unit seconds.

### Initial Profiles for Node Positions and Velocities
Some pre-defined profiles can be selected, *Amplitude Scaler* scales the initial profiles by the input (defaults = 1 i.e. no scaling), can be negative. The *Custom Profile* allows for custom functions and should be a function of "*x*". The input expression will converted to a lambda function using *eval()* so *numpy* and *math* methods can be used when writing the custom profile. It can also be used to create uniform initial profiles i.e. simply input *0* in the fields if you want the initial profile to be at rest.

### Calculate And Visualize
Once the inputs and profiles has been selected, press *Calculate* to numerically solve the FPUT problem. Once finished, the solution at sepcified time can be visualized. *Note: If the inputs have been changed, you need generate a new sets of solution by pressing "Calculate", otherwise you'll be only visualizing the old solution.*

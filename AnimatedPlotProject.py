# Animatedplot.py
# Written by Isaac Ableidinger, Seth Walen, and Aaron Yow

import serial                       # Importing pyserial to the program.
import matplotlib.pyplot as plt     # Importing matplotlib to the program.
from matplotlib.animation import FuncAnimation # This enables the Fucnanimation part of matplotlib.

fig, ax = plt.subplots()            # First line of code to make a graph.
x=[]                                # Empty x list to fill later.
y=[]                                # Empty y lsit to fill in later.
ser = serial.Serial('COM5', baudrate = 9600, timeout=1)  # Using pyserial this connects the COM5 port to the program.

def animation(i,x,y,ser):           # Beginning of animation function.
    arduinoData = ser.readline().decode()  # Reading the incoming pyserial data.
    data =arduinoData[0:5]          # The 0 to 5 filters the data to just numbers.          
     
    try:                            # This statement says to use the floats only for the data graphing.
        y.append(float(data))       # Append the empty y list with incoming data 'data'.
        x.append(i)                 # Append (fill) the x list.
    except:                         # If the try statement doesn't work, then the blank data will be passed and not used.
        pass                 
    y = y[-100:]                    # This cuts the live data down so the graph doesnt get super compacted with too much data.
    x = x[-100:]                    # This cuts the live data down so the graph doesnt get super compacted with too much data.
    
    ax.clear()                      
    
    if data:                        # This if statement is the start of the filtering process for the incoming data. Only uses the data that can be changed to a float.
        float(data) 
        # High Range                
        if float(data)>=25:         # This is our first 'hot' threshold. If the temperature is above 25 degrees C, the line color changes to red and a message is displayed in the prompt and the graph.
            ax.plot(x,y,'r')        # Changing graph line color to red.

            ax.annotate('Water too hot. \n Check your fish!', # Displaying message in graph.
            xy=(50, 150),
            xycoords='figure pixels',
            horizontalalignment='left',
            verticalalignment='top')

            print('Temperature of your fish tank is reading too Hot. Please check your fish!') # Displaying message in prompt.
        # Mid Range
        elif float(data)<=25 and float(data)>23: # This code will print the graphs line with a black one to show that the temperature is normal.
            ax.plot(x,y,'k')        # Graph line color to black.
        # Low Range
        elif float(data)<=23:       # If the temperature drops below this number, it will change the color of the graph line to blue and print a warning in the prompt and on the graph.
            ax.plot(x,y,'b')        # Change graph line color to blue.
            
            ax.annotate('Water too cold. \n Check your fish!', # Print message on graph with a warning.
            xy=(50, 150),
            xycoords='figure pixels',
            horizontalalignment='left',
            verticalalignment='top')

            print('Temperature of your fish tank is reading too Cold. Please check your fish!') # Print warning message in prompt .
    else:                           # This lets the blank data pass and not be used which would otherwise would cause an error.          
        pass

    ax.set_title('Live Temperature Reading') # Set axes title. 
    ax.set_ylabel('Temperature in Celsius')  # Set y label.
    ax.set_xlabel('Time Elapsed in Seconds') # Set x label.

ani = FuncAnimation(fig, animation, fargs=(x,y,ser),interval=100) # This runs the animation.


plt.show()                          # This shows the plot
ser.close                           # This closes the serial
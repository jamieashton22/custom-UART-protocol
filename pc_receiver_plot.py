import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys
import serial
import serial.tools.list_ports
import time
import re
from collections import deque

in_frame = False
buffer = []
FLAG = 0x7E
ESC = 0x7D

# --------- SERIALPLOTTER CLASS ---------------------------------

class SerialPlotter: 

    def __init__(self, ax, twidth):                                     # ax - axis object where line will be plotted, twidth - length of time window for x axis
       
        self.ax = ax
        self.twidth = twidth

        # self.tdata = [0] # to hold time values
        # self.ydata = [0] # to hold sensor values


        # trying with deque
        self.tdata = deque(maxlen=1000)
        self.ydata = deque(maxlen=1000)

        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(0, 100)      # add y limits
        self.ax.set_xlim(0 ,self.twidth)
        

    def update(self, y, t):            # method to add a y-value to the plot and update it 

        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)

        if (self.tdata[-1]) < self.twidth:
            self.ax.set_xlim(0,10)
        else:
            self.ax.set_xlim((self.tdata[-1])-self.twidth, self.tdata[-1])

        if (self.ydata[-1]< 20):
            self.ax.set_ylim(0,20)
        else:
            self.ax.set_ylim(0, self.ydata[-1]+10)
        return self.line,


# ------ UNESCAPING function --------------

def unescape(buffer):
     
    result = []
    i = 0

    while i < len(buffer):
        if buffer[i] == ESC:
               
            if i + 1 < len(buffer):
                result.append(buffer[i+1] ^ 0x20)
                i += 2
            else:
                return [] # if frame is bad return empty frame 

        else:
               result.append(buffer[i])
               i += 1
            
    return result
     

# ---------- VERIFY FRAME function  ------------

def verify_frame(buffer):
     
    checksum = buffer[0] ^ buffer[1] ^ buffer[2] ^ buffer [3]

    if len(buffer) >=2 and len(buffer) == 3 + buffer[1] and checksum == buffer[4]:
        return(buffer)
    
    else:
         print("Invalid frame, discarding")
         return []
    

#--------- GET DISTANCE function ------------

def get_measurement(type, duration):

    if type == 1:        # ultrasonic distance measurement
        return(duration * 0.0343 * 0.5)
    

# ------ GET AND SELECT PORT --------------

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
port = ''
portList = []

print("\n List of available ports \n")
for onePort in ports:
    portList.append(str(onePort.device))
    print(str(onePort))

port = input("\n Select Port \n")

if port not in portList:
    print("Invalid port chosen")
    sys.exit(1)

print("\n Port selected: ")
print(port)

# OPEN PORT

# get baud rate from user

chosenBaud = input("\n Select Baud rate \n")

serialInst.baudrate = chosenBaud
serialInst.port = port
serialInst.open()
print("\n Port Open \n")


fig, ax = plt.subplots()
plotter = SerialPlotter(ax, 10)

start_time = time.time()

try:

    while True: 

        if serialInst.in_waiting:

            current_time = time.time()
            time_elapsed = current_time - start_time 
            
            byte_in = serialInst.read(1)[0]  # get numerical value

            if byte_in == FLAG: # if byte is a flag

                if in_frame == False:       
                    in_frame = True        # if we are not already in frame, we now are


                else:     # we ARE in frame and just processed a flag therefore we are at the end of a frame       
                #  so process the buffer then reset, 
                # run unescaping, extract type, length, payload bytes and checksum 

                    unescaped_buffer = unescape(buffer)
                    buffer = [] # clear buffer
                    in_frame = False # reset frame flag

                    # FIRST - verify length
                    unescaped_buffer = verify_frame(unescaped_buffer)

                    if len(unescaped_buffer) == 0:        # if buffer is empty
                        pass
                    
                    else:       # buffer is valid so carry on...
                    
                        type = unescaped_buffer[0]              # in case want to use later
                        payload_high = unescaped_buffer[2]
                        payload_low = unescaped_buffer[3]
                        
                        duration = payload_high << 8 | payload_low
                        distance = get_measurement(type, duration)
                        
                        plotter.update(float(distance), time_elapsed)
                        plt.pause(0.01)
                        
            elif in_frame == True:
                # append byte to buffer
                buffer.append(byte_in)

except KeyboardInterrupt:
    print(" Exiting")

finally:
    serialInst.close()
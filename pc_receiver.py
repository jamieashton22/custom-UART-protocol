import serial
import serial.tools.list_ports
import numpy as np
import sys
import time

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
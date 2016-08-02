# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:30:10 2016

@author: alexa_000
"""
import sys
from zaber.serial import *


#==============================================================================
# Required functionality:
#     -home command
#     -renumber command
#     -abs move
#     -rel move
#     -set origin
#     -set limits
#     -arbitrary scan, i.e. x by y pixels, with defined step size
#     -perhaps also arbitrary scan with x by y size in mm and generate approx step size.
#     -need to be able to save step size in both encoder values and um for each zaber device created
#     -need to be able to specify 2-axis or 3-axis
#     -should probably do this with classes, need to revise some pyhton
#==============================================================================

class zabers:
    
    def __init__(self):
        self.port = setup_com_port()
        self.device1 = Binarydevice(self.port,1)
        self.device2 = Binarydevice(self.port,2)
        self.home_command()
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.originX = 0
        self.originY = 0
    


    def setup_com_port(self):
        
        comPort = serial_ports()        
        self.port = BinarySerial(comPort,9600,20)
     
    
    def abs_command(axis,data):
            
        absCommand = BinaryCommand(1,20,int(data))
        if(axis == 'x'): 
            self.device1.send(absCommand)
        elif(axis == 'y'):
            self.device2.send(absCommand)
        else:
            print("invalid axis")
            
        
        
    def rel_command(axis,data):
        relCommand = BinaryCommand(1,21,int(data))
        if(axis == 'x'): 
            self.device1.send(relCommand)
        elif(axis == 'y'):
            self.device2.send(relCommand)
        else:
            print("invalid axis")

        
    def home_command():
        homeCommand = BinaryCommand(0,1)
        self.device1.send(homeCommand)
        self.device2.send(homeCommand)

    
    def renumber_command():
    
        return    
        
    def set_bound(axis,upper,lower):
        
        if(axis == 'x'):
            self.minX = lower
            self.maxX = upper
        elif(axis == 'y'):
            self.minY = lower
            self.maxY = upper            
        else:
            print("Invalid axis.\n")
 
    def set_origin():
        currentPosCmd = BinaryCommand(1,60)
        self.originX = self.device1.send(currentPosCmd).data
        self.originY = self.device2.send(currentPosCmd).data

        
    def set_2d_abs(xData,yData):
        absCommand1 = BinaryCommand(1,20,int(xData))
        absCommand2 = BinaryCommand(1,20,int(yData))        
        self.device1.send(absCommand1)
        self.device2.send(absCommand2)
        
        return
        
    def set_3d_abs(xData,yData,zData):
        absCommand1 = BinaryCommand(1,20,int(xData))
        absCommand2 = BinaryCommand(1,20,int(yData))        
        absCommand3 = BinaryCommand(1,20,int(zData))
        self.device1.send(absCommand1)
        self.device2.send(absCommand2)
        self.device3.send(absCommand3)
 
    
    
def serial_ports():
""" Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
"""
if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')

result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
        pass
return result
    



# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:30:10 2016

@author: alexa_000
"""
import sys
import serial
import atexit
from zaber.serial import *

class zaber:
    
    def __init__(self,xmin,xmax,ymin,ymax,xstart,ystart):
        self.comPorts = serial_ports()
        self.port = self.setup_com_port()        
        self.device1 = BinaryDevice(self.port,1)
        self.device1.move_vel(40000) #unsure if this is doing anything
        self.device2 = BinaryDevice(self.port,2)
        self.minX = xmin
        self.maxX = xmax
        self.minY = ymin
        self.maxY = ymax
        self.originX = 0
        self.originY = 0
        self.startX = xstart
        self.startY = ystart
        
        self.home_command()
    


    def setup_com_port(self):
           
        if not self.comPorts:
            print("No COM Ports available.\n")
        else:
            serialPort = BinarySerial('COM4',9600,40)
            print("Using COM Port: " + self.comPorts[0] + "\n")
            
            return serialPort
        return
     
    
    def abs_command(self,axis,data):
            
        absCommand = BinaryCommand(1,20,int(data))
        if(axis == 'x'): 
            if(data > self.maxX or data < self.minX):
                print("Data out of bounds on x-axis\n")
            else:
                self.device1.send(absCommand)
        elif(axis == 'y'):
            if(data > self.maxY or data < self.minY):
                print("Data out of bounds on y-axis\n")
            else:
                self.device2.send(absCommand)
        else:
            print("invalid axis")
            
        
        
    def rel_command(self,axis,data):
        relCommand = BinaryCommand(1,21,int(data))
        currentPosCmd = BinaryCommand(1,60)
        currentX = self.device1.send(currentPosCmd).data
        currentY = self.device2.send(currentPosCmd).data
        
        if(axis == 'x'): 
            if(currentX + data > self.maxX or currentX + data < self.minX):
                print("Bounds reached on x-axis\n")
            else:
                self.device1.send(relCommand)
        elif(axis == 'y'):
            if(currentY + data > self.maxY or currentY + data < self.minY):
                print("Bounds reached on y-axis\n")
            else:
                self.device2.send(relCommand)
        else:
            print("invalid axis")

        
    def home_command(self):
        homeCommand = BinaryCommand(0,1)
        self.device1.send(homeCommand)
        self.device2.send(homeCommand)

    
    def renumber_command():
    
        return    
        
    def set_bound(self,axis,upper,lower):
        
        if(axis == 'x'):
            self.minX = lower
            self.maxX = upper
        elif(axis == 'y'):
            self.minY = lower
            self.maxY = upper            
        else:
            print("Invalid axis.\n")
 
    def set_origin(self):
        currentPosCmd = BinaryCommand(1,60)
        self.originX = self.device1.send(currentPosCmd).data
        self.originY = self.device2.send(currentPosCmd).data
        
    def set_to_start(self):
        absCommand1 = BinaryCommand(1,20,int(self.startX))
        absCommand2 = BinaryCommand(1,20,int(self.startY)) 
        
        self.device1.send(absCommand1)
        self.device2.send(absCommand2)

        
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
        return
        
    def debug_info(self):
        currentPosCmd = BinaryCommand(1,60)
        currentX = self.device1.send(currentPosCmd).data
        currentY = self.device2.send(currentPosCmd).data
        
        print(self.comPorts[0])
        print("Current Position:  X: " + str(currentX) + " Y: " + str(currentY) + "\n")
        print("X-Axis Bounds: " + str(self.minX) + " " * 3 + str(self.maxX) +"\n")
        print("Y-Axis Bounds: " + str(self.minY) + " " * 3 + str(self. maxY) + "\n")
        print("Origin:  X: " + str(self.originX) + " " * 3 + "Y: " + str(self.originY) + "\n")
 
    def __exit__(self, exc_type, exc_value, traceback):
        #hopefully should release COM port on task kill, doesnt work too well with ipython though
        self.comPorts[0].close()
    
    
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
    

    
    

    



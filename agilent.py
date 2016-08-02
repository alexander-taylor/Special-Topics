# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:24:45 2016

@author: alexa_000
"""

import visa
import numpy as np

#file for interacting with agilent dso2002a oscilloscope

#==============================================================================
# required features:
#       create a main agilent class object that has most of the following properties.
#     setup and initialization of scope
#     vertical gain and horizontal controls
#     averaging and point set
#     waveform data grab
#     all measurements grab, specifically pk-pk voltage
#     data accquisition channel set etc.
#     Timeout and queueing features for commands
#==============================================================================
    
  
#==============================================================================
# Sets up the agilent oscilloscope with the hardcoded ISN, returns the oscilloscope as a visa
# resource object.  
#==============================================================================
def setup_oscilloscope():
    rm = visa.ResourceManager() #create resource manager
    rm.list_resources() #shows available resources
    oscilloscope = rm.open_resource('USB0::0x0957::0x179B::MY51361628::0::INSTR') #setup scope
    return oscilloscope
  
#==============================================================================
# Captures a waveform from the specified channel. Will return the data in fp format in a numpy
# array. Number of points is set with points_set
#==============================================================================
def waveform_capture(oscilloscope,channel):
    if(channel == 1 or channel == 2):
        oscilloscope.write(":WAVeform:SOURce CHAN"+str(channel))
        data = oscilloscope.query(":WAVeform:DATA?")
        oscilloscope.write(":RUN")
    

        #convert csv data to usable format, strip header
        splitdata = data[10:].split(",")
        floatData = [float(i) for i in splitdata]
        splitDataArray = np.asarray(floatData)
        return splitDataArray
    else:
        print("Invalid Channel Number\n")
        return
        
#==============================================================================
# Gets the peak to peak voltage of the desired channel from the oscilloscope and returns it in NR3
# format.
#==============================================================================
def vpp_get(oscilloscope,channel):
    if(channel == 1 or channel == 2):
        oscilloscope.write(":STOP")
        vpp = oscilloscope.query(":MEASure:VPP? CHANnel"+str(channel))
        oscilloscope.write(":RUN")
        return vpp
    else:
        print("Invalid Channel Number\n")
        return

#==============================================================================
# Sets the oscilloscope to averaging mode and set the number of averages.
#==============================================================================
def averaging_set(oscilloscope,num):
    if(num >= 2 or num < 65536):
        oscilloscope.write(":ACQuire:TYPE AVERage")
        oscilloscope.write(":ACQuire:COUNt "+str(num))
    else:
        print("Invalid averaging count")
    return
        
#==============================================================================
# Sets the voltage per division for the desired channel in either V or mV
#==============================================================================
def vertical_range_set(oscilloscope,vertDiv,channel,suffix):
    
    if(suffix == 'V' or suffix == 'mV'):
        oscilloscope.write(":CHANnel"+str(channel)+":SCALe "+str(vertDiv)+"["+str(suffix)+"]")
    else:
        print("Incorrect voltage units")
    
    return
    
#==============================================================================
# Sets the oscilloscope horizontal range, takes a NR3 float and set this as the time per division
# in seconds.
#==============================================================================
def horizontal_range_set(oscilloscope,horizDiv):
    
    oscilloscope.write(":TIMebase:SCALe "+str(horizDiv))    
    
    return
    

#==============================================================================
# Sets the number of points to be returned by waveform_capture()
#==============================================================================
def points_set(oscilloscope,points):

    oscilloscope.write(":WAVeform:POINts "+str(points))    
        
    return
    
#==============================================================================
# Set the AC/DC coupling for a desired channel on the oscilloscope
#==============================================================================
def channel_coupling_set(oscilloscope,channel,coupling):

    if(channel == 1 or channel ==2):
        if(coupling):
            oscilloscope.write(":CHANnel"+str(coupling)+":COUPling AC")
        else:
            oscilloscope.write(":CHANnel"+str(channel)+":COUPling DC")
    else:
        print("Invalid channel\n")
    return
    
    

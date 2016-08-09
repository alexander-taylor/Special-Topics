# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:04:53 2016

@author: alexa_000
"""


import numpy as np
import matplotlib.pylab as plt
from agilent import *
from dataLogging import *
from zabers import zaber
from time import sleep
from tqdm import tqdm
from tqdm import trange

#==============================================================================
# This file will be the main scan file. It will interact with datalogging, agilent and zabers
# and perhaps any signal processing that is required
#==============================================================================

#==============================================================================
# It needs to be able to do a aribtrary rectangle scan, with either number of pixels.
# I.e 30x30 with step size 1mm.
# or 30mm x 30mm with 40 steps, it then would calculate the nearest encoder value to achieve
# 40 steps per length.
# However we need arbitrary rectangle so if non-square i think we should only allow number of pixels
# with a fixed step size in mm or encoder value rather than take a rectangular area and try and get:
#     a perfect step size to fix in the area.
# in fact i think we will only use number of pixels and user entered step size.

# NEED TO REMEMBER THAT SOME ZABERS HAVE DIFFERENT ENCODER VALUES!!!!!
#==============================================================================

def scan(xWidth, yHeight, stepSize):
    
    xSteps = np.floor(xWidth / stepSize)
    ySteps = np.floor(yHeight / stepSize)
    
    scope = setup_oscilloscope() 
    averaging_set(scope,32)
    channel_coupling_set(scope,1,'AC')
    channel_coupling_set(scope,2,'DC')
    
    print("Scanning %dmm x %dmm, %fmm step size. %d x %d steps\n" % (xWidth,yHeight,stepSize,xSteps,ySteps))
    
    currentScan = scanData()
    currentScan.select_scan_path()
    currentScan.create_subfolders(int(ySteps))
    
    zab = zaber(0,10e6,0,10e6,780000,0)
    zab.set_to_start()
    zab.set_origin()
    
    stepSizeX = 2015 #Encoder value for X-axis zaber for 1mm step
    stepSizeY = 20997 #Encoder value for Y-axis zaber for 1mm step
    stepSizeEncoderX = stepSize * stepSizeX
    stepSizeEncoderY = stepSize * stepSizeY
    

        
    
    #loop over columns first to reduce backlash from zabers, y axis also has smaller microstep
    #size
    for i in tqdm(range(0,int(xSteps))):
        for j in range(0,int(ySteps)):
              
                       
            for k in range(20):
                try:
                    data = waveform_capture(scope,1)
                except:
                    print("timeout retrying attempt: %d\n" % (i))
            
                  
            
            zab.rel_command('y',stepSizeEncoderY)
            #saving after moving as save creates a pseudo delay for backlash
            np.save(currentScan.subPaths[j] + "/%d.npy" % i, data)
            #alter sleep here depending on amount of backlash caused by step size
            #time.sleep(0.5)
        zab.rel_command('x',-1*stepSizeEncoderX)
        zab.abs_command('y',zab.originY)
        time.sleep(2) #sleep longer here because large zaber movement when returning to top
            
    

    
    return
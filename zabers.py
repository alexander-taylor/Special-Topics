# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:30:10 2016

@author: alexa_000
"""

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



# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:15:25 2016

@author: alexa_000
"""

from tkinter import *

from tkinter.filedialog import askopenfilename
filename = askopenfilename()
if(filename == ''):
    print("user cancelled")
else:
    print(filename)
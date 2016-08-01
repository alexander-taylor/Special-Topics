# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:30:34 2016

@author: alexa_000
"""

import tkinter as tk
import tkinter.filedialog
import sys
import os
import time



#==============================================================================
# File for logging experimental data that with primarily consist of spatial scans.
#     -would like to save files in global folder with sub folders, 1 for each line or column of the
#     scan.
#     -would either like to have naming convention which contains appropriate info of the scan or
#     perhaps a standard header for each file.close
#     -maybe a named tuple could be saved for header info and an element could be the actual data.
#==============================================================================

#==============================================================================
# Probably going to avoid using sqlite3 or pickles or any of that nonsense.
# Need to let user select path for saved data scan.
# Need a time stamp, for scan creation
#==============================================================================

#==============================================================================
# Will need to create a scan data class.
# Should store current scan path, current scan folder
#==============================================================================

#==============================================================================
# Want to create a text file in the main scan folder with information about the scan
# need timestamp, scan size, pixels etc, scope settings
#==============================================================================

class scan:
    def __init__(self):
        self.scanPath = ''
        self.subPaths = []

    def select_scan_path(self):
        
        root = tk.Tk()    
        
        path = tk.filedialog.askdirectory()
        
        if(path == ''):
            print("User cancelled path select\n")
        else:
            print("Data Path: " + path +"\n")
            
        root.quit()        
            
        self.scanPath = path
    
    def create_scan_folder(self):
        
        self.scanPath = select_scan_path()
        
        return
        
    def create_subfolders(self,num):
        
        for i in range(1,num+1):

            subpath = self.scanPath + "/" + str(i)           
            print(subpath)
            self.subPaths.append(subpath)
            if not os.path.exists(subpath):           
                os.mkdir(self.scanPath + "/" + str(i))
                
        return
        
    def save_data(path):
        
        
        return
    
    
    
    
    
    
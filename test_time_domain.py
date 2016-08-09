# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 18:54:12 2016

@author: alexa_000
"""

import numpy as np
import scipy as sp
import scipy.fftpack
import scipy.signal
import matplotlib.pylab as plt
import matplotlib.colors as col
from tqdm import tqdm
import matplotlib.animation as animation

fig = plt.figure() # make figure

#path = "C:/Users/alexa_000/Desktop/Scan 2 03-08-16/"
path = r"C:/Users/Alex/Desktop/New folder/"
width = 60
height = 60

grid = np.zeros([width,height])
gridPhase = np.zeros([width,height])
gridAmplitude = np.zeros([width,height])
mainGrid = np.empty([width,height,32000])
mainGrid2 = np.empty([width,height,32000])
imageList = []

t = np.linspace(0,2/40000,6250)
freqs = sp.fftpack.fftfreq(32000, t[1]-t[0])



print("Loading Data\n")
for i in tqdm(range(0,width)):
    for j in range(1,height):
        mainGrid[j][i] = np.load(path + "{0}/{1}.npy" .format(j+1,i))

        fft = sp.fft(mainGrid[j][i])
        gridPhase[j][i] = np.angle(fft[2])
        gridAmplitude[j][i] = np.abs(fft[2])
    

print("Packing images\n")
for k in tqdm(range(0,int(len(mainGrid[0][0])/500))):
        
    for i in range(0,width):
        for j in range(1,height):
            data = mainGrid[j][i][:]

            avg = np.mean(data)
            data -= avg
            
            grid[j][i] = data[k * 500]
        
    imageList.append(grid)
    grid = np.zeros([width,height])
     
     
#phase wrapping for the image.
def mkcmap(): 
    white = '#ffffff'
    black = '#000000'
    red = '#ff0000'
    blue = '#0000ff'
    anglemap = col.LinearSegmentedColormap.from_list(
        'anglemap', [black, red, white, blue, black], N=256, gamma=1)
    return anglemap     
     

     
plt.imshow(gridPhase, cmap = mkcmap())
        
# make axesimage object
# the vmin and vmax here are very important to get the color map correct
#im = plt.imshow(imageList[0], cmap=plt.get_cmap('gray'))
im = plt.imshow(imageList[0], cmap=mkcmap())

# function to update figure
def updatefig(l):
    # set the data in the axesimage object
    im.set_array(imageList[l])
    # return the artists set
    return im,
# kick off the animation
ani = animation.FuncAnimation(fig, updatefig, frames=range(64), 
                              interval=50)
plt.show()

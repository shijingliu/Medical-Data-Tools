'''
Created on Nov 7, 2011
@author: lampejos  
'''

import pickle
import linecache
from matplotlib import *
#from ConfigNumParser import *   

from pylab import *
import numpy as np
import math    
import csv    

def RMS(data,axis=0):   
    return np.sqrt(np.mean(data**2,axis))   

def ReflectDataPad(data, halfwindow):
    leftdata = data[:halfwindow]
    rightdata = data[-halfwindow:]
    output = np.append(leftdata[::-1], data)
    output = np.append(output, rightdata[::-1])     
    return output     
    
def windowedRMS(data, SPS, CPS):   
    halfwindow = int(SPS/CPS)
    paddeddata = ReflectDataPad(data,halfwindow)
    windowlength = 2*halfwindow+1
    output = []  
    for index in range(len(data)):
        output = np.append(output,RMS(paddeddata[index:windowlength+index]))
    print 'length check', len(data),len(output)
    return output    
    
def Derivative(data, SPS, dertype):
    delt = 1.00/SPS
 #   delt = 0.01   
    print delt
    paddata = ReflectDataPad(data, 1)
    
    output = []
    if dertype == 'first':
    
        for index in range(1,len(paddata)-1):
    
            der = (paddata[index+1]-paddata[index-1])/(2*delt)
    
            output = np.append(output, der)
    if dertype == 'second':
        for index in range(1,len(paddata)-1):
            output = np.append(output, (paddata[index+1]-2*paddata[index]+paddata[index-1])/(2*delt))
    
    print 'derivative output', output[10:]
    return output

'just convert from int to float'    
def convert2flt(data):
    tempDATA = []
    for i in data:
        tempDATA.append([float(j) for j in i])
    return np.array(tempDATA)

def FindColumn(text, vector):
    for i in range(len(vector)):
        print vector[i]
        if text == vector[i]:
            break
        elif i == len(vector):
            print 'Error!', text, ' name not found'
            return None
    return i

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.    
     
     This method is based on the convolution of a scaled window with the signal.  
  7     The signal is prepared by introducing reflected copies of the signal 
   8     (with the window size) in both ends so that transient parts are minimized
   9     in the begining and end part of the output signal.
  10     
  11     input:    
  12         x: the input signal          
  13         window_len: the dimension of the smoothing window; should be an odd integer
  14         window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
  15             flat window will produce a moving average smoothing.  
  16 
  17     output:
  18         the smoothed signal               
  19         
  20     example:
  21 
  22     t=linspace(-2,2,0.1)
  23     x=sin(t)+randn(len(t))*0.1   
  24     y=smooth(x)
  25     
  26     see also: 
  27     
  28     numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve    
  29     scipy.signal.lfilter
  30  
  31     TODO: the window parameter could be the window itself if an array instead of a string
  32     NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
  33     """
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."     
 
    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."   
  
    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
 
    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')   
 
    y=np.convolve(w/w.sum(),s,mode='valid')
    del s 
    del w
    del x
    return y[(window_len/2-1):-(window_len/2)]


def FindExtrema(Vector,cps, sps):
#    print 'in FindExtrema'   
#    print Vector.shape     
    size = int(cps*sps)+10
#    print 'extrema length',    
    if size%2==0:
        size = size+1
    testvec = np.zeros(size)
    half=(size-1)/2
    maxvec = [0,0]
    minvec = [0,0]    
    for i in range(half,len(Vector)-half):   
        testvec = Vector[i-half:i+half]
        #print testvec
        if testvec[half] == max(testvec):
            tuple = np.asarray([i,Vector[i]])
            maxvec = np.vstack((maxvec,tuple))
#            print tuple  
        if testvec[half] == min(testvec):
            tuple = np.asarray([i,Vector[i]])
            minvec = np.vstack((minvec,tuple))
#            print minvec
#    print 'maxvec', maxvec      
    return minvec, maxvec

def FindEpoch(vector):
    length= len(vector)
    print 'initial epoch vector length', length
    locpossave = 0
    
    delpos = 0
    
    epoch = [0]
    for i in range(length):
        tuple = vector[i]
        locpos = tuple[0]
        value = tuple[1]
        #print 'position', locpos, 'value', value
        delposnew = locpos-locpossave
        #print 'delta position' , delposnew
        locpossave = locpos
        
        if abs(value) <100000:
            if delposnew > 100:
#            print 'position', round(locpos-delposnew/2,0)   
#            epoch = np.append(epoch, round(locpos-delposnew/2,0))
                epoch = np.append(epoch, locpos)
                #print 'record position'
        
        delpos = delposnew
        
    print 'epoch vector length', len(epoch)  
    return epoch  

  
def PeriodicIntegrate(vector,indexvector, timestep):
    #print vector
    if type(indexvector) == list:
        rows = len(indexvector)
    else:
        (rows,)=indexvector.shape
    intvalues = []
    medianvalues = []
    inttimes = []
    intavgs = []

    for index in range(rows-1):
        place1 = indexvector[index]
        place2 = indexvector[index+1]

        intervaltime = (place2-place1)*timestep

        sumvec = vector[place1:place2]
        
        total = (sumvec.sum())*timestep
        
        median = np.median(sumvec)
        
        intavg=total/intervaltime
        intvalues = np.append(intvalues,total)
        intavgs = np.append(intavgs,intavg)
        inttimes = np.append(inttimes,timestep*(place1+place2)/2)
        medianvalues = np.append(medianvalues, median)
    return inttimes, intvalues, intavgs, medianvalues

def PeriodicSegmentIntegrate(vector,indexvector,segindices, timestep):
    if type(indexvector) == list:
        rows = len(indexvector)
    else:
        (rows,)=indexvector.shape
    intvalues = []
    inttimes = []
    intavgs = []
    for index in range(rows-1):
        place1 = indexvector[index]
        place2 = indexvector[index+1]

        intervaltime = np.sum(segindices[place1:place2])*timestep
        sumvec = vector[place1:place2]
        
        total = (sumvec.sum())*timestep
        
        intavg=total/intervaltime
        intvalues = np.append(intvalues,total)
        intavgs = np.append(intavgs,intavg)
        inttimes = np.append(inttimes,timestep*(place1+place2)/2)
    
    return inttimes, intvalues, intavgs

def SparseFindExtrema(Vector,spc, sps):
#    print 'in FindExtrema'
#    print Vector.shape    
    size = int(spc*sps)+10
#    print 'extrema length', size
    if size%2==0:
        size = size+1
    testvec = np.zeros(size)
    half=(size-1)/2
    maxvec = [0,0]
    minvec = [0,0]    
    for i in range(half,len(Vector)-half):
        testvec = Vector[i-half:i+half]

        if np.all(testvec < 1)==False:
            
            if testvec[half] == max(testvec) and testvec[half+10] != 0 and testvec[half-10] !=0:
                tuple = np.asarray([i,Vector[i]])
                maxvec = np.vstack((maxvec,tuple))
                #print tuple
                #print testvec
            if testvec[half] == min(testvec) and testvec[half+10] != 0 and testvec[half-10] !=0:
                tuple = np.asarray([i,Vector[i]])
                minvec = np.vstack((minvec,tuple))
        print maxvec
    return minvec[1:,:], maxvec[1:,:]
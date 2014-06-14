'''
Created on Nov 7, 2011

@author: lampejos
'''
import pickle
import linecache
from matplotlib import *
from pylab import *
import numpy as np
import math
import csv   

#hacked timer here
import time
#hacked here   

'an optimized file loading function that can improve the data loading speed for hundred of times'
def load (fname):
    'first get data'
    f = open(fname, 'r')
    data = []
    index = 0
    for line in f.readlines():
        if index < 9:
            index = index +1 
        else:
            data.append([float(x) for x in line.split()]) 
    f.close()
    dataNumpy = np.asarray(data)
    
    'now get label'
    labelline = linecache.getline(fname, 5)
    labels=labelline.split('\t')   
    labels[0] = 'time'
    length = len(labels)    
    labels[length-1]=labels[length-1].rstrip()   
    
    return labels, dataNumpy

'old version for loading data'
def LoadADIData(filename):  
    #matfilobject = open(filename,'rb')             
    labelline = linecache.getline(filename, 5)
    #hacked a timer here 
    start = time.time()   
    #hacked here
    data = np.genfromtxt(filename, skip_header = 9, comments = '#*', delimiter = '\t')
    #hacked here 
    print "the time spend is:"    
    print (time.time() - start)
    #hacked here 
    
    labels=labelline.split('\t')   
    
    labels[0] = 'time'
    length = len(labels)    
    labels[length-1]=labels[length-1].rstrip()
    #print labels
    return labels, data #, height, width  

'load data from electrical spectrum'   
def loadESData(filename):
    'first get data'
    f = open(filename, 'r')
    data = []
    index = 0
    for line in f.readlines():
        if index < 15:
            index = index +1 
        else:
            data.append([float(x) for x in line.split()]) 
    f.close()
    dataNumpy = np.asarray(data)   
    return dataNumpy 
    

def LoadNIData(filename):
    labelline = linecache.getline(filename, 1)
    data = np.genfromtxt(filename, delimiter = ',', dtype = float)
    labels=labelline.split(',')
    length = len(labels)
    labels[length-1]=labels[length-1].rstrip()
    return labels, data #, height, width  


    
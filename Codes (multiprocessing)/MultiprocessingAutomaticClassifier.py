'for around 17,000 files multiprocessing automatic classifier is about 2.7 times faster than single processing automatic classifier'

import os.path
from multiprocessing import Pool
import sys
import time
import shutil
import DataFileLoader 
import numpy as np 
from scipy.optimize import leastsq
import os
import csv


'check if there is any peak point in the window'
def CheckPeak(y, window):
    index = 0
    for i in range(len(window)):
        index = index + 1
        if y[window[i]] > 120.0:
            return True
    if index == len(window):
        return False  

def process_file(name):
     NoLightPath = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification1\\no light'
     LightPath365 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification1\\light with 365 nm'
     LightPath450 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification1\\light with 450 nm'
     
     data = DataFileLoader.loadESData(name)    
     x = data[:,0]
     y = data[:,1]
     'now classify files into three categories'
     Window365 = []   
     Window450 = []   
     for i in range(len(x)):
         if (x[i] >=340.0) and (x[i] <= 390.0):
             Window365.append(i)
         if (x[i] >= 435.0) and (x[i] <= 475.0):
             Window450.append(i)   
     if (CheckPeak(y, Window365) == True):
         shutil.move(name, LightPath365)
     elif (CheckPeak(y, Window450) == True):
         shutil.move(name, LightPath450)
     else:
         shutil.move(name, NoLightPath) 

def process_files_parallel(arg, dirname, names):
    ''' Process each file in parallel via Poll.map() '''
    pool=Pool()
    results=pool.map(process_file, [os.path.join(dirname, name) for name in names])


if __name__ == '__main__':
    dir = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\4_8_calibrate1\\'

    start=time.time()
    os.path.walk(dir, process_files_parallel, None)
    print "process_files_parallel()", time.time()-start  
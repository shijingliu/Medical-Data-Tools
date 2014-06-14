'multiprocessing impulse modeling increases the speed for approximately 5.2 times'

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
import re


'discrete integration function'
def DiscreteInteg (light4547, spectrum4547):
    sum = 0
    for i in range (len(spectrum4547)):
        sum = sum + (light4547[i+1]-light4547[i])*spectrum4547[i]
    return sum
        
'returns the location of the maximum number in the list'
def MaximumRecorder (Spectrum):
    record = 0
    MaximumSP = 0
    for i in range (len(Spectrum)):
        if Spectrum[i]>= MaximumSP:
            MaximumSP = Spectrum[i]
            record = i
    return record

'returns the location of the minimum number in the list'  
def MinimumRecorder (Spectrum):
    record = 0
    MinimumSP = 10000
    for i in range (len(Spectrum)):
        if Spectrum[i]<= MinimumSP:
            MinimumSP = Spectrum[i]
            record = i
    return record


def process_file365(name):
    Path = name
    data = DataFileLoader.loadESData(Path)
    lightNM = data[:,0]   
    Spectrum = data[:,1] 
    
    guess_a = 200
    maximumLoc = MaximumRecorder(Spectrum)
    guess_b = lightNM[maximumLoc] 
    guess_c = 100
    
    'find out the half max number'
    maxSpec = np.max(Spectrum)  
    halfmaxArray = [np.abs(x-(maxSpec/2.0)) for x in Spectrum]   
    
    'divide this into two parts' 
    halfmaxBeforeMax = halfmaxArray[0:maximumLoc]
    halfmaxAfterMax = halfmaxArray[(maximumLoc+1):len(halfmaxArray)]
    
    'obtain the minimum from each side'
    location1 = MinimumRecorder(halfmaxBeforeMax)
    location2 = MinimumRecorder(halfmaxAfterMax)
    
    'now calculate the half maximum distance'
    finalDistance = lightNM[maximumLoc+1+location2]-lightNM[location1]
    
    'now we calculate the integration from 450 to 470'
    lightNM450 = lightNM[450:471]
    spectrum450 = Spectrum[450:470]
     
    integral = DiscreteInteg(lightNM450, spectrum450)   
    
    optimize_func = lambda x: 1.0/(x[0]*np.sqrt(lightNM))*(np.e)**(-x[2]*(lightNM-x[1])*(lightNM-x[1])/(x[0]*x[0]))-Spectrum
    result = leastsq(optimize_func, [guess_a, guess_b, guess_c])
    
    est_a, est_b, est_c = result[0]    
    
    'milk 1/A average is obtained by averaging file 44, 45, 46, 47, 48'
    Milk1A = 24901.28253
    
    return [int(re.findall('\d+', name)[6])*0.1, est_a, 1/est_a, est_a*est_a, est_b, est_c, (est_c/(est_a*est_a)), np.max(Spectrum), lightNM[maximumLoc], finalDistance, integral, (1/est_a)/Milk1A]


def process_file450(name):
    Path = name
    data = DataFileLoader.loadESData(Path)
    lightNM = data[:,0]   
    Spectrum = data[:,1] 
    
    guess_a = 200
    maximumLoc = MaximumRecorder(Spectrum)
    guess_b = lightNM[maximumLoc] 
    guess_c = 100
    
    'find out the half max number'
    maxSpec = np.max(Spectrum)  
    halfmaxArray = [np.abs(x-(maxSpec/2.0)) for x in Spectrum]   
    
    'divide this into two parts' 
    halfmaxBeforeMax = halfmaxArray[0:maximumLoc]
    halfmaxAfterMax = halfmaxArray[(maximumLoc+1):len(halfmaxArray)]
    
    'obtain the minimum from each side'
    location1 = MinimumRecorder(halfmaxBeforeMax)
    location2 = MinimumRecorder(halfmaxAfterMax)
    
    'now calculate the half maximum distance'
    finalDistance = lightNM[maximumLoc+1+location2]-lightNM[location1]
    
    'now we calculate the integration from 450 to 470'
    lightNM540 = lightNM[540:561]
    spectrum540 = Spectrum[540:560]
     
    integral = DiscreteInteg(lightNM540, spectrum540)   
    
    optimize_func = lambda x: 1.0/(x[0]*np.sqrt(lightNM))*(np.e)**(-x[2]*(lightNM-x[1])*(lightNM-x[1])/(x[0]*x[0]))-Spectrum
    result = leastsq(optimize_func, [guess_a, guess_b, guess_c])
    
    est_a, est_b, est_c = result[0]    
    
    'milk 1/A average is obtained by averaging file 24, 25, 26, 27, 28'
    Milk1A = 57338.16194 
    
    return [int(re.findall('\d+', name)[6])*0.1, est_a, 1/est_a, est_a*est_a, est_b, est_c, (est_c/(est_a*est_a)), np.max(Spectrum), lightNM[maximumLoc], finalDistance, integral, (1/est_a)/Milk1A]


def process_files_parallel365(arg, dirname, names):
    pool=Pool()
    results=pool.map(process_file365, [os.path.join(dirname, name) for name in names])
    
    'now we record all the results into csv file'
    saveEVFile = open("Impulse Modeling 365nm Data and Different Kind of Caluculations.csv", 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "time", "estimated A", "estimated 1/A", "estimated A^2", "estimated B", "estimated C", "estimated c/a^2", "real max", "real max location", "half max length", "integral", "Factor A"]]) 
    for i in range (len(results)):
        fileWriter.writerows([[i+1, results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], results[i][6], results[i][7], results[i][8], results[i][9], results[i][10], results[i][11]]]) 


def process_files_parallel450(arg, dirname, names):
    pool=Pool()
    results=pool.map(process_file450, [os.path.join(dirname, name) for name in names])
    
    'now we record all the results into csv file'
    saveEVFile = open("Impulse Modeling 450nm Data and Different Kind of Caluculations.csv", 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "time", "estimated A", "estimated 1/A", "estimated A^2", "estimated B", "estimated C", "estimated c/a^2", "real max", "real max location", "half max length", "integral", "Factor A"]]) 
    for i in range (len(results)):
        fileWriter.writerows([[i+1, results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], results[i][6], results[i][7], results[i][8], results[i][9], results[i][10], results[i][11]]]) 


if __name__ == '__main__':
    dir365 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification1\\light with 365 nm\\'
    dir450 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification1\\light with 450 nm\\'

    start=time.time()   
    os.path.walk(dir450, process_files_parallel450, None)
    print "process_files_parallel()", time.time()-start  
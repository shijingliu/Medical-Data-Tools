import DataFileLoader 
import numpy as np 
from scipy.optimize import leastsq
from scipy.integrate import quad
import os
import csv
import re  
import matplotlib.pyplot as plt


'discrete integration function'
def DiscreteInteg (light4547, spectrum4547):
    sum = 0
    for i in range (len(spectrum4547)):
        sum = sum + (light4547[i+1]-light4547[i])*spectrum4547[i]
    return sum

'returns a list of 1/A factor'
'choose file 44, 45, 46, 47, 48 as samples for Milk 365nm 1/A average calculation'
'choose file 24, 25, 26, 27, 28 as samples for Milk 450nm 1/A average calculation'
def readAFactor(filename):
    index = 1
    AfactorArray = []
    IndexArray = []
    TimeArray = []
    with open(filename, 'rb') as csvfile:
        rowreader = csv.reader(csvfile)
        for row in rowreader:
            if index > 1:
                AfactorArray.append(float(row[12]))   
            else:
                index = index + 1
    return AfactorArray

'choose file 44, 45, 46, 47, 48 as samples for Milk 365nm spectrum average calculation'
def AverageMilkSpectrum365():
    path1 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 365 nm\Raw_Time_Integ_Acquire1_00044.txt'
    path2 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 365 nm\Raw_Time_Integ_Acquire1_00045.txt'
    path3 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 365 nm\Raw_Time_Integ_Acquire1_00046.txt'
    path4 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 365 nm\Raw_Time_Integ_Acquire1_00047.txt'
    path5 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 365 nm\Raw_Time_Integ_Acquire1_00048.txt'
    
    PathDir = [path2, path3, path4, path5]
    FirstData = DataFileLoader.loadESData(path1)
    Sum = FirstData[:,1]
    for i in range (len(PathDir)):
        data = DataFileLoader.loadESData(PathDir[i])
        Sum = Sum + data[:,1]   
    return (Sum/5.0) 

'choose file 24, 25, 26, 27, 28 as samples for Milk 450nm spectrum average calculation'
def AverageMilkSpectrum450():
    path1 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 450 nm\Raw_Time_Integ_Acquire1_00024.txt'
    path2 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 450 nm\Raw_Time_Integ_Acquire1_00025.txt'
    path3 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 450 nm\Raw_Time_Integ_Acquire1_00026.txt'
    path4 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 450 nm\Raw_Time_Integ_Acquire1_00027.txt'
    path5 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Milk Spectrum After Classification\light with 450 nm\Raw_Time_Integ_Acquire1_00028.txt'
    
    PathDir = [path2, path3, path4, path5]
    FirstData = DataFileLoader.loadESData(path1)
    Sum = FirstData[:,1]
    for i in range (len(PathDir)):
        data = DataFileLoader.loadESData(PathDir[i])
        Sum = Sum + data[:,1]   
    return (Sum/5.0) 


def FlourescenceExtraction365(csvname, lightDir365):
    AFactor = readAFactor(csvname)
    'add several number to match up the index'
    
    i = 0
    AverageMilkSP = AverageMilkSpectrum365()
    saveEVFile = open("Flourescence Extraction 365nm.csv", 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "time", "integration"]])
    for filename in os.listdir(lightDir365): 
        Path = lightDir365+filename
        data = DataFileLoader.loadESData(Path)
        lightNM = data[:,0]   
        Spectrum = data[:,1]    
        AdjustedSpectrum = Spectrum - (AFactor[i]*AverageMilkSP)
        
        'now we calculate the integration from 450 to 470'
        lightNM450 = lightNM[450:471]
        spectrum450 = AdjustedSpectrum[450:470]
        integral = DiscreteInteg(lightNM450, spectrum450) 
        fileWriter.writerows([[(i+1), int(re.findall('\d+', filename)[1])*0.1, integral]])
        i = i + 1 

def FlourescenceExtraction450(csvname, lightDir450):
    AFactor = readAFactor(csvname)
    'add several number to match up the index'
    
    i = 0
    AverageMilkSP = AverageMilkSpectrum450()
    saveEVFile = open("Flourescence Extraction 450nm.csv", 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "time", "integration"]])
    for filename in os.listdir(lightDir450): 
        Path = lightDir450+filename
        data = DataFileLoader.loadESData(Path)
        lightNM = data[:,0]   
        Spectrum = data[:,1]    
        AdjustedSpectrum = Spectrum - (AFactor[i]*AverageMilkSP)
        
        'now we calculate the integration from 540 to 560'
        lightNM540 = lightNM[540:561]
        spectrum540 = AdjustedSpectrum[540:560]
        integral = DiscreteInteg(lightNM540, spectrum540) 
        fileWriter.writerows([[(i+1), int(re.findall('\d+', filename)[1])*0.1, integral]])   
        i = i + 1 
            
            
if __name__ == '__main__':  
    cvsname365 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Impulse Modeling 365nm Data and Different Kind of Caluculations.csv'
    lightDir365 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification\\light with 365 nm\\'
    cvsname450 = 'C:\Users\shijingliu\Dropbox\Some Software\eclipse-standard-kepler-R-win32-x86_64\eclipse\Impulse Modeling 450nm Data and Different Kind of Caluculations.csv'
    lightDir450 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification\\light with 450 nm\\'
    FlourescenceExtraction450(cvsname450, lightDir450)

    
    
    
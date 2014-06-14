import DataFileLoader 
import os
import shutil
import time
import matplotlib.pyplot as plt

'check if there is any peak point in the window'
def CheckPeak(y, window):
    index = 0
    for i in range(len(window)):
        index = index + 1
        if y[window[i]] > 120.0:
            return True
    if index == len(window):
        return False    

'automatically classify the milk spectrum'
def AutomaticClassifier(dir, NoLightPath, LightPath365, LightPath450):
     
     index = 1 
     for filename in os.listdir(dir):
         finalname = dir + filename
         data = DataFileLoader.loadESData(finalname)    
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
             shutil.move(finalname, LightPath365)
         elif (CheckPeak(y, Window450) == True):
             shutil.move(finalname, LightPath450)  #
         else:
             shutil.move(finalname, NoLightPath) 

if __name__ == '__main__':   
    start=time.time()
    dir = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\4_8_calibrate\\'
    NoLightPath = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification\\no light'
    LightPath365 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification\\light with 365 nm'
    LightPath450 = 'C:\\Users\\shijingliu\\Dropbox\\Some Software\\eclipse-standard-kepler-R-win32-x86_64\\eclipse\\After Classification\\light with 450 nm'
    
    AutomaticClassifier(dir, NoLightPath, LightPath365, LightPath450)
    print "process_files_single_process()", time.time()-start
import numpy as np
from scipy.optimize import leastsq
import DataFileLoader 
import VectorOperations 
import csv
import pylab as plt
import scipy.signal
import cProfile

'record the A, B, D value of AOP Sinusoid Modeling into excel'
'warning: if the window size is more than 2 seconds, then this modeling approach will be very bad'
def AOPSinusoidModeling(filename, WindowSize = 2):
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'    
    file = filename
    finalname = path+file+'.txt'
    LabelVector, DataMatrix = DataFileLoader.load(finalname)    
    AOPcolumn = VectorOperations.FindColumn('AOP',LabelVector)   
    
    if AOPcolumn > 10:
        print "finding new AOP"  
        AOPcolumn = VectorOperations.FindColumn('AOP 1',LabelVector)
        
    AOP = DataMatrix[:,AOPcolumn]   
    
    'declare a file'
    saveEVFile = open ('SinusoidModeling CPR Flow 347.csv', 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "estimated A:", "estimated B", "estimated D"]]) 
    
    for i in range ((len(AOP)/100)-WindowSize):
        'define the start time and end time of each interval'
        StartTime = i; 
        EndTime = StartTime + WindowSize   
    
        AopInterval = AOP[StartTime*100:EndTime*100]
        t = np.linspace(StartTime, EndTime-0.01, WindowSize*100)    
        
        'figure out the appropriate guess using FFT'
        amplitude = np.abs(np.fft.fft(AopInterval))[1:(len(t)/2+1)]
        frequency = np.fft.fftfreq(len(t), 0.01)[1:(len(t)/2+1)]
        
        'find out the maximum amplitude and its corresponding frequency'
        maxFreq, maxAmp = MaximumRecorder(amplitude) 
            
        'now we guess the a, b, c, d for the sinusoid modeling'  
        guess_a = VectorOperations.RMS(scipy.signal.detrend(AopInterval))*np.sqrt(2)   
        guess_b = (3.1415926*2.0)*frequency[maxFreq]
        guess_c = 0.0
        guess_d = np.mean(AopInterval)
        
        'optimize the guess values using least square algorithm'  
        optimize_func=lambda x:x[0]*np.sin(x[1]*t+x[2])+x[3] - AopInterval    
        result = leastsq(optimize_func, [guess_a, guess_b, guess_c, guess_d])   
        
        'we only record the sets when the least square can converge'
        if (result[1]== 1) or (result[1]==2) or (result[1]==3) or (result[1]==4) :
            est_a, est_b, est_c, est_d = result[0]  
            fileWriter.writerows([[i, est_a, est_b, est_d]]) 
    saveEVFile.close()  


'record the A, B, D value of Aorta Sinusoid Modeling into excel'
'warning: if the window size is more than 2 seconds, then this modeling approach will be very bad'    
def AortaSinusoidModeling(filename, WindowSize = 2):
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'    
    file = filename
    finalname = path+file+'.txt'
    LabelVector, DataMatrix = DataFileLoader.load(finalname)    
    AORTScolumn = VectorOperations.FindColumn('Aorta', LabelVector) 
        
    Aorta = DataMatrix[:,AORTScolumn] 
    
    'declare a file'
    saveEVFile = open ('SinusoidModeling CPR Flow 030.csv', 'wb')
    fileWriter = csv.writer(saveEVFile)
    fileWriter.writerows([["index", "estimated A:", "estimated B", "estimated D"]]) 
    
    for i in range ((len(Aorta)/100)-WindowSize):
        'define the start time and end time of each interval'
        StartTime = i; 
        EndTime = StartTime + WindowSize 
    
        AortaInterval = Aorta[StartTime*100:EndTime*100]
        t = np.linspace(StartTime, EndTime-0.01, WindowSize*100)  
        
        'figure out the appropriate guess using FFT'
        amplitude = np.abs(np.fft.fft(AortaInterval))[1:(len(t)/2+1)]
        frequency = np.fft.fftfreq(len(t), 0.01)[1:(len(t)/2+1)]
        
        'find out the maximum amplitude and its corresponding frequency'
        maxFreq, maxAmp = MaximumRecorder(amplitude)  
            
        'now we guess the a, b, and c for the sinusoid modeling'  
        guess_a = VectorOperations.RMS(scipy.signal.detrend(AortaInterval))*np.sqrt(2)   
        guess_b = (3.1415926*2.0)*frequency[maxFreq]
        guess_c = 0.0
        guess_d = np.mean(AortaInterval)
        
        'optimize the guess values using least square algorithm'
        optimize_func=lambda x:x[0]*np.sin(x[1]*t+x[2])+x[3] - AortaInterval
        result = leastsq(optimize_func, [guess_a, guess_b, guess_c, guess_d])     
        
        'we only record the sets when the least square can converge'
        if (result[1]== 1) or (result[1]==2) or (result[1]==3) or (result[1]==4) :
            est_a, est_b, est_c, est_d = result[0]  
            fileWriter.writerows([[i, est_a, est_b, est_d]]) 
    saveEVFile.close()  

'returns the location of the maximum number in the list'
def MaximumRecorder (AmpList):
    record = 0
    MaximumAmp = 0
    for i in range (len(AmpList)):
        if AmpList[i]>= MaximumAmp:
            MaximumAmp = AmpList[i]
            record = i
    return record, MaximumAmp
    
if __name__ == '__main__': 
    #cProfile.run('AortaSinusoidModeling("Zoll CPR Flow 030 20120510", 2)')
    AortaSinusoidModeling('Zoll CPR Flow 030 20120510', 2)  
    
    
    
       
    
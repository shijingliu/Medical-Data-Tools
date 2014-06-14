import DataFileLoader 
import VectorOperations 
import matplotlib.pyplot as plt
import numpy as np   
from numpy.fft import fft, fftfreq


'this function returns the maximum frequency, mean frequency, maximum amplitude, mean amplitude'
def FFTAnalysis(filename, windowSize = 4, timeStep=1):
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'    
    file = filename
    finalname = path+file+'.txt'
    LabelVector, DataMatrix = DataFileLoader.LoadADIData(finalname)   
    EKGcolumn = VectorOperations.FindColumn('EKG',LabelVector) 
    
    time = DataMatrix[:,0]
    EKG = DataMatrix[:, EKGcolumn]   
               
    Fmean = []
    Fmax = []
    Amean = []
    Amax = []
        
    for i in xrange (0, len(time)/100, timeStep):
        intervalStart = i                 
        intervalEnd = i+windowSize
        
        currentTS = time[intervalStart*100:intervalEnd*100]
        currentES = EKG[intervalStart*100:intervalEnd*100]
        
        'first of all get rid of nan value in EKG'
        recordNan = []
        for j in range(len(currentES)):
            if np.isnan(currentES[j]):
                recordNan.append(j)
        
        currentESRefine = currentES[~np.isnan(currentES)]
        currentTSRefine = np.delete(currentTS, recordNan)
    
        'now we can apply the FFT'
        time_step = 0.01 
        freqs = np.fft.fftfreq(len(currentTSRefine), time_step)
         
        halfFreqs = freqs[0:len(freqs)/2]
        
        'then we calculate the amplitude using FFT'
        amplitude = np.abs(np.fft.fft(currentESRefine))**2
        
        amplitudeNorm = amplitude/np.sum(amplitude)  
        
        'only analyze half of the amplitude due to symmetrical problems'
        halfAmplitude = amplitudeNorm[0:len(amplitude)/2]
        
        'now we calculate the Fmean, Fmax, Amean, and Amax'
        Fmean.append(halfFreqs.mean())
        Fmax.append(halfFreqs.max())
        Amean.append(halfAmplitude.mean())
        Amax.append(halfAmplitude.max())

    return Fmax, Fmean, Amax, Amean

'calculate AMSA score using frequency and amplitude'
def AMSAcalculation(filename, windowSize = 4, timeStep = 1):
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'    
    file = filename
    finalname = path+file+'.txt'
    LabelVector, DataMatrix = DataFileLoader.LoadADIData(finalname)   
    EKGcolumn = VectorOperations.FindColumn('EKG',LabelVector) 
    
    time = DataMatrix[:,0]
    EKG = DataMatrix[:, EKGcolumn]               
    
    AMSA = []
        
    for i in xrange (0, len(time)/100, timeStep):
        intervalStart = i
        intervalEnd = i+windowSize
        
        currentTS = time[intervalStart*100:intervalEnd*100]
        currentES = EKG[intervalStart*100:intervalEnd*100]
        
        'first of all get rid of nan value in EKG'
        recordNan = []
        for j in range(len(currentES)):
            if np.isnan(currentES[j]):
                recordNan.append(j)
        
        currentESRefine = currentES[~np.isnan(currentES)]
        currentTSRefine = np.delete(currentTS, recordNan)
    
        'now we can apply the FFT'
        time_step = 0.01 
        freqs = np.fft.fftfreq(len(currentTSRefine), time_step)
         
        halfFreqs = freqs[0:len(freqs)/2]
        
        'then we calculate the amplitude using FFT'
        amplitude = np.abs(np.fft.fft(currentESRefine))**2
        
        amplitudeNorm = amplitude/np.sum(amplitude)
        
        'only analyze half of the amplitude due to symmetrical problems'
        halfAmplitude = amplitudeNorm[0:len(amplitude)/2]
        
        'now we need to get rid of the frequency beyond the range of 4 and 48 '
        amplitudefilter = []
        frequencyfilter = []
        for k in range (len(halfFreqs)):
            if halfFreqs[k]>=4.0 and halfFreqs[k]<=48.0:
                frequencyfilter.append(halfFreqs[k])
                amplitudefilter.append(halfAmplitude[k])
                
        'now calculate the amsa score here'
        AMSA.append(np.sum(np.multiply(amplitudefilter, frequencyfilter)))  
    return AMSA
   

if __name__ == '__main__': 
#    Fmax, Fmean, Amax, Amean = FFTAnalysis('Zoll CPR Flow 047 20120601', 4)                    
     window = 4
     timestep = 1 
     fileName = 'Zoll CPR Flow 347 20131204_CHOP'    
     
     'obtain a list of maximum frequency, mean frequency, maximum amplitude, mean amplitude'
     Fmean, Fmax, Amean, Amax = FFTAnalysis (fileName, window, timestep)
     
     'obtain a list of AMSA score'      
     AMSA_score = AMSAcalculation(fileName, window, timestep)      
     
    
    
   
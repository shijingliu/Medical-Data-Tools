import numpy as np
import VectorOperations
from numpy import linalg as LA
import DataFileLoader
import csv 



def EigenValueAnalysis(filename, windowSize = 1):
 
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'        
    file = filename      
    finalname = path+file+'.txt'
    LabelVector, DataMatrix = DataFileLoader.LoadADIData(finalname)   
    EKGcolumn = VectorOperations.FindColumn('EKG',LabelVector) 
    
    time = DataMatrix[:,0]
    EKG = DataMatrix[:, EKGcolumn]
    
    'first of all get rid of nan value in EKG'    
    recordNan = []
    for j in range(len(EKG)):
        if np.isnan(EKG[j]):
            recordNan.append(j)   
    
    EKGrefined = EKG[~np.isnan(EKG)]
    Timerefined = np.delete(time, recordNan)
    
    'declare a file'
    saveEVFile = open ('EigenVector and EigenValue CPR Flow 347.csv', 'wb')
    fileWriter = csv.writer(saveEVFile)
    
    'now we go through the entire txt data file'
    for i in xrange (0, (len(Timerefined)/100)):
        intervalStart = i                 
        intervalEnd = i+windowSize*windowSize 
        
        currentTS = Timerefined[intervalStart*100:intervalEnd*100]
        currentES = EKGrefined[intervalStart*100:intervalEnd*100]
    
        'matrix construction'   
        MConstruction = np.zeros(shape=(10*windowSize, 10*windowSize))
        for j in range (10*windowSize):
            center = (currentES[j*10*windowSize+5*windowSize]+currentES[j*10*windowSize+5*windowSize-1])/2.0
            for k in range (10*windowSize):
                MConstruction[j][k] = currentTS[j*10*windowSize+k] - center   
        
        'then calculate the eigenvectors'     
        eigenvalues, eigenvectors = np.linalg.eig(MConstruction)
        fileWriter.writerows([[i]])
        fileWriter.writerows([["eigenvalues:"]])
        fileWriter.writerows([eigenvalues])
        fileWriter.writerows([["eigenvectors:"]]) 
        fileWriter.writerows(eigenvectors)
        fileWriter.writerows([""]) 
    saveEVFile.close()

if __name__ == '__main__': 
    EigenValueAnalysis('Zoll CPR Flow 347 20131204_CHOP', 1)
                        
        
        
        
import DataFileLoader 
import VectorOperations 
import matplotlib.pyplot as plt
import numpy as np 

def PowerFactor(filename, time, type):
    path = 'C:\\Users\\shijingliu\\workspace\\PowerFactor\\'    
    file = filename  
    filename = path+file+'.txt'
    
    LabelVector, DataMatrix = DataFileLoader.LoadADIData(filename)   
    AORTScolumn = VectorOperations.FindColumn('Aorta', LabelVector)  
    AOPcolumn = VectorOperations.FindColumn('AOP',LabelVector)
    RAPcolumn = VectorOperations.FindColumn('RAP',LabelVector)
    IVCTScolumn = VectorOperations.FindColumn('IVC', LabelVector)
      
    if AOPcolumn > 10:
        print "finding new AOP"  
        RAPcolumn = VectorOperations.FindColumn('RAP 1',LabelVector)
        AOPcolumn = VectorOperations.FindColumn('AOP 1',LabelVector)   
    
    if type == 'aorta':
        'obtain data from the first t seconds'  
        Aorts = DataMatrix[:,AORTScolumn][0:time*100]
        'process the flow one more time get all absolute values'       
        AbsAorts = np.abs(Aorts)
        Aop = DataMatrix[:,AOPcolumn][0:time*100]
        S = np.multiply(AbsAorts, Aop)
    elif type == 'vena':
        Ivcts = DataMatrix[:,IVCTScolumn][0:time*100]
        AbsIvcts = np.abs(Ivcts)
        Rap = DataMatrix[:,RAPcolumn][0:time*100]  
        S = np.multiply(AbsIvcts, Rap)
    else:
        print "wrong input!"
        return 
    
    'smooth the value with 11 in window and hanning in type'
    sasmooth = VectorOperations.smooth(S, 11, 'hanning')
    
    'obtain the RMS value of t minutes baseline'   
    SValue = VectorOperations.RMS(sasmooth[0:12000], 0)
    
    'obtain the min, max value of each phase'    
    min, max = VectorOperations.FindExtrema(sasmooth, 0.6, 100)  
    
    'now we obtain the RMS value of each phase during t minutes'
    SEachPhase = []
    for i in range (2, len(max)):
        SEachPhase.append(VectorOperations.RMS(sasmooth[max[i-1][0]:max[i][0]], 0))
    
    'obtain the power factor vector'
    PF = [x/(SValue*1.0) for x in SEachPhase]
    
    return PF   


'calculate the graph of the first t seconds'     
if __name__ == '__main__': 
    
     'define the period of time here'
     period = 120.0
      
     y = PowerFactor('Zoll CPR Flow 346 20131205_CHOP', period, 'vena')      
     x = []
     for i in range (len(y)):
         x.append((i*period*1.0)/(len(y)*1.0))  
     plt.plot(x,y)   
     plt.savefig("CPR Flow 346 120 seconds") 
     plt.show()                      
     
 
    
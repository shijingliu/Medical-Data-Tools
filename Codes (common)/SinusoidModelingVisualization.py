import numpy as np
from scipy.optimize import leastsq
import DataFileLoader 
import VectorOperations 
import csv
import scipy.signal
from mayavi import mlab


'rendering the A, B, D value from sinusoidal modeling'  
def AOPSinusoidModelingVisualization(filename):
    path = 'C:\\Users\\shijingliu\\Dropbox\\Reggie\\Results\\Sinusoid Modeling Result (2 seconds window size)\\AOP Modeling Results\\'    
    file = filename
    finalname = path+file+'.csv'

    'declare the x, y, z, s array for point visualization'
    index = 0
    x_array = []
    y_array = []   
    z_array = []
    s_array = []   
    with open(finalname, 'rb') as csvfile:
        rowreader = csv.reader(csvfile)
        for row in rowreader:
            if index <1:
                index = index + 1
            else:
                s = int(row[0])
                x_data = float(row[1])
                y_data = float(row[2])
                z_data = float(row[3])
                if (np.abs(x_data)<=20.0) and (np.abs(y_data)<=20.0) and (np.abs(z_data)<=200.0):
                     s_array.append(s)  
                     x_array.append(x_data)
                     y_array.append(y_data)
                     z_array.append(z_data)
    mlab.axes(mlab.outline(mlab.points3d(x_array, y_array, z_array, s_array, colormap="Reds", scale_factor = 0.001))) 
    


'record the A, B, D value from sinusoidal modeling'      
def AortaSinusoidModelingVisualization(filename):
    path = 'C:\\Users\\shijingliu\\Dropbox\\Reggie\\Results\\Sinusoid Modeling Result (2 seconds window size)\\Aorta Modeling Results\\'    
    file = filename
    finalname = path+file+'.csv'   

    'declare the x, y, z, s array for point visualization'
    index = 0
    x_array = []     
    y_array = []   
    z_array = []
    s_array = []   
    with open(finalname, 'rb') as csvfile:
        rowreader = csv.reader(csvfile)
        for row in rowreader:
            if index <1:
                index = index + 1
            else:
                s = int(row[0])
                x_data = float(row[1])
                y_data = float(row[2])
                z_data = float(row[3])
                if (np.abs(x_data)<=20.0) and (np.abs(y_data)<=20.0) and (np.abs(z_data)<=200.0):
                     s_array.append(s)  
                     x_array.append(x_data)
                     y_array.append(y_data)
                     z_array.append(z_data)
    mlab.axes(mlab.outline(mlab.points3d(x_array, y_array, z_array, s_array, colormap="Reds", scale_mode='none')))  

if __name__ == '__main__':   
    AOPSinusoidModelingVisualization('SinusoidModeling CPR Flow 030')   
    
    
    
    
       
    
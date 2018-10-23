import cv2
import pylab
from scipy import ndimage
import numpy as np
import pandas as pd
import os
import glob

# Specify the directory where images are:
#dir = "D:\\usr\\...\\Images\\"

# Get directory of all 96 images:
from os import getcwd
dir = getcwd()

directory_list = glob.glob(dir + "\\*.tif")

# Create a list with the 96 measurements:
list_cell_count =[]
for i in range(len(directory_list)):
    # i = 0
    im = (cv2.imread(directory_list[i]))*255
    #pylab.figure(0)
    #pylab.imshow(im)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5,5), 0)
    maxValue = 255
    adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C # or cv2.ADAPTIVE_THRESH_MEAN_C
    thresholdType = cv2.THRESH_BINARY#_INV
    # Play with the next two values for optimal counting:
    blockSize = 5 #Size of neigberhood -> must be odd number like 3,5,7,9,11 (The bigger it is, the more restrict it is!)
    C = -5 #Constant to be subtracted to the mean value (The more negative it is, the more restrict it is!)
    im_thresholded = cv2.adaptiveThreshold(im_gray, maxValue, adaptiveMethod, thresholdType, blockSize, C) 
    labelarray, particle_count = ndimage.measurements.label(im_thresholded)
    
    #pylab.figure(1)
    #pylab.imshow(im_thresholded)
    #pylab.show()
    
    #list_particle_count =[]
    list_cell_count.append(particle_count)
    i = i+1
#print(list_cell_count)


# Create a list of lists, each element will be a row of 12 elements (12x8 plate = 96 wells):
list_of_list = [list_cell_count[0:12],
                list_cell_count[12:24],
                list_cell_count[24:36],
                list_cell_count[36:48],
                list_cell_count[48:60],
                list_cell_count[60:72],
                list_cell_count[72:84],
                list_cell_count[84:96]]

# Transform it into a Pandas dataframe and Rename Rows (A-H) and Columns (1-12):
Results = pd.DataFrame(list_of_list,
                       columns=['1', '2', '3', '4', '5','6','7','8','9','10','11','12'])
Results.rename(index={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}, inplace=True)
print(Results)

# Finally export the Result dataframe to a CSV file:
Results.to_csv((str(dir) + "\\SuperGEGEisTheBest.csv"), sep = ',', index = True)
print("\nPlease check the file SuperGEGEisTheBest.csv on the following directory:\n\n" + str(dir) + "\n")
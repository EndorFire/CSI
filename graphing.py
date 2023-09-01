import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
# Importing modules

def main():
    fullMatrix = []

    with open("Python\DrDave\CSI\ZMatrix.txt",'r') as f: #Put file location of Matrix file in relation to current file location
        for row in f: #Loops through each row in the file
            layerVals = row[:-1].strip().split('\t') #This is for data seperated by tabs, if it is comma seperated, change '\t' to ', '
            fullMatrix.append(layerVals) #adds each processed row to a full matrix

    #Creates a grid for the data to be plotted on. This is in pixels, not in microns, but can be changed as need be
    x = np.arange(0, 10*len(fullMatrix), 10)
    y = np.arange(0, 10*len(fullMatrix[0]), 10)
    x, y = np.meshgrid(y, x)

    #sets irrelevant values to 'nan' 
    condensedArray = np.array(fullMatrix)
    condensedArray[condensedArray == '--'] = np.nan
    condensedArray[condensedArray == 'NaN'] = np.nan

    print(x)
    print(y)
    print(len(fullMatrix))
    print(len(fullMatrix[0]))
    #Plots the surface, if you'd like different colours you can change 'coolwarm' to something else in the matplotlib
    fig = plt.figure() 
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(x, y, condensedArray, cmap = "coolwarm")

    plt.show()

if __name__ == "__main__":
    print("hello")
    main()

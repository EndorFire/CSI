import numpy as np
import os 
from math import sqrt
PI = np.pi
XYPOWERS = ((2,2),(2,1),(2,0),(1,2),(1,1),(1,0),(0,2),(0,1),(0,0))
COEFMATRIX = (
    ((4,4),(4,3),(4,2),     (3,4),(3,3),(3,2),      (2,4),(2,3),(2,2)),
    ((4,3),(4,2),(4,1),     (3,3),(3,2),(3,1),      (2,3),(2,2),(2,1)),
    ((4,2),(4,1),(4,0),     (3,2),(3,1),(3,0),      (2,2),(2,1),(2,0)),

    ((3,4),(3,3),(3,2),     (2,4),(2,3),(2,2),      (1,4),(1,3),(1,2)),
    ((3,3),(3,2),(3,1),     (2,3),(2,2),(2,1),      (1,3),(1,2),(1,1)),
    ((3,2),(3,1),(3,0),     (2,2),(2,1),(2,0),      (1,2),(1,1),(1,0)),

    ((2,4),(2,3),(2,2),     (1,4),(1,3),(1,2),      (0,4),(0,3),(0,2)),
    ((2,3),(2,2),(2,1),     (1,3),(1,2),(1,1),      (0,3),(0,2),(0,1)),
    ((2,2),(2,1),(2,0),     (1,2),(1,1),(1,0),      (0,2),(0,1),(0,0))
)


def main(FILEHEADER, subX, subY, minDeg, maxDeg, stepDeg, selection):
    results = []
    with open(f"{FILEHEADER}CurvatureLog.txt", 'w') as q:
        q.write("Xindex_Yindex: degree, error, radius x (cm), radius y (cm)\n")
        for yindex in range(subY):
            findRow = []
            for xindex in range(subX):
                findColumn = []
                with open(os.getcwd() + f"\{FILEHEADER}SubdataFiles\{FILEHEADER}Subdata_{xindex+1}_{yindex+1}.txt",'r') as f:
                    dataArr = createDataArray(f)
                    meanCoord = np.mean(dataArr, axis = 0)
                    for degree in range(minDeg, maxDeg+1, stepDeg):
                        data = rotate(dataArr, degree)
                        center = pointRotate(meanCoord, degree)
                        solved = solveLinear(data)
                        error = findError(solved, data)
                        xCurvature = findCurvatureX(solved, center)
                        yCurvature = findCuvatureY(solved, center)
                        findColumn.append((error, xCurvature, yCurvature, degree))
                        q.write(f"{xindex+1}_{yindex+1}: {degree}, {error:4e}, {xCurvature:4f}, {yCurvature:4f} \n")
                    appendResults(findRow, findColumn, selection)
                    q.write(f"Center of {xindex+1}_{yindex+1} is {meanCoord[0]}, {meanCoord[1]}\n")
                q.write('\n')
            results.append(findRow)
        outputMatricies(results, FILEHEADER, selection)
        print("FINISHED CURVATURE CALCULATIONS")

def createDataArray(f):
    arr = []
    for line in f:
        point = line.strip().split("\t")
        if point[2] != "NaN":
            point[0] = float(point[0]) 
            point[1] = float(point[1]) 
            point[2] = float(point[2]) 
            arr.append(point)
    return arr

def rotate(arr, degree): 
    if(degree == 0):
        return arr
    else: 
        newArr = []
        for point in arr:
            p = [0,0,0]
            x,y = point[0], point[1]
            rad = np.deg2rad(degree)
            p[0] = (x * np.cos(rad)) + (y * np.sin(rad))
            p[1] = (-1 * x * np.sin(rad)) + (y * np.cos(rad))
            p[2] = point[2]
            newArr.append(p)
    return newArr

def pointRotate(point, degree):
    if(degree == 0):
        return point
    else: 
        p = [0,0,0]
        x,y = point[0], point[1]
        rad = np.deg2rad(degree)
        p[0] = (x * np.cos(rad)) + (y * np.sin(rad))
        p[1] = (-1 * x * np.sin(rad)) + (y * np.cos(rad))
        return p

def solveLinear(data):
    dependent = []
    for powerpair in XYPOWERS:
        #inefficient but more readable
        sum = 0
        for point in data:
            x = float(point[0])
            y = float(point[1])
            sum += point[2] * (x**powerpair[0]) * (y ** powerpair[1])
        dependent.append(sum)

    arr = [[0 for i in range(5)] for i in range(5)]
    for point in data:
        for x in range(5):
            for y in range(5):
                arr[x][y] += (point[0] ** x) * (point[1] ** y)

    independent = [[arr[j[0]][j[1]] for j in i] for i in COEFMATRIX]

    return np.linalg.solve(independent,dependent)

def findError(solved, data):
    error = 0
    for point in data: 
        zPredict = 0
        for i in range(9): #This is probably inefficient as hell but hard coding it seems prone to errors
            zPredict += ((point[0] ** XYPOWERS[i][0]) * (point[1] ** XYPOWERS[i][1]) * solved[i])
        error += ((float(point[2]) - zPredict) ** 2)
    return sqrt(error/len(data))

def findCurvatureX(solved, center):
    c = solved
    x = center[0]
    y = center[1]

    secDeriv = (2 * c[0] * (y**2)) + (2 * c[1] * y) + (2 * c[2])
    secDeriv = abs(secDeriv)

    firstDeriv = (2 * c[0] * x * (y**2)) + (2 * c[1] * x * y) + (2 * c[2] * x) + (c[3] * (y**2)) + (c[4] * y) + (c[5]) #save me
    
    denom = (1 + (firstDeriv ** 2)) ** (3/2) 
    k =  secDeriv/denom
    return 1/k

def findCuvatureY(solved, center):
    c = solved
    x = center[0]
    y = center[1]

    secDeriv = (2 * c[0] * (x**2)) + (2 * c[3] * x) + (2 * c[6])
    secDeriv = abs(secDeriv)

    firstDeriv = (2 * c[0] * (x**2) * y)+(c[1] * (x**2))+(2 * c[3] * x * y)+(c[4] * x)+(2 * c[6] * y) + (c[7]) #oh god please no

    denom = (1 + (firstDeriv ** 2)) ** (3/2) 
    k = secDeriv/denom
    return 1/k

def appendResults(findRow, findColumn, selection):
    if(selection == "min"): 
        mins = np.min(findColumn, axis = 0)
        argmins = np.argmin(findColumn, axis = 0)
        a = [[mins[q], findColumn[argmins[q]][3]] for q in range(3)]
        findRow.append(a)
    else:
        selection = int(selection)
        for q in findColumn:
            if q[3] == selection: 
                a = [[q[i], selection] for i in range(3)]
                findRow.append(a)

def outputMatricies(results, FILEHEADER, selection): #[( (Error, deg), (x, deg), (y,deg) ),...]
    if(selection == "min"): 
        fileNameLabel = "Minimum"
    else:
        fileNameLabel = selection + "Degrees"
    errorRes = open(f"{FILEHEADER}{fileNameLabel}Error.txt", 'w')
    xRes = open(f"{FILEHEADER}{fileNameLabel}XCurvature.txt", 'w')
    yRes = open(f"{FILEHEADER}{fileNameLabel}YCurvature.txt", 'w')

    for x in results:
        for y in x:
            errorRes.write(f"{y[0][0]}\t")
            xRes.write(f"{y[1][0]}\t")
            yRes.write(f"{y[2][0]}\t")
        errorRes.write("\n")
        xRes.write("\n")
        yRes.write("\n")

    errorRes.write("\n")
    xRes.write("\n")
    yRes.write("\n")

    for x in results:
        for y in x:
            errorRes.write(f"{y[0][1]}\t")
            xRes.write(f"{y[1][1]}\t")
            yRes.write(f"{y[2][1]}\t")
        errorRes.write("\n")
        xRes.write("\n")
        yRes.write("\n")

    errorRes.close()
    xRes.close()
    yRes.close()

if __name__ == "__main__":
    FILEHEADER = input("File header: ")
    xSize = int(input("xSize: "))
    ySize = int(input("ySize: "))
    minDeg = int(input("Min Degree: "))
    maxDeg = int(input("Max Degree: "))
    stepDeg = int(input("Degree Step: "))

    main(FILEHEADER, xSize, ySize, minDeg, maxDeg, stepDeg)
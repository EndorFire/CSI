import numpy as np
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


def main(subX, subY):
    with open("curvatureLog.txt", 'w') as q:
        q.write("Xindex_Yindex: degree; error; kx; ky\n")
        for xindex in range(subX):
            for yindex in range(subY): 
                with open(f"Python\DrDave\CSI\SubdataFiles\Subdata_3_3.txt",'r') as f:
                        dataArr = createDataArray(f)
                        for degree in range(-10,11):
                            data = rotate(dataArr, degree)
                            center = centerOf(data)
                            solved = solveLinear(data)
                            error = findError(solved, data)
                            xCurvature = findCurvatureX(solved, center)
                            yCurvature = findCuvatureY(solved, center)
                            q.write(f"{xindex+1}_{yindex+1}: {degree}; {error:.3f} ; {xCurvature:.3f} ; {yCurvature:.3f}\n")
                q.write('\n')

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

def centerOf(data): #incredibly inefficient, but I can't really find a better method
    xArr = []
    yArr = []
    for point in data: 
        if(point[0] not in xArr):
            xArr.append(point[0])
        if(point[1] not in yArr): 
            yArr.append(point[1])
    return (xArr[len(xArr)//2], yArr[len(yArr)//2])

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
    print(str(dependent))

    arr = [[0 for i in range(5)] for i in range(5)]
    for point in data:
        for x in range(5):
            for y in range(5):
                arr[x][y] += (point[0]**x) * (point[1] ** y)

    independent = [[arr[j[0]][j[1]] for j in i] for i in COEFMATRIX]

    return np.linalg.solve(independent, dependent)

def findError(solved, data):
    error = 0
    for point in data: 
        zPredict = 0
        for i in range(9): #This is probably inefficient as **** but hard coding it seems prone to errors
            zPredict += ((point[0] ** XYPOWERS[i][0]) * (point[1] ** XYPOWERS[i][1]) * solved[i])
        error += ((float(point[2]) - zPredict) ** 2)
    return error

def findCurvatureX(solved, center):
    c = solved
    x = center[0]
    y = center[1]

    secDeriv = (2 * c[0] * (y**2)) + (2 * c[1] * (y**2)) + (2 * c[2] * (y**2))
    secDeriv = abs(secDeriv)

    firstDeriv = (2 * c[0] * x * (y**2)) + (2 * c[1] * x * y) + (2 * c[2] * x) + (c[3] * (y**2)) + (c[4] * y) + (c[5]) #save me
    
    numer = (secDeriv ** 2)
    denom = (1 + (firstDeriv ** 2)) ** (3/2) 
    return numer/denom

def findCuvatureY(solved, center):
    c = solved
    x = center[0]
    y = center[1]

    secDeriv = (2 * c[0] * (x**2)) + (2 * c[3] * (x**2)) + (2 * c[6] * (x**2))
    secDeriv = abs(secDeriv)

    firstDeriv = (2 * c[0] * (x**2) * y)+(c[1] * (x**2))+(2 * c[3] * x * y)+(c[4] * x)+(2 * c[6] * y) + (c[7]) #oh god please no

    numer = (secDeriv ** 2)
    denom = (1 + (firstDeriv ** 2)) ** (3/2) 
    return numer/denom

def outputMatricies(xCurvature,yCurvature):
    #Has not yet been implemented
    pass

if __name__ == "__main__":
    xSize = int(input("xSize: "))
    ySize = int(input("ySize: "))
    main(xSize, ySize)
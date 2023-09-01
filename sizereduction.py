def main(DATAFILE, FILEHEADER):
    with open(DATAFILE,'r') as f: 
        next(f)
        next(f)
        next(f)
        metaData = f.readline().split(" ")
        X = int(metaData[2])
        Y = int(metaData[3])


    condensedArray = [[[0,0] for j in range(int(Y/10)+1)] for i in range(int(X/10)+1)]

    with open(DATAFILE,'r') as f:
        for i in range(14):
            next(f)
        for point in f: 
            splitPoint = point.split(" ", 2) #[x, y, z] 

            try:
                if((splitPoint[2][:-1] == "No Data")): #checks for end of file, or no data
                    pass 
                
                else:
                    #Places each point into a different 'bucket'
                    xIndex = int(float(splitPoint[0])//10)
                    yIndex = int(float(splitPoint[1])//10)

                    #Adds the values and increments the counter
                    condensedArray[xIndex][yIndex][0] += float(splitPoint[2])
                    condensedArray[xIndex][yIndex][1] += 1 #increment counter
            except(IndexError):
                print("error or eof")
                pass
        

    xValues = []
    yValues = []

    #This only works for averaging by 10, converts pixels to cms
    for x in range(len(condensedArray)):
        xValues.append(100*((x+1)*10 + 5.5)*(8.87437e-6))
    for y in range(len(condensedArray[0])):
        yValues.append(100*((y+1)*10 + 5.5)*8.87437e-6)


    zMatrix = []
    zCol = []

    #Averages each data point
    for x in condensedArray: 
        for y in x: 
            if y[1] != 0: 
                y[0] = y[0]/y[1]
                zCol.append(y[0]/10000) #converts microns to cms
            else:
                zCol.append("NaN")
        zMatrix.append(zCol)
        zCol = []

    #Intermediate file with all the data in case of future error
    with open(FILEHEADER + "interFile.txt",'w') as f: 
        f.write(str(condensedArray))

    #Writes each file
    with open(FILEHEADER + "XValues.txt",'w') as f: 
        for x in xValues: 
            f.write(str(x) + '\n')
    with open(FILEHEADER + "YValues.txt",'w') as f: 
        for y in yValues: 
            f.write(str(y) + '\n')    
    with open(FILEHEADER + "ZMatrix.txt",'w') as f: 
        for z in zMatrix: 
            for z2 in z: 
                f.write(str(z2) + "\t") #Tab delimited
            f.write("\n")

    print("FINISHED SIZE REDUCTION")



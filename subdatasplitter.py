import os

#xSize and ySize decide how big the subsets are, usually 10x10

def main(xSize,ySize):
    buckets = [[[] for j in range(ySize)] for i in range(xSize)]

    #Change file location as necessary 
    with open("ZMatrix.txt",'r') as f:
        rCount = 0
        for l in f: 
            rCount+= 1
        xSliceSize = rCount//xSize+1

    with open("YValues.txt", 'r') as f: 
        yDict = {}
        for (key, y) in enumerate(f):
            yDict[key] = y.strip()
        print(yDict)
            
    #FIX
    with open("ZMatrix.txt",'r') as f:
        with open("XValues.txt", 'r') as q:
            for (rowNum, row) in enumerate(f):
                x = q.readline().strip()
                layerVals = list(enumerate(row.strip().split('\t')))
                ysliceSize = len(layerVals)//ySize+1
                for (num, zValue) in layerVals:
                    point = [x, yDict[num], zValue]
                    buckets[rowNum//xSliceSize][num//ysliceSize].append(point)

    #attempts to create "SubdataFiles" if it already exists, continues
    try: 
        os.mkdir(os.getcwd() + "\SubdataFiles")
        print("gothere")
    except OSError as error: 
        print("already exists")
        pass 

    for xindex, x in list(enumerate(buckets,start = 1)):
        for yindex, bucket in list(enumerate(x,start = 1)): 
            #Change file location as necessary. It will label them as Subdata_x_y.txt
            with open(os.getcwd() + f"\SubdataFiles\Subdata_{xindex}_{yindex}.txt",'w') as f:

                for val in bucket: 
                    for z2 in val: 
                        f.write(str(z2) + "\t") #Tab delimited
                    f.write("\n")
    print("DONE")


if __name__ == "__main__":
    print("hello")
    xSize = input("xSize: ")
    ySize = input("ySize: ") 
    main(xSize, ySize)

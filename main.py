#GUI
import tkinter as tk
#Programs
import sizereduction
import graphing
import subdatasplitter


def execute():
    if(CheckSizeReduce.get()):
        sizereduction.main(int(sizeX.get()),int(sizeY.get()))
    if(CheckGraph.get()):
        graphing.main()
    if(CheckSplitter.get()):
        subdatasplitter.main(int(subX.get()),int(subY.get()))



#############################################################################################################################
top = tk.Tk()


CheckSizeReduce = tk.IntVar()
sizeX = tk.StringVar()
sizeY = tk.StringVar()
CheckGraph = tk.IntVar()
CheckSplitter = tk.IntVar()
subX = tk.StringVar()
subY = tk.StringVar()


WarningLabel = tk.Label(top, text = "Expects the Data.xyz file to be in the current directory, may not run otherwise \n")
SXLabel = tk.Label(top, text = "Size in X")
SX = tk.Entry(top, textvariable = sizeX)
SYLabel = tk.Label(top, text = "Size in Y")
SY = tk.Entry(top, textvariable = sizeY)

CsizeReduce = tk.Checkbutton(top, text = "Size Reduction: Reduces the size of the Data.xyz file by 100x", variable = CheckSizeReduce)
Cgraph = tk.Checkbutton(top, text = "Grapher: Graphs the result of Size Reduction", variable = CheckGraph)
Csplitter = tk.Checkbutton(top, text = "Splitter: Splits the data into chunks of size X by Y", variable = CheckSplitter)
EXLabel = tk.Label(top, text = "X")
EX = tk.Entry(top, textvariable = subX)
EYLabel = tk.Label(top, text = "Y")
EY = tk.Entry(top, textvariable = subY)




runProgram = tk.Button(top, text = "Run specified programs", command = execute)

WarningLabel.pack()
SXLabel.pack()
SX.pack()
SYLabel.pack()
SY.pack()
CsizeReduce.pack()
Cgraph.pack()
Csplitter.pack()
EXLabel.pack()
EX.pack()
EYLabel.pack()
EY.pack()
runProgram.pack()

top.mainloop()


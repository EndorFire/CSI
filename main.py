#GUI
import tkinter as tk
#Programs
import sizereduction
import graphing
import subdatasplitter
import curvature

#############################################################################################################################
class LabeledText:
    def __init__(self, label) -> None:
        self.value = tk.StringVar()
        self.label = tk.Label(root, text = label)
        self.data = tk.Entry(root, textvariable = self.value)

class Checkbox:
    def __init__(self, name, description) -> None:
        self.value = tk.IntVar()
        self.check = tk.Checkbutton(root, text = name, variable = self.value)
        self.desc = tk.Label(root, text = description)

#############################################################################################################################
def execute():
    DATAFILE = dataFilename.value.get()
    FILEHEADER = resultFilename.value.get()

    if(sizeReductionCheck.value.get()):
        sizereduction.main(DATAFILE,FILEHEADER)
    if(graphingCheck.value.get()):
        graphing.main(FILEHEADER)
    if(splitingCheck.value.get()):
        subdatasplitter.main(FILEHEADER, int(subX.value.get()), int(subY.value.get()))
    if(curvatureCheck.value.get()):
        curvature.main(FILEHEADER, int(subX.value.get()), int(subY.value.get()), int(minDeg.value.get()), int(maxDeg.value.get()), int(stepDeg.value.get()), matrixSelect.value.get())

#############################################################################################################################
root = tk.Tk()
root.title("Coherence Scanning Interferometry")


#Text input fields
textSubX = tk.StringVar()
textSubY = tk.StringVar()


currRow = 0
dataFilename = LabeledText("Data Filename:")
resultFilename = LabeledText("Resulting Filename Headers:")
labeledTextArray = [dataFilename, resultFilename]

for item in labeledTextArray:
    item.label.grid(row = currRow, column = 1)
    item.data.grid(row = currRow, column = 2, sticky = "W")
    currRow += 1

tk.Label(root).grid(row = currRow)
currRow += 1

sizeReductionCheck = Checkbox("Size Reduction", "Reduces the size of the datafile by a factor of 100 (10x10)")
graphingCheck = Checkbox("Graphing", "Opens a graph in matplotlib using the results of Size Reduction")
checkboxArray = [sizeReductionCheck, graphingCheck]

for item in checkboxArray:
    item.check.grid(row = currRow, column = 0, sticky = "W")
    item.desc.grid(row = currRow, column = 1, columnspan = 2, sticky = "W")
    currRow += 1

subX = LabeledText("SubX: ")
subY = LabeledText("SubY: ")

for item in (subX,subY):
    item.label.grid(row = currRow, column = 0, sticky = "E")
    item.data.grid(row = currRow, column = 1, sticky = "W")
    currRow += 1

splitingCheck = Checkbox("Splitter", "Splits the data into subsets. \nExample: X = 4, and Y = 5, would split into 20 subfiles")
splitingCheck.check.grid(row = currRow, column = 0, sticky = "W")
splitingCheck.desc.grid(row = currRow, column = 1, columnspan = 2, sticky = "W")
currRow += 1


minDeg = LabeledText("Minimum Degree: ")
maxDeg = LabeledText("Maximum Degree: ")
stepDeg = LabeledText("Degree Step: ")
matrixSelect = LabeledText("Configure Matrix Output:\n'min' for minimum\nnumber for specific degree")

for item in (minDeg, maxDeg, stepDeg, matrixSelect):
    item.label.grid(row = currRow, column = 0, sticky = "E")
    item.data.grid(row = currRow, column = 1, sticky = "W")
    currRow += 1
curvatureCheck = Checkbox("Curvature", "Calculates the curvature of subdata using the result of splitter.")
curvatureCheck.check.grid(row = currRow, column = 0, sticky = "W")
curvatureCheck.desc.grid(row = currRow, column = 1, columnspan = 2, sticky = "W")
currRow += 1



executeButton = tk.Button(root, command = execute, text = "Run Selected Programs")
executeButton.grid(row = currRow, column = 0, columnspan = 3)
currRow += 1

tk.Label(root, text = "Warning: Running the programs may cause this window to stop responding.\nThis is normal, please do not close this window. ").grid(row = currRow, column = 0, columnspan = 3)

root.mainloop()



import os, sys, re, string

myinput = sys.argv [ 1 ]

filename = os.path.basename(myinput) # Remove the file path from the file name

# Add a "_mod" to the end of the Excel file name
noxlsFilename=filename.strip(".xls")
outputFilename =  noxlsFilename + "_mod.xls"

# Attach the file path to the file name again
myoutput = os.path.dirname(myinput)+"/"+outputFilename

inputFile = open(myinput, "r")
outputFile = open(myoutput,"w")


myList = inputFile.readlines()

# The removal of the scientific numbers
for myLine in myList:
	spLine = myLine.split("\t")
	if "e-" in spLine[1].strip():
		num = spLine[1].strip()
		Dec = str(int(num[num.index("e-")+2:])+3)
		num = float(spLine[1].strip())
		outputFile.write(spLine[0]+"\t"+format(num, '.'+Dec+'f')+"\n")

	else:
		outputFile.write(spLine[0]+"\t"+spLine[1])
		

inputFile.close()
outputFile.close()

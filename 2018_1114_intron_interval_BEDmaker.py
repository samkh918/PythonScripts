import os, sys, re, string
import datetime, subprocess

inputFile = sys.argv [ 1 ]
myInput = open(inputFile,'r')
myList = myInput.readlines()

for k in range(len(myList)-1):
	splineK=myList[k].split()
	splineKplus1=myList[k+1].split()

	print splineK[0],"	",splineK[2],"	",splineKplus1[1]

	#print (myList[k])

myInput.close()

import os, sys, re, string
import datetime, subprocess
import operator

inputFile = sys.argv [ 1 ]

myInput = open(inputFile,'r')
myList = myInput.readlines()

#CALLERS_list=[] #Holds all different variant types
CALLERS_list={} #Holds all different variant types



#################################################################################################
# Following code gets a list (VT_list) of all variant types found in the provided VCF file at the command line
for myLine in myList:
	if '#' in myLine:
		continue
	else:
		spline=myLine.split("\t")

		# Break up the information column
		InforColumn=spline[7].split(";")
		for el in InforColumn:
			if "CALLERS" in el:
				caller=el.strip("CALLERS=")
				if caller in CALLERS_list:
					CALLERS_list[caller]+=1
				else:
					CALLERS_list[caller]=1
				
				#print caller
				#VT=el[el.index("=")+1:]
				#print "VT is: ",VT
				#if caller not in CALLERS_list:
					#CALLERS_list.append(caller)

#print CALLERS_list
print "dict_length: ", len(CALLERS_list)

#for callers in CALLERS_list:
#	if CALLERS_list[callers] == 20:
#		print callers
#		print CALLERS_list[callers]

for callers in CALLERS_list:
	print CALLERS_list[callers],"\t",callers 



#sorted_CALLERS_list = sorted(CALLERS_list.items(), key=operator.itemgetter(1))
#for j in VT_list:
#	print j


#################################################################################################


myInput.close()

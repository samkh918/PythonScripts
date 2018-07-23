from __future__ import division
import os, sys, re, string
import datetime, subprocess


'''
This script parses the final VCF files of a pipeline and shows how many of each filtering parameters are found
in the FILTER field. There are two parts:

The first part counts the number of each different Jacek annotations found in the FILTER column. 
The problem with this count is that once the first filter type
has been detected, which are listed in:
/hpf/largeprojects/ccmbio/samkh/jaceq_sam/pipelines/forge/scripts/filter_combined_variants.pl
and does not show the rest of the filters that could have been applied.

Because of this the second segment was written so that, we explicitly count the filters that could be set for each
variant line.
'''


# The input VCF file is provided at the command line argument
inputFile = sys.argv [ 1 ]


myInput = open(inputFile,'r')

myList = myInput.readlines()

output=open("VT.txt",'w')


counter1,counter2,counter3,counter4,counter5, counter6, counter7, counter8, counter9, counter10, counter11, counter12, counter13, counter14=0,0,0,0,0,0,0,0,0,0,0,0,0,0

for myLine in myList:
	if '#' in myLine:
		continue
	elif "Qual<" in myLine:
		counter1+=1

	elif "Read_depth<" in myLine:
		counter2+=1

	elif "Alt_count<" in myLine:
		counter3+=1

	elif "MapQ<" in myLine:
		counter4+=1

	elif "num_prev_seen_samples>" in myLine:
		counter5+=1

	elif "MAF>" in myLine:
		counter6+=1

	elif "Extended_splicing_variant" in myLine:
		counter7+=1

	elif "Alt_read_ratio<0.2" in myLine:
		counter8+=1

	elif "Alt_read_ratio<0.15" in myLine:
		counter9+=1

	elif "random_or_unassembled_chromosome" in myLine:
		counter10+=1

	elif "Variant_type_excluded" in myLine:
		counter11+=1
		spline=myLine.split("\t")
		InforColumn=spline[7].split(";")
		for el in InforColumn:
		    if "=" in el and "VT" == el[0:el.index("=")]: 
			VT=el[el.index("=")+1:]
			output.write(VT+"\n")
			
	
	elif "Probable_SSE" in myLine:
		counter12+=1
		
	elif "SNP_failed_GATKHardSNP_filter" in myLine:
		counter13+=1

	elif "Indel_failed_GATKHardIndel_filter" in myLine:
		counter14+=1

print "Qual filter: ", counter1
print "Read depth filter: ", counter2
print "Alt count filter: ", counter3
print "MapQ filter: ", counter4
print "num prev seen samples filter: ", counter5
print "MAF filter: ", counter6
print "Extended splicing variant filter: ", counter7
print "Alt read ratio < minSNVReadRatio(0.2) filter: ", counter8
print "Alt read ratio < minIndelReadRatio(0.15) filter: ", counter9
print "randome or unassembled chromosome filter: ", counter10
print "Variant type excluded filter: ", counter11
print "Probable SSE filter: ", counter12
print "SNP_failed_GATKHardSNP_filter: ", counter13
print "Indel_failed_GATKHardIndel_filter: ", counter14

print "----------------------------------------------------"


Qual_counter=0
ReadDepth_counter=0
AltCount_counter=0
MapQ_counter=0
numPrevSeen_counter=0
MAF_counter=0
ExtSplVar_counter=0
ReadRatioSNV_counter=0
ReadRatioIndel_counter=0
RndChr_counter=0
VarType_counter=0
ProbSSE_counter=0
GATKHardSNP_filter_counter=0
GATKHardIndel_filter_counter=0
RanUnChr_counter=0
GL_Chr_counter=0


for myLine in myList:
	# variables to hold 1000 genome and EVS frequency of each variant and then compare to MAFThreshold
	thgMAF=0
	evsMAF=0

	if '#' in myLine:
		continue
	else:
		spline=myLine.split("\t")

		# Break up the information column
		InforColumn=spline[7].split(";")
		RDC, AlTC, MQ, PSN, MQRankSum, ReadPosRankSum, QD, FS=0.0,0.0,0,0,0,0,0,0
		thgMAF, evsMAF, VT="","",""
		evsMAF=""	
		VT="" 

		# Breakup the INFO column
		for el in InforColumn:
			#Note: an alternative for finding the following fields is (if el.split("=",1)[0]=="RDC")
			if "=" in el and "RDC" == el[0:el.index("=")]: RDC=int(el[el.index("=")+1:])
			if "=" in el and "ALTC" == el[0:el.index("=")]: ALTC=int(el[el.index("=")+1:])
			if "=" in el and "MQ" == el[0:el.index("=")]: MQ=float(el[el.index("=")+1:]) #Check if MQ is the right term to use
			if "=" in el and "PSN" == el[0:el.index("=")]: PSN=int(el[el.index("=")+1:])
			if "=" in el and "THGMAF" == el[0:el.index("=")]: thgMAF=el[el.index("=")+1:]
			if "=" in el and "EVSMAF" == el[0:el.index("=")]: evsMAF=el[el.index("=")+1:]

			# Double check the "Strict" condition on this in the Perl script		
			if "=" in el and "VT" == el[0:el.index("=")]: VT=el[el.index("=")+1:] 
			if "=" in el and "VT" == el[0:el.index("=")]: variantType = el[el.index("=")+1:]
			if "=" in el and "MQRankSum" == el[0:el.index("=")]: MQRankSum=float(el[el.index("=")+1:])
			if "=" in el and "ReadPosRankSum" == el[0:el.index("=")]: ReadPosRankSum=float(el[el.index("=")+1:])
			if "=" in el and "QD" == el[0:el.index("=")]: QD=float(el[el.index("=")+1:])
			if "=" in el and "FS" == el[0:el.index("=")]: FS=float(el[el.index("=")+1:])


		if float(spline[5]) < 50: Qual_counter+=1
		if RDC < 3: ReadDepth_counter+=1
		if ALTC < 2: AltCount_counter+=1
		if MQ < 20.0: MapQ_counter+=1
		if PSN > 15: numPrevSeen_counter+=1
		if thgMAF!=".": thgMAF=float(thgMAF)
		if evsMAF!=".": evsMAF=float(evsMAF)
		if ((thgMAF !='.' and thgMAF > 0.05) or (evsMAF !='.' and evsMAF > 0.05)): MAF_counter+=1
		if "extended" in el: ExtSplVar_counter+=1
		if variantType not in ["nonsynonymous SNV","splicing","splicing-extended","stopgain SNV","stoploss SNV","frameshift deletion","frameshift insertion","nonframeshift deletion","nonframeshift insertion"]: VarType_counter+=1
		if ((len(spline[3]) == len(spline[4])) and RDC!=0 and ALTC/RDC < 0.2): ReadRatioSNV_counter+=1
		if ((len(spline[3]) != len(spline[4])) and RDC!=0 and ALTC/RDC < 0.15): ReadRatioIndel_counter+=1; #print myLine,ALTC/RDC,"ALTC: ",ALTC, "RDC: ",RDC,"\n\n"
		if ((len(spline[3]) == len(spline[4])) and (MQ < 30 or MQRankSum < -12.5 or ReadPosRankSum < -8.0 or QD < 2.0 or FS > 60.0)): GATKHardSNP_filter_counter+=1
		if ((len(spline[3]) != len(spline[4])) and ReadPosRankSum < -20.0 or QD < 2.0 or FS > 200.0): GATKHardIndel_filter_counter+=1
		if "random" in spline[0] or "Un" in spline[0]: RanUnChr_counter+=1
		if "GL" in spline[0]: GL_Chr_counter+=1

print "# QUAL < 50: ",Qual_counter
print "# Read depth < 3: ",ReadDepth_counter
print "# Alt count < 2: ",AltCount_counter
print "# MQ < 20: ",MapQ_counter
print "# PSN > 15: ",numPrevSeen_counter
print "# MAF > 0.05: ",MAF_counter
print "# with 'extended splicing variant' in VT (with variantTypeStrict): ",ExtSplVar_counter
print "# variants other than VarType: ",VarType_counter
print "# SNV read ratio < 0.2: ",ReadRatioSNV_counter
print "# Indel read ratio < 0.15: ",ReadRatioIndel_counter
print "# GATKHardIndel_filter: ",GATKHardIndel_filter_counter
print "# GATKHardSNP_filter: ",GATKHardSNP_filter_counter
print "# random/Un chromosomes: ",RanUnChr_counter
print "# chrGL000NN: " , GL_Chr_counter

myInput.close()
output.close()

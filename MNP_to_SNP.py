

from __future__ import division
import os, sys, re, string
import datetime, subprocess, gzip

# This script looks at the variants in the VCF file and if there is a line with MNPs and immediately before and after this line are the corresponding SNPs, then the MNP line will be removed from the output VCF file.
# It also stores the deleted variants in a "Deleted_MNPs" file for reference.


VCFfile_input = sys.argv [ 1 ]
VCFfile_output = sys.argv [ 2 ]
Deleted_MNPs = sys.argv [ 3 ]

VCFinput = open(VCFfile_input,'r')
myList = VCFinput.readlines()

VCFoutput = open(VCFfile_output, 'w')
DeletedMNPsOutput = open(Deleted_MNPs, 'w')


k=0
while k<len(myList)-1:
	if myList[k].startswith("#"):
		VCFoutput.write(myList[k])
	else:
		kmin1_spline = myList[k-1].split()
		k_spline = myList[k].split()
		kplus1_spline = myList[k+1].split()

		if (k_spline[0] == kmin1_spline[0] and k_spline[1] == kmin1_spline[1]) and (k_spline[0] == kplus1_spline[0] and int(kplus1_spline[1]) == int(k_spline[1])+1) and (len(k_spline[3]) == 2 and len(k_spline[4]) == 2):
			DeletedMNPsOutput.write("prev:\t"+kmin1_spline[0]+"\t"+kmin1_spline[1]+"\t"+kmin1_spline[2]+"\t"+kmin1_spline[3]+"\t"+kmin1_spline[4]+"\n")
			DeletedMNPsOutput.write("current:\t "+k_spline[0]+"\t"+k_spline[1]+"\t"+k_spline[2]+"\t"+k_spline[3]+"\t"+k_spline[4]+"\n")
			DeletedMNPsOutput.write("next:\t"+kplus1_spline[0]+"\t"+kplus1_spline[1]+"\t"+kplus1_spline[2]+"\t"+kplus1_spline[3]+"\t"+kplus1_spline[4]+"\n\n")
		else:
			VCFoutput.write(myList[k])
			

	k+=1

VCFoutput.write(myList[k]) ## write the last input VCF line to the output VCF file

VCFinput.close()
VCFoutput.close()
DeletedMNPsOutput.close()


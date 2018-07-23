import os, sys, re, string
import datetime, subprocess

inputFile = sys.argv [ 1 ]

myInput = open(inputFile,'r')

myList = myInput.readlines()

VT_list=[] #Holds all different variant types


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
			if "=" in el and "VT" == el[0:el.index("=")]:
				VT=el[el.index("=")+1:]
				#print "VT is: ",VT
				if VT not in VT_list:
					VT_list.append(VT)

for j in VT_list:
	print j

print "---------------------------\n"

#################################################################################################

# Following code gets a list of all variant types and counts how many of each are found in the provided VCF file

intergenic_cnt=0
ncRNA_exonic_cnt=0
ncRNA_intronic_cnt=0
upstream_cnt=0
intronic_cnt=0
nonsynonymous_SNV_cnt=0
UTR3_cnt=0
synonymous_SNV_cnt=0
splicing_extended_cnt=0
UTR5_cnt=0
downstream_cnt=0
upstream_downstream_cnt=0
nonframeshift_insertion_cnt=0
stoploss_cnt=0
frameshift_deletion_cnt=0
splicing_cnt=0
unknown_cnt=0
ncRNA_splicing_cnt=0
stopgain_cnt=0
nonframeshift_deletion_cnt=0
frameshift_insertion_cnt=0
UTR5_UTR3_cnt=0

for myLine in myList:
        if '#' in myLine:
                continue
        else:
                spline=myLine.split("\t")


                # Break up the information column
                InforColumn=spline[7].split(";")
                for el in InforColumn:
                        if "=" in el and "VT" == el[0:el.index("=")]:
                                VT=el[el.index("=")+1:]
				if VT == "intergenic": intergenic_cnt+=1
				if VT == "ncRNA_exonic": ncRNA_exonic_cnt+=1
				if VT == "ncRNA_intronic": ncRNA_intronic_cnt+=1
				if VT == "upstream": upstream_cnt+=1
				if VT == "intronic": intronic_cnt+=1
				if VT == "nonsynonymous SNV": nonsynonymous_SNV_cnt+=1
				if VT == "UTR3": UTR3_cnt+=1
				if VT == "synonymous SNV": synonymous_SNV_cnt+=1
				if VT == "splicing-extended": splicing_extended_cnt+=1
				if VT == "UTR5": UTR5_cnt+=1
				if VT == "downstream": downstream_cnt+=1
				if VT == "upstream-downstream": upstream_downstream_cnt+=1
				if VT == "nonframeshift insertion": nonframeshift_insertion_cnt+=1
				if VT == "stoploss": stoploss_cnt+=1
				if VT == "frameshift deletion": frameshift_deletion_cnt+=1
				if VT == "splicing": splicing_cnt+=1
				if VT == "unknown": unknown_cnt+=1
				if VT == "ncRNA_splicing": ncRNA_splicing_cnt+=1
				if VT == "stopgain": stopgain_cnt+=1
				if VT == "nonframeshift deletion": nonframeshift_deletion_cnt+=1
				if VT == "frameshift insertion": frameshift_insertion_cnt+=1
				if VT == "UTR5-UTR3": UTR5_UTR3_cnt+=1


print "splicing: ", splicing_cnt
print "splicing-extended: ", splicing_extended_cnt
print "nonframeshift insertion: ", nonframeshift_insertion_cnt
print "nonframeshift deletion: ", nonframeshift_deletion_cnt
print "frameshift insertion: ", frameshift_insertion_cnt
print "frameshift deletion: ", frameshift_deletion_cnt
print "stoploss: ", stoploss_cnt
print "stopgain: ", stopgain_cnt
print "nonsynonymous SNV: ", nonsynonymous_SNV_cnt
print "synonymous SNV: ", synonymous_SNV_cnt
print "UTR5: ", UTR5_cnt
print "UTR3: ", UTR3_cnt
print "UTR5-UTR3: ", UTR5_UTR3_cnt
print "upstream-downstream: ", upstream_downstream_cnt
print "upstream: ", upstream_cnt
print "downstream: ", downstream_cnt
print "intronic: ", intronic_cnt
print "intergenic: ", intergenic_cnt
print "ncRNA_exonic: ", ncRNA_exonic_cnt
print "ncRNA_intronic: ", ncRNA_intronic_cnt
print "ncRNA_splicing: ", ncRNA_splicing_cnt
print "unknown: ", unknown_cnt




'''
# Double check the "Strict" condition on this in the Perl script		
if "=" in el and "VT" == el[0:el.index("=")] and "extended" in el:
	ExtSplVar_counter+=1

if "=" in el and "VT" == el[0:el.index("=")]:
	variantType = el[el.index("=")+1:]
	if variantType not in ["nonsynonymous SNV","splicing","splicing-extended","stopgain SNV","stoploss SNV","frameshift deletion","frameshift insertion","nonframeshift deletion","nonframeshift insertion"]:
		VarType_counter+=1
'''


myInput.close()

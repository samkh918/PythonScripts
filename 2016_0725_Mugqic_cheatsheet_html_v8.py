import os, sys, re, string
import datetime, subprocess

from subprocess import call

# By: Sam Khalouei
# Created on: August 9th, 2016
# Last updated: August 10th, 2017

# Purpose: To create a 'cheat sheet' of the files and methods in latest hpf pipeline
# Input: the latest_hpf directory full path
# Output: a HTML file showing the python files, and class and method definitions inside them
# How to run: change the "GenAP_Folder" variable below to the appropriate mugqic_pipelines folder
#             type "python this_python_file" with no arguments
#	      An HTML file will be generated in the same folder

# ToDo list:

'''
* Add which screen generated the output
* for multiline methods their usage appears on second line
'''
today=str(datetime.date.today())[:4]+"_"+str(datetime.date.today())[5:].replace("-","")

#GenAP_Folder = "/hpf/tools/centos6/mugqic-pipelines/latest_hpf"
#GenAP_Folder = "/hpf/largeprojects/ccmbio/kng/mcgill_jacek/mugqic-2.2.0"
#GenAP_Folder = "/hpf/largeprojects/ccmbio/samkh/GenAPmod_Aug16th2016/mugqic_pipelines"
GenAP_Folder = "/hpf/largeprojects/ccmbio/samkh/GenAP3.0.0/mugqic_pipelines"
###GenAP_Folder = "/hpf/tools/centos6/mugqic-pipelines/2.1.0" #This one takes forever to run since there are so many files
#GenAP_Folder = "/hpf/tools/centos6/mugqic-pipelines/2.2.0"

# Obtain the GenAP version number
versionInput = open (GenAP_Folder+"/VERSION")
myList=versionInput.readlines()
version=myList[0].strip()

# Create the output html file
output=open(today+"_GenAP_"+version+"_Cheat_Sheet.html","w")

output.write("<html>")
output.write("<h1 align=center><b>GenAP Cheat Sheet</b></h1>")

# Write the time to html file
output.write("<b>Date: </b>"+today+"<br>")

# Write the GenAP version to the html file
output.write("<b>Pipeline Version: </b>"+version+"<br>")

# Write the GenAPP folder
output.write("<b>GenAP folder: </b>"+GenAP_Folder+"<br>")


output.write("__"*80)


def class_method_reader(inputfile,inputfolder):
	DefEndReached=True
	myInput = open(inputfile,'r')
	myList = myInput.readlines()
	fileName=os.path.basename(inputfile)
	output.write("<br><b><font color='blue' size='5'><a name='"+fileName+"'>"+ fileName + "</a></font></b><br>")

	for myLine in myList:
		# End of definition has not been reached yet
		if DefEndReached==False:
			output.write("&nbsp&nbsp&nbsp&nbsp"+myLine+"<br>")
			if ")" in myLine:
				DefEndReached=True
		myspline=myLine.split()
		if len(myspline)==0:
			continue
		if myspline[0]=='class' and '#' not in myspline[0]:
			output.write("<font color='red'>"+myLine+"</font><br>")

			# Obtain the class name so that it can be attached to the method_name below
			if "(" in myLine:
				class_name = myLine[6:myLine.index("(")]
			else:
				class_name = myLine[6:myLine.index(":")]


		if myspline[0]=='def' and '#' not in myspline[0]:
			if myLine[0:4]=="    ": # this is a class method
				output.write("&nbsp&nbsp&nbsp&nbspdef <b>"+myLine[8:myLine.index("(")+1]+"</b>"+myLine[myLine.index("(")+1:]+"<br>")

				method_name=myLine[8:myLine.index("(")]
				if inputfolder=="bfx" and DefEndReached==True:

					proc = subprocess.Popen(['grep -rn "'+class_name+'\.'+method_name+'" '+GenAP_Folder], shell=True, stdout=subprocess.PIPE)
					c = proc.stdout.readlines()

					for mel in c:
						ckl=mel.split("\t")
						output.write("<font color='DarkOrange' size='2'> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b> <--- </b> &nbsp"+ckl[0]+"</font><br>")


			else:
				output.write("def <b>"+myLine[4:myLine.index("(")+1]+"</b>"+myLine[myLine.index("(")+1:]+"<br>")

				method_name=myLine[4:myLine.index("(")]
				if inputfolder=="bfx" and DefEndReached==True:
					inpfile= os.path.basename(inputfile).replace(".py","")

					proc = subprocess.Popen(['grep -rn "'+inpfile+'\.'+method_name+'" '+GenAP_Folder], shell=True, stdout=subprocess.PIPE)
					c = proc.stdout.readlines()

					for mel in c:
						#ckl=mel.split("\t")
						ckl=mel.rsplit(":",1)
						#print ckl
						if "matches" not in ckl[0]: # skip the matches that have "binary .... matches"
							calling_class = os.path.basename(ckl[0])
							calling_class_dir = os.path.dirname(ckl[0])
							output.write("<font color='DarkOrange' size='2'> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b> <--- </b> &nbsp"+calling_class_dir[-40:]+"/<b>"+calling_class+"</b>&nbsp&nbsp&nbsp&nbsp"+ckl[1]+"</font><br>")

			if ")" not in myLine:
				DefEndReached=False



# Recording the links at the top of the html file in a table
for folder in os.listdir(GenAP_Folder):
    if folder=="bfx" or folder == "core" or folder == "pipelines":


        output.write("<br><b><font size='6'>" + folder + " </font></b>")
        num_pyfile=0 #keeping track of how many python files--> used for the number of table columns
        output.write("<table border='0' cellpadding='6'><tr>")
        for inputFile in os.listdir(GenAP_Folder+"/"+folder):
            if inputFile.endswith(".py") and "__init__" not in inputFile:
                num_pyfile+=1
                output.write("<td><a href='#"+inputFile+"' style='text-decoration:none'>"+inputFile+"</a></td>") # Write the link to the file at the top of the html file
                if num_pyfile>7:
                    output.write("</tr><tr>")
                    num_pyfile=0


        if folder=="pipelines":
            # going through subdirectories in pipeline folder
            for pipeline_folder in os.listdir(GenAP_Folder+"/pipelines"):
                if os.path.isdir(GenAP_Folder+"/pipelines/"+pipeline_folder):
                    for pplFile in os.listdir(GenAP_Folder+"/pipelines/"+pipeline_folder):
                        if pplFile.endswith(".py") and "__init__" not in pplFile:
                            output.write("<td><a href='#"+pplFile+"' style='text-decoration:none'>"+pplFile+"</a></td>") # Write the link to the file at the top of the html file


        output.write("</tr></table>")


output.write("__"*80)

# Traverse the 3 folders (bfx, core, pipeline) and for each python file found, list the classes and methods
for folder in os.listdir(GenAP_Folder):
	if folder=="bfx" or folder == "core" or folder == "pipelines":
		output.write("<br><br>###############<font size='6'> <b> " + folder + " </b> </font>#############<br>")
		for inputFile in os.listdir(GenAP_Folder+"/"+folder):
			if inputFile.endswith(".py") and "__init__" not in inputFile:
				class_method_reader(GenAP_Folder+"/"+folder+"/"+inputFile,folder)


	if folder=="pipelines":
		# going through subdirectories in pipeline folder
		for pipeline_folder in os.listdir(GenAP_Folder+"/pipelines"):
			if os.path.isdir(GenAP_Folder+"/pipelines/"+pipeline_folder):
				for pplFile in os.listdir(GenAP_Folder+"/pipelines/"+pipeline_folder):
					if pplFile.endswith(".py") and "__init__" not in pplFile:
						class_method_reader(GenAP_Folder+"/pipelines/"+pipeline_folder+"/"+pplFile,folder)


output.write("</html>")

output.close()

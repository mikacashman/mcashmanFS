#BEGIN_HEADER
# The header block is where all import statments should live
import sys
import traceback
import uuid
import random
import os #for callig weka - fix later
from pprint import pprint, pformat
from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class mcashman_FS:
    '''
    Module Name:
    mcashman_FS

    Module Description:
    A KBase module: mcashman_FS
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
	self.scratch = config['scratch']
        #END_CONSTRUCTOR
        pass

    def FeatureSelection(self, ctx, params):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN FeatureSelection
        print('Starting function')

	### STEP 1 - Parse input and catch any errors
	if 'workspace_name' not in params:
		raise ValueError('Parameter workspace is not set in input arguments')
	workspace_name = params['workspace_name']
	if 'classes' not in params:
		raise ValueError('Parmeter classes is not set in input arguements')
	if 'pangenome_ref' not in params:
		raise ValueError('Parameter pangenome_ref is not set in input arguments')
	pangenome = params['pangenome_ref']
	print("runCount: " + str(params['runCount']))
	runCountOrig = params['runCount']
	runCount = None
	try:
		runCount=int(params['runCount'])
	except ValueError:
		raise ValueError('Cannot parse integer from runCount parameter' + str(params['runCount']))
	if runCount<1:
		raise ValueError('runCount must be more than zero')	

	### STEP 2 - Get the Input Data
	token = ctx['token']
	wsClient = workspaceService(self.workspaceURL, token=token)
	try:
		#why the 0th element?
		pan = wsClient.get_objects([{'ref': pangenome}])[0]['data']
	except:
		#idk what these do
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		orig_error = ''.join('   ' + line for line in lines)
		raise ValueError('Error loading original Pangenome object from workspace:\n' + orig_error)
	print('Got Pangenome')
	if len(params['classes']) != len(pan['genome_refs']):
		raise ValueError('Error: Number of classes and genomes don\'t match')
	
	### STEP 3 - Create Matrix
	print('Reading Pangenome into Array')
	Data = [[0 for x in range(len(pan['genome_refs']))] for y in range(len(pan['orthologs']))] #counts
	count = 0
	Strains = [] #genome names
	Genes = [] #gene names
	Functions = [] #gene functions
	Scores = [] #Scores
	ClassesOrdered = [] #classes from user matched to pangenome
	temp = 0
	for i in range(0,len(pan['genome_refs'])):
		Strains.append(pan['genome_refs'][i])
		ClassesOrdered.append(0)
	for i in range(0,len(pan['genome_refs'])):
		ClassesOrdered[Strains.index(params['genomes'][i])] = params['classes'][i]
	for i in range(0,len(pan['genome_refs'])):
		print(Strains[i] + " - " + str(ClassesOrdered[i]))
	for i in range(0,len(pan['orthologs'])): #for each gene
		count+=1
		Scores.append(0)
		Genes.append(pan['orthologs'][i]['id'])
		Functions.append(pan['orthologs'][i]['function'])
		for j in range(0,len(pan['orthologs'][i]['orthologs'])):#for each instance of gene
			#check genome and add to proper place
			temp = Strains.index(pan['orthologs'][i]['orthologs'][j][2])
			Data[i][temp] = 1 #+=1 for numeric ---- =1 for binary
		
	### STEP temp - Print matrix to a file
	matfilename = self.scratch + "/matrix.txt"
	matrixFile = open(matfilename,"w+")
	funcfilename = self.scratch + "/funcs.txt"
	funcFile = open(funcfilename,"w+")
	for i in range(0,len(pan['genome_refs'])):
		matrixFile.write(Strains[i])
	for i in range(0,len(pan['orthologs'])):
		matrixFile.write(Genes[i])
		for j in range(0,len(pan['genome_refs'])):
			matrixFile.write(" " + str(Data[i][j]))
		matrixFile.write('\n')
		funcFile.write(Functions[i] + '\n')
	matrixFile.close()	
	funcFile.close()

	### STEP 4 - Create random list of indices
	Index=[]
	for i in range(0,len(pan['orthologs'])):
		Index.append(i)

	print("Size of genomes: " + str(len(Strains)))
	print("Size of genes: " + str(len(Genes)))
	
	print("runCount: " + str(params['runCount']))
	for k in range(0,params['runCount']):#loop for running in Weka x  times	
		print("Run " + str(k))
		random.shuffle(Index)

		### STEP 5 - Create Arff file
		filename = self.scratch + "/weka.arff"
		outfilename = self.scratch + "/weka.out"
		arff = open(filename,"w+")
		arff.write("@RELATION FS\n\n")
		for i in range(0,len(pan['orthologs'])):
			arff.write("@ATTRIBUTE " + Genes[Index[i]] + " {ON,OFF}\n")
		arff.write("@ATTRIBUTE class {WT,THICK,HAIRY,THICK-HAIRY}\n")
		arff.write("\n@data\n")
		#print("Testing Order")
		#for i in range(0,len(pan['genome_refs'])):
		#	print(Strains[i] + " - " + str(ClassesOrdered[i]))
		for i in range(0,len(pan['genome_refs'])):
			for j in range(0,len(pan['orthologs'])):
				if Data[Index[j]][i] == 1:
					arff.write("ON,")
				else:
					arff.write("OFF,")
			#print("IF " + str(ClassesOrdered[i]) + " = 1 => " + str(ClassesOrdered[i]==1))
			arff.write(ClassesOrdered[i])
			arff.write('\n')
			#if ClassesOrdered[i] == 1:
			#	arff.write("GROWTH\n")
			#else:
			#	arff.write("NO_GROWTH\n") 
		arff.close()
		#print("ARFF")
		filepresent = os.path.isfile(filename)
		#print("File present?: " + str(filepresent))
		#print("File Path: " + filename)
		#print("Size of file: " + str(os.path.getsize(filename)))
		#os.system("tail -n 4 " + filename)
		tempC = 0
		#with open(filename,'r') as t:
			#t = file(filename).read()
		#	for line in t:
		#		if tempC>12663:	
		#			print(line[-10:])
		#		tempC+=1
		
		
		### STEP 6 - Run in Weka FIX THIS LATER
		#print("Running Weka")
		os.system("java weka.classifiers.trees.J48 -t " + filename + " -T " + filename + " -i > " + outfilename) 
		#print("java weka.classifiers.trees.J48 -t " + filename + " -T " + filename + " -i > " + outfilename) 
		outfilepresent = os.path.isfile(outfilename)
		#print("OutFile present?: " + str(outfilepresent))
		#print("OutFile Path: " + outfilename)
		#print("Size of outfile: " + str(os.path.getsize(outfilename)))
		
	
		### STEP 7 - Record results for all genes (metric equation)
		#parse file and add 1 to cluster if present
		#print("Tree-----")
		with open(outfilename,'r') as f:
			f = file(outfilename).read()
			for word in f.split():
				#print(word)
				if word[0:7]=='cluster':
					#print("     Att: " + word)
					temp = Genes.index(word)
					Scores[temp]+=1
				elif word=='Number': break
		
		### STEP 8 - Repeat x times
		

	### STEP 9 - Compute final metrics and report
	ScoreGene = zip(Scores,Genes)
	sortedGenes = sorted(ScoreGene, key = lambda pair: pair[0], reverse=True)
	
	for i in range(0,count):
		if sortedGenes[i][0] == 0: break
		tempI = Genes.index(sortedGenes[i][1])
		#print(str(sortedGenes[i][0]) + " : " + sortedGenes[i][1] + " (" + Functions[tempI] + ")")
	#[x for (y,x) in sorted(zip(Scores,Genes), key = lambda pair: pair[0])]

	### STEP temp - Print results to report
	#create report
	report = "Testing HTML\n"
	report+= "<!DOCTYPE html>"
	report+= "<html>"
	report+= "<body>"
	report+= "<b>Ordered Genes</b>"
	report+= "</head>"
	report+= "</html>"
	report+= "\n-----------------------------\nScore   Cluster (Function)\n-----   ------------------\n"
	#report = "<table border=1>"
	#report+= " <tr>"
	#report+= "  <th>Score</th>"
	#report+= "  <th>Cluster (Function)</th> </tr>"
	#report+= " <tr>"
	#report+= "  <td>A</td>"
	#report+= "  <td>Something</td>"
	#report+= " </tr>"
	#report+= "</table>"
	#with open(outfilename) as f:
	#	lines = f.readlines()
	#	report+=str(lines)
	#f.close()
	for i in range(0,count):
		if sortedGenes[i][0] == 0: 
			countR = i
			break
		#tempI = pan['orthologs'].index(str(sortedGenes[i][1])['id'])
		#report+=sortedGenes[i][1] + "(" + pan['orthologs'][tempI]['function'] + ") : " + str(sortedGenes[i][0]) + '\n'
		tempI = Genes.index(sortedGenes[i][1])
		report+=str(sortedGenes[i][0]) + " : " + sortedGenes[i][1] + " (" + Functions[tempI] + ")" + '\n'
	report+="-----------------------------\n"
	report+="Total Genes Ranked = " + str(countR) + " out of " + str(len(Genes)) + '\n'
	print("count: " + str(countR)) 
	
	reportObj = {
		'objects_created':[],
		'text_message':report
	}
	#save report
	provenance = [{}]
	if 'provenance' in ctx:
		provenance = ctx['provenance']
	# add additional info to provenance here, in this case the input data object reference
	provenance[0]['input_ws_objects']=[workspace_name+'/'+pan['id']]
	report_info_list = None
	try:
		report_info_list = wsClient.save_objects({
			'workspace':workspace_name,
			'objects':[
			{
				'type':'KBaseReport.Report',
				'data':reportObj,
				'name':'FS_report',
				'meta':{},
				'hidden':1, # important!  make sure the report is hidden
				'provenance':provenance
			}
			]
		})
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		orig_error = ''.join('    ' + line for line in lines)
		raise ValueError('Error saving Report object to workspace:\n' + orig_error)
	report_info = report_info_list[0]
	print('saved report: ' + pformat(report_info))
	print(report)

	#print('Final Scores\n')
	#for i in range(0,100):
	#	print(Genes[i] + ': ' + str(Scores[i]))
	
	print('Size of Data: ' + str(len(Data)))
	#for i in range(0,4):
	#	for j in range(0,len(pan['genome_refs'])):
	#		print(str(Data[i][j]) + ' ') 

	print('Ready to return')
	returnVal = {
		'temp' : str(count),
		'report_name':'FS_report',
		'report_ref': str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4])
	}
        # At some point might do deeper type checking...
        #if not isinstance(returnVal, dict):
        #    raise ValueError('Method FeatureSelection return value ' +
        #                     'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
        #END FeatureSelection

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method FeatureSelection return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

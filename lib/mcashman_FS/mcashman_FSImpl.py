#BEGIN_HEADER
# The header block is where all import statments should live
import sys
import traceback
import uuid
import random
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
	#END_CONSTRUCTOR
        pass

    def FeatureSelection(self, ctx, params):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN FeatureSelection
        print('Starting function')

	#Step 1 - Parse input and catch any errors
	if 'workspace_name' not in params:
		raise ValueError('Parameter workspace is not set in input arguments')
	workspace_name = params['workspace_name']
	if 'classes' not in params:
		raise ValueError('Parmeter classes is not set in input arguements')
	if 'pangenome_ref' not in params:
		raise ValueError('Parameter pangenome_ref is not set in input arguments')
	pangenome = params['pangenome_ref']

	#Step 2 - Get the Input Data
	token = ctx['token']
	wsClient = workspaceService(self.workspaceURL, token=token)
	try:
		#why the 0th element?
		pan = wsClient.get_objects([{'ref': workspace_name+'/'+pangenome}])[0]['data']
	except:
		#idk what these do
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		orig_error = ''.join('   ' + line for line in lines)
		raise ValueError('Error loading original Pangenome object from workspace:\n' + orig_error)
	print('Got Pangenome')
	if len(params['classes']) != len(pan['genome_refs']):
		raise ValueError('Error: Number of classes and genomes don\'t match')
	
	#Step 3 - Create Matrix
	print('Reading Pangenome into Array')
	Data = [[0 for x in range(len(pan['genome_refs']))] for y in range(len(pan['orthologs']))] #counts
	count = 0
	Strains = [] #genome names
	Genes = [] #gene names
	Functions = [] #gene functions
	temp = 0
	for i in range(0,len(pan['genome_refs'])):
		Strains.append(pan['genome_refs'][i])
		print(Strains[i])
	for i in range(0,len(pan['orthologs'])): #for each gene
		count+=1
		Genes.append(pan['orthologs'][i]['id'])
		Functions.append(pan['orthologs'][i]['function'])
		for j in range(0,len(pan['orthologs'][i]['orthologs'])):#for each instance of gene
			#check genome and add to proper place
			temp = Strains.index(pan['orthologs'][i]['orthologs'][j][2])
			Data[i][temp] = 1 #+=1 for numeric ---- =1 for binary
		
	#Step 4 - Create random list of indices
	Index=[]
	for i in range(0,len(pan['orthologs'])):
		Index.append(i)
	random.shuffle(Index)

	#Step 5 - Create Arff file
	arff = open("weka.arff","w+")
	arff.write("@RELATION FS\n\n")
	for i in range(0,len(pan['orthologs'])):
		arff.write("@ATTRIBUTE " + Genes[i] + "{ON,OFF}\n")
	arff.write("@ATTRIBUTE class {GROWTH,NO_GROWTH}\n")
	arff.write("\n@data\n")
	for i in range(0,len(pan['genome_refs'])):
		for j in range(0,len(pan['orthologs'])):
			if Data[j][i] == 1:
				arff.write("ON,")
			else:
				arff.write("OFF,")
		if params['classes'][i] == 1:
			arff.write("GROWTH\n")
		else:
			arff.write("NO_GROWTH\n") 
	arff.close()
	#Step 6 - Run in Weka
	#Step 7 - Record results for all genes (metric equation)
	#Step 8 - Repeat x times
	#Step 9 - Compute final metrics and report

	print('Size of Data: ' + str(len(Data)))
	for i in range(0,4):
		for j in range(0,len(pan['genome_refs'])):
			print(str(Data[i][j]) + ' ') 

	print('Ready to return')
	returnVal = {
		'temp' : str(count)
	}
        # At some point might do deeper type checking...
        #if not isinstance(returnVal, dict):
        #    raise ValueError('Method FeatureSelection return value ' +
        #                     'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
	#END FeatureSelection

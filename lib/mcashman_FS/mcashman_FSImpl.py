#BEGIN_HEADER
# The header block is where all import statments should live
import sys
import traceback
import uuid
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
	#check for classes
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
	
	#Step 3 - Create Matrix
	print('Reading Pangenome into Array')
	Data = []
	Row = []
	count = 0
	Strains = []
	Genes = []
	for i in range(0,len(pan['orthologs'])): #for each gene
		#print(pangenome.ortholog[i].id)
		count+=1
		
	
		#for j in range(0,pangenome.genome_refs):#for each genome
		#Row[i]=length(pangenome.orthologs.orthologs)
		
	#Step 4 - Create random list of indices
	#Index=[]
	#for i in range(0,len(pangenome.ortholog)):
	#	Index[i]=i
	#random.shuffle(Index)

	#Step 5 - Run in Weka
	#Step 6 - Record results for all genes (metric equation)
	#Step 7 - Repeat x times
	#Step 8 - Compute final metrics and report

	print('Done I guess')
	#END FeatureSelection
	


	returnVal = {
		'temp' : str(count)
	}
        # At some point might do deeper type checking...
        #if not isinstance(returnVal, dict):
        #    raise ValueError('Method FeatureSelection return value ' +
        #                     'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

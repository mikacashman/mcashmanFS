import unittest
import os
import json
import time

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from mcashman_FS.mcashman_FSImpl import mcashman_FS


class mcashman_FSTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.ctx = {'token': token, 'provenance': [{'service': 'mcashman_FS',
            'method': 'please_never_use_it_in_production', 'method_params': []}],
            'authenticated': 1}
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('mcashman_FS'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = mcashman_FS(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_mcashman_FS_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_FeatureSelection(self):
        # Prepare test objects in workspace if needed using 
        # self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
	
	# This test should probably fail but isn't even running
	print("starting test...")
	#test_dir = os.path.dirname(os.path.realpath(__file__))
	#file_path = test_dir + "/TestOrthoRhizo.json" 
	#print(file_path + "\n")
	#print(os.system('pwd'))
	#print(os.system('ls'))
	#print(self.getWsName())
	#panEX = open ('TestOrthoRhizo.json')
	#import json - json.read
	#with open("{0}/{1}".format(test_dir,'TestOrthoRhizo.json'),'r') as json_data:
	#	eo = json.load(json_data)
	#self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects':
	#	[{'type': 'KBaseGenomes.Pangenome', 'name': 'TestRhizo', 'data': json_data}]})
	ret = self.getImpl().FeatureSelection(self.getContext(),{'workspace_name':'mikaelacashman:1469216639277',
		'classes':{0}, 'pangenome_ref':'TestOrthoRhizo'})
	print("Running asserts...")
	self.assertEqual(ret[0],12660)
	#pass
        

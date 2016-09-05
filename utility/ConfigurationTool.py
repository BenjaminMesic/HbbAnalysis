import os
import subprocess as sp
import json

import MiscTool

class ConfigurationLoader(object):
	'''
	-----------
	Description:
	Loads all configuration file and stores them into single dictionary
	called self.cfg_files.

	-----------	
	Input files:
	Configuration files from directory config/analysis_name

	-----------
	Library: os, subprocess, json
	External: print_nice

	-----------
	Parameters:
	self.analysis_name 	- got from utility.analysis_name(), sys.argv
						argument, if doesn't exist default is set to Wlv
	self.cfg_files 		- dictionary with config files from the
						directory config/analysis_name

	-----------
	Functions:
	get_configuration_files - gets and store all config files (json format)
						in self.cfg_files

	-----------
	Useful commands:


	-----------
	To DO:

	'''	
	def __init__(self, analysis_name):

		MiscTool.print_nice('python_info', '\nCreated instance of ConfigurationLoader class')	

		self.analysis_name = analysis_name
		self.cfg_files = {}

		self.get_configuration_files()

	def get_configuration_files(self):
		
		_configuration_files_path = os.path.join('../config', self.analysis_name)

		MiscTool.print_nice('analysis_info', 'Configuration files from ', self.analysis_name)	

		_files = sp.check_output(['ls', _configuration_files_path]).split()

		for _config in _files:
			MiscTool.print_nice('analysis_info', '', _config)
			try:
				self.cfg_files[_config.split('.')[0]] = json.load(open(os.path.join( _configuration_files_path, _config)))
			except Exception, e:
				MiscTool.print_nice('error', 'Problem with loading: ' + _config)
				raise

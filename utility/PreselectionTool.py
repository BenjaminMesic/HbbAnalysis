import os
import stat
import subprocess as sp

import ROOT

from utility import MiscTool
from utility import BatchTool
from utility import TreeTool


class PreselectionTool(object):
	'''
	-----------
	Description:
	Preselection is used to apply preselection cut on all the samples
	and as a result we have smaller files with only events of our interest.
	It gets list of all files from self.samples_path, apply preselection
	and copy them in XXX. After that, merging of these files is done
	so that we have only one file for each sample. Local batch system in 
	Zagreb is used.

	-----------	
	Input files: self.batch_templates_path, 
	Output files: self.batch_path, self.location_of_preselected_samples

	-----------
	Parameters:

	-----------
	Functions:
	preselection() - get list of files from _step_1_logical_file_names
					directory. If you want to add other samples start 
					first add them in config file samples.ini and then
					start _step_1 script which creates file with logical
					file names. preselection() doesnt need samples.ini



	-----------
	Useful commands:
	limit maxproc 2048 - set if getting error with number of processes

	-----------
	To DO:


	'''	

	def __init__(self, analysis_name, configuration, force_all, sample = None):

		MiscTool.Print('python_info', '\nCreated instance of Preselection class')

		# force preselection on already existing files
		self.force_all = force_all

		# ------ Paths -------
		self.path_working_directory = os.environ['Hbb_WORKING_DIRECTORY']
		self.path_batch_templates 	= os.path.join( self.path_working_directory, 'utility', 'templates', 'preselection_batch')
		self.path_batch_scripts 	= os.path.join( self.path_working_directory, 'results', analysis_name, '_2_preselection_batch')
		self.path_samples 			= configuration['paths']['samples_directory']
		self.path_list_of_samples 	= os.path.join( self.path_samples, 'logical_file_names')
		try:
			self.path_preselected_samples = configuration['paths']['preselection_directory']
		except Exception, e:
			self.path_preselected_samples = self.path_samples + '_preselection'

		# ------ Samples -------
		if sample == None:
			self.list_of_samples = filter(lambda x: '_local.txt' in x , os.listdir(self.path_list_of_samples)) # ['SingleMuon_local.txt', 'SingleElectron_local.txt']#
		else:
			self.list_of_samples = ['{0}_local.txt'.format(sample)]
		self.list_of_search_keywords		= ['.root']

		# ------ Cuts -------
		self.preselection_cut = configuration['cuts']['preselection_cut']


		MiscTool.Print('analysis_info', 'Working directory:', self.path_working_directory)
		MiscTool.Print('analysis_info', 'Path to list of samples:', self.path_list_of_samples)
		MiscTool.Print('analysis_info', 'Path to batch templates:', self.path_batch_templates)
		MiscTool.Print('analysis_info', 'Path to batch scripts:', self.path_batch_scripts)
		MiscTool.Print('analysis_info', '\nPreselection cut:', self.preselection_cut)

	def preselection(self):

		MiscTool.Print('python_info', '\nCalled preselection function.')

		# Loop over samples
		for _sample in self.list_of_samples:

			MiscTool.Print('status', '\n' + _sample)

			_files = open(os.path.join(self.path_list_of_samples, _sample),'r')

			# For each file create job by copying template script
			for _i,_f in enumerate(_files):

				if not self.filter(_f):
					continue

				_file = _f.replace('\n', '')

				_output_file = _file.replace(self.path_samples, self.path_preselected_samples)		
				_inital_directory, _script_name = _file.replace(self.path_samples, self.path_batch_scripts).split('tree')

				# If preselected file already exists skip
				if TreeTool.TreeTool.check_if_tree_ok(_output_file) and not self.force_all:
					MiscTool.Print('python_info','File {0} already exists.'.format(_output_file))
					continue

				_batch_arguments = {
					'<initial_directory>'	: _inital_directory, 				# path to newly created batch script
					'<input_file>' 			: _file, 							# file w/o presel
					'<output_file>'			: _output_file, 					# file w/ presel
					'<cut>'					: self.preselection_cut,			# 'V_pt>100'
					'<script_name>' 		: _script_name.replace('.root',''), # 1401
					'python_template' 		: os.path.join(self.batch_templates_path, 'preselection_batch_template.py')
				}

				_batch = BatchTool.BatchTool(_batch_arguments)
				_batch.make_scripts()
				_batch.send_job()

	def merge(self):

		MiscTool.Print('python_info', '\nCalled merge function.')

		# Loop over samples
		for _sample in self.list_of_samples:

			MiscTool.Print('status', '\nMerging preselected files for: ' + _sample)

			_files = open(os.path.join( self.path_list_of_samples, _sample),'r')

			# name of merged root file			
			_file_name = _sample.replace('_local.txt', '.root')
			_merge_file_name = os.path.join( self.path_preselected_samples, _file_name )

			# If merged preselected file already exists skip
			if TreeTool.TreeTool.check_if_tree_ok(_merge_file_name) and not self.force_all:
				MiscTool.Print('python_info','File {0} already exists.'.format(_merge_file_name))
				continue

			_merger = ROOT.TFileMerger(ROOT.kFALSE)
			_merger.OutputFile(_merge_file_name, 'RECREATE')

			for _i,_f in enumerate(_files):

				_file = _f.replace('\n', '').replace( self.path_samples, self.path_preselected_samples)

				MiscTool.Print('status', _file)

				# if i != 0:
				# 	continue

				# Check if file exists, if not store
				if not os.path.isfile(_file):
					MiscTool.Print('error', 'File {0} is missing.'.format(_file))
					continue

				_merger.AddFile(_file)				
				
			_merger.Merge()

			MiscTool.Print('status', '\nMerging done.')

	def check_root_preselected_files(self, sample):

		MiscTool.Print('python_info', '\nCalled check_root_preselected_files function.')

		_destination_file 	= open(os.path.join(self.path_list_of_samples, sample),'r')	

		for _f in _destination_file:

			# destination path for each file
			_file = _f.replace('\n', '').replace(self.path_samples, self.path_preselected_samples)

			try:
				if TreeTool.TreeTool.check_if_tree_ok(_file):
					pass
					# MiscTool.Print('status', 'File: {0} OK.'.format(_file))
				else:
					MiscTool.Print('error', 'File: {0} not OK.'.format(_file))
			
			except Exception, e:
				pass

	# Only work on files which have the keywords
	def filter(self, file_name):

		if not any(_k in file_name for _k in self.list_of_search_keywords):
			return False
		else:
			return True

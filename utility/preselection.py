import os
import stat
import subprocess as sp

import ROOT

import utility


class Preselection(object):
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

	def __init__(self, analysis_name, configuration, force_all):

		utility.print_nice('python_info', '\nCreated instance of Preselection class')

		# force preselection on already existing files
		self.force_all = force_all

		# ------ Paths -------
		self.working_directory 		= configuration.cfg_files['paths']['working_directory']
		self.batch_templates_path 	= os.path.join( self.working_directory, 'utility', 'templates', 'preselection_batch')
		self.batch_path 			= os.path.join( self.working_directory, 'results', analysis_name, '_step_2_preselection_batch')
		self.location_of_samples 	= configuration.cfg_files['paths']['samples_directory']
		self.samples_path 			= os.path.join( self.location_of_samples, 'logical_file_names')
		try:
			self.location_of_preselected_samples = configuration.cfg_files['paths']['preselection_directory']
		except Exception, e:
			self.location_of_preselected_samples = self.location_of_samples + '_preselection'

		# ------ Samples -------
		self.list_of_samples = ['SingleElectron_local.txt'] #filter(lambda x: '_local' in x , os.listdir(self.samples_path))

		# ------ Cuts -------
		self.preselection_cut = configuration.cfg_files['cuts']['preselection_cut']


		utility.print_nice('analysis_info', 'Working directory:', self.working_directory)
		utility.print_nice('analysis_info', 'Path to list of samples:', self.samples_path)
		utility.print_nice('analysis_info', 'Path to batch templates:', self.batch_templates_path)
		utility.print_nice('analysis_info', 'Path to batch scripts:', self.batch_path)
		utility.print_nice('analysis_info', '\nPreselection cut:', self.preselection_cut)


	def preselection(self):

		utility.print_nice('python_info', '\nCalled preselection function.')

		# Loop over samples
		for _sample in self.list_of_samples:

			utility.print_nice('status', '\n' + _sample)

			_files = open(os.path.join(self.samples_path, _sample),'r')

			# For each file create job by copying template script
			for _i,_f in enumerate(_files):

				if '.root' not in _f:
					continue

				_file = _f.replace('\n', '')

				_output_file = _file.replace(self.location_of_samples, self.location_of_preselected_samples)		
				_inital_directory, _script_name = _file.replace(self.location_of_samples, self.batch_path).split('tree')

				# If preselected file already exists skip
				if utility.file_exists(_output_file) and not self.force_all:
					utility.print_nice('python_info','File {0} already exists.'.format(_output_file))
					continue

				_batch_arguments = {
					'<initial_directory>'	: _inital_directory, 				# path to newly created batch script
					'<input_file>' 			: _file, 							# file w/o presel
					'<output_file>'			: _output_file, 					# file w/ presel
					'<cut>'					: self.preselection_cut,			# 'V_pt>100'
					'<script_name>' 		: _script_name.replace('.root',''), # 1401
					'python_template' 		: os.path.join(self.batch_templates_path, 'preselection_batch_template.py')
				}

				_batch = utility.BatchSender(_batch_arguments)
				_batch.make_scripts()
				_batch.send_job()

	def merge(self):

		utility.print_nice('python_info', '\nCalled merge function.')

		# Loop over samples
		for _sample in self.list_of_samples:

			utility.print_nice('status', '\nMerging preselected files for: ' + _sample)

			_files = open(os.path.join(self.samples_path, _sample),'r')

			# name of merged root file			
			_file_name = _sample.split('_')[0] + '.root'
			_merge_file_name = os.path.join(self.location_of_preselected_samples, _file_name )

			# If merged preselected file already exists skip
			if utility.file_exists(_merge_file_name) and not self.force_all:
				utility.print_nice('python_info','File {0} already exists.'.format(_merge_file_name))
				continue

			_merger = ROOT.TFileMerger(ROOT.kFALSE)
			_merger.OutputFile(_merge_file_name, 'RECREATE')

			for _i,_f in enumerate(_files):

				_file = _f.replace('\n', '').replace(self.location_of_samples, self.location_of_preselected_samples)

				utility.print_nice('status', _file)

				# if i != 0:
				# 	continue

				# Check if file exists, if not store
				if not os.path.isfile(_file):
					utility.print_nice('error', 'File {0} is missing.'.format(_file))
					continue

				_merger.AddFile(_file)				
				
			_merger.Merge()

			utility.print_nice('status', '\nMerging done.')

	def check_root_files(self, sample):

		utility.print_nice('python_info', '\nCalled check_root_files function.')

		_destination_file 	= open(os.path.join(self.samples_path, sample),'r')	

		for _f in _destination_file:

			# destination path for each file
			_file = _f.replace('\n', '').replace(self.location_of_samples, self.location_of_preselected_samples)

			try:
				if utility.file_exists(_file):
					utility.print_nice('status', 'File: {0} OK.'.format(_file))
				else:
					utility.print_nice('error', 'File: {0} not OK.'.format(_file))
			
			except Exception, e:

				pass

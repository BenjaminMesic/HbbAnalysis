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
		self.samples_path 			= os.path.join( self.working_directory, 'results', analysis_name, '_step_1_logical_file_names')
		self.batch_templates_path 	= os.path.join( self.working_directory, 'utility', 'templates', 'preselection_batch')
		self.batch_path 			= os.path.join( self.working_directory, 'results', analysis_name, '_step_2_preselection_batch')
		try:
			self.location_of_preselected_samples = configuration.cfg_files['paths']['preselection_directory']
		except Exception, e:
			self.location_of_preselected_samples = configuration.cfg_files['paths']['samples_directory'] + '_preselection'

		# ------ Samples -------
		self.list_of_samples = filter(lambda x: 'missing' not in x and '.txt' in x , os.listdir(self.samples_path))

		# ------ Cuts -------
		self.preselection_cut = configuration.cfg_files['cuts']['preselection_cut']


		utility.print_nice('analysis_info', 'Working directory:', self.working_directory)
		utility.print_nice('analysis_info', 'Path to list of samples:', self.samples_path)
		utility.print_nice('analysis_info', 'Path to batch templates:', self.batch_templates_path)
		utility.print_nice('analysis_info', 'Path to batch scripts:', self.batch_path)
		utility.print_nice('analysis_info', '\nPreselection cut:', self.preselection_cut)


	def preselection(self):

		utility.print_nice('python_info', '\nCalled preselection function.')

		# Check if batch dir exist, if not create one
		utility.make_directory(self.batch_path)

		# Loop over samples
		for _sample in self.list_of_samples:

			utility.print_nice('status', '\n' + _sample)

			_files = open(os.path.join(self.samples_path, _sample),'r').read().split('\n')

			# For each file create job by copying template script
			for _i,_file in enumerate(_files):

				if _file == '':
					continue

				_file_split = _file.split('/')
				_output_dir =  os.path.join(self.location_of_preselected_samples, *_file_split[4:-1])

				# Here comes the part of modifying template batch scripts
				XXX_1 = _file 																# file w/o presel
				XXX_2 = os.path.join(_output_dir, _file_split[-1])							# file w presel
				XXX_3 = self.preselection_cut 												# 'V_pt>100'
				XXX_4 = _file_split[-1].split('.')[0]										# tree_1401
				XXX_5 = os.path.join(self.batch_path, '/'.join(_file_split[4:-1]))			# path to newly created batch script

				# If preselected file already exists skip
				if utility.file_exists(XXX_2) and not self.force_all:
					utility.print_nice('python_info','File {0} already exists.'.format(XXX_2))
					continue

				utility.print_nice('status', XXX_2)

				# Check if output dir for preselected files exist, if not create one
				utility.make_directory(_output_dir)

				# print '\n'.join([XXX_1, XXX_2, XXX_3, XXX_4, XXX_5])

				# Make directory to store batch scripts
				utility.make_directory(XXX_5)

				# Modify template scripts and save them
				for _template in os.listdir( self.batch_templates_path ):

					_f = open( os.path.join(self.batch_templates_path, _template),'r')
					_filedata = _f.read()
					_f.close()

					_newdata = _filedata\
							.replace('XXX_1', XXX_1)\
							.replace('XXX_2', XXX_2)\
							.replace('XXX_3', XXX_3)\
							.replace('XXX_4', XXX_4)\
							.replace('XXX_5', XXX_5)\

					_newdata_name = XXX_5 + '/' + XXX_4 + '.' + _template.split('.')[1]
					_f = open( _newdata_name,'w')
					_f.write(_newdata)
					_f.close()

					# Send jobs
					if 'sh' in _template:

						utility.print_nice('status', _i)

						# if _i > 5:
						# 	continue
						# if i%100 == 0 and i!=0:
						# 	time.sleep(40)

						# Change permission so that it can be executed 
						os.chmod(_newdata_name, os.stat(_newdata_name).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
						_working_dir = os.getcwd()
						os.chdir(XXX_5)
						# print sp.check_output('pwd', shell=True)
						sp.call('condor_submit ' + XXX_4 + '.txt', shell=True)			
						os.chdir(_working_dir)

	def merge(self):

		utility.print_nice('python_info', '\nCalled merge function.')

		# Loop over samples
		for _sample in self.list_of_samples:

			utility.print_nice('status', '\nMerging preselected files for:' + _sample)

			_files = open(os.path.join(self.samples_path, _sample),'r').read().split('\n')

			_files_split = _files[0].split('/')
			
			# name of merged root file
			_merge_file_name = os.path.join(self.location_of_preselected_samples, _files_split[4] + '.root')

			# If merged preselected file already exists skip
			if utility.file_exists(_merge_file_name) and not self.force_all:
				utility.print_nice('python_info','File {0} already exists.'.format(_merge_file_name))
				continue

			_merger = ROOT.TFileMerger(ROOT.kFALSE)
			_merger.OutputFile(_merge_file_name, 'RECREATE')

			for _i,_file in enumerate(_files):

				utility.print_nice('status', _file)

				# if i != 0:
				# 	continue

				if _file == '':
					continue

				# Check if file exists, if not store
				_file_name = os.path.join(self.location_of_preselected_samples, *_files_split[4:])
				if not os.path.isfile(_file_name):
					continue

				# print _i, _file_name

				_merger.AddFile(_file_name)				
				
			_merger.Merge()

			utility.print_nice('status', '\nMerging done.')
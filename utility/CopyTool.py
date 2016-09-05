import os
import subprocess as sp

import MiscTool
import DirectoryTool
import TreeTool


class CopyTool(object):
	'''
	-----------
	Description:
	
	----------- 
	Input files:    samples.ini, paths.ini, general.ini

	-----------
	Parameters:

	-----------
	Functions:


	-----------
	Useful commands:
	lcg-ls -b -v -l -D srmv2 srm:"//stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/store/user/cvernier/VHBBHeppyV23" 
	
	gfal-ls -Hl srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/
	gfal-ls -Hl srm://stormfe1.pi.infn.it/cms/store/user/cvernier/VHBBHeppyV23/
	gfal-copy --force srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/ZZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V23_ZZ_TuneCUETP8M1_13TeV-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160718_082331/0000/tree_1.root file:////$PWD/
	gfal-copy --force srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 file:////$PWD/

	-----------
	To DO:

	''' 
	def __init__(self, analysis_name, configuration, force_all):

		MiscTool.print_nice('python_info', '\nCreated instance of CopyTool class')

		# force preselection on already existing files
		self.force_all = force_all  

		# ------ Paths -------
		self.list_of_samples    = configuration.cfg_files['samples']
		self.output_directory   = configuration.cfg_files['paths']['samples_directory']
		self.working_directory  = configuration.cfg_files['paths']['working_directory']
		self.logical_file_names = os.path.join( self.output_directory, 'logical_file_names')

		# ------ Copy options -------
		self.storage_element 	= configuration.cfg_files['general']['storage_element']
		self.locations 			= configuration.cfg_files['general']['locations']
		self.list_of_all_samples_from_sources = {}
		self.search_keywords	= ['.root']


		MiscTool.print_nice('analysis_info', 'Analysis name:', analysis_name)
		MiscTool.print_nice('analysis_info', 'Samples will be stored in:', self.output_directory)
		MiscTool.print_nice('analysis_info', 'Working_directory:', self.working_directory)
		MiscTool.print_nice('analysis_info_list', 'List of samples:', self.list_of_samples.keys())

		# Get the list of all the samples from source
		self.get_list_of_all_samples_from_sources()

	# Wrappers for ls, cp, which are used for outside
	def wrapper_gfal_ls(self, location):

		MiscTool.print_nice('python_info', '\nCalled wrapper_gfal_ls function.')

		_command = ['gfal-ls'] #,'-Hl']
		_command.append('srm:/' + location)

		MiscTool.print_nice('python_info', 'Command: ' + ' '.join(_command))

		return sp.check_output(_command)

	def wrapper_gfal_ls_r(self, location):
		
		MiscTool.print_nice('python_info', '\nCalled wrapper_gfal_ls_r function.')

		_paths = Queue()
		_paths.enqueue(location)

		# list to store logical file names
		_logical_file_names = []

		while not _paths.isEmpty():

			# get one path
			_x = _paths.dequeue()

			# do ls
			_y = self.wrapper_gfal_ls( _x )

			# maybe problematic part
			if _x in _y:

				# if ls gets you the same result as input you are done
				_logical_file_names.append(_x)

			else:
				# go deeper in the folder
				for _p in _y.splitlines():
					_paths.enqueue( os.path.join(_x, _p))


		return _logical_file_names

	def wrapper_gfal_cp_file(self, source, destination):
	
		MiscTool.print_nice('python_info', '\nCalled wrapper_gfal_cp_file function.')

		_command = ['gfal-copy', '--force']
		_command.append('srm:/' + source)
		_command.append('file:///' + destination)

		MiscTool.print_nice('python_info', 'Command: ' + ' '.join(_command))

		sp.call(_command)

	# Used to find files outside
	def get_list_of_all_samples_from_sources(self):

		MiscTool.print_nice('python_info', '\nCalled get_list_of_all_samples_from_sources function.')

		# Loop over all locations from which you are copying files
		for _l in self.locations:
			_path = os.path.join( self.storage_element[_l], self.locations[_l])
			
			# execute ls command
			for _s in self.wrapper_gfal_ls( _path ).splitlines():
				self.list_of_all_samples_from_sources[_s] = _l

	def save_logical_file_names_source(self, sample):
		
		if sample in self.list_of_all_samples_from_sources:

			_loc = self.list_of_all_samples_from_sources[sample]
			MiscTool.print_nice('status', '\nSample {0} exists in {1}.'.format(sample, _loc))	

			# sample txt file to store LFNs
			_outpath = os.path.join(self.logical_file_names, sample + '.txt')
			
			# If txt file already exists skip
			if os.path.isfile(_outpath) and not self.force_all:
				MiscTool.print_nice('python_info','File {0} already exists.'.format(_outpath))
			
			else:
				_path = os.path.join(self.storage_element[_loc], self.locations[_loc], sample)
				_logical_file_names = self.wrapper_gfal_ls_r(_path)
				with open(_outpath, 'w') as _outfile:
					for _lfn in _logical_file_names:
						_outfile.write(_lfn + '\n')
				MiscTool.print_nice('status', 'The LFNs were written to "{}".'.format(_outpath))

		else:
			MiscTool.print_nice('error', _s + ' is missing!')

	def save_logical_file_names_all_samples_from_config_source(self):

		MiscTool.print_nice('python_info', '\nCalled save_logical_files_names_all_samples_from_config function.')

		# Create the output directory if it doesn't exist
		DirectoryTool.DirectoryTool.make_directory(self.logical_file_names)

		# Loop over all samples
		for _s in self.list_of_samples:

			self.save_logical_file_names_source(_s)

	# Used to find files locally, check if something is missing
	def save_logical_file_names_from_config_destination(self, sample):

		MiscTool.print_nice('python_info', '\nCalled save_logical_file_names_from_config_destination function.')
		MiscTool.print_nice('status', 'Getting local lfns for sample {0}'.format(sample))

		_source_file 		= open(os.path.join(self.logical_file_names, sample + '.txt'),'r')
		_destination_file 	= open(os.path.join(self.logical_file_names, sample + '_local.txt'), 'w')
		_missing_file 		= open(os.path.join(self.logical_file_names, sample + '_missing.txt'), 'w') 

		_loc = self.list_of_all_samples_from_sources[sample]
		_path_to_be_replaced = os.path.join( self.storage_element[_loc], self.locations[_loc])
		_path_to_be_replaced_with = self.output_directory

		for _f in _source_file:

			if not self.filter( _f):
				continue

			# Create destination path for each file
			_lfn_destination = _f.strip().replace(_path_to_be_replaced, _path_to_be_replaced_with)

			if os.path.isfile(_lfn_destination):
				_destination_file.write(_lfn_destination + '\n')
			else:
				_missing_file.write(_lfn_destination + '\n')

		_source_file.close()
		_destination_file.close()
		_missing_file.close()

	def save_logical_file_names_all_samples_from_config_destination(self):

		MiscTool.print_nice('python_info', '\nCalled save_logical_file_names_all_samples_from_config_destination function.')
		
		# Loop over all samples
		for _s in self.list_of_samples:
			
			self.save_logical_file_names_from_config_destination(_s)

	# Copy files
	def copy_files_single_sample(self, sample):

		MiscTool.print_nice('python_info', '\nCalled copy_files_single_sample function.')
		
		_missing_file 		= open(os.path.join(self.logical_file_names, sample + '_missing.txt'), 'r')

		_loc = self.list_of_all_samples_from_sources[sample]
		_path_to_be_replaced = self.output_directory
		_path_to_be_replaced_with = os.path.join( self.storage_element[_loc], self.locations[_loc])
		

		for _f in _missing_file:

			# Copy only root files
			if not self.filter( _f):
				continue

			_source = _f.strip().replace(_path_to_be_replaced, _path_to_be_replaced_with)
			_destination = _f.strip().split('tree')[0]

			try:
				DirectoryTool.DirectoryTool.make_directory(_destination)
				self.wrapper_gfal_cp_file(_source, _destination)
			except Exception, e:
				MiscTool.print_nice('error', 'Problem copying {0}'.format(_source))
				raise

	def copy_files_all_samples_from_config(self):
		
		MiscTool.print_nice('python_info', '\nCalled copy_files_all_samples_from_config function.')
		
		# Loop over all samples
		for _s in self.list_of_samples:
			
			self.copy_files_single_sample(_s)

	# Check if .root files ok
	def check_root_files(self, sample):

		MiscTool.print_nice('python_info', '\nCalled check_root_files function.')

		_destination_file 	= open(os.path.join(self.logical_file_names, sample + '_local.txt'), 'r')		
		_error_file 		= open(os.path.join(self.logical_file_names, sample + '_error.txt'), 'w') 

		for _f in _destination_file:

			if not self.filter( _f):
				continue

			# destination path for each file
			_lfn_destination = _f.replace('\n', '')

			try:
				if TreeTool.TreeTool.check_if_tree_ok(_lfn_destination):
					MiscTool.print_nice('status', 'File: {0} OK.'.format(_lfn_destination))
				else:
					MiscTool.print_nice('error', 'File: {0} not OK.'.format(_lfn_destination))
					_error_file.write(_lfn_destination + '\n')
			
			except Exception, e:
				MiscTool.print_nice('error', 'File: {0} could not be checked.'.format(_lfn_destination))


		_error_file.close()
		_destination_file.close()		

	# Remove all files for one sample
	def remove_files_single_sample(self, sample):

		MiscTool.print_nice('python_info', '\nCalled remove_files_single_sample function.')
		
		_missing_file 	= open(os.path.join(self.logical_file_names, sample + '_missing.txt'), 'r') 

		for _f in _missing_file:

			# Create destination path for each file
			_lfn_destination = _f.strip()

			try:
				sp.call(['rm', '-rf', _lfn_destination])
			except Exception, e:
				sp.call(['rm', '-f', _lfn_destination])
			else:
				pass
			finally:
				pass

	# Only copy files which have the keywords
	def filter(self, file_name):

		if not any(_k in file_name for _k in self.search_keywords):
			return False
		else:
			return True
			

class Queue:
	'''
	-----------
	Description:
	Just a simple queue needed to store logical file names in wrapper_gfal_ls_r.

	''' 
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def enqueue(self, item):
		self.items.insert(0,item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)


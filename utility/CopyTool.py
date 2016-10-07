import os
import subprocess as sp
import Queue

import ROOT

from utility import MiscTool
from utility import TreeTool

class CopyTool(object):
	'''
	-----------
	Description:
	
	----------- 
	Input files:    samples.py, paths.py, general.py

	-----------
	Parameters:

	-----------
	Functions:


	-----------
	Useful commands:
	lcg-ls -b -v -l -D srmv2 srm:"//stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/store/user/cvernier/VHBBHeppyV23" 
	
	gfal-ls -Hl srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/
	gfal-ls -Hl srm://stormfe1.pi.infn.it/cms/store/user/cvernier/VHBBHeppyV23/
	gfal-copy --force srm://t3se01.psi.ch/pnfs/pfsi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/ZZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V23_ZZ_TuneCUETP8M1_13TeV-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160718_082331/0000/tree_1.root file:////$PWD/
	gfal-copy --force srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 file:////$PWD/

	-----------
	To DO:
	- add complete Description


	''' 
	def __init__(self, analysis_name, configuration, force_all):

		MiscTool.Print('python_info', '\nCreated instance of CopyTool class')

		# force preselection on already existing files
		self.force_all = force_all  
		
		# ------ Paths -------
		self.path_working_directory  = os.environ['Hbb_WORKING_DIRECTORY']
		self.path_output_directory   = configuration['paths']['samples_directory']
		self.path_logical_file_names = os.path.join( self.path_output_directory, 'logical_file_names')

		# ------ Copy options -------
		self.list_of_samples_from_config    = configuration['samples']
		self.list_of_storage_elements 		= configuration['general']['storage_element']
		self.list_of_locations 				= configuration['general']['locations']
		self.list_of_samples_from_sources 	= {}
		self.list_of_search_keywords		= ['.root']


		MiscTool.Print('analysis_info', 'Analysis name:', analysis_name)
		MiscTool.Print('analysis_info', 'Samples will be stored in:', self.path_output_directory)
		MiscTool.Print('analysis_info', 'Working_directory:', self.path_working_directory)
		MiscTool.Print('analysis_info_list', 'List of samples:', self.list_of_samples_from_config.keys())

	# Wrappers for ls, cp, which are used for browsing sources where files are located
	def wrapper_gfal_ls(self, location):

		MiscTool.Print('python_info', '\nCalled wrapper_gfal_ls function.')

		_command = ['gfal-ls'] #,'-Hl']
		_command.append('srm:/' + location)

		MiscTool.Print('python_info', 'Command: ' + ' '.join(_command))

		return sp.check_output(_command)

	def wrapper_gfal_ls_r(self, location):
		
		MiscTool.Print('python_info', '\nCalled wrapper_gfal_ls_r function.')

		_paths = Queue.Queue()
		_paths.put(location)

		# list to store logical file names
		_logical_file_names = []

		while not _paths.empty():

			# get one path
			_x = _paths.get()

			# if .tar.gz in name skip
			if '.tar.gz' in _x:
				continue

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
	
		MiscTool.Print('python_info', '\nCalled wrapper_gfal_cp_file function.')

		_command = ['gfal-copy', '--force']
		_command.append('srm:/' + source)
		_command.append('file:///' + destination)

		MiscTool.Print('python_info', 'Command: ' + ' '.join(_command))

		sp.call(_command)

	# Used to find files outside
	def get_list_of_samples_from_sources(self):

		MiscTool.Print('python_info', '\nCalled get_list_of_samples_from_sources function.')

		# Loop over all locations from which you are copying files
		for _l in self.list_of_locations:
			_path = os.path.join( self.list_of_storage_elements[_l], self.list_of_locations[_l])
			
			# execute ls command
			for _s in self.wrapper_gfal_ls( _path ).splitlines():
				self.list_of_samples_from_sources[_s] = _l

	def save_logical_file_names_source(self, sample):
		
		if sample in self.list_of_samples_from_sources:

			# Get the location where this sample is located (pisa, psi, ...)
			_loc = self.list_of_samples_from_sources[sample]
			MiscTool.Print('status', '\nSample {0} exists in {1}.'.format(sample, _loc))	

			# txt file to store sample LFNs
			_outpath = os.path.join(self.path_logical_file_names, sample + '.txt')
			
			# If txt file already exists skip
			if os.path.isfile(_outpath) and not self.force_all:
				MiscTool.Print('python_info','File {0} already exists.'.format(_outpath))
			
			else:
				_path = os.path.join(self.list_of_storage_elements[_loc], self.list_of_locations[_loc], sample)
				_logical_file_names = self.wrapper_gfal_ls_r(_path)
				with open(_outpath, 'w') as _outfile:
					for _lfn in _logical_file_names:
						_outfile.write(_lfn + '\n')
				MiscTool.Print('status', 'The LFNs were written to "{}".'.format(_outpath))

		else:
			MiscTool.Print('error', sample + ' is missing!')

	def save_logical_file_names_all_samples_from_config_source(self):

		MiscTool.Print('python_info', '\nCalled save_logical_files_names_all_samples_from_config function.')

		# Create the output directory if it doesn't exist
		MiscTool.make_directory(self.path_logical_file_names)

		# Loop over all samples
		for _s in self.list_of_samples_from_config:

			self.save_logical_file_names_source(_s)

	# Used to find files locally, check if something is missing
	def save_logical_file_names_from_config_destination(self, sample):

		MiscTool.Print('python_info', '\nCalled save_logical_file_names_from_config_destination function.')
		MiscTool.Print('status', 'Getting local lfns for sample {0}'.format(sample))

		try:
			_source_file 		= open(os.path.join(self.path_logical_file_names, sample + '.txt'),'r')
			_destination_file 	= open(os.path.join(self.path_logical_file_names, sample + '_local.txt'), 'w')
			_missing_file 		= open(os.path.join(self.path_logical_file_names, sample + '_missing.txt'), 'w') 

			_loc = self.list_of_samples_from_sources[sample]
			_path_to_be_replaced = os.path.join( self.list_of_storage_elements[_loc], self.list_of_locations[_loc])
			_path_to_be_replaced_with = self.path_output_directory

			for _f in _source_file:

				# If keyword not in file name, skip (this way we prevent copying anything but .root files)
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

		except Exception, e:
			MiscTool.Print('error', 'Missing:{0}'.format(sample))

	def save_logical_file_names_all_samples_from_config_destination(self):

		MiscTool.Print('python_info', '\nCalled save_logical_file_names_all_samples_from_config_destination function.')
		
		# Loop over all samples
		for _s in self.list_of_samples_from_config:
			
			self.save_logical_file_names_from_config_destination(_s)

	# Copy files
	def copy_files_single_sample(self, sample):

		MiscTool.Print('python_info', '\nCalled copy_files_single_sample function.')

		try:

			_missing_file 		= open(os.path.join(self.path_logical_file_names, sample + '_missing.txt'), 'r')

			_loc = self.list_of_samples_from_sources[sample]
			_path_to_be_replaced = self.path_output_directory
			_path_to_be_replaced_with = os.path.join( self.list_of_storage_elements[_loc], self.list_of_locations[_loc])
			

			for _f in _missing_file:

				# Copy only root files
				if not self.filter( _f):
					continue

				_source = _f.strip().replace(_path_to_be_replaced, _path_to_be_replaced_with)
				_destination = _f.strip().split('tree')[0]

				try:
					MiscTool.make_directory(_destination)
					self.wrapper_gfal_cp_file(_source, _destination)
				except Exception, e:
					MiscTool.Print('error', 'Problem copying {0}'.format(_source))
					raise

		except Exception, e:
			MiscTool.Print('error', 'Missing:{0}'.format(sample))

	def copy_files_all_samples_from_config(self):
		
		MiscTool.Print('python_info', '\nCalled copy_files_all_samples_from_config function.')
		
		# Loop over all samples
		for _s in self.list_of_samples_from_config:
			
			self.copy_files_single_sample(_s)

	# Check if .root files ok
	def check_root_files(self, sample):

		MiscTool.Print('python_info', '\nCalled check_root_files function.')

		try:

			_destination_file 	= open(os.path.join(self.path_logical_file_names, sample + '_local.txt'), 'r')		
			_error_file 		= open(os.path.join(self.path_logical_file_names, sample + '_error.txt'), 'w') 

			for _f in _destination_file:

				if not self.filter( _f):
					continue

				# destination path for each file
				_lfn_destination = _f.replace('\n', '')

				try:
					if TreeTool.TreeTool.check_if_tree_ok(_lfn_destination):
						pass
						# MiscTool.Print('status', 'File: {0} OK.'.format(_lfn_destination))
					else:
						MiscTool.Print('error', 'File: {0} not OK.'.format(_lfn_destination))
						_error_file.write(_lfn_destination + '\n')
				
				except Exception, e:
					MiscTool.Print('error', 'File: {0} could not be checked.'.format(_lfn_destination))
					_error_file.write(_lfn_destination + '\n')

			_error_file.close()
			_destination_file.close()		

		except Exception, e:
			MiscTool.Print('error', 'Missing:{0}'.format(sample))

	def check_root_files_all_samples_from_config(self):
		MiscTool.Print('python_info', '\nCalled check_root_files_all_samples_from_config function.')
		
		# Loop over all samples
		for _s in self.list_of_samples_from_config:
			
			self.check_root_files(_s)

	# Check if .root files missing
	def check_root_files_non_existing(self, sample):

		MiscTool.Print('python_info', '\nCalled check_root_files_non_existing function.')

		try:
			_txt_file_name = sample + '.txt'		
			_txt_file = open(os.path.join(self.path_logical_file_names, _txt_file_name), 'r')
			_txt_non_existing_file = open(os.path.join(self.path_logical_file_names, _txt_file_name.replace('.txt', '_non_existing.txt')), 'w')

			_list_of_file_numbers = {}

			# First load all numbers/files from txt_file
			for _f in _txt_file:

				if not self.filter( _f):
					continue

				_x = _f.split('tree_')

				_path 	= _x[0]
				_number = _x[1].replace('.root', '')		

				if _path not in _list_of_file_numbers:
					_list_of_file_numbers[_path] = []
					_list_of_file_numbers[_path].append(int(_number.strip()))
				else:
					_list_of_file_numbers[_path].append(int(_number.strip()))
		
			# Here goes the loop which search for any missing numbers in int sequence
			for _l in _list_of_file_numbers:

				start 	= sorted(_list_of_file_numbers[_l])[0]
				end 	= sorted(_list_of_file_numbers[_l])[-1]
				_non_existing_numbers = sorted(set(xrange(start, end + 1)).difference(_list_of_file_numbers[_l]))
				_non_existing_file = [ 'tree_{0}.root'.format(_n) for _n in _non_existing_numbers]

				# print '\n'
				# print start, end
				# print _l, sorted(_list_of_file_numbers[_l])


				if _non_existing_file:
					MiscTool.Print('error', 'Path: {0} not OK.'.format(_l))
					MiscTool.Print('error', 'Missing: {0}'.format(_non_existing_file))
				else:
					MiscTool.Print('status', 'Path: {0} OK.'.format(_l))

				# Save all to txt file
				for _f in _non_existing_file:
					_txt_non_existing_file.write(os.path.join(_l, _f) + '\n')

			_txt_file.close()
			_txt_non_existing_file.close

		except Exception, e:
			MiscTool.Print('error', 'Missing:{0}'.format(_txt_file_name))

	def check_root_files_non_existing_all_samples_from_config(self):
		MiscTool.Print('python_info', '\nCalled check_root_files_non_existing_all_samples_from_config function.')
		
		# Loop over all samples
		for _s in self.list_of_samples_from_config:
			
			self.check_root_files_non_existing(_s)

	# Remove all files for one sample
	def remove_files_single_sample(self, sample):

		MiscTool.Print('python_info', '\nCalled remove_files_single_sample function.')
		
		_missing_file 	= open(os.path.join(self.path_logical_file_names, sample + '_error.txt'), 'r') 

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

		if not any(_k in file_name for _k in self.list_of_search_keywords):
			return False
		else:
			return True
	

	# match events with files and store them ...
	def events_files_matching(self, sample):

		MiscTool.Print('python_info', '\nCalled events_files_matching function.')

		_destination_file 	= open(os.path.join(self.path_logical_file_names, sample),'r').readlines()
		_output_file_events = open(os.path.join(self.path_logical_file_names, sample.replace('.txt','_events_file_matching.txt')),'w')
		_number_of_files 	= len(_destination_file)

		for _n, _file in enumerate(_destination_file):

			MiscTool.Print('python_info', 'Opened file: {0}'.format( _file))

			_output_file_events.write(_file)

			_input = ROOT.TFile.Open(_file.rstrip(), 'read')
			_tree = _input.Get('tree')
			_number_of_entries = _tree.GetEntriesFast()

			for _i in xrange(_number_of_entries):

				_tree.GetEntry(_i)

				if not ((_tree.Vtype==2 or _tree.Vtype==3) and _tree.V_pt>100 and _tree.HCSV_reg_pt>100 and _tree.Jet_btagCSV[_tree.hJCidx[1]]>0.4):
					continue

				# print str(_tree.evt)
				_output_file_events.write(str(_tree.evt) + '\n')

			_input.Close()
			MiscTool.Print('status', 'Done: {0} %'.format( 100.0*_n/_number_of_files))

		_output_file_events.close()

		# for _e in list_of_events:
		# 	MiscTool.Print('error', 'Event {0} not found in files.'.format(_e))


			# except Exception, e:
			# 	MiscTool.Print('error', 'File: {0} not OK.'.format(_file))

	def event_list_file_matching(self, sample):

		MiscTool.Print('python_info', '\nCalled event_list_file_matching function.')

		_destination_file 	= open(os.path.join(self.path_logical_file_names, sample),'r').readlines()
		_output_file_events = open(os.path.join(self.path_logical_file_names, sample.replace('.txt','_event_list_file_matching.txt')),'w')

		_events = [
			809985932,
			960407679,
			162460091,
			107198839,
			119502597,
			1448738370,
			1469217398,
			424831594,
			156747715,
			160002037,
			1077036494,
			533784762
		] 

		_n_events = len(_events)


		for _file in _destination_file:

			MiscTool.Print('python_info', 'Opened file: {0}'.format( _file))

			_input = ROOT.TFile.Open(_file.rstrip(), 'read')
			_tree = _input.Get('tree')

			_x = []

			for _ev in _events:

				_hit = _tree.Scan("evt","evt=={0}".format(_ev))

				if _hit > 0:
					_output_file_events.write('Event:{0} File:{1}'.format( _ev, _file))
					MiscTool.Print('error', _ev + _file)
					_x.append(_ev)

			if len(_x) > 0:
				_events = list(set(_events) - set(_x))
			
			# if len(_events) == 0:
			# 	break

			_input.Close()

			MiscTool.Print('status', 'Done: {0} %'.format( (1 - 1.0*len(_events)/_n_events)*100.0))
			print _events

		_output_file_events.close()


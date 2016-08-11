import os
import subprocess as sp
import time
import utility

class CopySamples(object):
	'''
	-----------
	Description:
	Get the logical file names (EOS,PISA,...) for samples 
	which are defined in config/samples.ini and copy them 
	to the locations which are defined in config/../paths.ini.
	
	----------- 
	Input files:    samples.ini, paths.ini

	-----------
	Parameters:

	-----------
	Functions:

	get_list_of_logical_file_names()    - as the name says, it
	gets list of all LFNs for each sample using das_query and 
	save them in directory results/_step_1_logical_file_names/location/sample.txt

	copy_files() 

	-----------
	Useful commands:


	-----------
	To DO:
	Big problem with das_client.py. Slow execution.

	''' 
	def __init__(self, analysis_name, configuration, force_all):

		utility.print_nice('python_info', '\nCreated instance of CopySamples class')

		# force preselection on already existing files
		self.force_all = force_all  

		# ------ Paths -------
		self.list_of_samples    = configuration.cfg_files['samples']
		self.output_directory   = configuration.cfg_files['paths']['samples_directory']
		self.working_directory  = configuration.cfg_files['paths']['working_directory']
		self.logical_file_names = os.path.join( *[self.working_directory,'results', analysis_name, '_step_1_logical_file_names'])

		# ------ DAS options -------
		self.locations      = {'PSI':'perrozzi-VHBB_HEPPY_V21bis*', 'PISA':'arizzi-VHBB_HEPPY_V21*' }
		self.data_tier      = 'USER'
		self.dbs_instance   = 'prod/phys03'
		self.pisa_redirector= 'xrootd-cms.infn.it'
		self.psi_redirector = 't3se01.psi.ch'
		self.PEM_pass_phrase = ''


		utility.print_nice('analysis_info', 'Analysis name:', analysis_name)
		utility.print_nice('analysis_info', 'Samples will be stored in:', self.output_directory)
		utility.print_nice('analysis_info', 'Working_directory:', self.working_directory)
		utility.print_nice('analysis_info_list', 'List of samples:', self.list_of_samples.keys())

	def get_list_of_logical_file_names(self):

		utility.print_nice('python_info', '\nCalled get_list_of_logical_file_names function.')
		utility.print_nice('status', 'Collecting logical file names for all the samples.')

		# Loop over all locations
		for _location in self.locations:

			utility.print_nice('status', '\nGetting informations from {0} ...'.format(_location))

			# Loop over samples
			for _sample in self.list_of_samples:

				utility.print_nice('status', 'For sample: {0}'.format(_sample))

				# Create the output directory for particular location if it doesn't exist
				_outdir = os.path.join( self.logical_file_names, _location)
				utility.make_directory(_outdir)

				# sample txt file to store LFNs
				_outpath = os.path.join(_outdir, _sample + '.txt')
				# If txt file already exists skip
				if os.path.isfile(_outpath) and not self.force_all:
					utility.print_nice('python_info','File {0} already exists.'.format(_outpath))
					continue

				# Query DAS to find the dataset(s).
				_datasets = self.das_find_datasets(_sample, self.locations[_location], self.data_tier, self.dbs_instance)

				# Query DAS to find files for datasets
				_logical_file_names = self.das_find_files(_datasets, self.data_tier, self.dbs_instance)

				if not _logical_file_names:
					utility.print_nice('error', 'No files were found for "{}".\n'.format(_sample))
					continue

				# If the file does not exist, create it and write the LFNs.
				with open(_outpath, 'w') as _outfile:
					for _LFN in _logical_file_names:
						_outfile.write(_LFN + '\n')
				utility.print_nice('status', 'The LFNs were written to "{}".'.format(_outpath))

	def copy_files(self):

		utility.print_nice('python_info', '\nCalled copy_files function.')
		
		# Loop over all samples
		for _sample in self.list_of_samples:

			utility.print_nice('status', '\nCopying files for {0} sample.'.format(_sample))

			# Open the same files for all locations and make list of their files
			_comparison_LFNs = CopySamples.compare_files_in_same_location( _sample, self.locations, self.logical_file_names)

			# Create unique list
			_unique_LFNs = CopySamples.make_unique_list_of_files(_comparison_LFNs, self.locations)

			# _unique list is numbered list of all files for each sample
			# this way we can see if something is missing
			_unique_list = list(_unique_LFNs.keys())
			_unique_list.sort()

			# Check if any file is missing
			CopySamples.missing_files(_unique_list, _sample, self.logical_file_names )
			
			# Start copying 
			for _file in _unique_LFNs.values():

				_in         = os.path.join( self.output_directory, '/'.join(_file.split('/')[5:-1]))
				_out        = ''
				_file_name  = os.path.join( self.output_directory, '/'.join( _file.split('/')[5:]))

				utility.make_directory(_in)

				if 'perrozzi' in _file:
					_out = 'root://192.33.123.24:1094/' + _file
					
				elif 'arizzi' in _file:
					_out = 'root://xrootd-cms.infn.it:1094/' + _file

				try:

					if os.path.isfile(_file_name): 
						utility.print_nice('status', 'File already copied: ', _file_name )
					else:
						_command = ['xrdcp', _out, _in]
						sp.call(_command)
						utility.print_nice('status', 'xrdcp ' + _out + ' ' + _in )
				except: 
					utility.print_nice('error', 'Problem with copying: ', _file_name )

			# Save complete list of files
			with open( os.path.join( self.logical_file_names, _sample)  + '.txt', 'w') as _outfile:
				for _file in _unique_LFNs.values():
					_outfile.writelines(os.path.join( self.output_directory, '/'.join( _file.split('/')[5:])) + '\n')

	@staticmethod               
	def das_find_datasets(sample, location, data_tier, dbs_instance):
		utility.print_nice('python_info', 'Called das_find_datasets function.')

		_dataset_query_output = []

		_dataset_query = '--query=dataset=/{}/{}/{}'.format(sample, location, data_tier)
		if dbs_instance:
			_dataset_query += ' instance={}'.format(dbs_instance)

		try:
			# das command
			_command = ['das_client.py',
						'--key=~/.globus/userkey.pem',
						'--cert=~/.globus/usercert.pem',
						_dataset_query,
						'--limit=0']

			_proc = sp.Popen(_command, stdin=sp.PIPE, stdout=sp.PIPE)
			_dataset_query_output =	_proc.communicate()[0].splitlines()

		except sp.CalledProcessError as e:
			utility.print_nice('error', '{0}The dataset query failed for "{1}".'.format(e, sample))

		return _dataset_query_output
	
	@staticmethod   
	def das_find_files(datasets, data_tier, dbs_instance):
		utility.print_nice('python_info', 'Called das_find_files function.')

		_LFNs = []

		for _dataset in datasets:

			_file_query = '--query=file dataset={}'.format(_dataset)
			if dbs_instance:
				_file_query += ' instance={}'.format(dbs_instance)

			try:
				# das command
				_command = ['das_client.py',
							'--key=~/.globus/userkey.pem',
							'--cert=~/.globus/usercert.pem',
							_file_query,
							'--limit=0']
				_proc = sp.Popen(_command, stdin=sp.PIPE, stdout=sp.PIPE)
				_file_query_output = _proc.communicate()[0].splitlines()
			except sp.CalledProcessError as e:
				utility.print_nice('error', '{0}\nThe file query failed for "{1}".\n'.format(e, _dataset))
				continue
			else:
				_LFNs.extend(_file_query_output)

		return _LFNs

	@staticmethod
	def compare_files_in_same_location(sample, locations, location_LFN):

		_lists = {}

		# Open same files for all locations
		for _location in locations:

			_outdir = os.path.join( location_LFN, _location)
			try:
				with open( os.path.join( _outdir, sample + '.txt'), 'r') as _outfile:
					_lists[ _location + '_old'] = [_line.strip() for _line in _outfile.readlines() if not ('passAll' in _line or 'ext1' in _line)]
			except:
				_lists[_location + '_old'] = [] 
				utility.print_nice('error', 'No file {0} in {1}.'.format(sample, _location))
		return _lists

	@staticmethod
	def make_unique_list_of_files(comparison_list, locations):

		_unique_LFNs = {}

		for _location in locations:
			for _LFN in comparison_list[_location + '_old']:
			
				_x = int(_LFN.split('/')[-1][5:-5])

				if _x not in _unique_LFNs:
					_unique_LFNs[_x] =  _LFN

		return _unique_LFNs

	@staticmethod
	def missing_files(unique_list, sample, location ):
		
		_missing_files = []

		for i in xrange(1,len(unique_list)+1):

			if i not in unique_list:
				_missing_files.append(sample + '_' + str(i))

		# Save missing files
		# print location + '/' + sample + '_missing_files.txt'
		with open( os.path.join( location + '/' + sample + '_missing_files.txt'), 'aw') as _outfile:
			_outfile.writelines('\n'.join(_missing_files))

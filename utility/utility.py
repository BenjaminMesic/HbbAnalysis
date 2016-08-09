import os
import sys
import json
import hashlib
import subprocess as sp

import ROOT

class ConfigurationFiles(object):
	'''
	-----------
	Description:
	Loads all configuration file and stores them into single dictionary
	called self.cfg_files.

	-----------	
	Input files:
	Configuration files from directory config/analysis_name

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

		print '\n','-'*50, '\nCreated instance of ConfigurationFiles class\n', '-'*50	

		self.analysis_name = analysis_name
		self.cfg_files = {}

		self.get_configuration_files()

		print '-'*50

	def get_configuration_files(self):
		
		_configuration_files_path = os.path.join('../config', self.analysis_name)

		print '{0:30s}{1}'.format('Configuration files from ', self.analysis_name)

		_files = sp.check_output('ls ' + _configuration_files_path, shell=True).split()

		for _config in _files:
			print '{0:30s}{1}'.format('', _config)
			try:
				self.cfg_files[_config.split('.')[0]] = json.load(open(os.path.join( _configuration_files_path, _config)))
			except Exception, e:
				print '\nProblem with loading: {0} !!\n'.format(_config)
				raise


def analysis_name():
	_analysis_name = ''
	if len(sys.argv) == 1:
		_analysis_name = 'Wlv'
		print 'Missing analysis_name argument, using default:', _analysis_name
	else:
		_analysis_name = sys.argv[1]

	return _analysis_name

def das_find_datasets(sample, location, data_tier, dbs_instance):
	'''Query DAS to find the dataset(s).'''

	_dataset_query_output = []

	_dataset_query = '--query="dataset=/{}/{}/{}'.format(sample, location, data_tier)
	if dbs_instance:
		_dataset_query += ' instance={}"'.format(dbs_instance)

	try:
		# das command
		_command = ' '.join(['das_client.py', _dataset_query, '--limit', '0'])
		_dataset_query_output = sp.check_output( _command, shell=True)
		_dataset_query_output = _dataset_query_output.splitlines()

	except sp.CalledProcessError as e:
		print '{0}\nThe dataset query failed for "{1}".\n'.format(e, sample)
		
	return _dataset_query_output
	
def das_find_files(datasets, data_tier, dbs_instance):
	''' Query DAS to find each dataset's files and return their logical file names (LFNs). '''

	_LFNs = []

	for _dataset in datasets:

		_file_query = '--query="file dataset={}'.format(_dataset)
		if dbs_instance:
			_file_query += ' instance={}"'.format(dbs_instance)

		try:
			_command = ' '.join(['das_client.py', _file_query, '--limit', '0'])
			_file_query_output = sp.check_output( _command, shell=True)
		except sp.CalledProcessError as e:
			print '{0}\nThe file query failed for "{1}".\n'.format(e, _dataset)
			continue
		else:
			_LFNs.extend(_file_query_output.splitlines())

	return _LFNs

def make_directory(directory):

	if not os.path.exists(directory):

		try:
			os.makedirs(directory)
		except OSError:
			if not os.path.isdir(directory):
				raise

def trim_trees(cut, subsamples_cut, samples_list, location_of_samples, forceReDo = False):
	''' Creates cached trees with cut and returns their dictionary'''
	print '\n','-'*10,'\nCalled trim_trees function.'

	_samples_dict = {} 

	for _id in samples_list:

		_unique_name = hashlib.md5(cut).hexdigest()
		_source = os.path.join(location_of_samples, samples_list[_id] + '.root')
		_tmp_name = _id + '_' + _unique_name + '.root'
		_tmp_directory = os.path.join(location_of_samples, 'cache')
		_tmp = os.path.join(_tmp_directory, _tmp_name)

		make_directory(_tmp_directory)

		print '\nSample: ', samples_list[_id]
		print '{0:30s}{1}'.format( 'Cut' , cut)
		print '{0:30s}{1}'.format( 'Source' , _source)
		print '{0:30s}{1}'.format( 'Tmp_file' , _tmp_name)

		_tmp_status_ok = file_exists(_tmp)

		# If file doesn't exists or it is corrupted
		if (not _tmp_status_ok) or forceReDo:
			# Creating cached file (tmp file)
			try:
				if forceReDo:
					_output = ROOT.TFile.Open(_tmp,'recreate')
				else:
					_output = ROOT.TFile.Open(_tmp,'create')
				_output.cd()
			except:
				print 'Problem with creating _tmp. Delete root file and try again.'

			# Load source file
			_input = ROOT.TFile.Open( _source,'read')
			_tree = _input.Get('tree')
			assert type(_tree) is ROOT.TTree

			# ------ Here starts actual skimming -------
			_input.cd()
			_obj = ROOT.TObject
			for key in ROOT.gDirectory.GetListOfKeys():
				_input.cd()
				_obj = key.ReadObj()
				if _obj.GetName() == 'tree':
					continue
				_output.cd()
				_obj.Write(key.GetName())
			_output.cd()

			# ------ Sub samples cut -------
			if any(x in subsamples_cut for x in _id.split('_')):
				_subsample_cut = '&&' + subsamples_cut[_id.split('_')[1]]
			else:
				_subsample_cut = ''

			_cut = ''.join([cut, _subsample_cut])

			#Problem here: not working when empty tree
			_cuttedTree = _tree.CopyTree(_cut)
			_cuttedTree.Write()
			_output.Write()
			_input.Close()
			del _input
			_output.Close()
			del _output

		else:
			print('File exists and it is ok.')

		_samples_dict[_id] = _tmp

	return _samples_dict

def file_exists(file_name):
		''' 
		Check if file exists and if it's ok. If yes return True, else False
		'''

		_status = ''

		if os.path.isfile(file_name):

			f = ROOT.TFile.Open(file_name,'read')

			if not f or f.GetNkeys() == 0 or f.TestBit(ROOT.TFile.kRecovered) or f.IsZombie():
					
				_status = False

			else:
				_status = True

			f.Close()

		else:
			_status = False

		return _status

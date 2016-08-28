import os
import sys
import json
import hashlib
import subprocess as sp
import stat

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

		print_nice('python_info', '\nCreated instance of ConfigurationFiles class')	

		self.analysis_name = analysis_name
		self.cfg_files = {}

		self.get_configuration_files()

	def get_configuration_files(self):
		
		_configuration_files_path = os.path.join('../config', self.analysis_name)

		print_nice('analysis_info', 'Configuration files from ', self.analysis_name)	

		_files = sp.check_output(['ls', _configuration_files_path]).split()

		for _config in _files:
			print_nice('analysis_info', '', _config)
			try:
				self.cfg_files[_config.split('.')[0]] = json.load(open(os.path.join( _configuration_files_path, _config)))
			except Exception, e:
				print_nice('error', 'Problem with loading: ' + _config)
				raise

class BatchSender(object):
	'''
	-----------
	Description:
	Load existing batcth templates, adjust and saves them, send job

	-----------	
	Input files:


	-----------
	Parameters:


	-----------
	Functions:

	-----------
	Useful commands:


	-----------
	To DO:

	'''	
	def __init__(self, arguments):

		self.arguments 				= arguments
		self.template_txt 			= [
			'executable  =  <script_name>.sh',
			'universe    =  vanilla',
			'log         =  <script_name>.log',
			'initialdir  =  <initial_directory>',
			'error       =  <script_name>.error',
			'getenv      =  True',
			'queue'
		]

		self.template_sh			= [
			'#!/bin/bash',
			'cd <initial_directory>',
			'python <script_name>.py'
		]


		# make batch directory
		make_directory(self.arguments['<initial_directory>'])


	def make_scripts(self):

		# make scripts

		_scripts = {
			'.sh' : '\n'.join(self.template_sh),
			'.txt': '\n'.join(self.template_txt)
		}


		with open(self.arguments['python_template']) as f:
			_scripts['.py'] = f.read()
		del self.arguments['python_template']

		# make loop through all arguments and change all scripts
		for _arg, value in self.arguments.iteritems():

			for _script in _scripts:

				_scripts[_script] = _scripts[_script].replace(_arg, value)

		# Save files
		for _script in _scripts:

			_f = open( os.path.join(self.arguments['<initial_directory>'], self.arguments['<script_name>'] + _script),'w')
			_f.write(_scripts[_script])
			_f.close()

	def send_job(self):

		# if _i > 5:
		# 	continue
		# if i%100 == 0 and i!=0:
		# 	time.sleep(40)

		# Change permission so that it can be executed 
		_sh = os.path.join(self.arguments['<initial_directory>'], self.arguments['<script_name>'] + '.sh')
		os.chmod(_sh, os.stat(_sh).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
		
		print_nice('status', _sh)

		_working_dir = os.getcwd()
		os.chdir( self.arguments['<initial_directory>'] )
		# print sp.check_output('pwd', shell=True)
		sp.call('condor_submit ' + self.arguments['<script_name>'] + '.txt', shell=True)			
		os.chdir(_working_dir)
		

def print_nice(print_type, *text):
 
	try:

		if print_type == 'python_info': # Bright Yellow
			print '\033[1;33;40m' + ''.join(text) + '\033[0m'

		elif print_type == 'analysis_info': # Bright Cyan
			print '\033[1;36;40m{0:30s}{1}\033[0m'.format(*text)

		elif print_type == 'analysis_info_list': # Bright Cyan
			print '\033[1;36;40m' + text[0] + '\033[0m'
			for _l in text[1]:
				print '\033[1;36;40m{0:30s}{1}\033[0m'.format('' , _l)

		elif print_type == 'error':  # Bright Red
			print '\033[1;31;40m' + ''.join(text) + '\033[0m'

		elif print_type == 'status': # Bright Green
			print '\033[1;32;40m' + ''.join(text) + '\033[0m'	


	except Exception, e:
		print text

	# ----- Example ------
	# print "\033[1;32;40m Bright Green  \033[0m \n"
	# \033[  Escape code, this is always the same
	# 1 = Style, 1 for normal.
	# 32 = Text colour, 32 for bright green.
	# 40m = Background colour, 40 is for black.

	# print("\033[0;37;40m Normal text\n")
	# print("\033[2;37;40m Underlined text\033[0;37;40m \n")
	# print("\033[1;37;40m Bright Colour\033[0;37;40m \n")
	# print("\033[3;37;40m Negative Colour\033[0;37;40m \n")
	# print("\033[5;37;40m Negative Colour\033[0;37;40m\n")
	 
	# print("\033[1;37;40m \033[2;37:40m TextColour BlackBackground          TextColour GreyBackground                WhiteText ColouredBackground\033[0;37;40m\n")
	# print("\033[1;30;40m Dark Gray      \033[0m 1;30;40m            \033[0;30;47m Black      \033[0m 0;30;47m               \033[0;37;41m Black      \033[0m 0;37;41m")
	# print("\033[1;31;40m Bright Red     \033[0m 1;31;40m            \033[0;31;47m Red        \033[0m 0;31;47m               \033[0;37;42m Black      \033[0m 0;37;42m")
	# print("\033[1;32;40m Bright Green   \033[0m 1;32;40m            \033[0;32;47m Green      \033[0m 0;32;47m               \033[0;37;43m Black      \033[0m 0;37;43m")
	# print("\033[1;33;40m Yellow         \033[0m 1;33;40m            \033[0;33;47m Brown      \033[0m 0;33;47m               \033[0;37;44m Black      \033[0m 0;37;44m")
	# print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m            \033[0;34;47m Blue       \033[0m 0;34;47m               \033[0;37;45m Black      \033[0m 0;37;45m")
	# print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m            \033[0;35;47m Magenta    \033[0m 0;35;47m               \033[0;37;46m Black      \033[0m 0;37;46m")
	# print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m            \033[0;36;47m Cyan       \033[0m 0;36;47m               \033[0;37;47m Black      \033[0m 0;37;47m")
	# print("\033[1;37;40m White          \033[0m 1;37;40m            \033[0;37;40m Light Grey \033[0m 0;37;40m               \033[0;37;48m Black      \033[0m 0;37;48m")
	
def analysis_name():
	_analysis_name = ''
	if len(sys.argv) == 1:
		_analysis_name = 'Wlv'
		print_nice('analysis_info','Missing analysis_name argument, using default: ', _analysis_name)
	else:
		_analysis_name = sys.argv[1]

	return _analysis_name

def make_directory(directory):

	if not os.path.exists(directory):

		try:
			os.makedirs(directory)
		except OSError:
			if not os.path.isdir(directory):
				raise

def trim_trees(cut, subsamples_cut, samples_list, location_of_samples, forceReDo = False):
	''' Creates cached trees with cut and returns their dictionary'''

	print_nice('python_info', '\nCalled trim_trees function.')

	_samples_dict = {} 

	for _id in samples_list:

		_unique_name = hashlib.md5(cut).hexdigest()
		_source = os.path.join(location_of_samples, samples_list[_id] + '.root')
		_tmp_name = _id + '_' + _unique_name + '.root'
		_tmp_directory = os.path.join(location_of_samples, 'cache')
		_tmp = os.path.join(_tmp_directory, _tmp_name)

		make_directory(_tmp_directory)

		print_nice('status', '\nSample: ' + samples_list[_id])
		print_nice('analysis_info', 'Cut:', cut)
		print_nice('analysis_info', 'Source:', _source)
		print_nice('analysis_info', 'Tmp_file:', _tmp_name)

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
				print_nice('error', 'Problem with creating _tmp. Delete root file and try again.')

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
			print_nice('status', 'File done.')

		else:
			print_nice('python_info', 'File exists and it is ok.')

		_samples_dict[_id] = _tmp

	return _samples_dict

def file_exists(file_name):
		''' 
		Check if file exists and if it's ok. If yes return True, else False
		'''

		_status = ''

		if os.path.isfile(file_name):

			f = ROOT.TFile.Open(file_name,'read')

			if (not f) or f.GetNkeys() == 0 or f.TestBit(ROOT.TFile.kRecovered) or f.IsZombie():
					
				_status = False

			else:
				_status = True

			f.Close()

		else:
			_status = False

		return _status


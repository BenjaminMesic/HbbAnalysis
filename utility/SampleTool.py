import os

import ROOT

from utility import MiscTool
from utility import TreeTool

class SampleTool(object):

	def __init__(self, task, configuration, split_samples = False):

		MiscTool.Print('python_info', '\nCreated instance of SampleTool class')

		self.task 				= task
		self.configuration 		= configuration
		self.split_samples		= split_samples

		# ------ Paths -------
		self.path_working_directory = os.environ['Hbb_WORKING_DIRECTORY']
		self.list_of_all_samples= self.configuration['samples']['list']
		self.list_of_samples 	= self.configuration['samples']['task'][self.task]
		self.path_samples 		= self.configuration['paths']['path_samples_preselection']

		# Load VHbbNameSpace.h
		ROOT.gROOT.ProcessLine('.L {0}/utility/VHbbNameSpace.h'.format(self.path_working_directory))
		# print ROOT.VHbb.deltaPhi(1,2)

		self.samples 			= {}

		# First you need to initalize samples
		self.initialize_samples()
		# Second, initialize cuts for samples which were just initialized
		self.set_samples_cuts()
		# Third get/set_sample_files using cuts from above
		self.set_samples_files()
		# TBE
		self.set_samples_number_of_entries()
		# TBE
		self.set_samples_normalization_factor()

	def initialize_samples(self):

		MiscTool.Print('python_info', '\nCalled initialize_samples function.')

		# -----------------------------------------
		# Load all samples
		# -----------------------------------------
		if self.list_of_samples[0] == 'all': 

			# Load all samples with subsamples splitting
			if self.split_samples:

				for _s in self.list_of_all_samples:

					_sample_config = self.list_of_all_samples[_s]
				
					if 'sub' in _sample_config:
						for _sub in _sample_config['sub']:
							self.samples[_sub] = Sample( _s, _sub, _sample_config['types'], _sample_config['xsec'])

					else:
						_id = _sample_config['ID']
						self.samples[_id] = Sample( _s, _id, _sample_config['types'], _sample_config['xsec'])
			

			# Load all samples without splitting
			else:
				for _s in self.list_of_all_samples:
					_sample_config = self.list_of_all_samples[_s]
					_id = _sample_config['ID']
					self.samples[_id] = Sample( _s, _id, _sample_config['types'], _sample_config['xsec'])

		# -----------------------------------------
		# Load samples which are explicitly written
		# -----------------------------------------
		else:

			# Loop over list of ID samples
			for _id in self.list_of_samples:

				_id_match = False

				# Loop over list of all samples and check if ID sample match with any of IDs
				for _s in self.list_of_all_samples:

					_sample_config = self.list_of_all_samples[_s] 

					# Try to find ID match
					if not _id_match:

						# Check if ID has match in sample ID
						if _id == _sample_config['ID']:
							_id_match = True

						# Check if maybe has match in subsample ID
						elif 'sub' in _sample_config:

							if _id in _sample_config['sub']:
								_id_match = True

					# If match found
					if _id_match:

						# ---- Load sample with subsample splitting ------
						if self.split_samples:

							# First check if sample has subsamles
							if 'sub' in _sample_config:

								# Check if this ID is already subsample ID
								if _id in _sample_config['sub']:
									self.samples[_id] = Sample( _s, _id, _sample_config['types'], _sample_config['xsec'])

								# If not, add all subsamples
								else:
									for _sub in _sample_config['sub']:
										self.samples[_sub] = Sample( _s, _sub, _sample_config['types'], _sample_config['xsec'])

							# If there is no subsample structure just add sample
							else:
								self.samples[_id] = Sample( _s, _id, _sample_config['types'], _sample_config['xsec'])

						# ----- Load sample without splitting ------
						else:
							self.samples[_id] = Sample( _s, _id, _sample_config['types'], _sample_config['xsec'])

						break						

				# If ID not found at all
				if not _id_match:
					MiscTool.Print('error', 'ID: {0} is not defined.'.format(_id))

	def set_samples_cuts(self):
		'''Set samples cuts and IDs.'''

		_default_cut 	= self.configuration['cuts']['blinding_cut']
		_subsamples_cut = self.configuration['cuts']['subsamples_cut'] 
		_task_cut 		= self.configuration['cuts'][self.task] 

		for _s in self.samples:

			# ----- Add task cut -----
			if isinstance(_task_cut, dict):

				for _tc in _task_cut:
					_id = '___'.join([_s, _tc])
					self.samples[_s].files[_id] = {'ID': _id, 'cut': _task_cut[_tc]}

			elif isinstance(_task_cut, str):
				self.samples[_s].files[_s] = {'ID': _s, 'cut': _task_cut}

			# ----- Add default cut ------
			for _id in self.samples[_s].files:
				self.samples[_s].files[_id]['cut'] += ' && ' + _default_cut

			# ----- Add subsample cut -----
			_id_subsample = _s.split('_')
			# First check if _s is subsample
			if len(_id_subsample) != 1:
			
				if _id_subsample[1] in _subsamples_cut:
					for _id in self.samples[_s].files:
						self.samples[_s].files[_id]['cut'] += ' && ' + _subsamples_cut[_id_subsample[1]]
				else:
					MiscTool.Print('error', 'Missing "{0}" subsamples cut definition'.format(_id_subsample[1]))
		
	def set_samples_files(self):

		MiscTool.Print('python_info', '\nCalled set_samples_files function.')

		for _s in self.samples:

			# Set parent file (input) for this sample
			self.samples[_s].file_parent = os.path.join(self.path_samples, self.samples[_s].name + '.root')

			for _id in self.samples[_s].files:

				_cut 	= self.samples[_s].files[_id]['cut']
				_ID 	= self.samples[_s].files[_id]['ID']

				# Set samples i.e. root files for study
				self.samples[_s].files[_id]['tree'] = TreeTool.TreeTool.trim_tree( _cut, self.samples[_s].file_parent, _ID, self.configuration['paths']['path_cache'])

	# This part is designed for PlotTool which works with only one cut defined in cuts.py
	def set_samples_number_of_entries(self):

		MiscTool.Print('python_info', '\nCalled set_samples_number_of_entries function.')

		for _s in self.samples:
					
			try:		
				
				# Get total number of entries for this sample
				_file 	= ROOT.TFile.Open( self.samples[_s].file_parent,'read')
				self.samples[_s].number_of_all_entries = _file.Get('CountFullWeighted').GetBinContent(1)					
				_file.Close()
			
			except Exception, e:
				MiscTool.Print('error', 'Problem with loading: ' + _f)
				raise

	def set_samples_normalization_factor(self):

		MiscTool.Print('python_info', '\nCalled set_samples_normalization_factor function.')

		_luminosity	= self.configuration['general']['luminosity']

		for _s in self.samples:

			if self.samples[_s].types == 'mc':
				_x_sec	= self.samples[_s].xsec
				self.samples[_s].normalization_factor  = str(_luminosity*_x_sec/self.samples[_s].number_of_all_entries)
			else:
				self.samples[_s].normalization_factor  = str(1.0)

			MiscTool.Print('analysis_info', _s + ' normalization:', self.samples[_s].normalization_factor )


class Sample(object):
	''' Class which contains all info about particular sample '''

	def __init__(self, name, ID, types, xsec):

		self.name 				= name
		self.ID 				= ID
		self.types 				= types
		self.xsec 				= xsec

		self.file_parent 			= None		
		self.files					= {}	# 'ID': '', 'cut':'', 'tree':''
		self.number_of_all_entries  = None
		self.normalization_factor 	= None

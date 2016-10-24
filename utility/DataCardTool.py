import os

import ROOT

from utility import MiscTool

ROOT.gROOT.SetBatch(True)

class DataCardTool(object):
	'''

	'''	
	
	def __init__(self, task, analysis_name, configuration, sample_tool):

		MiscTool.Print('python_info', '\nCreated instance of DataCardTool class')

		# ------ Paths -------
		self.path_working_directory = os.environ['Hbb_WORKING_DIRECTORY']
		self.path_results 			= os.path.join( self.path_working_directory, 'results', analysis_name, 'datacards')
		MiscTool.make_directory(self.path_results)

		# ------ Samples -------
		self.sample_tool 	= sample_tool

		# ------ Weights -------
		self.weights 		= configuration['weights']

		# ------ Datacard Config -------
	
		self.channels 	= configuration['datacards']['channels']
		self.bins 		= configuration['datacards']['bins']
		self.nuisance_parameters = configuration['datacards']['nuisance_parameters']
		
		self.process 	= configuration['datacards']['process']
		self.definitions= configuration['datacards']['definitions']

		self.yields		= {}

	def make_all(self):

		MiscTool.Print('python_info', '\nCreating datacards.')
		
		# Loop over all channels
		for _c in self.channels:

			# Loop over all bins for which we are going to make datacard
			for _b in self.bins:

				# ---------- Datacards --------------

				# prepare nuisance string
				_nuisance = ''
				for _n in self.nuisance_parameters:
					_nuisance += self._print_aligned().format( _n, '', self.nuisance_parameters[_n]['model'], *[str(self.nuisance_parameters[_n]['process'][_p[0]]) for _p in self.process] ) + '\n'

				# Strings which will replace template datacard strings
				_replacing_strings = {

					'<jmax>' 	: len(self.process) - 1,
					'<bin>'		: _b,
					'<kmax>' 	: len(self.nuisance_parameters),

					'<bin_entry>' 	: self._print_aligned().format( 'bin', '', '',str(_b), *['']*(len(self.process)-3)),					
					'<observation_entry>' 	: self._print_aligned().format( 'observation', '', '', str(self.yields[_c + '___' + _b]), *['']*(len(self.process)-3)),

					'<bin_process>' : self._print_aligned().format('bin', '', '', *[_b]*len(self.process)),
					'<process>'		: self._print_aligned().format('process', '', '', *[_p[0] for _p in self.process]),
					'<process_num>'	: self._print_aligned().format('process', '', '', *[_p[1] for _p in self.process]),
					'<rate>'		: self._print_aligned().format('rate', '', '', *[ str( round( self.yields[ '___'.join([ _p[0], _b])], 2)) for _p in self.process]),
					'<nuisance>' 	: _nuisance

					}

				# Creating and saving datacard
				with open(os.path.join(self.path_working_directory, 'utility', 'templates', 'datacard.txt'), 'r') as f:
					_datacard = f.read()

				for _s, _r in _replacing_strings.iteritems():
					_datacard = _datacard.replace( _s, str(_r))

				_f = open( os.path.join( self.path_results, '_'.join([ 'vhbb', _c, _b]) + '.txt'),'w')
				_f.write(_datacard)
				_f.close()


				# ---------- Histograms --------------
				
				# Create root file, always recreate
				_f = ROOT.TFile.Open(os.path.join( self.path_results, '_'.join([ 'hists', _c, _b]) + '.root'),'recreate')

				# TBD
				# # Loop over nuisance parameters, if shape fill
				# for _n in self.nuisance_parameters:

				_f.Close()

	def _print_aligned(self):
		_string = '{0:20s}'

		for _i in xrange(1, len(self.process)+1):
			_string += '{' + str(_i) + ':12s}'	

		return _string

	def _set_observations_and_rates(self):

		# Loop over all samples
		for _s in self.sample_tool.samples:

			for _f in self.sample_tool.samples[_s].files:

				_input = ROOT.TFile.Open( self.sample_tool.samples[_s].files[_f]['tree'],'read')
				_tree = _input.Get('tree')
				_histogram = ROOT.TH1F( 'integral', 'integral', 1, -1, 1000000)

	 			# Weights and scale factor part
				_weight = '1'
				if self.sample_tool.samples[_s].types == 'mc':
					_weight = '*'.join(self.weights.values()) + '*' + self.sample_tool.samples[_s].normalization_factor

				# Get histogram from the tree directly
				_tree.Draw('{0}>>{1}'.format( 'rho', 'integral'), _weight)

				# Get histogram integral
				_ID, _bin = _f.split('___')
				self.yields[self.definitions[_ID] + '___' + _bin] = _histogram.Integral()

				# Check if every process has its yields
				for _p in self.process:

					_id = _p[0] + '___' + _bin

					if _id not in self.yields:
						self.yields[ _id ] = -1


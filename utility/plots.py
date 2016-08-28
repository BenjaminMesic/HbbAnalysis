import os

import ROOT

import utility
import tdrStyle

ROOT.gROOT.SetBatch(True)

class Plot(object):
	'''
	-----------
	Description:


	-----------	
	Input files:
	Output files:  	

	-----------
	Parameters:
	self.plot_cut 		: should have the same name as the plot defined in plots.ini
	self.blinding_cut


	-----------
	Functions:
	get_trees 				: calls trim_trees function which returns dictionary
							as sample:name of the file and saves it in self.cache_trees.
	set_and_save_histograms : from self.cache_trees takes samples and create histograms
							with variables of our interest. Saves it in .root file in 
							self.plot_directory as self.plot_name.root.
	get_histograms 			:
	set_pads 				: name says it all
	set_legend 				:

	-----------
	Useful commands:

	# test_h = ROOT.TH1F('test_h', 'test_h', 100, 0, 10)
	# test_h.Fill(1,1000)
	# test_h.SetLineColor(632)
	# test_s = ROOT.THStack('test_s', 'test_s')
	# test_s.Add(test_h)

	-----------
	To DO:
	- add possibility to add info from extra, e.g. sample scale factor 
	- last bin (overflow)

	- log scale
	- y axis
	- error in ratio plot, Kolmogorov
	-stack_histograms function update variable argument
	'''	
	
	def __init__(self, analysis_name, plot_name, configuration, subsamples = False):

		utility.print_nice('python_info', '\nCreated instance of Plot class')

		# Load plot style, defined in tdrStyle.py
		tdrStyle.tdrStyle()

		# Load VHbbNameSpace.h
		ROOT.gROOT.ProcessLine(".L ../utility/VHbbNameSpace.h")
		# print ROOT.VHbb.deltaPhi(1,2)

		# ------ Paths -------
		self.working_directory 	= configuration.cfg_files['paths']['working_directory']
		self.plot_directory 	= os.path.join(self.working_directory, 'plots', analysis_name)
		try:
			self.samples_directory = configuration.cfg_files['paths']['preselection_directory']
		except Exception, e:
			self.samples_directory = configuration.cfg_files['paths']['samples_directory'] + '_preselection'

		# ------ Plot config -------
		self.plot_name 			= plot_name
		self.plot_options 		= configuration.cfg_files['plots'][self.plot_name]
		self.plot_definitions 	= configuration.cfg_files['plots']['definitions']
		self.general_options 	= configuration.cfg_files['general']

		# ------ Plot features -----
		self.cache_trees 				= {}
		self.histograms 				= {}
		self.stack_histograms 			= {}
		self.variables 					= {}
		self.pads 						= {}
		self.legends 					= {}
		self.legends_entries 			= {}
		self.error_graph 				= {}
		self.labels 					= {}
		self.ratio_histograms 			= {}
		self.ratio_horizontal_line 		= {}
		self.canvas 					= {}

		# ------ Cuts -------
		self.subsamples_cut 	= configuration.cfg_files['cuts']['subsamples_cut']
		self.blinding_cut 		= configuration.cfg_files['cuts']['blinding_cut']
		self.plot_cut 			= configuration.cfg_files['cuts'][self.plot_name]		
		self.final_cut 			= '&&'.join([self.blinding_cut, self.plot_cut])

		# ------ Samples -------
		# self.samples_in_dir 	= [x.split('.')[0] for x in os.listdir(self.samples_directory) if 'root' in x]
		self.samples_all 		= configuration.cfg_files['samples']
		self.subsamples 		= subsamples
		self.samples_plot 		= self.get_samples_for_plot()

		# ------ Weights, scaling -------
		self.weights 					= configuration.cfg_files['weights']
		self.samples_scale_factors 	= {}
		self.samples_number_of_entries = {}

		utility.print_nice('analysis_info', 'Working directory:', self.working_directory)
		utility.print_nice('analysis_info', 'Location of samples:', self.samples_directory)
		utility.print_nice('analysis_info', '\nBlinding cut:', self.blinding_cut)
		utility.print_nice('analysis_info', 'Plot cut:', self.plot_cut)
		utility.print_nice('analysis_info_list', 'Plot options:', self.plot_options.values())
		utility.print_nice('analysis_info_list', 'List of samples:', self.samples_plot.keys())

	def get_samples_for_plot(self):

		utility.print_nice('python_info', '\nCalled get_samples_for_plot function.')
		
		_samples = {}
		# if true include all samples in config file
		_include_all_samples = bool(self.plot_options['samples'][0] == 'all')
		# if self.subsamples set True split samples on subsamples
		_include_subsamples = self.subsamples

		# Check if samples should be split
		if _include_subsamples:

			if _include_all_samples:
				
				for _s in self.samples_all:

					# If sample has subsamples, add its ids
					if 'sub' in self.samples_all[_s]:
						for _id in self.samples_all[_s]['sub']:
							_samples[_id] = _s		

					# If sample doesn't have subsamples, add samples id
					else:
						_samples[self.samples_all[_s]['id']] = _s

			# Include only ids which are explicitly written in config file
			# possible to add subsample as well
			else:
				for _s in self.samples_all:

					for _id in self.plot_options['samples']:

						# If sample has subsamples, look for id
						if 'sub' in self.samples_all[_s]:

							if _id in self.samples_all[_s]['sub']:
								_samples[_id] = _s

							elif _id in self.samples_all[_s]:
								for _id_sub in self.samples_all[_s]['sub']:
									_samples[_id_sub] = _s	

						# If sample doesn't have subsamples
						elif _id == self.samples_all[_s]['id']:
							_samples[self.samples_all[_s]['id']] = _s

		else:
			# Check if maybe all samples should be included
			if _include_all_samples:
				_samples = {self.samples_all[_s]['id']: _s for _s in self.samples_all}

			# Include only samples which are explicitly written in plot config file
			# possible to add subsample as well
			else:
				for _id in self.plot_options['samples']:

					for _s in self.samples_all:

						# If sample doesn't have subsamples
						if _id == self.samples_all[_s]['id']:
							_samples[self.samples_all[_s]['id']] = _s

						# If sample has subsamples, look for id
						elif 'sub' in self.samples_all[_s]:
							if _id in self.samples_all[_s]['sub']:
								_samples[_id] = _s

		return _samples

	def get_trees(self):

		# Make trees with all cuts applied, if doesnt exist create them and store in cache dir
		self.cache_trees = utility.trim_trees( self.final_cut, self.subsamples_cut, self.samples_plot, self.samples_directory)

	def get_samples_number_of_entries(self):

		utility.print_nice('python_info', '\nCalled get_samples_number_of_entries function.')

		for _id,_f in self.cache_trees.iteritems():
					
			try:
				_file 	= ROOT.TFile.Open( _f,'read')
				self.samples_number_of_entries[_id] = _file.Get('Count').GetEntries()
				utility.print_nice('analysis_info', _id + ' number of entries', _file.Get('Count').GetEntries())
				_file.Close()
			except Exception, e:
				utility.print_nice('error', 'Problem with loading: ' + _f)
				raise

	def get_samples_scale_factors(self):

		utility.print_nice('python_info', '\nCalled get_samples_scale_factors function.')

		_luminosity	= self.general_options['luminosity']

		for _id,_s in self.samples_plot.iteritems():

			if self.samples_all[_s]['types'] == 'mc':
				_x_sec	= self.samples_all[_s]['xsec'] 
				self.samples_scale_factors[_s]= str(_luminosity*_x_sec/self.samples_number_of_entries[_id])
			else:
				self.samples_scale_factors[_s] = str(1.0)

			utility.print_nice('analysis_info', _id + ' scale factor:', self.samples_scale_factors[_s])

	def set_and_save_histograms(self):

		utility.print_nice('python_info', '\nCalled set_and_save_histograms function.')

		# Histograms will be saved in new root file
		_output_name = os.path.join(self.plot_directory, self.plot_name + '.root')
		_output = ROOT.TFile.Open( _output_name,'recreate')
		_output.Close()

		# Loop over all samples
		for _id, _f in self.cache_trees.iteritems():

			# Loop over all variables for each sample
			for _var in self.plot_options['variables'].keys():

				_name =  _var + '-' + _id

				# Histogram plot options
				_nbin 	= self.plot_options['variables'][_var]['n_bin']
				_x_min 	= self.plot_options['variables'][_var]['x_min']
				_x_max 	= self.plot_options['variables'][_var]['x_max']

				# Check if sample is data or mc
				_sample_name = self.samples_plot[_id]
				_sample_type = self.samples_all[_sample_name]['types']

				# Weights part
				if _sample_type == 'data':
					_weight = '1'
				else:
					_weight = '*'.join(self.weights.values())

				# Scale factors part
				if _sample_type == 'mc':
					_weight = _weight + '*' + self.samples_scale_factors[_sample_name]

				# ---- Explanation of weight as Draw parameter ----
				# Selection = "weight *(boolean expression)"
				# If the Boolean expression evaluates to true,
				# the histogram is filled with a weight.
				# If the weight is not explicitly specified it is assumed to be 1.
					
				# Get histogram from sample
				_input = ROOT.TFile.Open( _f,'read')
				_tree = _input.Get('tree')
				_histogram = ROOT.TH1D( _name, _name, _nbin, _x_min, _x_max)
				_tree.Draw('{0}>>{1}'.format( _var, _name), _weight)

				if _sample_type == 'data':
					_histogram.SetMarkerStyle(20)
					_histogram.SetMarkerColor(self.plot_definitions['colors'][_id])
				else:
					_histogram.SetFillColor(self.plot_definitions['colors'][_id])
					_histogram.SetLineColor(self.plot_definitions['colors'][_id])


				# c = ROOT.TCanvas('c', 'c', 800, 800)
				# _histogram.Draw('p')
				# _histogram.SetTitle(_name)
				# c.SaveAs(_name + '_.pdf')

				# Save histograms to new root file
				_output = ROOT.TFile.Open( _output_name, 'update')
				_histogram.Write()
				_output.Close()

				_input.Close()

	def get_histograms(self):

		utility.print_nice('python_info', '\nCalled get_histograms function.')

		# Get all histograms from _input_name and store them in dictionary		
		try:
			_input 	= os.path.join(self.plot_directory, self.plot_name + '.root')
			_file 	= ROOT.TFile.Open( _input,'read')

		except Exception, e:
			utility.print_nice('error', 'Problem with loading: ' + file_name)
			raise

		_dirlist = _file.GetListOfKeys()
		iter = _dirlist.MakeIterator()
		_key = iter.Next()

		while _key:
			self.histograms[_key.GetName()] = _file.Get(_key.GetName())
			_key = iter.Next()



		self.samples_scale_factors

	def get_variables(self):

		utility.print_nice('python_info', '\nCalled get_variables function.')

		# Get all plot _variables
		self.variables = self.plot_options['variables']	

	def set_stack_histograms(self, variable):

		utility.print_nice('python_info', '\nCalled set_stack_histograms function.')

		self.pads['stack_pad'].cd()

		# List to store samples in order
		_ordered_histograms = {'data':[], 'mc':[]}

		# Loop over plot samples for ordering histograms and creating stack
		for _id in self.samples_plot.keys():

			_sample_name = self.samples_plot[_id]
			_type = self.samples_all[_sample_name]['types']
			_stack_name 	= variable + '-' + _type + '-stack'
			_ratio_name 	= variable + '-' + _type + '-ratio'
			# Store samples in order histogram list
			_ordered_histograms[_type].append(_id)
			# Create stack histograms (same stack many times but it is ok)
			self.stack_histograms[_stack_name] = ROOT.THStack(_stack_name, _stack_name)				
			self.ratio_histograms[_ratio_name] = ROOT.THStack(_ratio_name, _ratio_name)

		# Here comes the ordering, do whatever you wish
		_ordered_histograms['data'].sort()
		_ordered_histograms['mc'].sort()

		# Make stack histogram for both data and mc samples
		# First, Loop for both mc/data
		for _t,_o_list in _ordered_histograms.iteritems():

			# Loop over all histograms
			for _n,_o in enumerate(_o_list):

				_stack_name 	= variable + '-' + _t + '-stack'
				_ratio_name 	= variable + '-' + _t + '-ratio'
				_histogram_name = variable + '-' + _o

				# all data sample histograms are transparent except the last one
				# print _t, _n, _o, _stack_name, _histogram_name
				if _t == 'data' and _n != len(_o_list)-1:
					self.histograms[_histogram_name].SetMarkerStyle(20)
					self.histograms[_histogram_name].SetMarkerSize(0.01)

				self.stack_histograms[_stack_name].Add(self.histograms[_histogram_name] )
				self.ratio_histograms[_ratio_name].Add(self.histograms[_histogram_name] )

		# ------ Draw Stacks ------- 
		# Very compact way for draw options
		_draw_options = {
			variable + '-mc-stack'	: '',
			variable + '-data-stack': 'hist p'
			}

		_draw_type = map(str, set(_draw_options) & set(self.stack_histograms))

		# if there are both mc and data plot data on top of it
		if  _draw_options.keys() == _draw_type:
			_draw_options[variable + '-data-stack'] += ' same'

		# Draw loop
		for _t in sorted(_draw_type, reverse=True):
			self.stack_histograms[_t].Draw(_draw_options[_t])
	
			# # Stack options must be set after Draw() function has been called
			# self.stack_histograms[_t].SetTitle('')
			# self.stack_histograms[_t].GetXaxis().SetTitle('')
			# self.stack_histograms[_t].GetXaxis().SetLabelSize(0)

			# self.stack_histograms[_t].GetYaxis().SetTitleSize(20)
			# self.stack_histograms[_t].GetYaxis().SetTitleFont(43)
			# self.stack_histograms[_t].GetYaxis().SetTitleOffset(1.55)

			# self.stack_histograms[_t].GetYaxis().SetLabelSize(0.)
			# _axis = ROOT.TGaxis( -5, 20, -5, 220, 20,220,510,"")
			# _axis.SetLabelFont(43) # Absolute font size in pixel (precision 3)
			# _axis.SetLabelSize(15)
			# _axis.Draw()

	def set_ratio_histograms(self, variable):

		utility.print_nice('python_info', '\nCalled set_ratio_histograms function.')

		# Histogram plot options
		_nbin 	= self.plot_options['variables'][variable]['n_bin']
		_x_min 	= self.plot_options['variables'][variable]['x_min']
		_x_max 	= self.plot_options['variables'][variable]['x_max']

		# ------ Draw Ratio ------- 
		self.pads['ratio_pad'].cd()


		if variable + '-data-ratio' in self.ratio_histograms.keys() and variable + '-mc-ratio' in self.ratio_histograms.keys():

			_ratio_histogram = self.ratio_histograms[variable + '-data-ratio'].GetStack().Last()
			_mc_histogram = self.ratio_histograms[variable + '-mc-ratio'].GetStack().Last()

			_ratio_histogram.Divide(_mc_histogram)


		else:
			utility.print_nice('status', 'Not able to plot Ratio, Data or MC sample is missing.')

			for _type in self.ratio_histograms.keys():
				_ratio_histogram = self.ratio_histograms[_type].GetStack().Last()
				_ratio_histogram.Divide(_ratio_histogram)
				_ratio_histogram.SetMarkerSize(0.01)

		_ratio_histogram.Draw('p')

		_ratio_histogram.SetMaximum(1.5)
		_ratio_histogram.SetMinimum(0.5)
		_ratio_histogram.GetYaxis().SetNdivisions(5)
		# _ratio_histogram.GetYaxis().

		_ratio_histogram.GetYaxis().SetTitle("Data/MC")
		_ratio_histogram.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
		_ratio_histogram.GetYaxis().SetTitleOffset(0.6)
		_ratio_histogram.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)

		_ratio_histogram.GetXaxis().SetTitle(variable)
		_ratio_histogram.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
		_ratio_histogram.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)

		# _ratio_histogram.CenterTitle(ROOT.kTRUE)

		# Add one horizontal line
		self.ratio_horizontal_line['ratio_line'] = ROOT.TLine(_x_min,1,_x_max,1)
		self.ratio_horizontal_line['ratio_line'].SetLineStyle(ROOT.kSolid)
		self.ratio_horizontal_line['ratio_line'].SetLineColor(ROOT.kBlack)
		self.ratio_horizontal_line['ratio_line'].Draw()


	def set_legends(self, variable):

		utility.print_nice('python_info', '\nCalled set_legends function.')

		_legend_dictionary = self.plot_definitions['legend']

		# There are two plots: histogram and ratio. Each one needs its legend		

		# ------ Upper pad: Stack Histogram -------
		self.pads['stack_pad'].cd()
		self.legends['stack_legend'] = ROOT.TLegend(0.45, 0.6,0.92,0.92)
		self.legends['stack_legend'].SetNColumns(2)
		self.legends['stack_legend'].SetLineWidth(2)
		self.legends['stack_legend'].SetBorderSize(1)
		self.legends['stack_legend'].SetFillColor(0)
		self.legends['stack_legend'].SetFillStyle(4000)
		self.legends['stack_legend'].SetTextFont(62)
		self.legends['stack_legend'].SetTextSize(0.035)
		self.legends['stack_legend'].Draw()

		# Arrange stack legend entries. Starting first with data, mc, errors
		self.legends_entries['stack_legend'] = list(set([_legend_dictionary[_id]
											for _id in self.samples_plot.keys()]))

		_additional_dict = {_legend_dictionary[_id]:_id for _id in self.samples_plot.keys()}

		# Set data on the first place if it exists of course
		try:
			self.legends_entries['stack_legend'].remove('Data')
			self.legends_entries['stack_legend'].insert(0, 'Data')
		except ValueError:
			pass

		for _l in self.legends_entries['stack_legend']:

			_id = _additional_dict[_l]

			if _l == 'Data':
				self.legends['stack_legend'].AddEntry( self.histograms[variable + '-' + _id], _l, 'p')
			else:
				self.legends['stack_legend'].AddEntry( self.histograms[variable + '-' + _id], _l, 'f')

		# if there is MC sample add
		if variable + '-mc-ratio' in self.ratio_histograms.keys():	
			# Add error graph
			self.legends['stack_legend'].AddEntry(self.error_graph['stack_error'],"MC uncert. (stat.)","fl")
		else:
			utility.print_nice('status', 'Not able to add errors, MC sample is missing.')
		# ------ Lower pad: Ratio Histogram -------

	def set_error_graphs(self, variable):

		utility.print_nice('python_info', '\nCalled set_error_graphs function.')

		if variable + '-mc-ratio' in self.ratio_histograms.keys():

			# There are two plots: histogram and ratio. Each one needs its error graph		
			_stack_name = variable + '-mc-stack'
			_stack_mc = self.stack_histograms[_stack_name].GetStack().Last().Clone()

			self.pads['stack_pad'].cd()
			# Error graph for stack	
			self.error_graph['stack_error'] = ROOT.TGraphErrors(_stack_mc)
			self.error_graph['stack_error'].SetFillColor(ROOT.kGray+3)
			self.error_graph['stack_error'].SetFillStyle(3013)
			self.error_graph['stack_error'].Draw('SAME2')

		else:
			utility.print_nice('status', 'Not able to add errors, MC sample is missing.')	
		
	def set_pads(self):
		
		utility.print_nice('python_info', '\nCalled set_pads function.')

		# There are two plots: histogram and ratio. Each one needs its Pad

		# Pad with stack (pad_upper)
		self.pads['stack_pad'] = ROOT.TPad('stack_pad','stack_pad',0,0.3,1.0,1.0)
		self.pads['stack_pad'].SetBottomMargin(0)
		self.pads['stack_pad'].SetFillStyle(4000)
		self.pads['stack_pad'].SetFrameFillStyle(1000)
		self.pads['stack_pad'].SetFrameFillColor(0)
		self.pads['stack_pad'].Draw()

		# Pad with Ratio (pad_lower)
		self.pads['ratio_pad'] = ROOT.TPad('ratio_pad','ratio_pad',0,0.0,1.0,0.3)
		self.pads['ratio_pad'].SetTopMargin(0.)
		self.pads['ratio_pad'].SetBottomMargin(0.35)
		self.pads['ratio_pad'].SetFillStyle(4000)
		self.pads['ratio_pad'].SetFrameFillStyle(1000)
		self.pads['ratio_pad'].SetFrameFillColor(0)
		self.pads['ratio_pad'].Draw()	

	def set_labels(self):

		utility.print_nice('python_info', '\nCalled set_labels function.')

		# Labels for stack pad
		self.pads['stack_pad'].cd()

		self.labels['cms'] = self.myText("CMS",0.17,0.88,1.04)
		_lumi 	= float(self.general_options['luminosity']/1000.0)
		_tag 	= self.general_options['tag']
		self.labels['lumi'] = self.myText('#sqrt{{s}} = {0}, L = {1} fb^{{-1}}'.format(_tag, _lumi ),0.17,0.83)
		# _label_add_flag = self.myText(_add_flag,0.17,0.78)		

	def set_canvas(self,v):

		utility.print_nice('python_info', '\nCalled set_canvas function.')

		self.canvas[v] = ROOT.TCanvas(v, v, 600, 600)
		self.canvas[v].SetFillStyle(4000)
		self.canvas[v].SetFrameFillStyle(1000)
		self.canvas[v].SetFrameFillColor(0)		

	def plot(self):

		utility.print_nice('python_info', '\nCalled plot function.')
		
		for _v in self.variables:

			# Set Canvas 
			self.set_canvas(_v)

			# Setup pads
			self.set_pads()

			# ------ Upper pad: Stack Histogram -------
			self.set_stack_histograms(_v)

			# ------ Lower pad: Ratio Histogram -------
			self.set_ratio_histograms(_v)

			# Setup error_graph
			self.set_error_graphs(_v)			

			# Setup legends 				
			self.set_legends(_v)

			# Setup labels
			self.set_labels()

			self.canvas[_v].SaveAs( os.path.join(self.plot_directory, self.plot_name + '_' + _v + '_.pdf'))

	@staticmethod
	def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
		ROOT.gPad.Update()
		text = ROOT.TLatex()
		text.SetNDC()
		text.SetTextColor(ROOT.kBlack)
		text.SetTextSize(text.GetTextSize()*size)
		text.DrawLatex(ndcX,ndcY,txt)
		return text

class ClassicalPlots(object):
	'''
	-----------
	Description:

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
	def __init__(self):
		utility.print_nice('python_info', '\nCreated instance of ClassicalPlots')
		
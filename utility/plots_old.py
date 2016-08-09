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



	-----------
	Useful commands:

	# test_h = ROOT.TH1F('test_h', 'test_h', 100, 0, 10)
	# test_h.Fill(1,1000)
	# test_h.SetLineColor(632)
	# test_s = ROOT.THStack('test_s', 'test_s')
	# test_s.Add(test_h)

	-----------
	To DO:
	- add weights, scale factors, lumi
	- overlay
	- last bin (overflow)
	- subsamples
	- errors
	- y axis
	- lower plot

	'''	
	
	def __init__(self, analysis_name, plot_name, configuration):

		print '\n','-'*50, '\nCreated instance of Plot class\n', '-'*50

		# Load plot style, defined in tdrStyle.py
		tdrStyle.tdrStyle()

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
		self.pads = {}
		self.cache_trees = {}

		# ------ Cuts -------
		self.blinding_cut 		= configuration.cfg_files['cuts']['blinding_cut']
		self.plot_cut 			= configuration.cfg_files['cuts'][self.plot_name]		
		self.final_cut 			= '&&'.join([self.blinding_cut, self.plot_cut])

		# ------ Samples -------
		self.samples_plot 		= filter(lambda x: 'root' in x, os.listdir(self.samples_directory)) 
		self.samples_all 		= configuration.cfg_files['samples']

		# if only element in samples is 'all' use all, else use specified samples
		if self.plot_options['samples'][0].encode('utf-8') != 'all':

			_matching = []

			for _sample in self.plot_options['samples']:
				_matching += [s for s in self.samples_plot if _sample in s]

			self.samples_plot = _matching

		self.samples_plot.sort()

		print '\n{0:30s}{1}'.format('Working directory:' , self.working_directory)
		print '{0:30s}{1}'.format('Location of samples:' , self.samples_directory)
		print '\n{0:30s}{1}'.format('Plot options:' , self.plot_options)	
		print '{0:30s}{1}'.format('Blinding cut:' , self.blinding_cut)	
		print '{0:30s}{1}'.format('Plot cut:' , self.plot_cut)
		print '\nList of samples:'
		for _sample in self.samples_plot:
			print '{0:30s}{1}'.format('' , _sample)

	def get_trees(self):

		# Make trees with all cuts applied, if doesnt exist create them and store in cache dir
		self.cache_trees = utility.trim_trees( self.final_cut, self.samples_plot, self.samples_directory)

	def set_histograms(self):

		# Histograms will be saved in new root file
		_output_name = os.path.join(self.plot_directory, self.plot_name + '.root')
		_output = ROOT.TFile.Open( _output_name,'recreate')
		_output.Close()

		# Loop over all samples
		for _sample, _f in self.cache_trees.iteritems():

			# Loop over all variables for each sample
			for _var, _o in self.plot_options['variables'].iteritems():

				_name =  _var + '-' + _sample

				# Histogram plot options
				_nbin 	= self.plot_options['variables'][_var]['n_bin']
				_x_min 	= self.plot_options['variables'][_var]['x_min']
				_x_max 	= self.plot_options['variables'][_var]['x_max']

				# Get histogram from sample
				_input = ROOT.TFile.Open( _f,'read')
				_tree = _input.Get('tree')
				_histogram = ROOT.TH1D( _name, _name, _nbin, _x_min, _x_max)
				_tree.Draw('{0}>>{1}'.format( _var, _name) )
				# print dir(_histogram)

				# Check if sample is data or mc
				_sample_type = self.samples_all[_sample]['types']

				if _sample_type == 'data':
					_histogram.SetMarkerColor(self.plot_definitions['colors'][_sample])
				else:
					_histogram.SetFillColor(self.plot_definitions['colors'][_sample])
					_histogram.SetLineColor(self.plot_definitions['colors'][_sample])
					
				# Histogram scaling
			
				# Histogram weights

				# c = ROOT.TCanvas('c', 'c', 800, 800)
				# _histogram.Draw()
				# _histogram.SetTitle(_name)
				# c.SaveAs(_name + '_.pdf')

				# Save histograms to new root file
				_output = ROOT.TFile.Open( _output_name, 'update')
				_histogram.Write()
				_output.Close()

				_input.Close()

	def set_stack_histograms(self):

		# Load all histograms
		_input 	= os.path.join(self.plot_directory, self.plot_name + '.root')

		# Get all histograms from _input_name and store them in dictionary
		_histograms = utility.get_histograms(_input)

		# Get all plot _variables
		_variables = [_h.split('-')[0] for _h in _histograms.keys() ]
		_variables = list(set(_variables))

		# Get all samples
		_samples = [_h.split('-')[1] for _h in _histograms.keys() ]
		_samples = list(set(_samples))

		# Save stack histograms in pdf for each variable
		for _v in _variables:

			# Stack mc/data histograms in order
			_stack_histograms = self.set_stack_histograms_order( _v, _samples, _histograms)

			_data 	= _v + '-' + 'data'
			_mc 	= _v + '-' + 'mc'

			_stack_mc = _stack_histograms[_mc].GetStack().Last().Clone()

			# ---------------------
			# ------ Canvas -------
			c = ROOT.TCanvas(_v, _v, 600, 600)
			c.SetFillStyle(4000)
			c.SetFrameFillStyle(1000)
			c.SetFrameFillColor(0)

			# ROOT.gPad.SetTicks(1,1)

			# -------------------
			# ------ Pads -------
			# There are two plots: histogram and ratio. Each one needs its Pad

			# Pad with Histogram (pad_upper)
			pad_upper = ROOT.TPad('pad_upper','pad_upper',0,0.3,1.0,1.0)
			pad_upper.SetBottomMargin(0)
			pad_upper.SetFillStyle(4000)
			pad_upper.SetFrameFillStyle(1000)
			pad_upper.SetFrameFillColor(0)
			pad_upper.Draw()

			# Pad with Ratio (pad_lower)
			pad_lower = ROOT.TPad('pad_lower','pad_lower',0,0.0,1.0,0.3)
			pad_lower.SetTopMargin(0.)
			pad_lower.SetBottomMargin(0.35)
			pad_lower.SetFillStyle(4000)
			pad_lower.SetFrameFillStyle(1000)
			pad_lower.SetFrameFillColor(0)
			pad_lower.Draw()

			# -----------------------------------------
			# ------ Upper pad: Stack Histogram -------
			pad_upper.cd()

			# Check if mc and data have stack histogram
			_stack 	= []

			if _mc in _stack_histograms.keys():
				_stack.append(_mc)
			if _data in _stack_histograms.keys():
				_stack.append(_data)

			if not _stack:
				print 'ERROR: Stack is empty.'

			for _s in _stack:

				if 'mc' in _s:
					_draw_option = ''

				# if there is not mc samples
				if 'data' in _s and len(_stack) == 1:
					_draw_option = 'hist p'

				# if there are both type of samples
				if 'data' in _s and len(_stack) == 2:
					_draw_option = 'same hist p'

				_stack_histograms[_s].Draw(_draw_option)

			# ------ Stack options -------------------
			_stack_histograms[_stack[0]].SetTitle('')
			_stack_histograms[_stack[0]].GetXaxis().SetTitle('')
			# _stack_histograms[_stack[0]].GetXaxis().SetRangeUser(self.xMin,self.xMax)
			_stack_histograms[_stack[0]].GetXaxis().SetLabelSize(0)
			# _stack_histograms[_stack[0]].GetYaxis().SetRangeUser(0,20000)

			# ------ labels (CMS, luminosity) ------
			_label_cms 	= self.myText("CMS",0.17,0.88,1.04)
			_lumi 		= float(self.general_options['luminosity']/1000.0)
			_tag 		= self.general_options['tag']
			_label_lumi = self.myText('#sqrt{{s}} = {0}, L = {1} fb^{{-1}}'.format(_tag, _lumi ),0.17,0.83)
			# _label_add_flag = self.myText(_add_flag,0.17,0.78)

			_upper_legend = ROOT.TLegend(0.45, 0.6,0.92,0.92)
			_upper_legend.SetNColumns(2)
			_upper_legend.SetLineWidth(2)
			_upper_legend.SetBorderSize(1)
			_upper_legend.SetFillColor(0)
			_upper_legend.SetFillStyle(4000)
			_upper_legend.SetTextFont(62)
			_upper_legend.SetTextSize(0.035)
			_upper_legend.Draw()

			# Data
			for _s in _samples:
				# constraint of marker size just to add one data histogram in legend
				if self.samples_all[_s]['types'] == 'data' and _histograms[_v + '-' + _s].GetMarkerSize() > 0.01:
					_upper_legend.AddEntry( _histograms[_v + '-' + _s], 'Data', 'p')

			# MC
			for _s in _samples:
				if self.samples_all[_s]['types'] == 'mc':
					_upper_legend.AddEntry(_histograms[_v + '-' + _s],'test','f')

			# ------ error graph ------------------
			
			_error_graph = ROOT.TGraphErrors(_stack_mc)
			_error_graph.SetFillColor(ROOT.kGray+3)
			_error_graph.SetFillStyle(3013)
			_error_graph.Draw('SAME2')
			_upper_legend.AddEntry(_error_graph,"MC uncert. (stat.)","fl")

			# -------------------------------
			# ------ Lower pad: Ratio -------
			pad_lower.cd()
			ROOT.gPad.SetTicks(1,1)

			# Plot.ratio_maker(_stack_mc, _stack_mc, _x_min, _x_max)

			_line = ROOT.TLine(self.xMin,1,self.xMax,1)
			_line.SetLineStyle(ROOT.kSolid)
			_line.Draw()

			c.SaveAs( os.path.join(self.plot_directory, self.plot_name + '_' + _v + '_.pdf'))

	def set_stack_histograms_order(self, variable, samples, histograms):

		# Dictionary to store stack histograms
		_stack_histograms = {}

		# print variable, samples, histograms

		# List to store samples in order
		_order_data = []
		_order_mc 	= []

		# Loop over all samples
		for _s in samples:
			
			# Create stack histograms
			_name = variable + '-' + self.samples_all[_s]['types']
			_stack_histograms[_name] = ROOT.THStack(_name, _name)

			# store sample names so that we can order them
			if 'data' in _name:	
				_order_data.append(_s)
			else:
				_order_mc.append(_s)

		# Make stack for data samples
		_order_data.sort()
		for _n,_o in enumerate(_order_data):
			_s_name = variable + '-' + self.samples_all[_o]['types']
			_h_name = variable + '-' + _o
			# all data sample histo are transparent except the last one
			if _n != len(_order_data)-1:
				histograms[_h_name].SetMarkerStyle(20)
				histograms[_h_name].SetMarkerSize(0.01)
			_stack_histograms[_s_name].Add( histograms[ _h_name ] )

		# Make stack for mc samples
		_order_mc.sort()
		for _o in _order_mc:
			_s_name = variable + '-' + self.samples_all[_o]['types']
			_h_name = variable + '-' + _o
			_stack_histograms[_s_name].Add( histograms[_h_name] )

		return _stack_histograms

	def set_ratio_histogram(self):
		pass

	def set_legend(self):
		pass

	def set_pads(self):
		pass

	def plot(stack_histogram, ratio_histogram):
		pass

	def get_histograms(file_name):

		histograms = {}

		try:
			_input = ROOT.TFile.Open( file_name, 'read')

		except Exception, e:
			print 'Problem with loading: ', file_name
			raise

		dirlist = _input.GetListOfKeys()
		iter = dirlist.MakeIterator()
		key = iter.Next()

		while key:
			histograms[key.GetName()] = _input.Get(key.GetName())
			key = iter.Next()

		return histograms


	# @staticmethod
	# def ratio_histogram_maker(histogram, ref_histogram, min_range, 
	# 	max_range, y_title = '', max_uncertainty = 1000.0, restrict = True):

		# _ratio = _cool_ratio.make_rebinned_ratios(histogram,ref_histogram,max_uncertainty,False,0)
		# _ref_error = _cool_ratio.make_rebinned_ratios(histogram,ref_histogram,max_uncertainty,False,1)
		# _ratio.GetXaxis().SetRangeUser(min_range,max_range)
		# #_ratio.GetXaxis().SetRangeUser(0,1)
		# if restrict:
		# 	_ratio.SetMinimum(0.5)
		# 	_ratio.SetMaximum(1.75)
		# else:
		# 	_ratio.SetMinimum(int(_ratio.GetMinimum()))
		# 	_ratio.SetMaximum(int(_ratio.GetMaximum()*1.5))
		# _ratio.GetYaxis().SetNdivisions(505)
		# _ratio.GetYaxis().SetTitle("Ratio")
		# _ratio.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
		# _ratio.GetYaxis().SetTitleOffset(0.6)
		# _ratio.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)
		# _ratio.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize()*2.2)
		# _ratio.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize() * 2.2)
		# _ratio.GetYaxis().SetTitleOffset(0.4)
		# _ratio.GetYaxis().CenterTitle(ROOT.kTRUE)
		# _ratio.GetYaxis().SetDrawOption("M")
		# _ratio.SetXTitle(yTitle)
		# _ratio.SetYTitle("Data/MC")
		# return _ratio, _ref_error


	@staticmethod
	def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
		ROOT.gPad.Update()
		text = ROOT.TLatex()
		text.SetNDC()
		text.SetTextColor(ROOT.kBlack)
		text.SetTextSize(text.GetTextSize()*size)
		text.DrawLatex(ndcX,ndcY,txt)
		return text

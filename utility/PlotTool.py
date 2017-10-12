import os

import ROOT

from utility import MiscTool
from utility import FileTool
from utility import WeightTool

ROOT.gROOT.SetBatch(True)

class PlotTool(object):
 
  '''
  -----------
  Description:

  -----------
  Useful commands:

  # test_h = ROOT.TH1F('test_h', 'test_h', 100, 0, 10)
  # test_h.Fill(1,1000)
  # test_h.SetLineColor(632)
  # test_s = ROOT.THStack('test_s', 'test_s')
  # test_s.Add(test_h)

  # c = ROOT.TCanvas('c', 'c', 800, 800)
  # _histogram.Draw('p')
  # _histogram.SetTitle(_name)
  # c.SaveAs(_name + '_.pdf')

  # print self.histograms_stack[_t].GetStack().Last().Integral()

  ''' 
  
  def __init__(self, configuration, sample_tool):

    MiscTool.Print('python_info', '\nCreated instance of Plot class')

    # ------ Paths -------
    self.path_working_directory           = configuration.paths.path_working_directory
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_cache                       = configuration.paths.path_cache
    self.path_plots                       = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'plots') )

    # ------ Samples -------
    self.sample_tool            = sample_tool

    # ------ Configuration -------
    self.task_name              = configuration.general.task_name
    self.plot_options           = configuration.plots.task[self.task_name]
    self.plot_definitions       = configuration.plots.definitions
    self.general_options        = configuration.general

    # ------ Plot features -----
    self.variables              = configuration.plots.task[self.task_name]['variables'] 
    self.canvas                 = {}
    self.pads                   = {}
    self.histograms             = {}
    self.histograms_stack       = {}
    self.histograms_stack_axis  = {}
    self.histograms_ratio       = {}
    self.histograms_ratio_line  = {}
    self.histograms_ratio_axis  = {}
    self.legends                = {}
    self.legends_entries        = {}
    self.graphs_error           = {}
    self.labels                 = {}

    self._x_name                = 'sample_x100'
    self._x_histograms          = {}

    self.luminosity             = configuration.general.luminosity
    self.tag                    = configuration.general.tag

    # ------ Other -------
    MiscTool.Print('analysis_info', 'Task:', self.task_name)
    MiscTool.Print('analysis_info', 'Working directory:', self.path_working_directory)
    MiscTool.Print('analysis_info_list', 'Plot options:', self.plot_options.values())
    
    # ------ Plot Setup -------
    self.set_and_save_histograms()
    self.get_and_prepare_histograms()

  def set_and_save_histograms(self):

    MiscTool.Print('python_info', '\nCalled set_and_save_histograms function.')

    # Histograms will be saved in new root file
    _output_name = os.path.join(self.path_plots, self.task_name + '.root')
    _output = ROOT.TFile.Open( _output_name, 'recreate')
    _output.Close()

    # # Loop over all samples
    for _id, _s in self.sample_tool.samples.iteritems():

      _f = _s.file

      # Loop over all variables for each sample
      for _var in self.variables:

        # Histogram plot options
        _nbin   = self.variables[_var]['n_bin']
        _x_min  = self.variables[_var]['x_min']
        _x_max  = self.variables[_var]['x_max']

        _name =  '__'.join([ _var, _id]) 

        # Open tree and create histogram
        _input = ROOT.TFile.Open( _f,'read')
        _tree = _input.Get('tree')
        _histogram = ROOT.TH1F( _name, _name, _nbin, _x_min, _x_max)
        # _histogram.SetFillColor(0)

        # Fill histograms event by event, THIS WILL BE MOVED INTO SEPARATE TOOL
        if self.plot_options['event_by_event']:

          MiscTool.Print('status', '\nFill histogram event by event.')

          _number_of_entries = _tree.GetEntriesFast()
          MiscTool.Print('analysis_info', 'Sample:', _id)
          MiscTool.Print('analysis_info', 'Number of entries (cached):', _number_of_entries)

          # Here comes the code you wish to apply

          for _ev in xrange(_number_of_entries):

            _tree.GetEntry(_ev)

            print  '\n', 'Event number:', _ev

            _x = getattr(_tree, self.variables[_var]['eval'])

            _histogram.Fill(_x)

        # Or by using Draw Function
        else:
          
          MiscTool.Print('status', '\nFill histogram directly from tree.')

          _weight = '*'.join([_s.weight_expression, _s.normalization_factor])

          # Get histogram from the tree directly
          _tree.Draw('{0}>>{1}'.format( self.variables[_var]['eval'], _name), _weight)

          _number_of_entries = _tree.GetEntriesFast()
          MiscTool.Print('analysis_info', 'Sample:', _id)
          MiscTool.Print('analysis_info', '# entries (skimmed tree): ', _number_of_entries)
          MiscTool.Print('analysis_info', 'Expected yields (skimmed tree): ', _histogram.Integral())

        # Save histograms to new root file
        _output = ROOT.TFile.Open( _output_name, 'update')
        _histogram.Write()
        _output.Close()

        _input.Close()

  def get_and_prepare_histograms(self):

    MiscTool.Print('python_info', '\nCalled get_histograms function.')

    # Get all histograms from _input and store them in dictionary   
    try:
      _input  = os.path.join(self.path_plots, self.task_name + '.root')
      _file   = ROOT.TFile.Open( _input,'read')

    except Exception, e:
      MiscTool.Print('error', 'Problem with loading: ' + _input)
      raise

    _dirlist = _file.GetListOfKeys()
    iter = _dirlist.MakeIterator()
    _key = iter.Next()

    while _key:
      self.histograms[_key.GetName()] = _file.Get(_key.GetName())
      self.histograms[_key.GetName()].SetDirectory(0)

      _var, _id = _key.GetName().split('__')

      if _id in self.plot_options[self._x_name]:
        self._x_histograms[_key.GetName()] = _file.Get(_key.GetName())
        self._x_histograms[_key.GetName()].SetDirectory(0)

      # Histograms plot options
      if self.sample_tool.samples[_id].types == 'data':
        self.histograms[_key.GetName()].SetMarkerStyle(20)
        self.histograms[_key.GetName()].SetMarkerColor(self.plot_definitions['colors'][_id])
      else:
        self.histograms[_key.GetName()].SetFillColor(self.plot_definitions['colors'][_id])
        self.histograms[_key.GetName()].SetLineColor(self.plot_definitions['colors'][_id])

      _key = iter.Next()

  def _set_histograms_stack(self, variable):

    MiscTool.Print('python_info', '\nCalled set_histograms_stack function.')

    # List to store samples in order
    _ordered_histograms = {'data':[], 'mc':[]}

    self.pads['stack_pad_' + variable].cd()

    # Loop over plot samples for ordering histograms and creating stack
    for _id, _s in self.sample_tool.samples.iteritems():

      _stack_name   = '__'.join([variable, _s.types, 'stack'])
      _ratio_name   = '__'.join([variable, _s.types, 'ratio'])
      _stack_x    = '__'.join([variable, self._x_name])

      # Store samples in ordered histogram list
      _ordered_histograms[_s.types].append(_id)

      # Create stack histograms (same stack created many times but it is ok)
      self.histograms_stack[_stack_name] = ROOT.THStack(_stack_name, _stack_name)       
      self.histograms_ratio[_ratio_name] = ROOT.THStack(_ratio_name, _ratio_name)
      
      # Add x histogram if defined in config
      if len(self.plot_options[self._x_name]) != 0:
        self.histograms_stack[ _stack_x ] = ROOT.THStack( _stack_x, _stack_x )      

    # Here comes the ordering which is defined in plots config
    _ordered_histograms['mc'] = [ _i for _i in self.plot_definitions['plot_order'] if _i in _ordered_histograms['mc']]

    # Make stack histogram for both data and mc samples
    # First, Loop for both mc/data
    for _t, _o_list in _ordered_histograms.iteritems():

      # Loop over all histograms
      for _n, _o in enumerate(_o_list):

        _stack_name   = '__'.join([variable, _t, 'stack'])
        _ratio_name   = '__'.join([variable, _t, 'ratio'])
        _histogram_name = '__'.join([variable, _o])

        # all data sample histograms are transparent except the last one
        # print _t, _n, _o, _stack_name, _histogram_name
        if _t == 'data' and _n != len(_o_list)-1:
          self.histograms[_histogram_name].SetMarkerStyle(20)
          self.histograms[_histogram_name].SetMarkerSize(0.01)

        self.histograms_stack[_stack_name].Add(self.histograms[_histogram_name] )
        
        # Add to histograms ratio only if defined in config name
        if self.plot_options['ratio_plot'] == 'Data_MC':
          if _histogram_name.split('__')[1] in self.plot_options['ratio_plot_bgk'] or 'all' in self.plot_options['ratio_plot_bgk']:
            self.histograms_ratio[_ratio_name].Add(self.histograms[_histogram_name] )

        elif self.plot_options['ratio_plot'] == 'SigBkg':
          if _histogram_name.split('__')[1] in self.plot_options['ratio_plot_sig'] or 'all' in self.plot_options['ratio_plot_sig']:
            self.histograms_ratio[_ratio_name].Add(self.histograms[_histogram_name] )

    # ------ Histogram x100 ------
    _stack_x    = '__'.join([variable, self._x_name])
    for _o in self._x_histograms:

      if variable in _o:

        # self.test[_histogram_name] = self.histograms[_histogram_name].Clone()
        self._x_histograms[_o].Scale(10)
        # # self.test[_histogram_name].SetLineWidth(0)
        self._x_histograms[_o].SetFillColorAlpha(ROOT.kBlack, 0.0)
        self._x_histograms[_o].SetLineColorAlpha(self.plot_definitions['colors'][self._x_name], 1.0)
        self.histograms_stack[ _stack_x].Add( self._x_histograms[_o])

    # Set y range
    _global_max = 0
    for _i, _s in self.histograms_stack.iteritems():
      if variable in _i:
        _global_max = max(_s.GetMaximum(), _global_max)

    for _i, _s in self.histograms_stack.iteritems():
      if variable in _i:
        _s.SetMaximum(_global_max)

    # ------ Draw Stacks ------- 
    # Very compact way for setup drawing options
    _draw_options = {
      '__'.join([variable, 'mc', 'stack'])    : 'hist',
      '__'.join([variable, 'data', 'stack'])  : 'hist p',
      '__'.join([variable, self._x_name])     : 'hist'
      }

    _first = True
    _draw_type = []

    for _d in self.histograms_stack:

      if 'mc' in _d and variable in _d:
        _first = False
        _draw_type.append(_d)

    for _d in self.histograms_stack:

      if 'data' in _d and variable in _d:
        _draw_type.append(_d)
        if _first:
          _first = False
        else:
          _draw_options['__'.join([variable, 'data', 'stack'])] += ' same'


    for _d in self.histograms_stack:

      if self._x_name in _d and variable in _d:
        _draw_type.append(_d)
        if _first:
          _first = False
        else:
          _draw_options['__'.join([variable, self._x_name])] += ' same'    

    # Draw loop
    for _t in _draw_type:

      if self._x_name in _t:
        x = self.histograms_stack[_t].GetStack().Last()
      else:
        x = self.histograms_stack[_t]

      x.Draw(_draw_options[_t])
      # Stack options must be set after Draw() function has been called
      x.SetTitle('')
      x.GetXaxis().SetTitle('')
      x.GetXaxis().SetLabelSize(0)
      x.GetXaxis().SetTickSize(0)
      x.GetYaxis().SetLabelSize(0)
      x.GetYaxis().SetTickSize(0)

    # self.pads['stack_pad'].Update()

    # Definition of new y axis
    _xmin = self.pads['stack_pad_' + variable].GetUxmin()
    _ymin = self.pads['stack_pad_' + variable].GetUymin()
    _ymax = self.pads['stack_pad_' + variable].GetUymax()
    _dy   = _ymax - _ymin

    self.histograms_stack_axis['y'] = ROOT.TGaxis( _xmin, _ymin + _dy*0.01, _xmin, _ymax, _ymin + _dy*0.01, _ymax, 510, "")
    self.histograms_stack_axis['y'].SetLabelFont(43) # Absolute font size in pixel (precision 3)
    self.histograms_stack_axis['y'].SetLabelSize(15)
    self.histograms_stack_axis['y'].SetTitle('')
    self.histograms_stack_axis['y'].Draw()

  def _set_histograms_ratio(self, variable):

    MiscTool.Print('python_info', '\nCalled set_histograms_ratio function.')

    # Histogram plot options
    _nbin   = self.variables[variable]['n_bin']
    _x_min  = self.variables[variable]['x_min']
    _x_max  = self.variables[variable]['x_max']

    # ------ Draw Ratio ------- 
    self.pads['ratio_pad_' + variable].cd()
    self.pads['ratio_pad_' + variable].SetTopMargin(0.04)

    if self.plot_options['ratio_plot'] == 'Data_MC':

      MiscTool.Print('status', 'Ploting Data / MC sample ratio.')

      if '__'.join([variable, 'data', 'ratio']) in self.histograms_ratio.keys() and '__'.join([variable, 'mc', 'ratio']) in self.histograms_ratio.keys():

        _ratio_histogram  = self.histograms_ratio['__'.join([variable, 'data', 'ratio'])].GetStack().Last()
        _mc_histogram     = self.histograms_ratio['__'.join([variable, 'mc', 'ratio'])].GetStack().Last()

        _ratio_histogram.Divide(_mc_histogram)

      else:
        MiscTool.Print('status', 'Not able to plot Ratio, Data or MC sample is missing.')

        _ratio_histogram = self.histograms_ratio['__'.join([variable, 'mc', 'ratio'])].GetStack().Last()
        _ratio_histogram.Divide(_ratio_histogram)
        _ratio_histogram.SetMarkerSize(0.01)

    elif self.plot_options['ratio_plot'] == 'SigBkg':
     
      pass

    else:
      
      pass

    # Title, statistics
    _ratio_histogram.Draw('histo p')
    _ratio_histogram.SetTitle('')
    _ratio_histogram.SetStats(0)
    _ratio_histogram.SetMaximum(2)
    _ratio_histogram.SetMinimum(0)

    self.pads['ratio_pad_' + variable].Update()    

    # Axes
    _xmin   = self.pads['stack_pad_' + variable].GetUxmin()
    _xmax   = self.pads['stack_pad_' + variable].GetUxmax()
    _ymin   = self.pads['ratio_pad_' + variable].GetUymin()
    _ymax   = self.pads['ratio_pad_' + variable].GetUymax()
    _dy   = _ymax - _ymin
    _dx   = _xmax - _xmin

    # X axis
    _ratio_histogram.GetXaxis().SetLabelSize(0)
    _ratio_histogram.GetXaxis().SetTickSize(0)
    self.histograms_ratio_axis['x_' + variable] = ROOT.TGaxis( _xmin + _dx*0.01, _ymin, _xmax, _ymin, _xmin + _dx*0.01, _xmax, 510, "")
    self.histograms_ratio_axis['x_' + variable].SetLabelFont(43) # Absolute font size in pixel (precision 3)
    self.histograms_ratio_axis['x_' + variable].SetLabelSize(15)
    self.histograms_ratio_axis['x_' + variable].SetTitle(variable)
    self.histograms_ratio_axis['x_' + variable].SetTitleSize(self.histograms_ratio_axis['x_' + variable].GetTitleSize()*2.4)
    self.histograms_ratio_axis['x_' + variable].SetTitleOffset(0.7)
    self.histograms_ratio_axis['x_' + variable].Draw()

    # Y axis
    _ratio_histogram.GetYaxis().SetLabelSize(0)
    _ratio_histogram.GetYaxis().SetTickSize(0)
    self.histograms_ratio_axis['y_' + variable] = ROOT.TGaxis( _xmin, _ymin, _xmin, _ymax, _ymin, 2, 410, "")
    self.histograms_ratio_axis['y_' + variable].SetLabelFont(43) # Absolute font size in pixel (precision 3)
    self.histograms_ratio_axis['y_' + variable].SetLabelSize(12)
    self.histograms_ratio_axis['y_' + variable].SetTitle('')
    self.histograms_ratio_axis['y_' + variable].SetTitleSize(self.histograms_ratio_axis['y_' + variable].GetTitleSize()*2.0)
    self.histograms_ratio_axis['y_' + variable].SetTitleOffset(0.5)
    # self.histograms_ratio_axis['y'].SetNdivisions(5)
    self.histograms_ratio_axis['y_' + variable].Draw()

    self.labels['histogram_ratio_y_axis_' + variable] = self.histogram_ratio_title_Y_axis("Data / MC", 0.05, 0.45, 1.3)

    self.pads['ratio_pad_' + variable].Update()  

    # Add one horizontal line
    self.histograms_ratio_line['ratio_line_' + variable] = ROOT.TLine(_x_min,1,_x_max,1)
    self.histograms_ratio_line['ratio_line_' + variable].SetLineStyle(ROOT.kSolid)
    self.histograms_ratio_line['ratio_line_' + variable].SetLineColor(ROOT.kBlack)
    self.histograms_ratio_line['ratio_line_' + variable].Draw()

  def _set_legends(self, variable):

    MiscTool.Print('python_info', '\nCalled set_legends function.')

    _legend_dictionary = self.plot_definitions['legend']

    # There are two plots: histogram and ratio. Each one needs its legend   

    # ------ Upper pad: Stack Histogram -------
    
    self.pads['stack_pad_' + variable].cd()
    self.legends['stack_legend'] = ROOT.TLegend(0.5, 0.6, 0.9, 0.9)
    self.legends['stack_legend'].SetNColumns(2)
    self.legends['stack_legend'].SetLineWidth(2)
    self.legends['stack_legend'].SetBorderSize(1)
    self.legends['stack_legend'].SetFillColor(0)
    self.legends['stack_legend'].SetFillStyle(4000)
    self.legends['stack_legend'].SetTextFont(62)
    self.legends['stack_legend'].SetTextSize(0.035)
    self.legends['stack_legend'].Draw()

    _legend_dictionary_compressed = {}

    # Make sure to add only one label if samples have the same label
    for _s in self.sample_tool.samples:

      if _legend_dictionary[_s] not in _legend_dictionary_compressed.values():

        # Add data legend entry if there is one
        if _legend_dictionary[_s] == 'Data':
          if not self.histograms['__'.join([variable, _s])].GetMarkerSize() > 1.0:
            continue

        _legend_dictionary_compressed[_s] = _legend_dictionary[_s]

    # Order legend entries
    _ordered_legends = [ _s for _s in self.plot_definitions['plot_order'] if _s in _legend_dictionary_compressed ]

    for _id in _ordered_legends:

      _name = _legend_dictionary_compressed[_id]

      if _name == 'Data':
        self.legends['stack_legend'].AddEntry( self.histograms['__'.join([variable, _id])], _name, 'p')
      else:
        self.legends['stack_legend'].AddEntry( self.histograms['__'.join([variable, _id])], _name, 'f')

    # Special part for x100 part
    if len(self.plot_options[self._x_name]) != 0:
      _name = '__'.join([variable, self.plot_options[self._x_name][0]]) 
      self.legends['stack_legend'].AddEntry( self._x_histograms[_name], self.plot_definitions['legend'][self._x_name], 'l')

    # # if there is MC sample add
    # if '__'.join([variable, 'mc', 'ratio']) in self.histograms_ratio.keys():  
    #   # Add error graph
    #   self.legends['stack_legend'].AddEntry(self.graphs_error['stack_error'],"MC uncert. (stat.)","fl")
    # else:
    #   MiscTool.Print('status', 'Not able to add errors, MC sample is missing.')

    # ------ Lower pad: Ratio Histogram -------
    # TBD

  def _set_graphs_errors(self, variable):

    MiscTool.Print('python_info', '\nCalled set_graphs_errors function.')

    if '__'.join([variable, 'mc', 'ratio']) in self.histograms_ratio.keys():

      # There are two plots: histogram and ratio. Each one needs its error graph    
      _stack_name = '__'.join([variable, 'mc', 'stack'])
      _stack_mc = self.histograms_stack[_stack_name].GetStack().Last().Clone()

      self.pads['stack_pad_' + variable].cd()
      # Error graph for stack 
      self.graphs_error['stack_error'] = ROOT.TGraphErrors(_stack_mc)
      self.graphs_error['stack_error'].SetFillColor(ROOT.kGray+3)
      self.graphs_error['stack_error'].SetFillStyle(3013)
      self.graphs_error['stack_error'].Draw('SAME2')

    else:
      MiscTool.Print('status', 'Not able to add errors, MC sample is missing.') 
    
  def _set_pads(self, variable):
    
    MiscTool.Print('python_info', '\nCalled set_pads function.')

    # There are two plots: histogram and ratio. Each one needs its Pad

    # Pad with stack (pad_upper)
    self.pads['stack_pad_' + variable] = ROOT.TPad('stack_pad','stack_pad',0,0.28,1.0,1.0)
    self.pads['stack_pad_' + variable].SetBottomMargin(0)
    self.pads['stack_pad_' + variable].SetFillStyle(4000)
    self.pads['stack_pad_' + variable].SetFrameFillStyle(1000)
    self.pads['stack_pad_' + variable].SetFrameFillColor(0)
    self.pads['stack_pad_' + variable].Draw()

    # Pad with Ratio (pad_lower)
    self.pads['ratio_pad_' + variable] = ROOT.TPad('ratio_pad','ratio_pad',0,0.0,1.0,0.28)
    self.pads['ratio_pad_' + variable].SetTopMargin(0.)
    self.pads['ratio_pad_' + variable].SetBottomMargin(0.2)
    self.pads['ratio_pad_' + variable].SetFillStyle(4000)
    self.pads['ratio_pad_' + variable].SetFrameFillStyle(1000)
    self.pads['ratio_pad_' + variable].SetFrameFillColor(0)
    self.pads['ratio_pad_' + variable].Draw()  

  def _set_labels(self, variable):

    MiscTool.Print('python_info', '\nCalled set_labels function.')

    # Labels for stack pad
    self.pads['stack_pad_' + variable].cd()

    self.labels['cms'] = self.myText("CMS, Preliminary", 0.13, 0.82, 0.6)
    _lumi   = float(self.luminosity/1000.0)
    _tag    = self.tag
    self.labels['lumi'] = self.myText('#sqrt{{s}} = {0}, L = {1} fb^{{-1}}'.format(_tag, _lumi ), 0.13, 0.77, 0.6)  

  def _set_canvas(self, variable):

    MiscTool.Print('python_info', '\nCalled set_canvas function.')

    self.canvas[variable] = ROOT.TCanvas(variable, variable, 800, 800)
    self.canvas[variable].SetFillStyle(4000)
    self.canvas[variable].SetFrameFillStyle(1000)
    self.canvas[variable].SetFrameFillColor(0)   

  def _save_canvas(self, variable):

    MiscTool.Print('python_info', '\nCalled save_canvas function.')

    self.canvas[variable].SaveAs( os.path.join(self.path_plots, self.task_name + '_' + variable.replace(' ', '') + '.pdf'))
    self.canvas[variable].Close()

  def plot(self):

    MiscTool.Print('python_info', '\nCalled plot function.')
    
    for _v in self.variables:

      # Set Canvas 
      self._set_canvas(_v)

      # Setup pads
      self._set_pads(_v)

      # ------ Upper pad: Stack Histogram -------
      self._set_histograms_stack(_v)

      # ------ Lower pad: Ratio Histogram -------
      self._set_histograms_ratio(_v)

      # # Setup graphs_error
      # self._set_graphs_errors(_v) Before uncommenting change function   

      # Setup legends         
      self._set_legends(_v)

      # Setup labels
      self._set_labels(_v)

      # Finally save plot
      self._save_canvas(_v)

  @staticmethod
  def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
    ROOT.gPad.Update()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextColor(ROOT.kBlack)
    text.SetTextSize(text.GetTextSize()*size)
    text.DrawLatex(ndcX,ndcY,txt)
    return text

  @staticmethod
  def histogram_ratio_title_Y_axis(txt='test',ndcX=0,ndcY=0,size=1.0):
    ROOT.gPad.Update()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextColor(ROOT.kBlack)
    text.SetTextAngle(90)
    text.SetTextSize(text.GetTextSize()*size)
    text.DrawLatex(ndcX,ndcY,txt)
    return text   

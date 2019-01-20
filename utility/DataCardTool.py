import os
import copy
import hashlib
import numpy as np

import ROOT

from utility import MiscTool, SampleTool, FileTool

ROOT.gROOT.SetBatch(True)

NORMALIZATION_HISTOGRAM = 'CountWeighted'
# NORMALIZATION_HISTOGRAM = 'CountFullWeighted'

class DataCardTool(object):

    # Templates structure is as below
    # templates[channel][process][name][type]
    # ---------------------------
    # Examples of possible flags
    # [channel] : 'WenHighPt', 'ttWmn', ... NOTE: not config name, but datacard name
    # [process] : 'WH', 'TT', 'Wj0b', 'Wj1b', ...
    # [name]    : 'main', 'CMS_vhbb_puWeight', 'CMS_vhbb_AK04btag_light', 'CMS_vhbb_stats_Top', ...
    # [type]    : 'up', 'down' NOTE: for name != main

  def __init__(self, configuration):

    MiscTool.Print('python_info', '\nCreated instance of DataCardTool class')

    # ------ Paths -------
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_datacards                   = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'datacards') )

    # Configurations
    self.configuration            = configuration
    self.configuration_datacards  = configuration.datacards.datacard

    self.yields                   = {}
    self.templates                = {}

  def get_yields_and_templates(self):

    MiscTool.Print('python_info', '\nCalled get_yields_and_templates function.')

    # Loop over channels
    for _c in self.configuration_datacards['channels']:

      # Channel name which is written in a datacard
      _dc_channel_name = self.configuration_datacards['channels'][_c]['name']

      self.yields[_dc_channel_name]     = {}
      self.templates[_dc_channel_name]  = {}

      MiscTool.Print('status', '\nChannel: {0}'.format(_c))

      # Get samples using SampleTool
      sample_tool = SampleTool.SampleTool( self.configuration, task=_c)

      # Setup for histogram, each channel has its own definition
      _variable      = self.configuration_datacards['channels'][_c]['variable']
      _nbin          = self.configuration_datacards['variables'][_variable]['bin']
      _x_min         = self.configuration_datacards['variables'][_variable]['min']
      _x_max         = self.configuration_datacards['variables'][_variable]['max']
      _variable_tree = self.configuration_datacards['variables'][_variable]['tree variable']

      # Loop over all samples
      for _id, _s in sample_tool.samples.iteritems():

        _f            = _s.file
        _f_Lselection = _s.file_Lselection

        # Get the process name as defined in datacard: e.g. Wj1b, 
        _process = self.configuration_datacards['definitions'][_id]

        # Very very very stupid way of filtering processes
        _bool = any([_pp[0]==_process for _pp in self.configuration_datacards['process']])
        
        if not _bool and not 'data_obs' == _process:
          continue

        # regular normalization factor : xs*L/N*SF
        _weight = '*'.join([_s.weight_expression, _s.normalization_factor[NORMALIZATION_HISTOGRAM]])

        MiscTool.Print('analysis_info', '\nSample:', _id)
        MiscTool.Print('analysis_info', 'Process:', _process)

        # ------------------------------------------------------
        # Get templates and yields without any systematics, etc..

        self._get_main_templates_and_yields(_f, _dc_channel_name, _process, _weight, 
                          _nbin, _x_min, _x_max, _variable_tree)

        # ------------------------------------------------------
        # Get nuisance templates
        if 'data_obs' == _process:
          continue

        # Loop over all nuisance parameters
        for _np, _nc in self.configuration_datacards['nuisance_parameters'].iteritems():

          # Since we are filling here shapes only, skip all nuisance which are not shape
          if not _nc['model'] == 'shape':
            continue 

          # Bin ucertainties are done separately
          if 'bin_uncertainty'  in _nc:
            continue

          # Check if nuisance should be applied to this process
          if not _process in _nc['process']:
            MiscTool.Print('analysis_info', 'Nuisance {1} not used for {0}.'.format(_process, _np),'')
            continue

          MiscTool.Print('analysis_info', 'Nuisance:', _np)

          # Case #1: weight variation only
          if 'weight' in _nc:
            self._get_templates_weight_variation(_f, _dc_channel_name, _process, _s, _np, _nc, _weight, _nbin, _x_min, _x_max, _variable_tree)

          # Case #2: selection variation
          elif 'selection' in _nc:
            self._get_templates_selection_variation(_f_Lselection, _dc_channel_name, _process, _s, _np, _nc, _weight, _nbin, _x_min, _x_max, _variable_tree)

      # This should have its own function
      # ----------------------------------------
      # Nuisance 'bin uncertainty' requires templates(WH,TT, Wj0b, etc) for variation
      # Loop over all nuisances
      MiscTool.Print('status', '\nStarting with bin sys variation!')
      for _np, _nc in self.configuration_datacards['nuisance_parameters'].iteritems():

        # check if nuisance is bin uncertainty
        if not 'bin_uncertainty'  in _nc:
          continue

        MiscTool.Print('analysis_info', 'Nuisance:', _np)

        # Loop over all processes
        for _p in _nc['process']:

          # Loop over all bins
          for _b in xrange(1, _nbin+1):

            if _p in self.templates[_dc_channel_name]:
              dB = self.templates[_dc_channel_name][_p]['main'].GetBinError(_b)    # bin error 
              B  = self.templates[_dc_channel_name][_p]['main'].GetBinContent(_b)  # bin content
            else:
              MiscTool.Print('analysis_info', 'Process {0}, channel {1} is missing in templates.'.format(_p, _dc_channel_name), '')

            # Check bin condition if sys will be applied
            if B <= 0:
              continue

            condition_1 = abs(dB/np.sqrt(B)) > 0.5 and abs(B) > 1
            condition_2 = abs(dB/B) > 0.5 and abs(B) < 1

            if not (condition_1 or condition_2):
              continue
          
            # Loop over up/down variation
            for _sys in ['Up','Down']:

              # New name since each bin and channel sys is independant 
              _nuisance_new = '_'.join([_np, _dc_channel_name, 'bin{0}'.format(_b)])

              _temp_h_name = '_'.join([_dc_channel_name, _p, _nuisance_new + _sys])
              _temp_h      = copy.deepcopy(self.templates[_dc_channel_name][_p]['main'])
              _temp_h.SetName(_temp_h_name)
           
              if _sys == 'Down':
                _temp_h.SetBinContent(_b, max(B-dB,0))
              elif _sys == 'Up':
                _temp_h.SetBinContent(_b, B+dB)

              MiscTool.Print('analysis_info', 'Expected yields {0} bin {1}:'.format(_sys, _b), _temp_h.Integral())

              # In case some of upper template functions is commented
              if not _p in self.templates[_dc_channel_name]:
                self.templates[channel_name][_p] = {}

              # Store histograms and yields but first check if nuisance already in templates
              if _nuisance_new in self.templates[_dc_channel_name][_p]:
                
                # Check if sys type already stored
                if _sys in self.templates[_dc_channel_name][_p][_nuisance_new]:
                  self.templates[_dc_channel_name][_p][_nuisance_new][_sys].Add(_temp_h)
                else:
                  self.templates[_dc_channel_name][_p][_nuisance_new][_sys] = {}
                  self.templates[_dc_channel_name][_p][_nuisance_new][_sys] = copy.deepcopy(_temp_h)

              else:
                self.templates[_dc_channel_name][_p][_nuisance_new] = {}
                self.templates[_dc_channel_name][_p][_nuisance_new][_sys] = copy.deepcopy(_temp_h)

  def _get_main_templates_and_yields(self, root_file, channel_name, process, weight, nbins, xmin, xmax, variable_tree):

    # Open tree and create histogram
    _input = ROOT.TFile.Open( root_file,'read')
    _tree = _input.Get('tree')

    # Create histogram and setup for proper bin error with weighted events
    _temp_h_name =  '_'.join([channel_name, process])
    _temp_h      = ROOT.TH1F( _temp_h_name, _temp_h_name, nbins, xmin, xmax)
    _temp_h.Sumw2()
           
    # Get histogram from the tree directly
    _tree.Draw('{0}>>{1}'.format( variable_tree, _temp_h_name), weight)

    MiscTool.Print('analysis_info', 'Expected yields: ', _temp_h.Integral())

    # Store histograms and yields
    if process in self.yields[channel_name]:
      self.yields[channel_name][process] += _temp_h.Integral()
      self.templates[channel_name][process]['main'].Add(_temp_h)

    else:
      self.yields[channel_name][process]             = _temp_h.Integral()
      self.templates[channel_name][process]          = {}
      self.templates[channel_name][process]['main']  = copy.deepcopy(_temp_h)

    _input.Close()

  def _get_templates_weight_variation(self, root_file, channel_name, process, sample_tool, nuisance, nuisance_parameter_info, weight, nbins, xmin, xmax, variable_tree):
    
    # Open tree
    _input = ROOT.TFile.Open( root_file,'read')
    _tree = _input.Get('tree')

    # Loop over up down variation
    for _sys in ['Up','Down']:

      # Get weight variation string
      _weight_sys = weight.replace( nuisance_parameter_info['weight']['main'], nuisance_parameter_info['weight'][_sys])

      # Apply different normalization factor since some weights were computed using diff norm
      if 'norm' in nuisance_parameter_info:
        _norm_factor_default  = sample_tool.normalization_factor[NORMALIZATION_HISTOGRAM]
        _norm_factor_new      = sample_tool.normalization_factor[nuisance_parameter_info['norm'][_sys]]
        _weight_sys           = _weight_sys.replace( _norm_factor_default, _norm_factor_new)

      # Create histogram
      _temp_h_name =  '_'.join([channel_name, process ,nuisance + _sys])
      _temp_h      = ROOT.TH1F( _temp_h_name, _temp_h_name, nbins, xmin, xmax)

      # Get histogram from the tree directly with new weight
      _tree.Draw('{0}>>{1}'.format( variable_tree, _temp_h_name), _weight_sys)

      MiscTool.Print('analysis_info', 'Expected yields {0}:'.format(_sys), _temp_h.Integral())

      # In case some of upper template functions is commented
      if not process in self.templates[channel_name]:
        self.templates[channel_name][process] = {}

      # Store histograms and yields but first check if nuisance already in templates
      if nuisance in self.templates[channel_name][process]:
        
        # Check if sys type already stored
        if _sys in self.templates[channel_name][process][nuisance]:
          self.templates[channel_name][process][nuisance][_sys].Add(_temp_h)
        else:
          self.templates[channel_name][process][nuisance][_sys] = {}
          self.templates[channel_name][process][nuisance][_sys] = copy.deepcopy(_temp_h)

      else:
        self.templates[channel_name][process][nuisance] = {}
        self.templates[channel_name][process][nuisance][_sys] = copy.deepcopy(_temp_h)

    _input.Close()

  def _get_templates_selection_variation(self, root_file, channel_name, process, sample_tool, nuisance, nuisance_parameter_info, weight, nbins, xmin, xmax, variable_tree):
    # For this function it is necessary that _get_main_templates_and_yields in not commented

    for _sys in ['Up','Down']:
              
      _temp_selection = sample_tool.selection
      # _name_sys   = '_'.join([ _name, _np + _sys])

      # Replace all selection strings
      for _nn, _sel in enumerate(nuisance_parameter_info['selection']['main']):

        _temp_selection = _temp_selection.replace(_sel, nuisance_parameter_info['selection'][_sys][_nn])
      
      _temp_hash      = hashlib.md5( _temp_selection ).hexdigest()

      # File setup
      if '_' in sample_tool.ID:
        _output = os.path.join( self.configuration.paths.path_cache, sample_tool.name + '_' + _temp_hash + '_{0}.root'.format(sample_tool.ID))
      else:
        _output = os.path.join( self.configuration.paths.path_cache, sample_tool.name + '_' + _temp_hash + '.root')

      if not FileTool.FileTool.check_if_file_ok(_output):
        FileTool.FileTool.simple_trim_files( root_file, _output, _temp_selection)

      # Filling histogram
      _file_selection = ROOT.TFile.Open( _output,'read')
      _tree = _file_selection.Get('tree')

      _temp_h_name = '_'.join([channel_name, process, nuisance + _sys])
      _temp_h      = ROOT.TH1F( _temp_h_name, _temp_h_name, nbins, xmin, xmax)

      # Get histogram from the tree directly with new weight
      _tree.Draw('{0}>>{1}'.format( variable_tree, _temp_h_name), weight)

      MiscTool.Print('analysis_info', 'Expected yields {0}:'.format(_sys), _temp_h.Integral())

      # In case some of upper template functions is commented
      if not process in self.templates[channel_name]:
        self.templates[channel_name][process] = {}

      # Store histograms and yields but first check if nuisance already in templates
      if nuisance in self.templates[channel_name][process]:
        
        # Check if sys type already stored
        if _sys in self.templates[channel_name][process][nuisance]:
          self.templates[channel_name][process][nuisance][_sys].Add(_temp_h)
        else:
          self.templates[channel_name][process][nuisance][_sys] = {}
          self.templates[channel_name][process][nuisance][_sys] = copy.deepcopy(_temp_h)

      else:
        self.templates[channel_name][process][nuisance] = {}
        self.templates[channel_name][process][nuisance][_sys] = copy.deepcopy(_temp_h)
  
  def make_datacards_and_templates(self):

    MiscTool.Print('python_info', '\nCalled make_datacards_and_templates function.')

    for _c, _cc in self.configuration_datacards['channels'].iteritems():

      _path_datacard  = os.path.join( self.path_datacards, 'vhbb_{0}_13TeV.txt'.format(_cc['name']))
      _path_template  = os.path.join( self.path_datacards, '{0}.root'.format(_cc['name']))

      # Create datacard
      self._export_datacard( _path_datacard, self.configuration_datacards['datacard_type'], _c, _cc['name'])

      # Create root file with the templates
      self._export_templates( _path_template, _cc['variable'], _cc['name'])

  def _export_datacard(self, path_output, datacard_type, _c, channel):

    MiscTool.Print('python_info', '\nCalled _export_datacard function.')

    _variable = self.configuration_datacards['channels'][_c]['variable']
    _nbin     = self.configuration_datacards['variables'][_variable]['bin']
    _variable = _variable.replace(' ', '')

    # Basic init, num of channels, bkgs, sys
    _datacard = '# WHbb in boosted topology'
    _datacard += '\nimax 1  number of channels'
    _datacard += '\njmax {0}  number of backgrounds'.format( len(self.configuration_datacards['process'])-1)
    
    if self.configuration_datacards['number_of_nuisances'] == '*':
      _datacard += '\nkmax {0}  number of nuisance parameters (sources of systematical uncertainties)'.format('*')
    else:
      _datacard += '\nkmax {0}  number of nuisance parameters (sources of systematical uncertainties)'.format(len(self.configuration_datacards['nuisance_parameters']))

    # Setup shape of variables, inputs, etc
    if datacard_type == 'shape':
      _datacard += '\n------------'
      _datacard += '\nshapes * {0} hists_{0}.root {1}_$CHANNEL_$PROCESS'.format(channel, _variable)
      # If there are nuisance parameters add
      if len(self.configuration_datacards['nuisance_parameters']) > 0:
        _datacard += ' {0}_$CHANNEL_$PROCESS_$SYSTEMATIC'.format(_variable)

    # Data yields
    _datacard += '\n------------'
    _datacard += "\n# 1 channel, each with it's number of observed events"
    _datacard += '{0:20s}'.format('\nbin') + '{0:10s}'.format(channel)
    if 'data_obs' in self.yields[channel]:
      _datacard += '{0:20s}{1:10s}'.format('\nobservation', str(self.yields[channel]['data_obs']))
    else:
      _datacard += '{0:10s}'.format('0')

    _datacard += '\n------------'

    # MC yields
    _datacard += '\n# now we list the expected events for signal and all backgrounds in those bins'
    _datacard += '\n# the second process line must have a positive number for backgrounds, and 0 for signal'
    _datacard += '{0:50s}'.format('\nbin')      + ''.join([ '{0:10s}'.format(channel)*(len(self.configuration_datacards['process']))])
    _datacard += '{0:50s}'.format('\nprocess')  + ''.join([ '{0:10s}'.format(_p[0]) for _p in self.configuration_datacards['process']])
    _datacard += '{0:50s}'.format('\nprocess')  + ''.join([ '{0:10s}'.format(_p[1]) for _p in self.configuration_datacards['process']])
    # Numbers
    _datacard += '{0:50s}'.format('\nrate')     + ''.join([ '{0:10s}'.format( format(self.yields[channel][_p[0]], '.2f') ) for _p in self.configuration_datacards['process']])
    _datacard += '\n------------'

    _list_nuisance_alphabetically = sorted(self.configuration_datacards['nuisance_parameters'])

    # ----------------------------------------------------------
    # Nuisance parameters
    for _n in _list_nuisance_alphabetically:

      _np = self.configuration_datacards['nuisance_parameters'][_n]

      # If special treatment needed for particular channel/process
      if 'special' in _np:
        pass

      elif 'bin_uncertainty' in _np:
        pass

        # There is on process per sys by definition
        _process = _np['bin_uncertainty']
        _channel = channel

        # Loop over bins
        for _b in xrange(1,_nbin+1):        
        
          _nuisance_new = '_'.join([_n, _channel, 'bin{0}'.format(_b)])

          # Check if sys bin passed the criteria
          if not _nuisance_new in self.templates[_channel][_process]:
            continue

          # Nuisance name
          _datacard += '{0:40s}{1:10s}'.format('\n' + _nuisance_new, _np['model'])
          # Contribution to which processes
          _datacard += ''.join([ '{0:10s}'.format(str( _np['process'][_p[0]])) if _p[0] == _process else '{0:10s}'.format('-')  
                        for _p in self.configuration_datacards['process']])
          _datacard += _np['description']

      # Standard procedure
      else:
        _datacard += '{0:40s}{1:10s}'.format('\n'+_n, _np['model'])
        _datacard += ''.join([ '{0:10s}'.format(str( _np['process'][_p[0]])) if _p[0] in _np['process'] else '{0:10s}'.format('-')
                      for _p in self.configuration_datacards['process']])
        _datacard += _np['description']


    if self.configuration_datacards['SF_samples_apply']:
      _datacard += '\n------------\n'
      _datacard += self.configuration_datacards['SF_samples_string'].replace('<channel>', channel)

    # Stat uncertainty
    if self.configuration_datacards['auto_sys_uncertainty_apply']:
      _datacard += '\n------------\n'
      _datacard += self.configuration_datacards['auto_sys_uncertainty_string']

    # Save datacard
    with open(path_output, 'w') as _f:
      _f.write(_datacard)

    MiscTool.Print('status', 'Datacard saved as {0}'.format(path_output))
    print _datacard

  def _export_templates(self, path_output, variable, channel):

    MiscTool.Print('python_info', '\nCalled _export_templates function.')

    _output_name  = os.path.join(self.path_datacards, 'hists_{0}.root'.format(channel))
    _output       = ROOT.TFile.Open( _output_name, 'recreate')
    _variable     = variable.replace(' ','')

    _templates_flatten = {}
    self._dictionary_flatten(self.templates[channel], _templates_flatten)

    _list_templates_alphabetically = sorted(_templates_flatten)

    for _t in _list_templates_alphabetically:

      _new_name = _variable + '_' + _t
      _templates_flatten[_t].SetName(_new_name)
      _templates_flatten[_t].Write()
      MiscTool.Print('analysis_info', 'Exporting template:', _new_name)

    _output.Close()

    MiscTool.Print('status', 'Templates saved in {0}'.format(_output_name))

  def _dictionary_flatten(self, dictionary, flatten_dictionary):
    for k, v in dictionary.iteritems():
      if isinstance(v, dict):
        self._dictionary_flatten(v, flatten_dictionary)
      else:
        # print "{0} : {1}".format(v.GetName(), v.Integral())
        flatten_dictionary[v.GetName()] = v
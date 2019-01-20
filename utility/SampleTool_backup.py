import os
import hashlib

import ROOT

from utility import MiscTool
from utility import FileTool
from utility import WeightTool

NORMALIZATION_HISTOGRAM = 'CountWeighted'
# NORMALIZATION_HISTOGRAM = 'CountFullWeighted'

class SampleTool(object):

  def __init__(self, configuration, task=None):

    MiscTool.Print('python_info', '\nCreated instance of SampleTool class')

    self.force_all        = configuration.general.force_all
    self.postfit          = configuration.general.postfit_plot
    if task:
      self.task_name      = task
    else:
      self.task_name      = configuration.general.task_name
    self.luminosity       = configuration.general.luminosity

    self.split_samples    = configuration.plots.task[self.task_name]['split_samples']

    # ------ Paths -------
    self.path_working_directory           = configuration.paths.path_working_directory
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_cache                       = configuration.paths.path_cache

    # Convert IDs to samples
    self.list_of_IDs                      = configuration.samples.task[self.task_name]
    self.list_of_samples                  = MiscTool.ID_sample_dictionary( self.list_of_IDs, configuration.samples)
    self.info_samples                     = configuration.samples.samples_list

    self.selection_L                      = [configuration.selection.hierarchy[_s] for _s in configuration.selection.task[self.task_name]] 
    self.selection                        = self.selection_L + [configuration.selection.task_definitions[self.task_name]]
    self.selection_subsamples             = configuration.selection.subsamples

    # Load C functions
    ROOT.gROOT.ProcessLine('.L {0}/utility/utility_C.h'.format(self.path_working_directory))
    # print ROOT.deltaPhi(1,2)

    MiscTool.Print('analysis_info', 'Task:', self.task_name)
    MiscTool.Print('analysis_info', 'Force all:', self.force_all)
    MiscTool.Print('analysis_info', 'Split samples:', self.split_samples)
    MiscTool.Print('analysis_info', 'New files will be stored in:', self.path_cache)
    MiscTool.Print('analysis_info', 'Analysis working directory:', self.path_analysis_working_directory)
    MiscTool.Print('analysis_info_list', 'List of samples:', self.list_of_samples)

    # ------ Weights -------
    self.weights          = configuration.weights.weights
    self.load_weight_C_functions()
    self.datacards        = configuration.datacards.datacard

    # ------ Samples -------
    self.samples      = {}
    # First you need to initalize samples
    self.initialize_samples()
    # Second, set_sample_files
    self.set_samples_files()
    # Set the number of all weighted events in each sample
    self.set_samples_number_of_all_events()
    # Set the normalization factor for each sample
    self.set_samples_normalization_factor()
    # Set weights
    self.set_samples_weight_expression()

  def load_weight_C_functions(self):
  
    MiscTool.Print('python_info', '\nCalled load_weight_C_functions function.')

    for _w in self.weights.values():

      # Check if this weight has C function
      if 'C' in _w:
        try:
          ROOT.gROOT.ProcessLine('.L {0}/{1}'.format(os.path.join( self.path_analysis_working_directory, 'results/weights'), _w['C']))
          MiscTool.Print('analysis_info', 'Loaded successfully: ', format(_w['C']))
        except Exception, e:
          MiscTool.Print('error', 'Failed to load {0}.'.format(_w['C']))

  def initialize_samples(self):

    MiscTool.Print('python_info', '\nCalled initialize_samples function.')

    # Split samples if needed
    if self.split_samples:
      
      for _s in self.list_of_samples:

        # Check if files has subsamples
        if 'sub' in self.info_samples[_s]:

          # Add all the subsamples
          for _ss in self.info_samples[_s]['sub']:
            
            _sf_type = self.datacards['definitions'][_ss]

            if _sf_type in self.datacards['SF'] and self.postfit:
              _sf = self.datacards['SF'][_sf_type]
            else:
              _sf = 1.0
            
            self.samples[_ss] = Sample( _s, _ss, self.info_samples[_s]['types'], self.info_samples[_s]['xsec'])

        # Just add sample as it is
        else:
          
          _sf_type = self.datacards['definitions'][self.info_samples[_s]['ID']]

          if _sf_type in self.datacards['SF'] and self.postfit:
            _sf = self.datacards['SF'][_sf_type]
          else:
            _sf = 1.0          

          self.samples[self.info_samples[_s]['ID']] = Sample( _s, self.info_samples[_s]['ID'], self.info_samples[_s]['types'], self.info_samples[_s]['xsec']*_sf)

    # Just add samples without spliting
    else:

      for _s in self.list_of_all_samples:

        _sf_type = self.datacards['definitions'][self.info_samples[_s]['ID']]

        if _sf_type in self.datacards['SF'] and self.postfit:
          _sf = self.datacards['SF'][_sf_type]
        else:
          _sf = 1.0   

        self.samples[self.info_samples[_s]['ID']] = Sample( _s, self.info_samples[_s]['ID'], self.info_samples[_s]['types'], self.info_samples[_s]['xsec'])

  def set_samples_files(self):

    MiscTool.Print('python_info', '\nCalled set_samples_files function.')  

    _final_hash = hashlib.md5( ''.join(self.selection) ).hexdigest()
    _l_hash     = hashlib.md5( ''.join(self.selection_L) ).hexdigest()

    for _s in self.samples:

      # file with L selection only
      self.samples[_s].file_Lselection = os.path.join( self.path_cache, self.samples[_s].name + '_' + _l_hash + '.root')
      self.samples[_s].selection = ' && '.join(self.selection)

      # Subsample case
      if '_' in _s:
        
        _input  = os.path.join( self.path_cache, self.samples[_s].name + '_' + _final_hash + '.root')
        _output = os.path.join( self.path_cache, self.samples[_s].name + '_' + _final_hash + '_{0}.root'.format(_s))
        _cut    = self.selection_subsamples[_s.split('_')[-1]]
        self.samples[_s].selection += ' && ' + _cut

        if not FileTool.FileTool.check_if_file_ok(_output):
          FileTool.FileTool.simple_trim_files( _input, _output, _cut)

        if not FileTool.FileTool.check_if_file_ok(_output):
          MiscTool.Print('error', 'Problem with {0}'.format(_output))
        else:
          self.samples[_s].file = _output          

      # Just add sample
      else:
        self.samples[_s].file = os.path.join( self.path_cache, self.samples[_s].name + '_' + _final_hash + '.root')

      MiscTool.Print('analysis_info', 'Files used:', '{0}'.format(self.samples[_s].file))  

  def set_samples_number_of_all_events(self):

    MiscTool.Print('python_info', '\nCalled set_samples_number_of_all_events function.')

    # _normalizations = eval(open(os.path.join( self.path_working_directory, 'results', self.analysis_name, 'weights', 'total_number_of_events.py')).read())

    for _s in self.samples:

      _sample = self.samples[_s].name

      # Skip if sample is data type
      if self.samples[_s].types == 'data':
        continue
          
      try:
 
        # Get total number of events for this sample
        _file   = ROOT.TFile.Open( self.samples[_s].file,'read')

        self.samples[_s].number_of_all_events[NORMALIZATION_HISTOGRAM]  = _file.Get(NORMALIZATION_HISTOGRAM).GetBinContent(1)       
        
        for _lhe in xrange(6):
          _bin = _file.Get('CountWeightedLHEWeightScale').FindBin(_lhe)
          self.samples[_s].number_of_all_events['CountWeightedLHEWeightScale_{0}'.format(_lhe)] = _file.Get('CountWeightedLHEWeightScale').GetBinContent(_bin)
        
        _file.Close()
        
        # From the file which was manually made
        # self.samples[_s].number_of_all_events = _normalizations[_sample]
      
        # print '\n', _s
        # print 'Count: ', self.samples[_s].number_of_all_events
        # print 'My normalization: ', _normalizations[_sample]

      except Exception, e:
        MiscTool.Print('error', 'Problem with loading: {0}'.format(_sample))
        raise

  def set_samples_normalization_factor(self):

    MiscTool.Print('python_info', '\nCalled set_samples_normalization_factor function.')

    _luminosity = self.luminosity

    for _s in self.samples:

      MiscTool.Print('analysis_info', '\n' + _s, '')

      if self.samples[_s].types == 'mc':

        _x_sec  = self.samples[_s].xsec

        # Default normalization
        try:
          self.samples[_s].normalization_factor[NORMALIZATION_HISTOGRAM]  = str(_luminosity*_x_sec/self.samples[_s].number_of_all_events[NORMALIZATION_HISTOGRAM])
          MiscTool.Print('analysis_info', NORMALIZATION_HISTOGRAM, self.samples[_s].normalization_factor[NORMALIZATION_HISTOGRAM])
        except Exception, e:
          self.samples[_s].normalization_factor[ NORMALIZATION_HISTOGRAM]  = str(0.0)
          MiscTool.Print('error', '{0}_{1} Normalization set to 0.0'.format( NORMALIZATION_HISTOGRAM, _lhe))
        
        # LHE normalization for systematics
        for _lhe in xrange(6):

          _lhe_string = 'CountWeightedLHEWeightScale_{0}'.format(_lhe)

          try:
            self.samples[_s].normalization_factor[ _lhe_string] = str(_luminosity*_x_sec/self.samples[_s].number_of_all_events[_lhe_string])
            MiscTool.Print('analysis_info', _lhe_string, self.samples[_s].normalization_factor[_lhe_string] )
          except Exception, e:
            self.samples[_s].normalization_factor[_lhe_string] = str(0.0)
            MiscTool.Print('error', '{0} Normalization set to 0.0'.format(_lhe_string))
          
      else:
        self.samples[_s].normalization_factor[ NORMALIZATION_HISTOGRAM] = str(1.0)

  def set_samples_weight_expression(self):

    MiscTool.Print('python_info', '\nCalled set_samples_weight_expression function.')

    for _id, _s in self.samples.iteritems():
    
      _s.weight_expression = WeightTool.WeightTool.weight_handler( _s, self.weights)

      MiscTool.Print('analysis_info', _id + ' weight string:', _s.weight_expression )

class Sample(object):
  ''' Class which contains all info about particular sample '''

  def __init__(self, name, ID, types, xsec):

    self.name             = name
    self.ID               = ID
    self.types            = types
    self.xsec             = xsec

    self.selection            = None
    self.file_Lselection      = None
    self.file                 = None 
    self.number_of_all_events = {}
    self.normalization_factor = {}
    self.weight_expression    = None

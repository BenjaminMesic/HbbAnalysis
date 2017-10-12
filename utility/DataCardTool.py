import os

import ROOT

from utility import MiscTool

ROOT.gROOT.SetBatch(True)

class DataCardTool(object):
  
  def __init__(self, configuration):

    MiscTool.Print('python_info', '\nCreated instance of DataCardTool class')

    # ------ Paths -------
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_datacards                   = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'datacards') )
    MiscTool.make_directory(self.path_datacards)

    # ------ Datacard Config -------
    self.configuration            = configuration.datacards.datacard

    self.yields                   = {}
    self.templates                = {}

  def get_yields_and_templates(self):

    MiscTool.Print('python_info', '\nCalled set_observations_and_templates function.')

    for _c in self.configuration['channels']:
      
      MiscTool.Print('status', '\nChannel: {0}'.format(_c))

      self.yields[_c] = {}
      self.templates[_c] = {}

      _input_file  = ROOT.TFile.Open( self.configuration['input_files'][_c], 'read')
      _dirlist     = _input_file.GetListOfKeys()
    
      iter = _dirlist.MakeIterator()
      _key = iter.Next()

      while _key:
        
        _histogram = _input_file.Get(_key.GetName())
        _histogram.SetDirectory(0)

        _var, _id  = _key.GetName().split('__')

        if _id not in self.configuration['definitions']:
          MiscTool.Print('error', '{0} not in datacard definitions.'.format(_id))
          _key = iter.Next()
          continue

        _process   = self.configuration['definitions'][_id]

        # Make sure that you are using correct histograms for yield extraction
        if _var == self.configuration['variable']:

          # Adding yields
          if _process not in self.yields[_c]:              
              self.yields[_c][_process] = _histogram.Integral()
          else:
              self.yields[_c][_process] += _histogram.Integral()

        # Adding templates for root file
        if _var.replace('Up', '').replace('Down', '') in self.configuration['nuisance_parameters'] or _var == self.configuration['variable']:

          if _process not in self.templates[_c]:
              self.templates[_c][_process] = _histogram.Clone()
              self.templates[_c][_process].SetDirectory(0)

              # Set names following the COMBINE convetion
              if _var == self.configuration['variable']:
                self.templates[_c][_process].SetName(_process)
              elif 'Up' in _var or 'Down' in _var:
                self.templates[_c][_process].SetName(_process + '_' + _var)

          else:
              self.templates[_c][_process].Add(_histogram)
              self.templates[_c][_process].SetDirectory(0)

        else:
          MiscTool.Print('error', '{0} not used.'.format(_var))

        MiscTool.Print('analysis_info', 'Sample: {0} {1}'.format(_id, _process), 'Yield: {0}'.format(_histogram.Integral()))

        _key = iter.Next()

      # DATA Added manually but this need to be changed once we have data
      self.templates[_c]['data_obs'] = self.templates[_c]['WH'].Clone()
      self.templates[_c]['data_obs'].SetName('data_obs')
      self.templates[_c]['data_obs'].SetDirectory(0)
      self.templates[_c]['data_obs'].Scale(0)

  def make(self):

    MiscTool.Print('python_info', '\nCalled make function.')

    _path_datacard  = os.path.join( self.path_datacards, self.configuration['datacard_name'])
    _path_template  = os.path.join( self.path_datacards, self.configuration['template_name'])

    # Create datacard
    self._datacard( _path_datacard, self.configuration['datacard_type'])

    # Create root file with the templates
    self._templates( _path_template, self.configuration['datacard_type'])

  def _datacard(self, path_output, datacard_type):

    MiscTool.Print('python_info', '\nCalled _datacard function.')

    _datacard = '# WHbb in boosted topology'
    _datacard += '\nimax {0}  number of channels'.format(self.configuration['number_of_channels'])
    _datacard += '\njmax {0}  number of backgrounds'.format(self.configuration['number_of_backgrounds'])
    _datacard += '\nkmax {0}  number of nuisance parameters (sources of systematical uncertainties)'.format(self.configuration['number_of_nuisance_parameters'])

    if datacard_type == 'shape':
      _datacard += '\n------------'
      _datacard += '\nshapes * * {0} $PROCESS '.format(self.configuration['template_name'])
      # If there are nuisance parameteres add
      if self.configuration['number_of_nuisance_parameters'] > 0:
        _datacard += '$PROCESS_$SYSTEMATIC'

    _datacard += '\n------------'
    _datacard += "\n# {0} channels, each with it's number of observed events".format(self.configuration['number_of_channels'])
    _datacard += '{0:20s}'.format('\nbin') + ''.join([ '{0:10s}'.format(_c) for _c in self.configuration['channels']])
    _datacard += '{0:20s}'.format('\nobservation') + ''.join([ '{0:10s}'.format(str(_c)) if 'data' in self.yields[_c] else '{0:10s}'.format(str(0))
                    for _c in self.configuration['channels']])
    _datacard += '\n------------'


    print self.configuration['process']

    print self.configuration['channels']
    print self.yields

    _datacard += '\n# now we list the expected events for signal and all backgrounds in those bins'
    _datacard += '\n# the second process line must have a positive number for backgrounds, and 0 for signal'
    _datacard += '{0:20s}'.format('\nbin')      + ''.join([ '{0:10s}'.format(_c)*(self.configuration['number_of_backgrounds']+1) for _c in self.configuration['channels']])
    _datacard += '{0:20s}'.format('\nprocess')  + ''.join([ '{0:10s}'.format(_p[0]) for _c in self.configuration['channels'] for _p in self.configuration['process']])
    _datacard += '{0:20s}'.format('\nprocess')  + ''.join([ '{0:10s}'.format(_p[1]) for _c in self.configuration['channels'] for _p in self.configuration['process']])
    _datacard += '{0:20s}'.format('\nrate')     + ''.join([ '{0:10s}'.format( format(self.yields[_c][_p[0]], '.2f') ) 
                    for _c in self.configuration['channels'] for _p in self.configuration['process']])
    _datacard += '\n------------'

    for _n,_nn in self.configuration['nuisance_parameters'].iteritems():
      _datacard += '{0:14s}{1:6s}'.format('\n'+_n, _nn['model']) + ''.join([ '{0:10s}'.format(str( _nn['process'][_p[0]])) if _p[0] in _nn['process'] else '{0:10s}'.format('-')  
                      for _c in self.configuration['channels'] for _p in self.configuration['process']])
      _datacard += _nn['description']

    # Save datcard
    with open(path_output, 'w') as _f:
      _f.write(_datacard)

    MiscTool.Print('status', 'Datacard saved as {0}'.format(path_output))
    print _datacard

  def _templates(self, path_output, datacard_type):
 
    MiscTool.Print('python_info', '\nCalled _templates function.')

    if not datacard_type == 'shape':
      return False

    else:
      
      # Histograms will be saved in new root file
      _output      = ROOT.TFile.Open( path_output, 'recreate')

      for _c in self.templates:

        for _t, _h in self.templates[_c].iteritems():
          
          MiscTool.Print('analysis_info', 'Process: {0}'.format(_h.GetName()), 'Yield: {0}'.format(_h.Integral()))

          _h.Write()

      _output.Close()

    MiscTool.Print('status', 'Templates saved as {0}'.format(path_output))
import os
import json

import ROOT

from utility import MiscTool

ROOT.gROOT.SetBatch(True)

class WeightTool(object):
  '''

  ---- Explanation of weight as Draw parameter ----
  Selection = "weight *(boolean expression)"
  If the Boolean expression evaluates to true,
  the histogram is filled with a weight.
  If the weight is not explicitly specified it is assumed to be 1.

  '''

  def __init__(self, configuration):

    MiscTool.Print('python_info', '\nCreated instance of WeightTool class')

    self.task_name = configuration.general.task_name

    # self.analysis_name  = analysis_name
    # self.configuration  = configuration

    # ------ Paths -------
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_source                      = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'aux', 'weights'))
    self.path_results                     = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'weights'))

    # ------ Weights -------
    self.weights                = configuration.weights.weights

  @staticmethod
  def weight_handler( sample, configuration_weights):
    ''' Function used to get all weights and return string for Draw function'''

    _weight = '1'

    for _w in configuration_weights.values():

      if _w['samples'] == 'all':
        _weight += '*' + _w['weight']

      if _w['samples'] == 'all_but_data' and sample.types != 'data':
        _weight += '*' + _w['weight']

      if sample.ID in _w['samples']:
        _weight += '*' + _w['weight']

      # else:
      #   pass

    return _weight

  # ----------------- Pile Up ---------------------
  def pile_up_handler(self):
    ''' Function used to calculate pile_up weights and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled pile_up_distribution_handler function.')
    
    # Load MC/data files which are defined in configuration files 
    try:
      _name_mc  = self.weights['pile_up']['mc']
      _file_mc  = ROOT.TFile.Open( _name_mc,'read')
      _hist_mc  = _file_mc.Get('pileup')
      _hist_mc.Scale( 1.0 / _hist_mc.Integral())

      _name_data  = self.weights['pile_up']['data']     
      _file_data  = ROOT.TFile.Open( _name_data,'read')   
      _hist_data  = _file_data.Get('pileup')
      _hist_data.Scale( 1.0 / _hist_data.Integral() )

      MiscTool.Print('analysis_info', 'Successfully Opened: ', _name_mc)
      MiscTool.Print('analysis_info', 'Successfully Opened: ', _name_data)
    
    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with mc/data files.')
      raise

    # Some checks to see if everything is fine with histograms
    if not _hist_mc.GetNbinsX() == _hist_data.GetNbinsX():
      raise ValueError('data and mc histograms must have the same number of bins')
    if not _hist_mc.GetXaxis().GetXmin() == _hist_data.GetXaxis().GetXmin():
      raise ValueError('data and mc histograms must have the same xmin')
    if not _hist_mc.GetXaxis().GetXmax() == _hist_data.GetXaxis().GetXmax():
      raise ValueError('data and mc histograms must have the same xmax')

    _nBin     = _hist_mc.GetNbinsX()
    _x_min_bin  = _hist_mc.GetXaxis().GetXmin()
    _x_max_bin  = _hist_mc.GetXaxis().GetXmax()
    _dx     = 1.0*( _x_max_bin - _x_min_bin)/_nBin

    # Here we calculate weights bin by bin
    _weights = []
    for _n in xrange(_nBin):

      _puWeight = 1

      _bin = _hist_data.FindBin(_n)

      if _bin < 1. or _bin > _nBin:
        _puWeight = 0
      else:
        _data = _hist_data.GetBinContent(_bin)
        _mc   = _hist_mc.GetBinContent(_bin)
        if not _mc == 0.0:
          _puWeight = _data/_mc
        else:
          _puWeight = 1

      _weights.append( [_x_min_bin + _n*_dx, _x_min_bin + (_n+1)*_dx, _puWeight ])

      MiscTool.Print('status', '#PU: {0}  weight = {1}'.format( _n, _puWeight))

    # # alternative: put ratio of histogram in one new histo
    # weight_distribution = _hist_data.Clone("puWeights")
    # weight_distribution.Divide(_hist_mc)
    # puWeight2 = weight_distribution.GetBinContent(_bin)

    # Create and save C code
    _code = self._pile_up_C_writer(_weights)
    self._save_C_code( self.weights['pile_up']['C'], _code)

  def _pile_up_C_writer(self, weights):
    ''' This function is used to make C function using dictionary of pile up weights.'''

    _code = 'double pile_up(float n)\n{\n'

    # Boundary case
    _code += '  if (n < {0})\n'.format(0)
    _code += '    ' +  'return {0}'.format(1) + ';\n'

    for _w in weights:

      if _w[1] <= 37:
        _code += '  else if (n < {0})\n'.format(_w[1])
        _code += '    ' +  'return {0}'.format(_w[2]) + ';\n'
      # boundary case
      else:
        _code += '  else \n'
        _code += '    ' +  'return {0}'.format(_w[2]) + ';\n'
        break

    _code += '\n}'

    return _code

  # ----------------- Top ---------------------
  def gen_pt_top_handler(self):

    MiscTool.Print('python_info', '\nCalled gen_pt_top_handler function.')

    # Create and save C code
    _code = self.gen_pt_top_C_writer()
    self._save_C_code( self.weights['gen_pt_top']['C'], _code)

  def gen_pt_top_C_writer(self):

    MiscTool.Print('python_info', '\nCalled gen_pt_top_C_writer function.')

    _code = '#include <math.h>\n'
    # _code += '#include <stdio.h>\n\n'

    _code += 'double gen_pt_top( double pt_t, double pt_at)\n{\n'
    # _code += 'cout << exp(pt_t) << endl;\n'
    _code += '    ' +  'return sqrt(exp(0.0615 - 0.0005*pt_t)*exp(0.0615 - 0.0005*pt_at))' + ';\n'

    _code += '\n}'

    return _code

  # ----------------- Muons ---------------------
  def scale_factor_muon_ID_handler(self):
    ''' Function used to calculate muon ID scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_muon_ID_handler function.')

    try:

      _files = self.weights['scale_factor_muon_ID']['file']
      _type  = self.weights['scale_factor_muon_ID']['type']

      # There are different number of two run intervals
      _input = {}
      
      for _f in _files:
        
        _input[_f] = eval(open(_f).read())[_type]['pt_abseta_ratio']
        MiscTool.Print('analysis_info', 'Successfully Opened: ', _f)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with opening file{0}'.format(_f))
      raise

    # Get scale factors for all eta pt bins and all types, i.e. run intervals
    _scale_factors = {}

    for _f, _sf in _input.iteritems():

      _scale_factors[_f] = {}

      for _etab, _ptbins in _sf.iteritems():
        
        _eta_bin = _etab.split('[', 1)[1].split(']')[0]
        _scale_factors[_f][_eta_bin] = {}

        for _ptb, _sf in _ptbins.iteritems():

          _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
          _scale_factors[_f][_eta_bin][_pt_bin] = _sf

    _code = self._scale_factor_muon_ID_C_writer( _scale_factors)
    self._save_C_code(self.weights['scale_factor_muon_ID']['C'], _code)

  def _scale_factor_muon_ID_C_writer(self, scale_factors):

    _files = self.weights['scale_factor_muon_ID']['file']

    # function name
    _code = 'double scale_factor_muon_ID(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 13)\n    return 1;\n\n' 

    # All files have the same structure so it is ok to just make one for loop
    for _ptb, _etabins in scale_factors[scale_factors.keys()[0]].iteritems():

      _pt_min, _pt_max = _ptb.split(',')
      _code += '  if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
      _code += '  {\n' # opening bracket 

      for _etab in _etabins:
 
        # Loop over all files to get sf
        _sf = 0
        for _f, _f_w in _files.iteritems():
          _sf += float(scale_factors[_f][_ptb][_etab]['value'])*float(_f_w)

        # Add eta if statement
        _eta_min, _eta_max = _etab.split(',')
        _code += '    if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
        # _code += '    {\n' # opening bracket

        _code += '      return {0};\n'.format(_sf)

      # if eta not in any bin then return 1
      _code += '    else\n      return 1;\n'

      _code += '  }\n'

    # case if pt > max pt and closing bracket for eta if statement
    _code += '  else\n   return 1;\n'    
    _code += '}\n'

    return _code

  def scale_factor_muon_iso_handler(self):
    ''' Function used to calculate muon Iso scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_muon_iso_handler function.')

    try:

      _files = self.weights['scale_factor_muon_iso']['file']
      _type  = self.weights['scale_factor_muon_iso']['type']

      # There are different number of two run intervals
      _input = {}
      
      for _f in _files:
        
        _input[_f] = eval(open(_f).read())[_type]['pt_abseta_ratio']
        MiscTool.Print('analysis_info', 'Successfully Opened: ', _f)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with opening file{0}'.format(_f))
      raise

    # Get scale factors for all eta pt bins and all types, i.e. run intervals
    _scale_factors = {}

    for _f, _sf in _input.iteritems():

      _scale_factors[_f] = {}

      for _etab, _ptbins in _sf.iteritems():
        
        _eta_bin = _etab.split('[', 1)[1].split(']')[0]
        _scale_factors[_f][_eta_bin] = {}

        for _ptb, _sf in _ptbins.iteritems():

          _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
          _scale_factors[_f][_eta_bin][_pt_bin] = _sf

    _code = self._scale_factor_muon_iso_C_writer( _scale_factors)
    self._save_C_code(self.weights['scale_factor_muon_iso']['C'], _code)

  def _scale_factor_muon_iso_C_writer(self, scale_factors ):

    _files = self.weights['scale_factor_muon_iso']['file']

    # function name
    _code = 'double scale_factor_muon_iso(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 13)\n    return 1;\n\n' 

    # All files have the same structure so it is ok to just make one for loop
    for _ptb, _etabins in scale_factors[scale_factors.keys()[0]].iteritems():

      _pt_min, _pt_max = _ptb.split(',')
      _code += '  if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
      _code += '  {\n' # opening bracket 

      for _etab in _etabins:
 
        # Loop over all files to get sf
        _sf = 0
        for _f, _f_w in _files.iteritems():
          _sf += float(scale_factors[_f][_ptb][_etab]['value'])*float(_f_w)

        # Add eta if statement
        _eta_min, _eta_max = _etab.split(',')
        _code += '    if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
        # _code += '    {\n' # opening bracket

        _code += '      return {0};\n'.format(_sf)

      # if eta not in any bin then return 1
      _code += '    else\n      return 1;\n'

      _code += '  }\n'

    # case if pt > max pt and closing bracket for eta if statement
    _code += '  else\n   return 1;\n'    
    _code += '}\n'

    return _code

  def scale_factor_muon_trk_handler(self):
    ''' Function used to calculate muon trk scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_muon_trk_handler function.')

    try:

      _files = self.weights['scale_factor_muon_trk']['file']
      _type  = self.weights['scale_factor_muon_trk']['type']

      # There are different number of two run intervals
      _input = {}
      
      for _f in _files:
        
        _input[_f] = eval(open(_f).read())[_type]['pt_eta_ratio']
        MiscTool.Print('analysis_info', 'Successfully Opened: ', _f)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with opening file{0}'.format(_f))
      raise

    # Get scale factors for all eta pt bins and all types, i.e. run intervals
    _scale_factors = {}

    for _f, _sf in _input.iteritems():

      _scale_factors[_f] = {}

      for _etab, _ptbins in _sf.iteritems():
        
        _eta_bin = _etab.split('[', 1)[1].split(']')[0]
        _scale_factors[_f][_eta_bin] = {}

        for _ptb, _sf in _ptbins.iteritems():

          _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
          _scale_factors[_f][_eta_bin][_pt_bin] = _sf

    _code = self._scale_factor_muon_trk_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_muon_trk']['C'], _code)

  def _scale_factor_muon_trk_C_writer(self, scale_factors):

    _files = self.weights['scale_factor_muon_trk']['file']

    # function name
    _code = 'double scale_factor_muon_trk(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 13)\n    return 1;\n\n' 

    # All files have the same structure so it is ok to just make one for loop
    for _ptb, _etabins in scale_factors[scale_factors.keys()[0]].iteritems():

      _pt_min, _pt_max = _ptb.split(',')
      _code += '  if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
      _code += '  {\n' # opening bracket 

      for _etab in _etabins:
 
        # Loop over all files to get sf
        _sf = 0
        for _f, _f_w in _files.iteritems():
          _sf += float(scale_factors[_f][_ptb][_etab]['value'])*float(_f_w)

        # Add eta if statement
        _eta_min, _eta_max = _etab.split(',')
        _code += '    if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
        # _code += '    {\n' # opening bracket

        _code += '      return {0};\n'.format(_sf)

      # if eta not in any bin then return 1
      _code += '    else\n      return 1;\n'

      _code += '  }\n'

    # case if pt > max pt and closing bracket for eta if statement
    _code += '  else\n   return 1;\n'    
    _code += '}\n'

    return _code

  def scale_factor_muon_trigger_handler(self):
    ''' Function used to calculate single muon trigger efficiencies and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_muon_trigger_handler function.')

    try:

      _files = self.weights['scale_factor_muon_trigger']['file']
      _type  = self.weights['scale_factor_muon_trigger']['type']

      # There are different number of two run intervals
      _input = {}
      
      for _f in _files:
        
        _input[_f] = eval(open(_f).read())[_type]['pt_abseta_ratio']
        MiscTool.Print('analysis_info', 'Successfully Opened: ', _f)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with opening file{0}'.format(_f))
      raise

    # Get scale factors for all eta pt bins and all types, i.e. run intervals
    _scale_factors = {}

    for _f, _sf in _input.iteritems():

      _scale_factors[_f] = {}

      for _etab, _ptbins in _sf.iteritems():
        
        _eta_bin = _etab.split('[', 1)[1].split(']')[0]
        _scale_factors[_f][_eta_bin] = {}

        for _ptb, _sf in _ptbins.iteritems():

          _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
          _scale_factors[_f][_eta_bin][_pt_bin] = _sf

    # Create C function and save it
    _code = self._scale_factor_muon_trigger_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_muon_trigger']['C'], _code)

  def _scale_factor_muon_trigger_C_writer(self, scale_factors):
    ''' This function is used to make C function using dictionary of scale factors.'''

    _files = self.weights['scale_factor_muon_trigger']['file']

    # function name
    _code = 'double scale_factor_muon_trigger(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 13)\n    return 1;\n\n' 

    # All files have the same structure so it is ok to just make one for loop
    for _ptb, _etabins in scale_factors[scale_factors.keys()[0]].iteritems():

      _pt_min, _pt_max = _ptb.split(',')
      _code += '  if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
      _code += '  {\n' # opening bracket 

      for _etab in _etabins:
 
        # Loop over all files to get sf
        _sf = 0
        for _f, _f_w in _files.iteritems():
          _sf += float(scale_factors[_f][_ptb][_etab]['value'])*float(_f_w)

        # Add eta if statement
        _eta_min, _eta_max = _etab.split(',')
        _code += '    if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
        # _code += '    {\n' # opening bracket

        _code += '      return {0};\n'.format(_sf)

      # if eta not in any bin then return 1
      _code += '    else\n      return 1;\n'

      _code += '  }\n'

    # case if pt > max pt and closing bracket for eta if statement
    _code += '  else\n   return 1;\n'    
    _code += '}\n'

    return _code

  # ----------------- Electrons ---------------------
  def not_used_scale_factor_electron_handler(self):
    ''' Function used to calculate electron scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_electron_handler function.')

    try:

      _path_input = self.weights['scale_factor_electron']['file']
      _type     = self.weights['scale_factor_electron']['type']

      _input = eval(open(_path_input).read())[_type]['eta_pt_ratio']

      MiscTool.Print('analysis_info', 'Successfully Opened: ', _path_input)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with file{0}'.format(_path_input))
      raise

    # Get scale factors for all eta pt bins
    _scale_factors = {}

    for _etab, _ptbins in _input.iteritems():
      
      _eta_bin = _etab.split('[', 1)[1].split(']')[0]
      _scale_factors[_eta_bin] = {}

      for _ptb, _sf in _ptbins.iteritems():

        _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
        _scale_factors[_eta_bin][_pt_bin] = _sf

    # Create C function and save it
    _code = self._scale_factor_electron_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_electron']['C'], _code)

  def not_used_scale_factor_electron_C_writer(self, scale_factors):
    ''' This function is used to make C function using dictionary of scale factors.'''

    # function name
    _code = 'double scale_factor_electron(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 11)\n    return 1;\n\n' 

    # Loop over all sf
    for _etab, _ptbins in scale_factors.iteritems():
      
      # Add eta if statement
      _eta_min, _eta_max = _etab.split(',')
      _code += '  if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
      _code += '  {\n' # opening bracket

      # Add pt if statements
      for _ptb, _sf in _ptbins.iteritems():

        _pt_min, _pt_max = _ptb.split(',')
        _code += '    if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
        _code += '      return {0};\n'.format(_sf['value'])

      # case if pt > max pt and closing bracket for eta if statement
      _code += '    else\n      return 1;\n }\n'

    # if eta not in any bin then return 0
    _code += '  else\n    return 1; \n}'

    return _code

  def scale_factor_electron_ID_handler(self):
    ''' Function used to calculate electron ID scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_electron_ID_handler function.')

    try:

      _path_input = self.weights['scale_factor_electron_ID']['file']
      _type       = self.weights['scale_factor_electron_ID']['type']
      _input      = eval(open(_path_input).read())[_type]['eta_pt_ratio']

      MiscTool.Print('analysis_info', 'Successfully Opened: ', _path_input)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with file{0}'.format(_path_input))
      raise

    # Get scale factors for all eta pt bins
    _scale_factors = {}

    for _etab, _ptbins in _input.iteritems():
      
      _eta_bin = _etab.split('[', 1)[1].split(']')[0]
      _scale_factors[_eta_bin] = {}

      for _ptb, _sf in _ptbins.iteritems():

        _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
        _scale_factors[_eta_bin][_pt_bin] = _sf

    # Create C function and save it
    _code = self._scale_factor_electron_ID_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_electron_ID']['C'], _code)

  def _scale_factor_electron_ID_C_writer(self, scale_factors):
    ''' This function is used to make C function using dictionary of scale factors.'''

    # function name
    _code = 'double scale_factor_electron_ID(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 11)\n    return 1;\n\n' 

    # Loop over all sf
    for _etab, _ptbins in scale_factors.iteritems():
      
      # Add eta if statement
      _eta_min, _eta_max = _etab.split(',')
      _code += '  if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
      _code += '  {\n' # opening bracket

      # Add pt if statements
      for _ptb, _sf in _ptbins.iteritems():

        _pt_min, _pt_max = _ptb.split(',')
        _code += '    if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
        _code += '      return {0};\n'.format(_sf['value'])

      # case if pt > max pt and closing bracket for eta if statement
      _code += '    else\n      return 1;\n  }\n'

    # if eta not in any bin then return 0
    _code += '  else\n    return 1; \n}'

    return _code

  def scale_factor_electron_trk_handler(self):
    ''' Function used to calculate electron trk scale factors and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_electron_trk_handler function.')

    try:

      _path_input = self.weights['scale_factor_electron_trk']['file']
      _type       = self.weights['scale_factor_electron_trk']['type']
      _input      = eval(open(_path_input).read())[_type]['eta_pt_ratio']

      MiscTool.Print('analysis_info', 'Successfully Opened: ', _path_input)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with file{0}'.format(_path_input))
      raise

    # Get scale factors for all eta pt bins
    _scale_factors = {}

    for _etab, _ptbins in _input.iteritems():
      
      _eta_bin = _etab.split('[', 1)[1].split(']')[0]
      _scale_factors[_eta_bin] = {}

      for _ptb, _sf in _ptbins.iteritems():

        _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
        _scale_factors[_eta_bin][_pt_bin] = _sf

    # Create C function and save it
    _code = self._scale_factor_electron_trk_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_electron_trk']['C'], _code)

  def _scale_factor_electron_trk_C_writer(self, scale_factors):
    ''' This function is used to make C function using dictionary of scale factors.'''

    # function name
    _code = 'double scale_factor_electron_trk(double eta, double pt, int lepton_pdgID)\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 11)\n    return 1;\n\n' 

    # Loop over all sf
    for _etab, _ptbins in scale_factors.iteritems():
      
      # Add eta if statement
      _eta_min, _eta_max = _etab.split(',')
      _code += '  if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
      _code += '  {\n' # opening bracket

      # Add pt if statements
      for _ptb, _sf in _ptbins.iteritems():

        _pt_min, _pt_max = _ptb.split(',')
        _code += '    if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
        _code += '      return {0};\n'.format(_sf['value'])

      # case if pt > max pt and closing bracket for eta if statement
      _code += '    else\n      return 1;\n  }\n'

    # if eta not in any bin then return 0
    _code += '  else\n    return 1; \n}'

    return _code

  def scale_factor_electron_trigger_handler(self):
    ''' Function used to calculate electron trigger efficiencies and store them as C function.'''

    MiscTool.Print('python_info', '\nCalled scale_factor_electron_trigger_handler function.')

    try:

      _path_input = self.weights['scale_factor_electron_trigger']['file']
      _type       = self.weights['scale_factor_electron_trigger']['type']

      _input = eval(open(_path_input).read())[_type]['eta_pt_ratio']

      MiscTool.Print('analysis_info', 'Successfully Opened: ', _path_input)

    except Exception, e:
      MiscTool.Print('error', 'Something is wrong with file{0}'.format(_path_input))
      raise

    # Get scale factors for all eta pt bins
    _scale_factors = {}

    for _etab, _ptbins in _input.iteritems():
      
      _eta_bin = _etab.split('[', 1)[1].split(']')[0]

      _scale_factors[_eta_bin] = {}

      for _ptb, _sf in _ptbins.iteritems():

        _pt_bin = _ptb.split('[', 1)[1].split(']')[0]
        _scale_factors[_eta_bin][_pt_bin] = _sf

    # Create C function and save it
    _code = self._scale_factor_electron_trigger_C_writer(_scale_factors)
    self._save_C_code(self.weights['scale_factor_electron_trigger']['C'], _code)

  def _scale_factor_electron_trigger_C_writer(self, scale_factors):
    
    ''' This function is used to make C function using dictionary of scale factors.'''

    # function name
    _code = 'double scale_factor_electron_trigger(double eta, double pt, int lepton_pdgID )\n{\n'

    # Add lepton type check
    _code += '  if (abs(lepton_pdgID) != 11)\n    return 1;\n\n' 

    # Loop over all sf
    for _etab, _ptbins in scale_factors.iteritems():
      
      # Add eta if statement
      _eta_min, _eta_max = _etab.split(',')
      _code += '  if (eta > {0} && eta < {1})\n'.format(_eta_min, _eta_max)
      _code += '  {\n' # opening bracket

      # Add pt if statements
      for _ptb, _sf in _ptbins.iteritems():

        _pt_min, _pt_max = _ptb.split(',')
        _code += '    if (pt > {0} && pt < {1})\n'.format(_pt_min, _pt_max)
        _code += '      return {0};\n'.format(_sf['value'])

      # case if pt > max pt and closing bracket for eta if statement
      _code += '    else\n      return 1;\n  }\n'

    # if eta not in any bin then return 0
    _code += '  else\n    return 1; \n}'

    return _code

  # ----------------- bb Tag ---------------------
  def scale_factor_bbtag_handler(self):

    # Create C function and save it
    _code = self._scale_factor_bbtag_C_writer()
    self._save_C_code(self.weights['scale_factor_bb_tag']['C'], _code)

  def _scale_factor_bbtag_C_writer(self):

    ''' This function is used to make C function using dictionary of scale factors.'''

    # function name
    _code = 'double scale_factor_bb_tag( double pt )\n{\n'

    _code += '  if (pt > {0} && pt < {1})\n'.format( '250', '350')
    _code += '  {\n' # opening bracket
    _code += '    return {0};\n'.format(0.92)
    _code += '  }\n' # closing bracket

    _code += '  if (pt > {0} && pt < {1})\n'.format( '350', '430')
    _code += '  {\n' # opening bracket
    _code += '    return {0};\n'.format(1.01)
    _code += '  }\n' # closing bracket

    _code += '  if (pt > {0} && pt < {1})\n'.format( '430', '840')
    _code += '  {\n' # opening bracket
    _code += '    return {0};\n'.format(0.92)
    _code += '  }\n' # closing bracket

    _code += '  else\n      return 1;\n  }\n'

    return _code

  ###########################################################

  def get_total_number_of_events(self):
    ''' Get the total (weighted) number of events using files without any preselection. '''

    # Load C functions which define weights
    for _w in self.weights.values():
      if 'C' in _w:
        try:
          ROOT.gROOT.ProcessLine('.L {0}/{1}'.format(os.path.join( self.path_working_directory, 'results/Wlv/weights'), _w['C']))
          MiscTool.Print('analysis_info', 'Loaded successfully: ', format(_w['C']))
        except Exception, e:
          MiscTool.Print('error', 'Failed to load {0}.'.format(_w['C']))

    # Location of file where we save the results
    _path_results = os.path.join( self.path_results, 'total_number_of_events.py')

    # Location of logical file names
    _path_logical_file_names = os.path.join( self.configuration['paths']['path_samples'], 'logical_file_names')

    _normalization = {}

    # Loop over samples
    for _s in self.configuration['samples']['list']:
      
      # Skip if sample is data type
      if self.configuration['samples']['list'][_s]['types'] == 'data':
        continue

      # Add to weight string, only those weights which are on Gen Level
      _weight = '*'.join([self.weights['pile_up']['weight'], self.weights['genWeight']['weight']])

      # Special weight for WJets 
      if 'WJet' in _s:
        _weight += '*' + self.weights['EWK_NLO_correction']['weight']

      # Open list of sample files 
      with open(os.path.join( _path_logical_file_names, _s + '_local.txt'), 'r') as f:
        _files = f.read().splitlines()

      _total_sum_of_weighted_events = 0

      MiscTool.Print('python_info', '\nGetting total number of weighted events for {0}'.format(_s))

      # Loop over all non preselected files
      for _n, _f in enumerate(_files):

        _input  = ROOT.TFile.Open( _f,'read')
        _tree   = _input.Get('tree')
        _h    = ROOT.TH1F( 'count', 'count', 1, 0, 100)

        # Draw histogram with weights applied
        _tree.Draw('{0}>>{1}'.format('1', 'count'), _weight)

        # Get Integral and add to sum
        _total_sum_of_weighted_events += _h.GetBinContent(1)

        _input.Close()

        MiscTool.Print('status', 'Done: {0:.2f} %'.format(100.0*_n/len(_files)))

      # Save the number in dictionary
      _normalization[_s] = _total_sum_of_weighted_events
      
      MiscTool.Print('status', 'Total number of weighted events: {0}'.format(_total_sum_of_weighted_events))

    # Save dictionary into file
    with open(_path_results, 'w') as handle:
      json.dump(_normalization, handle, indent=4)

    MiscTool.Print('python_info', '\nCreated {0}'.format(_path_results))

  def _save_C_code(self, file_name, code):
    ''' Function name is self explanatory. Function saves code in .h script'''

    _path_file = os.path.join( self.path_results, file_name)

    _o_file = open( _path_file , 'w')
    _o_file.write(code)
    _o_file.close()   

    MiscTool.Print('python_info', 'Created {0}'.format(_path_file))

  def _load_C_code(self):

    ROOT.gROOT.ProcessLine('.L {0}/pile_up.h'.format(self.path_results))
    print ROOT.pile_up(1)

    ROOT.gROOT.ProcessLine('.L {0}/scale_factor_electron.h'.format(self.path_results))
    print ROOT.scale_factor_electron(2.0, 123.5)

    ROOT.gROOT.ProcessLine('.L {0}/EWK_NLO_correction.h'.format(self.path_results))
    print ROOT.ptWeightEWK( 1, 200, 2, 24)
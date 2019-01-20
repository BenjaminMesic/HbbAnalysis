import ROOT
import os
from array import array
import subprocess as sp

from keras.models import model_from_json

from utility import MiscTool
from utility import utility_py

ROOT.gROOT.SetBatch(True)

# Load some libs for getting btag SF:
ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau')

def load_model(name):
  
  with open( name + '.json') as json_model:
    model = model_from_json(json_model.read())

  model.load_weights( name + '.h5')

  model.compile(loss="mse", optimizer="rmsprop")

  return model

def create_boosted_tree(i_file, o_file, variables):
  """
  Apply preselection(cut) on input_file, as a result you get output_file
  Objects other than the TTree 'tree' are copied directly.
  """

  # Apply L0 selection
  _input    = ROOT.TFile.Open( i_file, 'read')
  _tree     = _input.Get('tree')

  _temp     = ROOT.TFile.Open( o_file.replace('.root', '_temp.root'), 'recreate')

  # Copy all TH1Fs in the tree
  _input.cd()
  _obj = ROOT.TObject
  for key in ROOT.gDirectory.GetListOfKeys():
    _input.cd()
    _obj = key.ReadObj()
    if _obj.GetName() == 'tree':
      continue
    _temp.cd()
    _obj.Write(key.GetName())
  _temp.cd()
  _temp.Write()

  _tree_temp = _tree.CopyTree('<L0>')

  _temp.cd()
  _input.Close()

  _tree_temp.Write()
  _temp.Close()

  # Continue with making new file
  _input    = ROOT.TFile.Open( o_file.replace('.root', '_temp.root'), 'read')
  _output   = ROOT.TFile( o_file, 'recreate')

  _tree_old = _input.Get('tree')

  # Apply L0 selection
  _tree     = _tree_old.CopyTree('<L0>')

  _tree_list_of_branches = [_b.GetName() for _b in _tree.GetListOfBranches()]

  assert type(_tree) is ROOT.TTree

  # Copy all TH1Fs in the tree
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
  _output.Write()

  # Remove all the branches first
  for _b in _tree_list_of_branches:
    _tree.SetBranchStatus(_b, 0)

  _additional_branches = {}

  # Leave only those branches you need
  for _b in variables['variables']:

    if _b in _tree_list_of_branches:
      _tree.SetBranchStatus(_b, 1)

    # Define your own
    else:

      if _b not in variables['definition']:
        continue
      
      _definition = variables['definition'][_b]
      _default_value = -9

      if _definition['type'] == 'f':
        _default_value = 1.0*_default_value

      _additional_branches[_b] = array( _definition['type'], _definition['size']*[ _default_value ] )

  # Copy entire tree with the branches from the config
  _new_tree = _tree.CloneTree(0)

  # Add your own branches and initalize neural networks if necessary
  _neural_nets  = {}
  _aux_files    = {}
  for _b,_array in _additional_branches.iteritems():

    _definition = variables['definition'][_b]

    if _definition['size'] == 1:
      _b_type = _b
    else:
      _b_type = _b + '[{0}]'.format( _definition['size'])

    _new_tree.Branch( _b, _array, '{0}/{1}'.format( _b_type, _definition['type'].upper()))

    # --------------------------------------
    # Add neural networks
    if 'nn' in _definition:
      for _n in _definition['nn']:
        _network_name     = os.path.join( os.environ['Hbb_WORKING_DIRECTORY'], 'aux/neural_network/{0}'.format(_n))
        _neural_nets[_n]  = load_model(_network_name)

    # --------------------------------------
    # add external/aux files
    if 'aux_files' in _definition:

      for _a, _af in _definition['aux_files'].iteritems():

        if 'root' in _a:
          _aux_files[ _b + '_' + _a] = ROOT.TFile.Open( _af, 'read')
        
        elif 'btagcal' in _a:

          calib = ROOT.BTagCalibration('csvv2', _af)

          # making a std::vector<std::string>> in python is a bit awkward, 
          # but works with root (needed to load other sys types):
          v_sys = getattr(ROOT, 'vector<string>')()
          v_sys.push_back('up')
          v_sys.push_back('down')

          # make a reader instance and load the sf data
          _aux_files[ _b + '_' + _a] = ROOT.BTagCalibrationReader(
              0,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
              "central",      # central systematic type
              v_sys,          # vector of other sys. types
          )    
          _aux_files[ _b + '_' + _a].load(
              calib, 
              0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "comb"      # measurement type
          )

          _aux_files[ _b + '_' + _a].load(
              calib, 
              1,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "comb"      # measurement type
          )

          _aux_files[ _b + '_' + _a].load(
              calib, 
              2,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "incl"      # measurement type
          )

        elif 'ctagcal' in _a:

          calib = ROOT.BTagCalibration('cTag', _af)

          # making a std::vector<std::string>> in python is a bit awkward, 
          # but works with root (needed to load other sys types):
          v_sys = getattr(ROOT, 'vector<string>')()
          v_sys.push_back('up')
          v_sys.push_back('down')

          # make a reader instance and load the sf data
          _aux_files[ _b + '_' + _a] = ROOT.BTagCalibrationReader(
              0,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
              "central",      # central systematic type
              v_sys,          # vector of other sys. types
          )

          _aux_files[ _b + '_' + _a].load(
              calib, 
              0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "TnP"      # measurement type
          )

          _aux_files[ _b + '_' + _a].load(
              calib, 
              1,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "comb"      # measurement type
          )

          _aux_files[ _b + '_' + _a].load(
              calib, 
              2,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
              "incl"      # measurement type
          )

  # Fill the branches you've just added
  for _ii in xrange(_tree.GetEntriesFast()):

    # if _ii > 5:
    #   break

    # Get event informations
    _tree.GetEntry(_ii)

    # --------------------------------------
    # First compute global values
    global_values = {}

    for _v in variables['global']:

      _definition = variables['definition'][_v]

      # Line where magic happens
      if 'nn' in _definition:
        global_values[_v] = getattr( utility_py, _v)(_tree, global_values, _neural_nets)
      elif 'aux_files' in _definition:
        global_values[_v] = getattr( utility_py, _v)(_tree, global_values, _aux_files)        
      else:
        global_values[_v] = getattr( utility_py, _v)(_tree, global_values)

    # --------------------------------------
    # Compute other values
    for _b, _array in _additional_branches.iteritems():

      _definition = variables['definition'][_b]

      # If already computed in global skip
      if _b in global_values:
        _values = global_values[_b]

      else:
        # Line where magic happens
        if 'nn' in _definition:
          _values = getattr( utility_py, _b)(_tree, global_values, _neural_nets)
        elif 'aux_files' in _definition:
          _values = getattr( utility_py, _b)(_tree, global_values, _aux_files)        
        else:
          _values = getattr( utility_py, _b)(_tree, global_values)

      # Fill single value
      if _definition['size'] == 1:
          _array[0] = _values

      # Fill vector
      else:
        for _i in xrange(len(_array)):
          _array[_i] = _values[_i]

    _new_tree.Fill()

  # Save all and close
  _output.cd()
  _new_tree.Write()
  _output.Close()
  _input.Close()

  sp.call('rm -rf {0}'.format(o_file.replace('.root', '_temp.root')), shell=True)

if __name__ == '__main__':
  
  input_file    = '<input_file>'
  output_file   = '<output_file>'
  variables     = <variables>

  output_directory = output_file.split('tree')[0]
  MiscTool.make_directory(output_directory)

  create_boosted_tree( input_file, output_file, variables)
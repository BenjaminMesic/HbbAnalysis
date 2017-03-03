import ROOT
from array import array

from utility import MiscTool
from utility import utility_py

ROOT.gROOT.SetBatch(True)

def create_boosted_tree(i_file, o_file, variables):
  """
  Apply preselection(cut) on input_file, as a result you get output_file
  Objects other than the TTree 'tree' are copied directly.
  """

  _input    = ROOT.TFile.Open( i_file, 'read')
  _output   = ROOT.TFile( o_file, 'recreate')

  _tree     = _input.Get('tree')
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
      _definition = variables['definition'][_b]
      _default_value = -9

      if _definition['type'] == 'f':
        _default_value = 1.0*_default_value

      _additional_branches[_b] = array( _definition['type'], _definition['size']*[ _default_value ] )

  # Copy entire tree with the branches from the config
  _new_tree = _tree.CloneTree(0)

  # Add your own branches
  for _b,_array in _additional_branches.iteritems():

    _definition = variables['definition'][_b]

    if _definition['size'] == 1:
      _b_type = _b
    else:
      _b_type = _b + '[{0}]'.format( _definition['size'])

    _new_tree.Branch( _b, _array, '{0}/{1}'.format( _b_type, _definition['type'].upper()))

  # Fill the branches you've just added
  for _ii in xrange(_tree.GetEntriesFast()):

    # Get event informations
    _tree.GetEntry(_ii)

    # Calculate values
    for _b, _array in _additional_branches.iteritems():

      # Line where magic happens
      _values = getattr( utility_py, _b)(_tree)

      _definition = variables['definition'][_b]

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

if __name__ == '__main__':
  
  input_file    = '<input_file>'
  output_file   = '<output_file>'
  variables     = <variables>

  output_directory = output_file.split('tree')[0]
  MiscTool.make_directory(output_directory)

  create_boosted_tree( input_file, output_file, variables)
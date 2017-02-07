import os
import stat
import subprocess as sp
from array import array
import hashlib

import ROOT

from utility import MiscTool
from utility import BatchTool
from utility import TreeTool
from utility import utility_py

class PreselectionTool(object):
  '''
  -----------
  Description:
  Preselection is used to apply preselection cut on all the samples
  and as a result we have smaller files with only events of our interest.
  It gets list of all files from self.samples_path, apply preselection
  and copy them in XXX. After that, merging of these files is done
  so that we have only one file for each sample. Local batch system in 
  Zagreb is used.

  ----------- 

  -----------
  Parameters:

  -----------
  Functions:
  preselection()



  -----------
  Useful commands:
  limit maxproc 2048 - set if getting error with number of processes

  -----------
  To DO:


  ''' 

  def __init__(self, analysis_name, configuration, force_all, sample = None):

    MiscTool.Print('python_info', '\nCreated instance of Preselection class')

    # force preselection on already existing files
    self.force_all = force_all

    # ------ Paths -------
    self.path_working_directory   = os.environ['Hbb_WORKING_DIRECTORY']
    self.path_batch_templates     = os.path.join( self.path_working_directory, 'utility', 'templates', 'preselection_batch')
    self.path_batch_scripts       = os.path.join( self.path_working_directory, 'results', analysis_name, '_2_preselection_batch')
    self.path_samples             = configuration['paths']['path_samples']
    self.path_list_of_samples     = os.path.join( self.path_samples, 'logical_file_names')
    self.path_preselected_samples = configuration['paths']['path_samples_preselection']
    self.path_cache               = configuration['paths']['path_cache']

    # ------ Samples -------
    if sample == None:

      _samples_id_list = configuration['samples']['task']['preselection']

      if _samples_id_list[0] == 'all':

        self.list_of_samples = [ _s + '_local.txt' for _s in  configuration['samples']['list'].keys()]

      else:
        self.list_of_samples = []
        for _id in _samples_id_list:
          for _s in configuration['samples']['list']:
            if _id == configuration['samples']['list'][_s]['ID']:
              self.list_of_samples.append( _s + '_local.txt')
              break

    else:
      self.list_of_samples = ['{0}_local.txt'.format(sample)]
    self.list_of_search_keywords    = ['.root']

    # ------ Cuts -------
    self.preselection_cut = configuration['cuts']['preselection_cut']

    # ------ Tree variables needed for create_boosted_trees function -------
    self.variables = configuration['variables']

    MiscTool.Print('analysis_info', 'Working directory:', self.path_working_directory)
    MiscTool.Print('analysis_info', 'Path to list of samples:', self.path_list_of_samples)
    MiscTool.Print('analysis_info', 'Path to batch templates:', self.path_batch_templates)
    MiscTool.Print('analysis_info', 'Path to batch scripts:', self.path_batch_scripts)
    MiscTool.Print('analysis_info', '\nPreselection cut:', self.preselection_cut)

  def preselection(self):

    MiscTool.Print('python_info', '\nCalled preselection function.')

    # Loop over samples
    for _sample in self.list_of_samples:

      MiscTool.Print('status', '\n' + _sample)

      _files = open(os.path.join(self.path_list_of_samples, _sample),'r')

      # For each file create job by copying template script
      for _i,_f in enumerate(_files):

        if not self.filter(_f):
          continue

        _file = _f.replace('\n', '')

        _output_file = _file.replace(self.path_samples, self.path_preselected_samples)    
        _inital_directory, _script_name = _file.replace(self.path_samples, self.path_batch_scripts).split('tree')

        # If preselected file already exists skip
        if TreeTool.TreeTool.check_if_tree_ok(_output_file) and not self.force_all:
          MiscTool.Print('python_info','File {0} already exists.'.format(_output_file))
          continue

        _batch_arguments = {
          '<initial_directory>' : _inital_directory,        # path to newly created batch script
          '<input_file>'      : _file,              # file w/o presel
          '<output_file>'     : _output_file,           # file w/ presel
          '<cut>'         : self.preselection_cut,      # 'V_pt>100'
          '<script_name>'     : _script_name.replace('.root',''), # 1401
          'python_template'     : os.path.join(self.path_batch_templates, 'preselection_batch_template.py')
        }

        _batch = BatchTool.BatchTool(_batch_arguments)
        _batch.make_scripts()
        _batch.send_job()

  def merge(self):

    MiscTool.Print('python_info', '\nCalled merge function.')

    # Loop over samples
    for _sample in self.list_of_samples:

      MiscTool.Print('status', '\nMerging preselected files for: ' + _sample)

      _files = open(os.path.join( self.path_list_of_samples, _sample),'r')

      # name of merged root file      
      _file_name = _sample.replace('_local.txt', '.root')
      _merge_file_name = os.path.join( self.path_preselected_samples, _file_name )

      # If merged preselected file already exists skip
      if TreeTool.TreeTool.check_if_tree_ok(_merge_file_name) and not self.force_all:
        MiscTool.Print('python_info','File {0} already exists.'.format(_merge_file_name))
        continue

      _merger = ROOT.TFileMerger(ROOT.kFALSE)
      _merger.OutputFile(_merge_file_name, 'RECREATE')

      for _i,_f in enumerate(_files):

        _file = _f.replace('\n', '').replace( self.path_samples, self.path_preselected_samples)

        MiscTool.Print('status', _file)

        # if i != 0:
        #   continue

        # Check if file exists, if not store
        if not os.path.isfile(_file):
          MiscTool.Print('error', 'File {0} is missing.'.format(_file))
          continue

        _merger.AddFile(_file)        
        
      _merger.Merge()

      MiscTool.Print('status', '\nMerging done.')

  def check_root_preselected_files(self):

    MiscTool.Print('python_info', '\nCalled check_root_preselected_files function.')

    # Samples loop
    for _s in self.list_of_samples:

      MiscTool.Print('status', 'Checking sample: {0}'.format(_s))

      try:

        _destination_file   = open(os.path.join(self.path_list_of_samples, _s),'r') 

        # files loop
        for _f in _destination_file:

          # destination path for each file
          _file = _f.replace('\n', '').replace(self.path_samples, self.path_preselected_samples)

          try:
            if TreeTool.TreeTool.check_if_tree_ok(_file):
              pass
              MiscTool.Print('status', 'File: {0} OK.'.format(_file))
            else:
              MiscTool.Print('error', 'File: {0} not OK.'.format(_file))
          
          except Exception, e:
            MiscTool.Print('error', 'File: {0} not OK.'.format(_file))

      except Exception, e:
        print 'Problem with {0}.'.format(_s)

  def create_boosted_trees(self):

    MiscTool.Print('python_info', '\nCalled create_boosted_trees function.')  

    # Loop over samples
    for _sample in self.list_of_samples:

      # Load old preselected root file     
      _file         = _sample.replace('_local.txt', '.root')
      _path_file    = os.path.join( self.path_preselected_samples, _file )
      _input        = ROOT.TFile.Open( _path_file,'read')
      _tree         = _input.Get('tree')
      _tree_list_of_branches = [_b.GetName() for _b in _tree.GetListOfBranches()]

      assert type(_tree) is ROOT.TTree

      # Create new preselected file
      _checksum_variables = hashlib.md5('_'.join(self.variables['variables'])).hexdigest() 
      _path_file_new = os.path.join( self.path_cache, '_'.join(['boost', _checksum_variables, _file]))
      # _path_file_new = 'test.root'

      if TreeTool.TreeTool.check_if_tree_ok(_path_file_new):
        MiscTool.Print('status', '\nBoosted tree {0} exists.'.format(_path_file_new))
        continue
      else:
        MiscTool.Print('status', '\nCreating boosted tree from {0}'.format(_path_file))

      _output = ROOT.TFile.Open( _path_file_new,'recreate')

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
      for _b in self.variables['variables']:

          if _b in _tree_list_of_branches:
            _tree.SetBranchStatus(_b, 1)
          else:
            _additional_branches[_b] = array( 'f', [ 0. ] )

      # Copy entire tree with the branches from the config
      _new_tree = _tree.CloneTree(0)

      # Add your own branches
      for _b,_type in _additional_branches.iteritems():
        _new_tree.Branch( _b, _type, '{0}/F'.format(_b))
        MiscTool.Print('analysis_info', 'Adding new variable:', _b)

      # Fill the branches you've just added
      for _ii in xrange(_tree.GetEntriesFast()):

        # Get event informations
        _tree.GetEntry(_ii)

        # Calculate values
        for _b, _type in _additional_branches.iteritems():

          _type[0] = getattr( utility_py, _b)(_tree)*1.0

        _new_tree.Fill()

      # Save all and close
      _output.cd()
      _new_tree.Write()
      _output.Close()
      _input.Close()

      MiscTool.Print('status', 'File {0} done.'.format(_path_file_new))

  # Filter files which have the keywords
  def filter(self, file_name):

    if not any(_k in file_name for _k in self.list_of_search_keywords):
      return False
    else:
      return True

def X():

  return 5

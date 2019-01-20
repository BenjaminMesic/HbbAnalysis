import os
import hashlib

import ROOT

from utility import MiscTool
from utility import BatchTool

class FileTool(object):

  def __init__(self, configuration):
    
    MiscTool.Print('python_info', '\nCreated instance of FileTool class')

    self.force_all = configuration.general.force_all
    # Needed to get list of samples
    self.task_name = configuration.general.task_name

    # ------ Paths -------
    self.path_working_directory           = configuration.paths.path_working_directory
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_samples_location            = configuration.paths.path_samples
    self.path_samples_user_defined        = configuration.paths.path_samples_user_defined
    self.path_logical_file_names          = MiscTool.make_directory( os.path.join( self.path_samples_location, 'logical_file_names') )
    self.path_batch_scripts               = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'user_defined_files') )
    self.path_batch_templates             = MiscTool.make_directory( os.path.join( self.path_working_directory, 'utility', 'templates', 'user_defined_files') )

    # ------ File options -------
    self.list_of_IDs                    = configuration.samples.task[self.task_name]
    self.list_of_locations              = configuration.general.locations
    self.variables                      = configuration.variables.variables
    self.L0_selection                   = configuration.selection.hierarchy['L0']
    self.user_defined_files             = configuration.general.user_defined_files
    self.send_jobs                      = configuration.general.send_jobs
    self.batch                          = configuration.general.batch

    # Convert IDs to samples
    self.list_of_samples                = MiscTool.ID_sample_dictionary( self.list_of_IDs, configuration.samples)
    self.info_samples                   = configuration.samples.samples_list

    MiscTool.Print('analysis_info', 'Task:', self.task_name)
    MiscTool.Print('analysis_info', 'Force all:', self.force_all)
    MiscTool.Print('analysis_info', 'New files will be stored in:', self.path_samples_user_defined)
    MiscTool.Print('analysis_info', 'Analysis working directory:', self.path_analysis_working_directory)
    MiscTool.Print('analysis_info_list', 'List of samples:', self.list_of_samples)

  def make_files(self, sample):

    MiscTool.Print('python_info', '\nCalled make_files function.')

    for _l in self.list_of_locations:

      _path_local = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local.txt')

      if not (_l in self.info_samples[sample]['origin'] or self.info_samples[sample]['origin'] == ['all']):
        continue        

      if not os.path.isfile( _path_local):
        continue

      MiscTool.Print('status', 'Working {0} '.format( _path_local))

      _file_local = open( _path_local, 'r')

      for _n, _f in enumerate(_file_local):

        # if _n > 0:
        #   continue
    
        _f = _f.strip()

        _output_file                    = _f.replace( self.path_samples_location, self.path_samples_user_defined)    
        _inital_directory, _script_name = _f.replace( self.path_samples_location, self.path_batch_scripts).split('tree')

        # If output file already exists skip
        if self.check_if_file_ok(_output_file) and not self.force_all:
          MiscTool.Print('python_info','File {0} already exists and ok.'.format(_output_file))
          continue

        _batch_arguments = {
          '<initial_directory>' : _inital_directory,                        # path to newly created batch script
          '<input_file>'        : _f,                                       # old file
          '<output_file>'       : _output_file,                             # new file
          '<variables>'         : str(self.variables),                      # variables
          '<script_name>'       : _script_name.replace('.root',''), # 1401
          '<L0>'                : self.L0_selection,  
          'python_template'     : os.path.join(self.path_batch_templates, 'user_defined_files_batch.py')
        }

        _batch = BatchTool.BatchTool(_batch_arguments, self.batch, self.send_jobs)
        _batch.make_scripts()
        _batch.send_job()

      _file_local.close()

  def make_files_all_samples(self):

    MiscTool.Print('python_info', '\nCalled make_files_all_samples function.')
    
    if not self.user_defined_files:
      MiscTool.Print('error', '\nSet user defined files flag in general to True and start again.')
      return 0

    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.make_files(_s)

  @staticmethod 
  def check_if_file_ok(file_name):
      ''' 
      Check if file exists and if it's ok. If yes return True, else False
      '''

      _status = ''

      if os.path.isfile(file_name):

        try:

          f = ROOT.TFile.Open(file_name,'read')

          if (not f) or f.GetNkeys() == 0 or f.TestBit(ROOT.TFile.kRecovered) or f.IsZombie():
              
            _status = False

          else:
            _status = True

          f.Close()

        except Exception, e:

          _status = False

      else:
        _status = False

      return _status

  # -------------------------------------

  # @staticmethod
  # def trim_files(cut, input_file, ID, path_cache, forceReDo=False):
  #   ''' Create and return cached tree'''
  #   # Not used anymore I guess

  #   MiscTool.Print('python_info', '\nCalled trim_tree function.')

  #   # Set location of files
  #   _path_cache = path_cache
  #   MiscTool.make_directory(_path_cache)

  #   # output file name based on md5 of complete cut for this sample
  #   _unique_name = hashlib.md5(cut).hexdigest()
  #   _output_file = os.path.join( _path_cache, ID + '_' + _unique_name + '.root' )

  #   MiscTool.Print('analysis_info', 'Output file:', _output_file)
  #   MiscTool.Print('analysis_info', 'ID:', ID)
  #   MiscTool.Print('analysis_info', 'Input_file:', input_file)
  #   MiscTool.Print('analysis_info', 'Cut:', cut)

  #   _check_output_file = TreeTool.check_if_tree_ok(_output_file)

  #   # If file doesn't exists or it is corrupted
  #   if forceReDo or (not _check_output_file):
      
  #     # Create cached file (tmp file)
  #     try:
  #       if forceReDo:
  #         _output = ROOT.TFile.Open( _output_file,'recreate')
  #       else:
  #         _output = ROOT.TFile.Open( _output_file,'create')
  #       _output.cd()
  #     except:
  #       MiscTool.Print('error', 'Problem with creating _tmp. Delete root file and try again.')

  #     # Load source file
  #     _input_file = ROOT.TFile.Open( input_file,'read')
  #     _tree = _input_file.Get('tree')
  #     assert type(_tree) is ROOT.TTree

  #     # ------ Here starts actual skimming -------
  #     _input_file.cd()
  #     _obj = ROOT.TObject
  #     for key in ROOT.gDirectory.GetListOfKeys():
  #       _input_file.cd()
  #       _obj = key.ReadObj()
  #       if _obj.GetName() == 'tree':
  #         continue
  #       _output.cd()
  #       _obj.Write(key.GetName())
  #     _output.cd()

  #     # Apparently problem here: not working when empty tree
  #     _cuttedTree = _tree.CopyTree(cut)
  #     _cuttedTree.Write()
  #     _output.Write()
  #     _input_file.Close()
  #     del _input_file
  #     _output.Close()
  #     del _output
  #     MiscTool.Print('status', 'File done.')

  #   else:
  #     MiscTool.Print('python_info', 'File exists and it is ok.')

  #   return _output_file

  @staticmethod
  def simple_trim_files(i_file, o_file, cut):
    """
    Apply preselection(cut) on input_file, as a result you get output_file
    Objects other than the TTree 'tree' are copied directly.
    """
    MiscTool.Print('python_info', 'Called simple_trim_files function.')

    MiscTool.Print('analysis_info', 'Input file:', i_file)
    MiscTool.Print('analysis_info', 'Output file:', o_file)

    input_file = ROOT.TFile.Open( i_file, 'read')
    output_file = ROOT.TFile( o_file, 'recreate')

    for key in input_file.GetListOfKeys():
      if key.GetName() == 'tree':
        continue
      obj = key.ReadObj()
      obj.Write()

    input_tree = input_file.Get('tree')
    n_total = input_tree.GetEntriesFast()
    output_tree = input_tree.CopyTree(cut)
    n_selected = output_tree.GetEntriesFast()
    output_tree.Write()

    return n_selected, n_total
    
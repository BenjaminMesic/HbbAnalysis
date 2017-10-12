import os
import subprocess as sp
import Queue

import ROOT

from utility import MiscTool
from utility import FileTool
from utility import BatchTool

class CopyTool(object):
  '''

  Useful commands:

  lcg-ls -b -v -l -D srmv2 srm:"//stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/store/user/cvernier/VHBBHeppyV23" 
  
  gfal-ls -Hl srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/
  gfal-ls -Hl srm://stormfe1.pi.infn.it/cms/store/user/cvernier/VHBBHeppyV23/
  gfal-copy --force srm://t3se01.psi.ch/pnfs/pfsi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/ZZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V23_ZZ_TuneCUETP8M1_13TeV-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160718_082331/0000/tree_1.root file:////$PWD/
  gfal-copy --force srm://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV23/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 file:////$PWD/

  gfal-copy --force srm://stormgf1.pi.infn.it:1094/store/user/arizzi/VHBBHeppyV25b/SingleElectron/VHBB_HEPPY_V25b_SingleElectron__Run2016C-03Feb2017-v1/170223_085517/0000/tree_527.root

  print copy_samples.wrapper_gfal_ls_r('/stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/store/user/arizzi/VHBBHeppyV24/ggZH_HToBB_ZToNuNu_M125_13TeV_amcatnlo_pythia8/VHBB_HEPPY_V24_ggZH_HToBB_ZToNuNu_M125_13TeV_amcatnlo_Py8__spr16MAv2-puspr16_HLT_80r2as_v14-v1')

  ''' 
  def __init__(self, configuration):

    MiscTool.Print('python_info', '\nCreated instance of CopyTool class')

    self.force_all = configuration.general.force_all
    # Needed to get list of samples
    self.task_name = configuration.general.task_name

    # ------ Paths -------
    self.path_working_directory           = configuration.paths.path_working_directory
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_samples_location            = configuration.paths.path_samples
    self.path_logical_file_names          = MiscTool.make_directory( os.path.join( self.path_samples_location, 'logical_file_names') )
    self.path_batch_scripts               = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'copy_batch') )
    self.path_batch_templates             = MiscTool.make_directory( os.path.join( self.path_working_directory, 'utility', 'templates', 'copy_batch') )

    # ------ Copy options -------
    self.list_of_IDs                    = configuration.samples.task[self.task_name]
    self.list_of_copying_protocols      = configuration.general.copy_protocol
    self.list_of_storage_elements       = configuration.general.storage_element
    self.list_of_locations              = configuration.general.locations
    self.search_keywords                = configuration.general.search_keywords

    # Convert IDs to samples
    self.list_of_samples                = MiscTool.ID_sample_dictionary( self.list_of_IDs, configuration.samples)

    MiscTool.Print('analysis_info', 'Task:', self.task_name)
    MiscTool.Print('analysis_info', 'Force all:', self.force_all)
    MiscTool.Print('analysis_info', 'Samples will be stored in:', self.path_samples_location)
    MiscTool.Print('analysis_info', 'Analysis working directory:', self.path_analysis_working_directory)
    MiscTool.Print('analysis_info_list', 'List of samples:', self.list_of_samples)

  # ------------------- Find files ---------------------------
  # Wrappers for ls, cp, which are used for browsing sources where files are located
  def wrapper_gfal_ls(self, location, protocol):

    MiscTool.Print('python_info', '\nCalled wrapper_gfal_ls function.')

    _command = ['gfal-ls', '-l'] #,'-Hl']
    _command.append(protocol + location)

    MiscTool.Print('python_info', 'Command: ' + ' '.join(_command))

    return sp.check_output(_command)

  def wrapper_gfal_ls_r(self, location, protocol):
    
    MiscTool.Print('python_info', '\nCalled wrapper_gfal_ls_r function.')

    _paths = Queue.Queue()
    _paths.put(location)

    # list to store logical file names
    _logical_file_names = []

    while not _paths.empty():

      # get one path
      _x = _paths.get()

      # If filter keywords failed, continue to next lfn
      if not self.filter_keywords( _x, self.search_keywords['all'], self.search_keywords['any'], self.search_keywords['none']):
        MiscTool.Print('error', 'Skipping {0}.'.format(_x))
        continue

      # do ls
      _y = self.wrapper_gfal_ls( _x, protocol)

      for _p in _y.splitlines():
        
        _type = _p[0]
        _name = _p.split(' ')[-1].rstrip()

        # If this particular ls result is directory, put in ls queue
        if _type == 'd':
          _paths.put( os.path.join(_x, _name))

        # Else just store in list
        else:
          _logical_file_names.append(os.path.join(_x, _name))

    return _logical_file_names

  def wrapper_gfal_cp_file(self, source, destination, protocol):
  
    MiscTool.Print('python_info', '\nCalled wrapper_gfal_cp_file function.')

    _command = ['gfal-copy', '--force']
    _command.append(protocol + source)
    _command.append('file:///' + destination)

    MiscTool.Print('python_info', 'Command: ' + ' '.join(_command))

    sp.call(_command)

  def filter_keywords(self, file_name, filter_keywords_all, filter_keywords_any, filter_keywords_none):
    '''  Filter files which have the keywords '''

    if not all(_k in file_name for _k in filter_keywords_all) and len(filter_keywords_all):
      return False
    elif not any(_k in file_name for _k in filter_keywords_any) and len(filter_keywords_any):
      return False
    elif any(_k in file_name for _k in filter_keywords_none) and len(filter_keywords_none):
      return False
    else:
      return True

  def save_logical_file_names_remote(self, sample):

    MiscTool.Print('status', '\nSample: {0}.'.format(sample))

    for _l in self.list_of_locations:

      # txt file to store sample LFNs
      _outpath = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_remote.txt')
      
      # If txt file already exists skip
      if os.path.isfile(_outpath) and not self.force_all:
        MiscTool.Print('python_info','File {0} already exists.'.format(_outpath))

      # See if sample exist on location _l
      try:

        _path = os.path.join(self.list_of_storage_elements[_l], self.list_of_locations[_l], sample)
        self.wrapper_gfal_ls_r( _path, self.list_of_copying_protocols[_l])
         
        _path               = os.path.join(self.list_of_storage_elements[_l], self.list_of_locations[_l], sample)
        _logical_file_names = self.wrapper_gfal_ls_r( _path, self.list_of_copying_protocols[_l])

        with open(_outpath, 'w') as _outfile:
          for _lfn in _logical_file_names:
            _outfile.write(_lfn + '\n')
        
        MiscTool.Print('status', 'The LFNs were written to "{}".'.format(_outpath))

      except Exception, e:
        pass

  def save_logical_file_names_all_samples_remote(self):

    MiscTool.Print('python_info', '\nCalled save_logical_file_names_all_samples_remote function.')

    # Loop over all samples
    for _s in self.list_of_samples:

      self.save_logical_file_names_remote(_s)

  def check_root_files_remote(self, sample):

    MiscTool.Print('python_info', '\nCalled check_root_files_remote function.')

    for _l in self.list_of_locations:

      # txt file with remote lfns
      _path_remote          = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_remote.txt')
      _path_remote_missing  = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_remote_missing.txt')

      if not os.path.isfile(_path_remote):
        continue

      MiscTool.Print('status', 'Looking at: {0} '.format(_path_remote))
        
      _file_remote         = open( _path_remote, 'r')
      _file_remote_missing = open( _path_remote_missing, 'w')

      _list_of_file_numbers   = {}

      # First load all numbers/files from txt_file
      for _f in _file_remote:

        _path, _number = _f.replace('.root', '').split('tree_')

        if _path not in _list_of_file_numbers:
          print _path

          _list_of_file_numbers[_path] = []
          _list_of_file_numbers[_path].append(int(_number.strip()))
        else:
          _list_of_file_numbers[_path].append(int(_number.strip()))
      
      # Here goes the loop which search for any missing numbers in int sequence
      for _ll in _list_of_file_numbers:

        _sorted          = sorted(_list_of_file_numbers[_ll])
        _start           = _sorted[0]
        _end             = _sorted[-1]
        _missing_numbers = sorted(set(xrange(_start, _end + 1)).difference( _list_of_file_numbers[_ll]))
        _missing_files   = [ 'tree_{0}.root'.format(_n) for _n in _missing_numbers]

        # print '\n'
        # print _start, _end
        # print _ll, sorted(_list_of_file_numbers[_ll])

        if _missing_numbers:
          MiscTool.Print('error', 'Path: {0} not OK.'.format(_ll))
          MiscTool.Print('error', 'Missing: {0}'.format( _missing_files))
        else:
          pass

        # Save all to txt file
        for _ff in _missing_files:
          _file_remote_missing.write( os.path.join( _ll, _ff) + '\n')

      _file_remote.close()
      _file_remote_missing.close()

      MiscTool.Print('status', 'The missing LFNs were written to "{}".'.format( _path_remote_missing))

  def check_root_files_all_samples_remote(self):
    
    MiscTool.Print('python_info', '\nCalled check_root_files_all_samples_remote function.')
    
    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.check_root_files_remote(_s)

  # ------------------- Copy files ---------------------------
  def save_logical_file_names_local(self, sample):

    MiscTool.Print('python_info', '\nCalled save_logical_file_names_local function.')

    for _l in self.list_of_locations:

      # txt file with remote lfns
      _path_remote         = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_remote.txt')
      _path_local          = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local.txt')
      _path_local_missing  = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local_missing.txt')

      if not os.path.isfile( _path_remote):
        continue

      MiscTool.Print('status', 'Looking at: {0} '.format(_path_remote))

      _file_remote        = open( _path_remote, 'r')
      _file_local         = open( _path_local, 'w')
      _file_local_missing = open( _path_local_missing, 'w')

      # Convert paths from remote to local
      _protocol                 = self.list_of_copying_protocols[_l]
      _path_to_be_replaced      = os.path.join( self.list_of_storage_elements[_l], self.list_of_locations[_l])
      _path_to_be_replaced_with = self.path_samples_location

      for _f in _file_remote:

        # Create destination path for each file
        _lfn_destination = _f.strip().replace( _path_to_be_replaced, _path_to_be_replaced_with).replace( _protocol, '')

        # If file ok save, else delete and save into missing list
        if FileTool.FileTool.check_if_file_ok(_lfn_destination):
          _file_local.write(_lfn_destination + '\n')
        
        else:
          _file_local_missing.write(_lfn_destination + '\n')
        
          try:
            sp.call(['rm', '-rf', _lfn_destination])
          except Exception, e:
            MiscTool.Print('error', 'Not able to delete: {0} '.format(_lfn_destination))
            MiscTool.Print('error', ' '.join(['rm', '-rf', _lfn_destination]))

      _file_remote.close()
      _file_local.close()
      _file_local_missing.close()

  def save_logical_file_names_all_samples_local(self):

    MiscTool.Print('python_info', '\nCalled save_logical_file_names_all_samples_local function.')
    
    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.save_logical_file_names_local(_s)

  def copy_files_single_sample(self, sample):

    MiscTool.Print('python_info', '\nCalled copy_files_single_sample function.')

    for _l in self.list_of_locations:

      _path_local_missing  = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local_missing.txt')

      if not os.path.isfile( _path_local_missing):
        continue

      MiscTool.Print('status', 'Looking at: {0} '.format( _path_local_missing))

      _file_local_missing       = open( _path_local_missing, 'r') 
      _path_to_be_replaced      = self.path_samples_location
      _path_to_be_replaced_with = os.path.join( self.list_of_storage_elements[_l], self.list_of_locations[_l])
    
      for _f in _file_local_missing:

        _source                     = _f.strip().replace( _path_to_be_replaced, _path_to_be_replaced_with)
        _destination, _script_name  = _f.strip().split('tree')
        _inital_directory           = _destination.replace(self.path_output_directory, self.path_batch_scripts)

        _batch_arguments = {
          '<initial_directory>' : _inital_directory,                # path to newly created batch script
          '<source>'            : _source,                          # path to newly created batch script
          '<destination>'       : _destination,                     # file w/o presel
          '<script_name>'       : _script_name.replace('.root',''), # 1401
          '<copy_protocol>'     : self.list_of_copying_protocols[_l],
          'python_template'     : os.path.join(self.path_batch_templates, 'copy_batch_template.py')
        }

        _batch = BatchTool.BatchTool(_batch_arguments)
        _batch.make_scripts()
        _batch.send_job()

  def copy_files_all_samples(self):

    MiscTool.Print('python_info', '\nCalled copy_files_all_samples function.')
    
    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.copy_files_single_sample(_s)

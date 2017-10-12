import os
import hashlib

import ROOT

from utility import MiscTool
from utility import FileTool
from utility import BatchTool

class SelectionTool(object):

  def __init__(self, configuration):

    MiscTool.Print('python_info', '\nCreated instance of SelectionTool class')

    self.force_all          = configuration.general.force_all
    self.batch              = configuration.general.batch
    self.send_jobs           = configuration.general.send_jobs

    # Needed to get list of samples
    self.task_name          = configuration.general.task_name
    self.user_defined_files = configuration.general.user_defined_files

    # ------ Paths -------
    self.path_working_directory           = configuration.paths.path_working_directory
    self.path_analysis_working_directory  = configuration.paths.path_analysis_working_directory
    self.path_samples_location            = configuration.paths.path_samples
    self.path_samples_user_defined        = configuration.paths.path_samples_user_defined
    self.path_cache                       = configuration.paths.path_cache
    self.path_logical_file_names          = MiscTool.make_directory( os.path.join( self.path_samples_location, 'logical_file_names') )
    self.path_batch_scripts               = MiscTool.make_directory( os.path.join( self.path_analysis_working_directory, 'results', 'selection') )
    self.path_batch_templates             = MiscTool.make_directory( os.path.join( self.path_working_directory, 'utility', 'templates', 'selection') )

    # ------ Selection options -------
    self.list_of_IDs                      = configuration.samples.task[self.task_name]
    self.list_of_locations                = configuration.general.locations
    self.user_defined_files               = configuration.general.user_defined_files
    self.work_with_Ls_only                = configuration.general.work_with_Ls_only
    self.task_selection_on_merged_files   = configuration.general.task_selection_on_merged_files
    
    self.selection                        = [configuration.selection.hierarchy[_s] for _s in configuration.selection.task[self.task_name]] 
    # Add final cut if required
    if not self.work_with_Ls_only:
      self.selection.append(configuration.selection.task_definitions[self.task_name])

    # Check if one wants to work with user defined files
    if self.user_defined_files:
      self.path_samples = self.path_samples_user_defined
    else:
      self.path_samples = self.path_samples_location

    # Convert IDs to samples
    self.list_of_samples    = MiscTool.ID_sample_dictionary( self.list_of_IDs, configuration.samples)
    self.info_samples       = configuration.samples.samples_list

    MiscTool.Print('analysis_info', 'Task:', self.task_name)
    MiscTool.Print('analysis_info', 'Force all:', self.force_all)
    MiscTool.Print('analysis_info', 'User defined files:', self.user_defined_files)
    MiscTool.Print('analysis_info', 'Work with L selection only:', self.work_with_Ls_only)
    MiscTool.Print('analysis_info', 'New files will be stored in:', self.path_cache)
    MiscTool.Print('analysis_info', 'Analysis working directory:', self.path_analysis_working_directory)
    MiscTool.Print('analysis_info_list', 'List of samples:', self.list_of_samples)

  def make_files_all_samples(self):

    MiscTool.Print('python_info', '\nCalled make_files_all_samples function.')
    
    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.make_files(_s)

  def make_files(self, sample):

    MiscTool.Print('python_info', '\nCalled make_files function.')

    # Check if one wants to apply final selection on merged file after L selection
    if self.task_selection_on_merged_files and not self.work_with_Ls_only:

      _input_hash   = hashlib.md5( ''.join(self.selection[:-1]) ).hexdigest()
      _output_hash  = hashlib.md5( ''.join(self.selection) ).hexdigest()
 
      _input_file_name  = os.path.join( self.path_cache, sample + '_' + _input_hash   + '.root' ) 
      _output_file_name = os.path.join( self.path_cache, sample + '_' + _output_hash  + '.root' )

      # Check if input file is ok
      if not FileTool.FileTool.check_if_file_ok(_input_file_name):
        MiscTool.Print('error', 'Input file {0} not ok!'.format(_input_file_name))
        return 0

      # Check if output file is ok/exists, if not send job
      if FileTool.FileTool.check_if_file_ok(_output_file_name) and not self.force_all:
        return 0

      _cut = ' && '.join(self.selection)

      FileTool.FileTool.simple_trim_files(_input_file_name, _output_file_name, _cut)

    else:

      for _l in self.list_of_locations:

        _path_local = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local.txt')

        # Check from which locations do you want to use files
        if not (_l in self.info_samples[sample]['origin'] or self.info_samples[sample]['origin'] == ['all']):
          continue        

        if not os.path.isfile( _path_local):
          continue

        MiscTool.Print('status', 'Working {0} '.format( _path_local))

        _file_local = open( _path_local, 'r')

        # Loop over all files
        for _nn,_f in enumerate(_file_local):
      
          _f = _f.strip()

          # if _nn > 500:
          #   continue

          # Initial directory and script name for batch
          _inital_directory, _script_name = _f.replace(self.path_samples_location, self.path_batch_scripts).split('tree')

          # Loop over selections
          for _n, _s in enumerate(self.selection):

            # As input use original file
            if _n == 0:

              _output_hash = hashlib.md5( ''.join(self.selection[0:_n+1]) ).hexdigest()

              _input  = _f.replace( self.path_samples_location, self.path_samples) 
              _output = _f.replace( self.path_samples_location, self.path_samples).replace( self.path_samples, self.path_cache).replace('tree_', 'tree_{0}_'.format(_output_hash))

            else:

              _input_hash  = hashlib.md5( ''.join(self.selection[0:_n]) ).hexdigest()
              _output_hash = hashlib.md5( ''.join(self.selection[0:_n+1]) ).hexdigest()

              _input  = _f.replace( self.path_samples_location, self.path_samples).replace( self.path_samples, self.path_cache).replace('tree_', 'tree_{0}_'.format(_input_hash))
              _output = _f.replace( self.path_samples_location, self.path_samples).replace( self.path_samples, self.path_cache).replace('tree_', 'tree_{0}_'.format(_output_hash))

            # Check if input file is ok
            if not FileTool.FileTool.check_if_file_ok(_input):
              MiscTool.Print('error', 'Input file {0} not ok!'.format(_input))
              break

            # Check if output file is ok/exists, if not send job
            if FileTool.FileTool.check_if_file_ok(_output) and not self.force_all:
              continue

            else:

              MiscTool.Print('status', '\nSelection level: {0}'.format(_n))
              MiscTool.Print('status', 'Output: {0}'.format(_output))

              _cut          = ' && '.join(self.selection[0:_n+1])

              _batch_arguments = {  
                '<initial_directory>' : _inital_directory,           # path to newly created batch script
                '<input_file>'        : _input,                      # file w/o presel
                '<output_file>'       : _output,                     # file w/ presel
                '<cut>'               : _cut,                        # 'V_pt>100'
                '<script_name>'       : _script_name.replace('.root',''), # 1401
                'python_template'     : os.path.join(self.path_batch_templates, 'selection_batch_template.py')
              }

              _batch = BatchTool.BatchTool(_batch_arguments, self.batch, self.send_jobs)
              _batch.make_scripts()
              _batch.send_job()

              break

        _file_local.close()

  def merge_files_all_samples(self):

    MiscTool.Print('python_info', '\nCalled merge_files_all_samples function.')
    
    # Loop over all samples
    for _s in self.list_of_samples:
      
      self.merge_files(_s)

  def merge_files(self, sample):
    
    MiscTool.Print('python_info', '\nCalled merge_files function.')  

    _final_hash = hashlib.md5( ''.join(self.selection) ).hexdigest()

    # name of merged root file      
    _file_name          = sample + '_' + _final_hash + '.root'
    _merged_file_name   = os.path.join( self.path_cache, _file_name )

    # If merged  file already exists skip
    if FileTool.FileTool.check_if_file_ok(_merged_file_name) and not self.force_all:
      MiscTool.Print('python_info','File {0} already exists.'.format(_merged_file_name))
      return 0

    _merger = ROOT.TFileMerger(ROOT.kFALSE)
    _merger.OutputFile(_merged_file_name, 'RECREATE')

    for _l in self.list_of_locations:

      _path_local = os.path.join(self.path_logical_file_names, sample + '_' +  _l + '_local.txt')

      # Check from which locations do you want use files
      if not (_l in self.info_samples[sample]['origin'] or self.info_samples[sample]['origin'] == ['all']):
        continue        

      if not os.path.isfile( _path_local):
        continue

      MiscTool.Print('status', 'Working {0} '.format( _path_local))

      _file_local = open( _path_local, 'r')

      # Loop over all files
      for _n, _f in enumerate(_file_local):

        # if _n > 500:
        #   continue

        _f = _f.strip()

        _file = _f.replace( self.path_samples_location, self.path_samples).replace( self.path_samples, self.path_cache).replace('tree_', 'tree_{0}_'.format(_final_hash))

        MiscTool.Print('status', _file)

        # Check if file ok
        if not FileTool.FileTool.check_if_file_ok(_file):
          MiscTool.Print('error', 'File {0} is missing.'.format(_file))
          continue

        _merger.AddFile(_file)   
      
      _file_local.close()
      
    _merger.Merge()

    MiscTool.Print('status', '\nMerging done {0}.'.format(_merged_file_name))

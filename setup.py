import os
import sys
import subprocess as sp

from utility import MiscTool

if __name__ == '__main__':
  
  MiscTool.Print('python_info', '\n','-'*50)
  MiscTool.Print('python_info', '\nWelcome to Hbb code! Setup started!')
  MiscTool.Print('python_info', '\n','-'*50)

  # ----------------------------------------------------
  # ------------ Change only this part -----------------
  # ----------------------------------------------------
  
  # This will be stored in configuration files after they are created, you can modify config files at any time
  analysis_name             = 'Wlv'
  path_samples              = '/STORE/Hbb/2017_04_VHBBHeppyV25'
  path_samples_cache        = '_'.join([path_samples, analysis_name, 'cache'])
  path_samples_user_defined = '_'.join([path_samples, analysis_name, 'user_defined'])

  # ----------------------------------------------------
  # ----------------------------------------------------
  path_working_directory    = os.path.dirname(os.path.realpath(__file__))

  paths = {
    'path_samples'              : path_samples,
    'path_samples_user_defined' : path_samples_user_defined,
    'path_cache'                : path_samples_cache,
    'path_configuration'        : os.path.join( path_working_directory, 'analysis', analysis_name, 'configuration'),
    'path_results'              : os.path.join( path_working_directory, 'analysis', analysis_name, 'results'),
    'path_test'                 : os.path.join( path_working_directory, 'analysis', analysis_name, 'test'),
  }

  MiscTool.Print('analysis_info', 'Analysis name:', analysis_name)
  MiscTool.Print('analysis_info', 'Path working directory:', path_working_directory)
  MiscTool.Print('analysis_info', 'Path samples:', path_samples)
  MiscTool.Print('analysis_info', 'Path samples cache:', path_samples_cache)

  # ------------ Setup location of samples, code structure, etc.... -----------------

  MiscTool.Print('python_info', '\nChecking directory structure ...')
  _ = [ MiscTool.make_directory(_p) for _p in paths.values()]

  # ------------ Setup analysis code structure -----------------
  if len(sys.argv) > 1 and sys.argv[1] == 'force':
    MiscTool.Print('error', 'Configuration files are overwritten.')
    force_recreate_config = True
  else:
    force_recreate_config = False

  MiscTool.Print('python_info', '\nSetup configuration files ...')

  # Copy configuration templates and modify them
  config_templates_path = os.path.join( path_working_directory, 'utility/templates/configuration')
  config_files          = os.listdir(config_templates_path)

  # Just create init file
  with open( os.path.join( path_working_directory, 'analysis', analysis_name, '__init__.py'), 'w') as _f:
    pass

  for _c in config_files:

    _path_template_config = os.path.join(config_templates_path, _c)
    _path_new_config      = os.path.join(paths['path_configuration'], _c)

    # Make config if it doesn't exist or if it is paths.py
    if not os.path.isfile(_path_new_config) or _c == 'paths.py' or force_recreate_config:
    
      with open(_path_template_config) as _f:
        _new_text = _f.read().\
            replace('<path_analysis_working_directory>',  os.path.join( path_working_directory, 'analysis', analysis_name)).\
            replace('<path_working_directory>',           path_working_directory).\
            replace('<path_samples>',                     path_samples).\
            replace('<path_samples_user_defined>',        path_samples_user_defined).\
            replace('<path_cache>',                       path_samples_cache)

      with open(_path_new_config, "w") as _f:
        _f.write(_new_text)

    else:
      pass

  MiscTool.Print('python_info', '\nSetup done ...')
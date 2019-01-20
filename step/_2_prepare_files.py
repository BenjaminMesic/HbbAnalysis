from utility import MiscTool, FileTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 2: preparing files.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Create instance of FileTool
  prepare_files = FileTool.FileTool(configuration)

  # ----------------------------------------

  # Create user defined files, add variables, etc ...
  prepare_files.make_files_all_samples()
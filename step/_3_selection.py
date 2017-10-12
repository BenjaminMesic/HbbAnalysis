from utility import MiscTool, SelectionTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 3: Doing selection.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Create instance of FileTool
  selection = SelectionTool.SelectionTool(configuration)

  # # ----------------------------------------
  # # Apply selection
  # selection.make_files_all_samples()

  # # Merge files
  # selection.merge_files_all_samples()
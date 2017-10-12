from utility import MiscTool, CopyTool

if __name__ == '__main__':
  
  MiscTool.Print('python_info',  '\nStep 1: copying samples.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.get_analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  # Create instance of CopySamples 
  copy_samples = CopyTool.CopyTool(configuration)

  # ----------------------------------------
  # Remote part
  # ----------------------------------------

  # # It executes ls command for each directory from pisa/psi..
  # copy_samples.save_logical_file_names_all_samples_remote()

  # # Check if some of files are missing, e.g. in Pisa/...
  # copy_samples.check_root_files_all_samples_remote()

  # ----------------------------------------
  # Local part
  # ----------------------------------------

  # # Check, remove and save lfns of local files
  # copy_samples.save_logical_file_names_all_samples_local()

  # # Copy files
  # copy_samples.copy_files_all_samples()

from utility import MiscTool, PreselectionTool

if __name__ == '__main__':

  MiscTool.Print('python_info',  '\nStep 2: preselection.')

  # Get analysis name, default is 'Wlv'
  analysis_name = MiscTool.analysis_name()

  # Load all configuration files
  configuration = MiscTool.get_configuration_files(analysis_name)

  force_all = False

  # Create instance of preselection class
  p = PreselectionTool.PreselectionTool(analysis_name, configuration, force_all) #, 'WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8')

  # ---------------------------------
  # Choose what you want to do
  # ---------------------------------

  # # Preselection
  # p.preselection()

  # # Check preselected files, if you want only one sample add name in PreselectionTool
  # p.check_root_preselected_files()

  # # Merge files
  # p.merge()

  # # Create boosted trees
  # p.create_boosted_trees()

  # Use batch
  # p.create_boosted_trees_on_unmerged_files_using_batch()
  # p.check_boosted_trees()
  p.merge_boosted_trees()